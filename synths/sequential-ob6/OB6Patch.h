/*
   Copyright (c) 2020 Christof Ruch. All rights reserved.

   Dual licensed: Distributed under Affero GPL license by default, an MIT license is available for purchase
*/

#pragma once

#include "Patch.h"

namespace midikraft {

	class OB6Number : public PatchNumber {
	public:
		using PatchNumber::PatchNumber;
		virtual std::string friendlyName() const override;
	};

	class OB6Patch : public Patch {
	public:
		using Patch::Patch;

		virtual std::string patchName() const override;
		virtual void setName(std::string const &name) override;
		virtual std::shared_ptr<PatchNumber> patchNumber() const override;
		virtual void setPatchNumber(MidiProgramNumber patchNumber) override;
		virtual std::vector<std::shared_ptr<SynthParameterDefinition>> allParameterDefinitions() override;

	private:
		MidiProgramNumber place_ = MidiProgramNumber::fromZeroBase(0);
	};

}
