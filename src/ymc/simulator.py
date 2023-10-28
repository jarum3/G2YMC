import pickle
from instructions.Instruction import Instruction
import YMCCPU as cpu


def main():
    with open("instructions/asm.pkl", "rb") as file:
        instructions: dict[str, Instruction] = pickle.load(file)
    # TODO: Edit this to first read the file into the start of memory as strings, then perform operations on that memory.
    with open("file.bin", "rb") as file:
        while (True):  # Halt instruction should call exit()
            file.seek(cpu.instructionPointer)
            byte = file.read(1)
            currHex = byte.hex()
            currInstr: Instruction = instructions[currHex]
            args: list[str] = []
            for i, arg in enumerate(currInstr.argTypes):
                args[i] = f'{file.read(cpu.typeWidths[arg]):0>8b}'
            cpu.instructionPointer += currInstr.width
            currInstr.function(*args)


if __name__ == "__main__":
    main()
