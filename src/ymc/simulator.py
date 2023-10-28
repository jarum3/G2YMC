import pickle
from instructions.Instruction import Instruction
import YMCCPU as cpu


def main():
    with open("instructions/asm.pkl", "rb") as file:
        instructions: dict[str, Instruction] = pickle.load(file)
    with open("file.bin", "rb") as file:
        while (byte := file.read(1)):
            currHex = byte.hex()
            currInstr: Instruction = instructions[currHex]
            args: list[str] = []
            for i, arg in enumerate(currInstr.argTypes):
                args[i] = file.read(cpu.typeWidths[arg])
            currInstr.function(*args)


if __name__ == "__main__":
    main()
