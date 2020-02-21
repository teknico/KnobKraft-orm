/*
   Copyright (c) 2020 Christof Ruch. All rights reserved.

   Dual licensed: Distributed under Affero GPL license by default, an MIT license is available for purchase
*/

#include "SettingsView.h"

#include "DataFileLoadCapability.h"
#include "MidiController.h"

#include "Rev2.h" //TODO This should be replaced by a "GlobalSettingsCapability"


SettingsView::SettingsView(std::vector<midikraft::SynthHolder> const &synths) : synths_(synths), librarian_(synths), 
	buttonStrip_(3001, LambdaButtonStrip::Direction::Horizontal)
{
	LambdaButtonStrip::TButtonMap buttons = {
	{ "loadGlobals", { 0, "Load Globals", [this]() {
		loadGlobals();
	} } },
	};
	buttonStrip_.setButtonDefinitions(buttons);
	addAndMakeVisible(buttonStrip_);
	addAndMakeVisible(propertyEditor_);

	auto rev2synth = std::dynamic_pointer_cast<midikraft::Rev2>(synths_[0].synth());
	propertyEditor_.setProperties(rev2synth->getGlobalSettings());
}

SettingsView::~SettingsView()
{
}

void SettingsView::resized()
{
	auto area = getLocalBounds();
	buttonStrip_.setBounds(area.removeFromBottom(100));
	propertyEditor_.setBounds(area);
}

void SettingsView::loadGlobals() {
	auto rev2 = std::dynamic_pointer_cast<midikraft::DataFileLoadCapability>(synths_[0].synth());
	auto namedDevice = std::dynamic_pointer_cast<midikraft::Synth>(synths_[0].synth());
	auto rev2synth = std::dynamic_pointer_cast<midikraft::Rev2>(synths_[0].synth());
	librarian_.startDownloadingSequencerData(midikraft::MidiController::instance()->getMidiOutput(namedDevice->midiOutput()), rev2.get(), 0, nullptr, [this, rev2synth]() {
		MessageManager::callAsync([this, rev2synth]() {
			// Kick off an update so the property editor can refresh itself
			auto settings = rev2synth->getGlobalSettings();
			propertyEditor_.setProperties(settings);
		});
	});
}
