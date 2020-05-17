#
#   Copyright (c) 2020 Christof Ruch. All rights reserved.
#
#   Dual licensed: Distributed under Affero GPL license by default, an MIT license is available for purchase
#


def name():
    return "Matrix 6/6R"


def createDeviceDetectMessage(channel):
    # Trying to detect the Matrix 6/6R with a request to the master data
    return createQuickEditModeMessage() + [0xf0, 0x10, 0x06, 0x04, 3, 0, 0xf7]


def createQuickEditModeMessage():
    # The Matrix 6 wants to be in QuickEdit mode in order to accept any sysex commands. As it seems to lose this
    # on any "MIDI reset", it is good practice to always prepend this command before any sysex you send to it
    return [0xf0, 0x10, 0x06, 0x05, 0xf7]


def deviceDetectWaitMilliseconds():
    return 200


def needsChannelSpecificDetection():
    return False


def channelIfValidDeviceResponse(message):
    # The answer is a master data dump
    if (len(message) > 3
            and message[0] == 0xf0  # Sysex
            and message[1] == 0x10  # Oberheim
            and message[2] == 0x06  # Matrix 6/6R
            and message[3] == 0x03):  # Master parameter data
        # Different from the documentation, the header is one byte longer and has a data byte valued 2 at pos 4
        # This needs to be ignored, we start reading the master data only from index 5
        master_data = denibble(message, 5)
        if len(master_data) != 236:
            print("Error, expected 236 bytes of master data")
        # Extract the current MIDI channel from byte 11 of the master data
        return master_data[11]
    return -1


def createEditBufferRequest(channel):
    # The Matrix 6/6R has no edit buffer request, in contrast to the later Matrix 1000. Just send some message it likes
    return createQuickEditModeMessage()


def isEditBufferDump(message):
    return False


def numberOfBanks():
    return 1


def numberOfPatchesPerBank():
    return 100


def createProgramDumpRequest(channel, patchNo):
    program = patchNo % numberOfPatchesPerBank()
    return createQuickEditModeMessage() + [0xf0, 0x10, 0x06, 0x04, 1, program, 0xf7]


def isSingleProgramDump(message):
    return (len(message) > 3
            and message[0] == 0xf0
            and message[1] == 0x10  # Oberheim
            and message[2] == 0x06  # Matrix
            and message[3] == 0x01)  # Single Patch Data


def nameFromDump(message):
    if isSingleProgramDump(message):
        # To extract the name from the Matrix 6 program dump, we need to correctly de-nibble and then force the first
        # 8 bytes into ASCII
        patchData = denibble(message, 5)
        return ''.join([chr(x if x >= 32 else x + 0x40) for x in patchData[0:8]])


def createProgramChangeMessage(channel, program):
    # -1 would be an invalid MIDI channel, don't create any message
    return [0xC0 | (channel & 0x0f), program] if channel != -1 else []


def convertToEditBuffer(channel, message):
    if isSingleProgramDump(message):
        # The Matrix 6 cannot send to the edit buffer, so we send into program 100 and append a program change to it
        return createQuickEditModeMessage() + message[0:4] + [99] + message[5:] + createProgramChangeMessage(channel, 99)
    raise Exception("This is not a program dump, can't be converted")


def denibble(message, start_index):
    denibbled_data_content = [message[x] | (message[x + 1] << 4) for x in range(start_index, len(message) - 2, 2)]
    expected_checksum = message[-2]
    checksum = sum(denibbled_data_content) & 0x7f
    if checksum != expected_checksum:
        print("Checksum error in data package from Matrix 6. Checksum is %d but expected was %d. Data package %s" %
              (checksum, expected_checksum, message))
    return denibbled_data_content


