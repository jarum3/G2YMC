import pickle
from instructions.Instruction import Instruction


def main():
    # Should use files asm.pkl to convert from assembly code to binary
    # asm.pkl should contain object files for all instructions, with their assigned hex code and length being used to create binary data

    with open("instructions/asm.pkl", "rb") as file:
        instructions: list[Instruction] = pickle.load(file)
    print(instructions)
    # Open input file

    # Loop through lines of input file

    # Convert line into instruction and arguments

    # Read argument types from instruction

    # Convert arguments into binary

    # Store instruction with arguments in binary

    # Move to next line


if __name__ == "__main__":
    main()