from collections import namedtuple
import struct
import json
import glob
import sys

knownTags = {
    b"SGct": "Control",
    b"SGAc": "ArrayControl",
    b"SGtc": "TestControl",
    b"SGbm": "BitmapControl",
    b"SGpl": "PaletteControl",
    b"SGac": "ActiveControl",
    b"SGst": "SimpleText",
    b"SGtb": "TestButton",
    b"SGtr": "TestRadial",
    b"SGtk": "TestCheck",
    b"SGts": "TSControl",
    b"SGte": "TextEdit",
    b"SGtm": "TimerControl",
    b"SGbb": "BitmapBox",
    b"SGtl": "TextList",
    b"SGtw": "TextWrap",
    b"SGtf": "TextFormat",
    b"SGsl": "Slider",
    b"SGcb": "ComboBox",
    b"SGsc": "ScrollControl",
    b"SGsC": "ScrollContentControl",
    b"SGmc": "MatrixControl",
    b"SGpc": "ProgressCtrl",
    b"SGab": "AnimateBMA",
    b"SGhc": "HelpCtrl",
}

def readControlBase(rawData, offset):
    versionFormat = "<B"
    (version) = struct.unpack_from(versionFormat, rawData, offset)
    offset += struct.calcsize(versionFormat)
    print(version)
    colorDataFormat = "<L8B"
    (colorData) = struct.unpack_from(colorDataFormat, rawData, offset)
    offset += struct.calcsize(colorDataFormat)
    print(colorData)

    (commandLength) = struct.unpack_from(versionFormat, rawData, offset)
    offset += struct.calcsize(versionFormat)
    print(commandLength)

    (commandLength) = struct.unpack_from(versionFormat, rawData, offset)
    offset += struct.calcsize(versionFormat)
    print(commandLength)

    positionFormat = "<2l2l2L2ll"
    (position) = struct.unpack_from(positionFormat, rawData, offset)
    offset += struct.calcsize(positionFormat)
    print(position)

    consoleFormat = "<81s"
    (console) = struct.unpack_from(consoleFormat, rawData, offset)
    offset += struct.calcsize(consoleFormat)
    print(console)

    numberOfChildren = "<l"
    (child) = struct.unpack_from(numberOfChildren, rawData, offset)
    offset += struct.calcsize(consoleFormat)

    print(child)


def readActiveControl(rawData, offset):
    timerFormat = "<BL"
    result = struct.unpack_from(timerFormat, rawData, offset)
    print(result)
    offset += struct.calcsize(timerFormat)

    readControlBase(rawData, offset)

    return (offset, result)

def readBitmapControl(rawData, offset):
    bitmapFormat = "<l81sB"
    result = struct.unpack_from(bitmapFormat, rawData, offset)
    print(result)
    offset += struct.calcsize(bitmapFormat)

    readActiveControl(rawData, offset)

    return (offset, result)

def readScrollContentControl(rawData, offset):
    return readControlBase(rawData, offset)

def readPaletteControl(rawData, offset):
    paletteFormat = "<l81s"
    result = struct.unpack_from(paletteFormat, rawData, offset)
    print(result)
    offset += struct.calcsize(paletteFormat)

    readControlBase(rawData, offset)

    return (offset, result)

def readSimpleText(rawData, offset):
    textFormat = "<LL4l81s2l"
    result = struct.unpack_from(textFormat, rawData, offset)
    print(result)
    offset += struct.calcsize(textFormat)

    readActiveControl(rawData, offset)

    return (offset, result)


def readTimerControl(rawData, offset):
    timerFormat = "<4s2LL2f"
    result = struct.unpack_from(timerFormat, rawData, offset)
    print(result)
    offset += struct.calcsize(timerFormat)

    readControlBase(rawData, offset)

    return (offset, result)


functionMappings = {
    "BitmapControl": readBitmapControl,
    "TimerControl": readTimerControl,
    "SimpleText": readSimpleText
}

offset = 0

importFilenames = sys.argv[1:]
tempNames = importFilenames.copy()

for importFilename in tempNames:
    files = glob.glob(importFilename)
    importFilenames.remove(importFilename)
    importFilenames.extend(files)

tempNames = None

for importFilename in importFilenames:
    try:
        with open(importFilename, "rb") as importFile:
            rawData = importFile.read()

        for key in knownTags:
            index = rawData.find(key)
            if index != -1:
                print(knownTags[key] + " found inside of " + importFilename)
                #if knownTags[key] in functionMappings:
                    #functionMappings[knownTags[key]](rawData, index)

    except Exception as e:
        print(e, offset)

