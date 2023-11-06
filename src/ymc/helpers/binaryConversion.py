from typing import LiteralString

## Returns unsigned integer from 8-bit binary string
def unsignedBinaryToInt(string: str) -> int:
    # Grabbing only last-8 characters from binary string
    clippedString: str = string[-8:]
    placeValue: int = 128 # Contains current place value, starts all the way at the left, and moves to the right
    value: int = 0 # Contains current value
    for char in clippedString: # Loop through each bit
        value += int(char) * placeValue # Add the place value if bit is 1
        placeValue = int(placeValue / 2) # Move down by a power of two for each bit passed
    return value

## Returns signed integer from 8-bit binary string
def signedBinaryToInt(string: str) -> int:
    clippedString: str = string[-7:] # Grabs last 7 bits from binary string
    value: int = 0 # Contains current value
    if string[-8] == "1":
        value = -128 # Subtracts 128 if the sign bit is 1
    placeValue: int = 64 # Contains current place value
    for char in clippedString: # Loop through each bit
        value += int(char) * placeValue # Add the place value if the bit is 1
        placeValue = int(placeValue / 2) # Move down by a power of 2 for each bit passed
    return value

# Return 8-bit binary string encoding an unsigned integer
def unsignedIntToBinary(num: int) -> str:
    return f"{num:b}"[-8:].zfill(8) # Convert number to binary
                                    # Then grab only the last 8 characters
                                    # Then zero-fill to the left if less than 8 characters


# Return 8-bit binary string encoding an unsigned integer
def signedIntToBinary(num: int) -> str:
    signBit = "0"
    if num < 0: # If number is negative
        signBit = "1" # Sign bit should be 1
        num = num + 2**8 # And We should add 256 to our number
    # Sign bit + binary representation of
    shortReturnString: str = signBit + bin(num)[2:][-7:]    # Convert to binary, trim 0b from string,
                                                            # Trim to only last 7 bits
                                                            # Add sign bit at the start 
    returnString = shortReturnString
    # Sign-bit fill to the left if length is less than 8
    if len(shortReturnString) < 8:
        extension: LiteralString = signBit * (8 - len(shortReturnString))
        returnString: str = extension + shortReturnString
    return returnString


# Convert memory address to binary (Little-endian)
def addrToBinary(num: int) -> str:
    bigEnd = f"{num:b}"[-16:].zfill(16) # Convert to binary, trim last 16 bits, zero fill to 16
    littleEnd = bigEnd[8:] + bigEnd[:8]
    return littleEnd
# Convert binary number to address (Little-endian)
def BinaryToAddr(addr: str) -> int:
    clippedString: str = addr[-16:] # Trim to last 16 characters (16-bit addresses)
    bigEnd = clippedString[8:] + clippedString[:8]
    placeValue: int = 2**15 # Start at 2^15 for place value
    value: int = 0 # Contains current value
    for char in bigEnd: # Loop through each bit
        value += int(char) * placeValue # Add place value if bit is 1
        placeValue = int(placeValue / 2) # Move place value down a power of 2
    return value


# Handles one byte at a time
def hexToBinary(hexCode: str) -> str:
    return bin(int(hexCode, 16))[2:].zfill(8)   # Convert hex into int, convert into binary
                                                # Trim off 0b from binary conversion
                                                # Zero-fill to the left to fill 8 bits
