import pickle
from instructions.Instruction import Instruction
import helpers.binaryConversion as bc
import helpers.registerLookup as rl


def main():
    # Should use files asm.pkl to convert from assembly code to binary
    # asm.pkl should contain object files for all instructions, with their assigned hex code and length being used to create binary data
    binaryString = ''
    with open("instructions/instructionsByName.pkl", "rb") as file:
        instructions: dict[str, Instruction] = pickle.load(file)
    # Open input file
    with open("file.asm", "r") as file:
        for line in file:
            # Loop through lines of input file
            if (len(line)) > 0:
                pieces = line.split(" ")
                currInstr = pieces[0]
                args = pieces[1:]
                # Convert line into instruction and arguments
                binary: list[str] = []
                binary[0] = bc.hexToBinary(instructions[currInstr].hexCode)
                argTypes = instructions[currInstr].argTypes
                if args and argTypes:
                    # Read argument types from instruction
                    byteCounter = 1
                    i = 0
                    while i < len(args):
                        if argTypes[i] == 'memory':
                            address = bc.addrToBinary(int(args[i]))
                            binary[byteCounter] = address[8:16]
                            binary[byteCounter + 1] = address[0:8]
                            byteCounter += 1
                        elif argTypes[i] == 'register':
                            binary[byteCounter] = rl.registerToFourBit(args[i])
                        elif argTypes[i] == 'register-register':
                            binary[byteCounter] = rl.registersToEightBit(
                                args[i], args[i + 1])
                            i += 1
                        elif argTypes[i] == 'literal':
                            if (args[i][0] == "-"):
                                binary[byteCounter] = bc.signedIntToBinary(
                                    int(args[i]))
                            else:
                                binary[byteCounter] = bc.unsignedIntToBinary(
                                    int(args[i]))
                        byteCounter += 1
                        i += 1
                for byte in binary:
                    binaryString += byte

    with open("file.bin", "w") as file:
        file.write(binaryString)


if __name__ == "__main__":
    main()