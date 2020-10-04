#pragma once

#include "JuceHeader.h"

#include "MasterkeyboardCapability.h"
#include "SoundExpanderCapability.h"
#include "SynthHolder.h"
#include "MidiChannelEntry.h"

#include "AutoDetection.h"

#include <map>

class MidiController;

class MasterkeyboardsView : public Component,
	public ChangeListener
{
public:
	MasterkeyboardsView(midikraft::AutoDetection &autoDetection);
	~MasterkeyboardsView();

	virtual void resized() override;
	virtual void changeListenerCallback(ChangeBroadcaster* source) override;

private:
	void recreate();
	void refreshCheckmarks();
	std::shared_ptr<midikraft::SoundExpanderCapability> expanderWithName(std::string const &name);
	std::shared_ptr<midikraft::MasterkeyboardCapability> keyboardWithName(std::string const &name);

	Label header;
	OwnedArray<Label> keyboards_;
	OwnedArray<MidiChannelEntry> keyboardChannels_;
	OwnedArray<ToggleButton> keyboadLocalButtons_;
	OwnedArray<Label> expanders_;
	OwnedArray<MidiChannelEntry> expanderChannels_;
	OwnedArray<Component> expanderClockMode_;
	OwnedArray<Button::Listener> listeners_;
	std::map<std::string, std::vector<ToggleButton *>> buttonsForExpander_;
};