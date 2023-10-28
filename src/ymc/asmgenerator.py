from instructions.Instruction import Instruction
from instructions.asmFunctions import *
import pickle

instructions: dict[str, Instruction] = {}


def addDict(instr: Instruction) -> None:
    instructions[instr.instruction] = instr


def main():
    # No parentheses for function name
    addDict(Instruction("hlt", "A0", 1, None, exit))
    # Continue for all instructions
    addDict(Instruction("outs", "A1", 2, ["register"], outputSigned))
    addDict(Instruction("outu", "A2", 2, ["register"], outputUnsigned))
    addDict(Instruction("outnl", "A3", 1, None, outputNewline))
    addDict(
        Instruction("movrr", "01", 2, ["register-register"],
                    movRegisterRegister))
    addDict(
        Instruction("movrm", "02", 4, ["register", "memory"],
                    movRegisterMemory))
    addDict(
        Instruction("movrl", "03", 3, ["register", "literal"],
                    movRegisterLiteral))
    addDict(Instruction("add"), "20", 2, ["register-register"], addNumbers,
            True, True)

    with open("instructions/asm.pkl", "wb") as file:
        pickle.dump(instructions, file)


if __name__ == "__main__":
    main()