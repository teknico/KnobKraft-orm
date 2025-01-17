/*
   Copyright (c) 2020 Christof Ruch. All rights reserved.

   Dual licensed: Distributed under Affero GPL license by default, an MIT license is available for purchase
*/

#include "RefaceDXPatch.h"

#include <algorithm>

namespace midikraft {

	const int kRefaceDXPatchType = 0;

	RefaceDXPatch::RefaceDXPatch(Synth::PatchData const &voiceData, MidiProgramNumber place) : Patch(kRefaceDXPatchType, voiceData), originalProgramNumber_(place)
	{
	}

	std::string RefaceDXPatch::name() const
	{
		std::string result;
		// Extract the first 10 bytes of the common block, that's the ascii name
		for (size_t i = 0; i < std::min((size_t)10, data().size()); i++) {
			result.push_back(data()[i]);
		}
		return result;
	}

	void RefaceDXPatch::setName(std::string const &name)
	{
		// Poke this into the first 10 bytes of the common block, which is the ASCII name. Ignore UTF 8 complexity for now.
		for (size_t i = 0; i < std::min((size_t)10, name.size()); i++) {
			setAt((int) i, name[i]);
		}
		for (int i = std::min(10, (int) name.size()); i < 10; i++) {
			setAt((int) i, ' ');
		}
	}

	bool RefaceDXPatch::isDefaultName(std::string const &patchName) const
	{
		return patchName == "Init Voice";
	}

	MidiProgramNumber RefaceDXPatch::patchNumber() const
	{
		return originalProgramNumber_;
	}

}
