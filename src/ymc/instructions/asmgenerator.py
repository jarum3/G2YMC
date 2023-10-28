from Instruction import *
from asmFunctions import *

instructions: dict[str, Instruction] = {}


def addDict(instr: Instruction) -> None:
    instructions[instr.instruction] = instr


hlt: Instruction = Instruction("hlt", "A0", 1, [""],
                               exit)  # No parentheses on function name
addDict(hlt)
# Continue for all instructions