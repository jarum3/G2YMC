##########################################
# Takes in a file from file.ymc
# then encodes it into a binary string
# and writes that string to file.bin 
##########################################
from __future__ import annotations
from pathlib import Path
import pickle
from instructions.Instruction import Instruction
import helpers.binaryConversion as bc
import helpers.registerLookup as rl
import re

def getBinaryFromLine(line: str, instructions: dict[str, Instruction]) -> str:
    binaryString = ""
    if (len(line)) > 0:
        # Remove everything that isn't alphanumeric, negative, or a space (Also removes commas)
        lineTrimmed = re.sub(r"[^-A-Za-z0-9 ]+", "", line)
        # Split string on spaces (Instr at pieces[0], arguments at rest)
        pieces = lineTrimmed.split(" ")
        # Extracts current instruction
        currInstr = pieces[0]
        # Extracts arguments
        args = pieces[1:]
        # Convert line into instruction and arguments
        binary: list[str] = []
        # Add binary form of string to string
        binary.append(bc.hexToBinary(instructions[currInstr].hexCode))
        # Get array of argument types
        argTypes = instructions[currInstr].argTypes
        if args and argTypes:  # Just making sure we have arguments to process
            # Read argument types from instruction
            arg = 0
            linePiece = 0
            while arg < len(argTypes):  # Stop processing once we're done with arguments
                match argTypes[arg]:
                    case "memory": # Memory address
                        address = bc.addrToBinary(int(args[linePiece]))
                        binary.append(address)
                    case "register": # One register in one byte
                        binary.append(rl.registerToFourBit(args[linePiece]))
                    case "register-register": # Both registers to one-byte (Two arguments in one match)
                        binary.append(rl.registersToEightBit(args[linePiece], args[linePiece + 1]))
                        linePiece += 1 # We're grabbing two arguments (this is why line piece and argument are counted separately)
                    case "literal":
                        if args[linePiece][0] == "-": # If number starts with negative, it definitely has to be signed
                            binary.append(bc.signedIntToBinary(int(args[linePiece])))
                        else: # Otherwise, interpreting as unsigned gives larger range
                            binary.append(bc.unsignedIntToBinary(int(args[linePiece])))
                # Increment both list pointers forward
                arg += 1
                linePiece += 1
        # Append current instruction to binary string
        for byte in binary:
            if byte:
                binaryString += byte
    return binaryString

def main():
    # Should use files asm.pkl to convert from assembly code to binary
    # asm.pkl should contain object files for all instructions, with their assigned hex code and length being used to create binary data
    nameFile = str(Path(__file__).parent) + "/instructions/instructionsByName.pkl"
    binaryString: str = ""
    with open(nameFile, "rb") as file:
        instructions: dict[str, Instruction] = pickle.load(file)
    # Open input file
    ymcFile = str(Path(__file__).with_name("assembly.ymc"))
    with open(ymcFile, "r") as file:
        for line in file:
            # Loop through lines of input files
            binary = getBinaryFromLine(line, instructions)
            if binary:
                binaryString += binary
    # Write binary string
    binaryFile = str(Path(__file__).with_name("binary.bin"))
    with open(binaryFile, "w") as file:
        file.write(binaryString)


if __name__ == "__main__":
    main()
