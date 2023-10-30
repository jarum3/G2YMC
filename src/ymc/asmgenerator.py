from instructions.Instruction import Instruction
from instructions.asmFunctions import *
import pickle

instructionsByHex: dict[str, Instruction] = {}
instructionsByName: dict[str, Instruction] = {}


def addDict(instr: Instruction) -> None:
    instructionsByHex[instr.hexCode] = instr
    instructionsByName[instr.instruction] = instr


def main():
    # No parentheses for function name
    addDict(Instruction("hlt", "A0", 1, None, exit))
    # Continue for all instructions
    addDict(Instruction("outs", "A1", 2, ["register"], outputSigned))
    addDict(Instruction("outu", "A2", 2, ["register"], outputUnsigned))
    addDict(Instruction("outnl", "A3", 1, None, outputNewline))
    addDict(Instruction("movrr", "01", 2, ["register-register"], movRegisterRegister))
    addDict(Instruction("movrm", "02", 4, ["register", "memory"], movRegisterMemory))
    addDict(Instruction("movrl", "03", 3, ["register", "literal"], movRegisterLiteral))
    addDict(
        Instruction("add", "20", 2, ["register-register"], addRegisters, True, True)
    )
    addDict(
        Instruction("sub", "21", 2, ["register-register"], subRegisters, True, True)
    )
    addDict(Instruction("mul", "22", 2, ["register-register"], uMultRegisters, True))
    addDict(Instruction("smul", "23", 2, ["register-register"], sMultRegisters, True))
    addDict(Instruction("div", "24", 2, ["register-register"], uDivRegisters, True))
    addDict(Instruction("sdiv", "25", 2, ["register-register"], sDivRegisters, True))
    addDict(
        Instruction(
            "addrm", "26", 2, ["register", "memory"], addRegisterMemory, True, True
        )
    )
    addDict(
        Instruction(
            "subrm", "27", 2, ["register", "memory"], subRegisterMemory, True, True
        )
    )
    addDict(
        Instruction("mulrm", "28", 2, ["register", "memory"], uMultRegisterMemory, True)
    )
    addDict(
        Instruction(
            "smulrm", "29", 2, ["register", "memory"], sMultRegisterMemory, True
        )
    )
    addDict(
        Instruction("divrm", "2A", 2, ["register", "memory"], uDivRegisterMemory, True)
    )
    addDict(
        Instruction("udivrm", "2B", 2, ["register", "memory"], sDivRegisterMemory, True)
    )
    addDict(
        Instruction(
            "cmprr", "40", 2, ["register-register"], compareRegisterRegister, True, True
        )
    )
    addDict(
        Instruction(
            "cmprm", "41", 4, ["register", "memory"], compareRegisterMemory, True, True
        )
    )
    addDict(Instruction("jmp", "60", 3, ["memory"], unconditionalJump))
    addDict(Instruction("jg", "60", 3, ["memory"], jumpGreater))
    addDict(Instruction("jge", "61", 3, ["memory"], jumpGreaterEqual))
    addDict(Instruction("jl", "62", 3, ["memory"], jumpLess))
    addDict(Instruction("jle", "63", 3, ["memory"], JumpLessEqual))
    addDict(Instruction("jne", "64", 3, ["memory"], jumpNotEqual))
    addDict(Instruction("je", "65", 3, ["memory"], jumpEqual))

    with open("instructions/instructionsByHex.pkl", "wb") as file:
        pickle.dump(instructionsByName, file)
    with open("instructions/instructionsByName.pkl", "wb") as file:
        pickle.dump(instructionsByName, file)


if __name__ == "__main__":
    main()
