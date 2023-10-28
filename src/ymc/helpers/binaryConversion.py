from typing import LiteralString


def unsignedBinaryToInt(string: str) -> int:
    clippedString: str = string[-8:]
    placeValue: int = 128
    value: int = 0
    for char in clippedString:
        value += int(char) * placeValue
        placeValue = int(placeValue / 2)
    return value


def signedBinaryToInt(string: str) -> int:
    clippedString: str = string[-7:]
    value: int = 0
    if (string[-8] == "1"):
        value = -128
    placeValue: int = 64
    for char in clippedString:
        value += int(char) * placeValue
        placeValue = int(placeValue / 2)
    return value


def unsignedIntToBinary(num: int) -> str:
    return f'{num:b}'[-8:].zfill(8)


# Has weird behavior when given numbers outside its data range, but that's expected
def signedIntToBinary(num: int) -> str:
    signBit = "0"
    if (num < 0):
        signBit = "1"
    shortReturnString: str = signBit + f'{abs(num):b}'[-7:]
    returnString = shortReturnString
    if (len(shortReturnString) < 8):
        extension: LiteralString = signBit * (8 - len(shortReturnString))
        returnString: str = extension + shortReturnString
    return returnString


def addrToBinary(num: int) -> str:
    return f'{num:b}'[-16:].zfill(0)


def BinaryToAddr(addr: str) -> int:
    clippedString: str = addr[-16:]
    placeValue: int = 2**15
    value: int = 0
    for char in clippedString:
        value += int(char) * placeValue
        placeValue = int(placeValue / 2)
    return value