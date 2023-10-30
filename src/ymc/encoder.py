import pickle
from instructions.Instruction import Instruction
import helpers.binaryConversion as bc
import helpers.registerLookup as rl
import re


def main():
    # Should use files asm.pkl to convert from assembly code to binary
    # asm.pkl should contain object files for all instructions, with their assigned hex code and length being used to create binary data
    binaryString = ""
    with open("instructions/instructionsByName.pkl", "rb") as file:
        instructions: dict[str, Instruction] = pickle.load(file)
    # Open input file
    with open("file.ymc", "r") as file:
        for line in file:
            # Loop through lines of input file
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
                    i = 0
                    while i < len(
                        args
                    ):  # Stop processing once we're done with arguments
                        if (
                            argTypes[i] == "memory"
                        ):  # Convert memory address to little-endian
                            address = bc.addrToBinary(int(args[i]))
                            binary.append(address[8:16])
                            binary.append(address[0:8])
                        elif argTypes[i] == "register":  # One register in one-byte
                            binary.append(rl.registerToFourBit(args[i]))
                        elif (
                            argTypes[i] == "register-register"
                        ):  # Both registers to one-byte (Two arguments in one match)
                            binary.append(rl.registersToEightBit(args[i], args[i + 1]))
                            i += 1
                        elif argTypes[i] == "literal":
                            if args[i][0] == "-":
                                binary.append(bc.signedIntToBinary(int(args[i])))
                            else:
                                binary.append(bc.unsignedIntToBinary(int(args[i])))
                        i += 1
                for byte in binary:
                    binaryString += byte
    print(binaryString)
    with open("file.bin", "w") as file:
        file.write(binaryString)


if __name__ == "__main__":
    main()
