# Also handles 8-bit arg if and only if register value is held in 4 most-significant bits
def fourBitToRegister(bits: str) -> str:
    if (bits[0] == "1"): return "EAX"
    if (bits[1] == "1"): return "EBX"
    if (bits[2] == "1"): return "ECX"
    if (bits[3]) == "1": return "EDX"
    else: raise Exception("Invalid string provided to register lookup")


def eightBitToRegisters(bits: str) -> list[str]:
    returnList: list[str] = []
    returnList[0] = fourBitToRegister(bits[0:3])
    returnList[1] = fourBitToRegister(bits[4:7])
    return returnList
