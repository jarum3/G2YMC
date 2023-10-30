# Also handles 8-bit arg if and only if register value is held in 4 most-significant bits
# Match bit to register string based on encoding standard
# Needs to still be searched in CPU dictionary
def fourBitToRegister(bits: str) -> str:
    if bits[0] == "1":
        return "EAX"
    if bits[1] == "1":
        return "EBX"
    if bits[2] == "1":
        return "ECX"
    if (bits[3]) == "1":
        return "EDX"
    else:
        raise Exception("Invalid string provided to register lookup")

# Returns list of both register strings
def eightBitToRegisters(bits: str) -> list[str]:
    returnList: list[str] = [] # Empty list initialization
    returnList[0] = fourBitToRegister(bits[0:3]) # Grab first 4 bits register
    returnList[1] = fourBitToRegister(bits[4:7]) # Grab second 4 bits register
    return returnList # Return list

# Returns binary string for one register according to encoding standard
def registerToFourBit(register: str) -> str:
    match register.lower():
        case "eax":
            return "10000000"
        case "ebx":
            return "01000000"
        case "ecx":
            return "00100000"
        case "edx":
            return "00010000"
        case _:
            return "00000000"

# Returns binary string for 2 registers according to encoding standard
def registersToEightBit(register1: str, register2: str) -> str:
    higher = "0000"
    lower = "0000"
    # Set higher 4 bits to appropriate register
    match register1.lower():
        case "eax":
            higher = "1000"
        case "ebx":
            higher = "0100"
        case "ecx":
            higher = "0010"
        case "edx":
            higher = "0001"
        case _:
            higher = "0000"
    # Set lower 4 bits to appropriate register
    match register2.lower():
        case "eax":
            lower = "1000"
        case "ebx":
            lower = "0100"
        case "ecx":
            lower = "0010"
        case "edx":
            lower = "0001"
        case _:
            lower = "0000"
    return higher + lower # Concatenate higher + lower registers to get final byte
