import pickle
from instructions.Instruction import Instruction
import instructions.YMCCPU as cpu


# None of this is close to finished, I just wanted an idea of the program flow
def main():
    with open("instructions/asm.pkl", "rb") as file:
        instructions: dict[str, Instruction] = pickle.load(file)
    # TODO: Edit this to first read the file into the start of memory as strings, then perform operations on that memory.
    # TODO: Add special case for Memory to process 2 bytes into one argument (little-endian)
    with open("file.bin", "rb") as file:
        while True:  # Halt instruction should call exit()
            file.seek(cpu.instructionPointer)
            byte = file.read(1)
            currHex = byte.hex()
            currInstr: Instruction = instructions[currHex]
            args: list[str] = []
            if currInstr.argTypes:
                for i, arg in enumerate(currInstr.argTypes):
                    args[i] = f"{file.read(cpu.typeWidths[arg]):0>8b}"
            cpu.instructionPointer += currInstr.width
            currInstr.function(*args)


if __name__ == "__main__":
    main()