# Some debugging and testing code
#master_data_from_M6 = [0xf0,0x10,0x06,0x03,0x02,0x00,0x00,0x08,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x0f,0x03,0x0e,0x0f,0x00,0x00,0x0f,0x03,0x00,0x00,0x01,0x00,0x01,0x00,0x01,0x00,0x01,0x00,0x01,0x00,0x04,0x00,0x00,0x04,0x01,0x00,0x02,0x00,0x00,0x00,0x00,0x00,0x0b,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x05,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x02,0x00,0x03,0x00,0x04,0x00,0x05,0x00,0x06,0x00,0x07,0x00,0x08,0x00,0x09,0x00,0x0a,0x00,0x0b,0x00,0x0c,0x00,0x0d,0x00,0x0e,0x00,0x0f,0x00,0x00,0x01,0x01,0x01,0x02,0x01,0x03,0x01,0x04,0x01,0x05,0x01,0x06,0x01,0x07,0x01,0x08,0x01,0x09,0x01,0x0a,0x01,0x0b,0x01,0x0c,0x01,0x0d,0x01,0x0e,0x01,0x0f,0x01,0x00,0x02,0x01,0x02,0x02,0x02,0x03,0x02,0x04,0x02,0x05,0x02,0x06,0x02,0x07,0x02,0x08,0x02,0x09,0x02,0x0a,0x02,0x0b,0x02,0x0c,0x02,0x0d,0x02,0x0e,0x02,0x0f,0x02,0x00,0x03,0x01,0x03,0x02,0x03,0x03,0x03,0x04,0x03,0x05,0x03,0x06,0x03,0x07,0x03,0x08,0x03,0x09,0x03,0x0a,0x03,0x0b,0x03,0x0c,0x03,0x0d,0x03,0x0e,0x03,0x0f,0x03,0x00,0x04,0x01,0x04,0x02,0x04,0x03,0x04,0x04,0x04,0x05,0x04,0x06,0x04,0x07,0x04,0x08,0x04,0x09,0x04,0x0a,0x04,0x0b,0x04,0x0c,0x04,0x0d,0x04,0x0e,0x04,0x0f,0x04,0x00,0x05,0x01,0x05,0x02,0x05,0x03,0x05,0x04,0x05,0x05,0x05,0x06,0x05,0x07,0x05,0x08,0x05,0x09,0x05,0x0a,0x05,0x0b,0x05,0x0c,0x05,0x0d,0x05,0x0e,0x05,0x0f,0x05,0x00,0x06,0x01,0x06,0x02,0x06,0x03,0x06,0x00,0x00,0x01,0x00,0x02,0x00,0x03,0x00,0x04,0x00,0x05,0x00,0x06,0x00,0x07,0x00,0x08,0x00,0x09,0x00,0x0a,0x00,0x0b,0x00,0x0c,0x00,0x0d,0x00,0x0e,0x00,0x0f,0x00,0x00,0x01,0x01,0x01,0x02,0x01,0x03,0x01,0x04,0x01,0x05,0x01,0x06,0x01,0x07,0x01,0x08,0x01,0x09,0x01,0x0a,0x01,0x0b,0x01,0x0c,0x01,0x0d,0x01,0x0e,0x01,0x0f,0x01,0x00,0x02,0x01,0x02,0x02,0x02,0x03,0x02,0x04,0x02,0x05,0x02,0x06,0x02,0x07,0x02,0x08,0x02,0x09,0x02,0x0a,0x02,0x0b,0x02,0x0c,0x02,0x0d,0x02,0x0e,0x02,0x0f,0x02,0x00,0x03,0x01,0x03,0x02,0x03,0x03,0x03,0x04,0x03,0x05,0x03,0x06,0x03,0x07,0x03,0x08,0x03,0x09,0x03,0x0a,0x03,0x0b,0x03,0x0c,0x03,0x0d,0x03,0x0e,0x03,0x0f,0x03,0x00,0x04,0x01,0x04,0x02,0x04,0x03,0x04,0x04,0x04,0x05,0x04,0x06,0x04,0x07,0x04,0x08,0x04,0x09,0x04,0x0a,0x04,0x0b,0x04,0x0c,0x04,0x0d,0x04,0x0e,0x04,0x0f,0x04,0x00,0x05,0x01,0x05,0x02,0x05,0x03,0x05,0x04,0x05,0x05,0x05,0x06,0x05,0x07,0x05,0x08,0x05,0x09,0x05,0x0a,0x05,0x0b,0x05,0x0c,0x05,0x0d,0x05,0x0e,0x05,0x0f,0x05,0x00,0x06,0x01,0x06,0x02,0x06,0x03,0x06,0x3d,0xf7]
#print("Midi Channel is", channelIfValidDeviceResponse(master_data_from_M6))