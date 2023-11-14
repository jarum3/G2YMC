########################
# Generates instances of each instruction as an object of Instruction class,
# then adds them to two dictionaries, and saves those dictionaries
# to two pickle files to be used later
########################
from instructions.Instruction import Instruction
from instructions.asmFunctions import *
import pickle

# Empty dictionaries
instructionsByHex: dict[str, Instruction] = {}
instructionsByName: dict[str, Instruction] = {}


## Adds a single instruction to dictionary of instructions with hex code key (for simulator) and instruction name (for encoder)
def addDict(instr: Instruction) -> None:
    instructionsByHex[instr.hexCode] = instr
    instructionsByName[instr.instruction] = instr


def main():
    # No parentheses for function name
    # Instruction name, hex code, total width, argument types, function, and optional general flags and carry flags
    # All can be found in encoding document, just written down in code
    # Halt, uses built-in exit
    addDict(Instruction("hlt", "A0", 1, None, exit))
    # Output instructions
    addDict(Instruction("outs", "A1", 2, ["register"], outputSigned))
    addDict(Instruction("outu", "A2", 2, ["register"], outputUnsigned))
    addDict(Instruction("outnl", "A3", 1, None, outputNewline))
    # Mov instructions
    addDict(Instruction("movrr", "01", 2, ["register-register"], movRegisterRegister))
    addDict(Instruction("movrm", "02", 4, ["register", "memory"], movRegisterMemory))
    addDict(Instruction("movrl", "03", 3, ["register", "literal"], movRegisterLiteral))
    addDict(Instruction("movmr", "04", 4, ["memory", "register"], movMemoryRegister))
    # Two-argument arithmetic
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
            "addrm", "26", 4, ["register", "memory"], addRegisterMemory, True, True
        )
    )
    addDict(
        Instruction(
            "subrm", "27", 4, ["register", "memory"], subRegisterMemory, True, True
        )
    )
    addDict(
        Instruction("mulrm", "28", 4, ["register", "memory"], uMultRegisterMemory, True)
    )
    addDict(
        Instruction(
            "smulrm", "29", 4, ["register", "memory"], sMultRegisterMemory, True
        )
    )
    addDict(
        Instruction("divrm", "2A", 4, ["register", "memory"], uDivRegisterMemory, True)
    )
    addDict(
        Instruction("udivrm", "2B", 4, ["register", "memory"], sDivRegisterMemory, True)
    )
    
    ## Compare
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
    # Jumps
    addDict(Instruction("jmp", "60", 3, ["memory"], unconditionalJump))
    addDict(Instruction("jg", "60", 3, ["memory"], jumpGreater))
    addDict(Instruction("jge", "61", 3, ["memory"], jumpGreaterEqual))
    addDict(Instruction("jl", "62", 3, ["memory"], jumpLess))
    addDict(Instruction("jle", "63", 3, ["memory"], JumpLessEqual))
    addDict(Instruction("jne", "64", 3, ["memory"], jumpNotEqual))
    addDict(Instruction("je", "65", 3, ["memory"], jumpEqual))
    ## Three-arg arithmetic, split to stay under 90 columns
    addDict(
        Instruction(
            "addsub",
            "80",
            3,
            ["register-register", "register"],
            addSubRegisters,
            True,
            True,
        )
    )
    addDict(
        Instruction(
            "addmul", "81", 3, ["register-register", "register"], addMulRegisters, True
        )
    )
    addDict(
        Instruction(
            "addsmul",
            "82",
            3,
            ["register-register", "register"],
            addsMulRegisters,
            True,
        )
    )
    addDict(
        Instruction(
            "adddiv", "83", 3, ["register-register", "register"], addDivRegisters, True
        )
    )
    addDict(
        Instruction(
            "addsdiv",
            "84",
            3,
            ["register-register", "register"],
            addsDivRegisters,
            True,
        )
    )
    addDict(
        Instruction(
            "subadd",
            "85",
            3,
            ["register-register", "register"],
            subAddRegisters,
            True,
            True,
        )
    )
    addDict(
        Instruction(
            "submul", "86", 3, ["register-register", "register"], subMulRegisters, True
        )
    )
    addDict(
        Instruction(
            "subsmul",
            "87",
            3,
            ["register-register", "register"],
            subsMulRegisters,
            True,
        )
    )
    addDict(
        Instruction(
            "subdiv", "88", 3, ["register-register", "register"], subDivRegisters, True
        )
    )
    addDict(
        Instruction(
            "subsdiv",
            "89",
            3,
            ["register-register", "register"],
            subsDivRegisters,
            True,
        )
    )
    addDict(
        Instruction(
            "muladd",
            "8A",
            3,
            ["register-register", "register"],
            mulAddRegisters,
            True,
            True,
        )
    )
    addDict(
        Instruction(
            "mulsub",
            "8B",
            3,
            ["register-register", "register"],
            mulSubRegisters,
            True,
            True,
        )
    )
    addDict(
        Instruction(
            "muldiv", "8C", 3, ["register-register", "register"], mulDivRegisters, True
        )
    )
    addDict(
        Instruction(
            "smuladd",
            "8D",
            3,
            ["register-register", "register"],
            smulAddRegisters,
            True,
            True,
        )
    )
    addDict(
        Instruction(
            "smulsub",
            "8E",
            3,
            ["register-register", "register"],
            smulSubRegisters,
            True,
            True,
        )
    )
    addDict(
        Instruction(
            "smulsdiv",
            "8F",
            3,
            ["register-register", "register"],
            smulsDivRegisters,
            True,
        )
    )
    addDict(
        Instruction(
            "divadd",
            "90",
            3,
            ["register-register", "register"],
            divAddRegisters,
            True,
            True,
        )
    )
    addDict(
        Instruction(
            "divsub",
            "91",
            3,
            ["register-register", "register"],
            divSubRegisters,
            True,
            True,
        )
    )
    addDict(
        Instruction(
            "divmul", "92", 3, ["register-register", "register"], divMulRegisters, True
        )
    )
    addDict(
        Instruction(
            "sdivadd",
            "93",
            3,
            ["register-register", "register"],
            sdivAddRegisters,
            True,
            True,
        )
    )
    addDict(
        Instruction(
            "sdivsub",
            "94",
            3,
            ["register-register", "register"],
            sdivSubRegisters,
            True,
            True,
        )
    )
    addDict(
        Instruction(
            "sdivsmul",
            "95",
            3,
            ["register-register", "register"],
            sdivsMulRegisters,
            True,
        )
    )
    addDict(Instruction("addadd", "96", 3, ["register-register", "register"], addAddRegisters, True, True))
    addDict(Instruction("subsub", "97", 3, ["register-register", "register"], subSubRegisters, True, True))
    addDict(Instruction("mulmul", "98", 3, ["register-register", "register"], mulMulRegisters, True))
    addDict(Instruction("smulsmul", "99", 3, ["register-register", "register"], smulsMulRegisters, True))
    addDict(Instruction("divdiv", "9A", 3, ["register-register", "register"], divDivRegisters, True))
    addDict(Instruction("sdivsdiv", "9B", 3, ["register-register", "register"], sdivsDivRegisters, True))

    # Write both dictionaries to pickle files
    #! Python processes filenames in relation to current working directory, make sure that it is set to G2YMC/src/ymc for this to work
    with open("instructions/instructionsByHex.pkl", "wb") as file:
        pickle.dump(instructionsByHex, file)
    with open("instructions/instructionsByName.pkl", "wb") as file:
        pickle.dump(instructionsByName, file)


if __name__ == "__main__":
    main()
