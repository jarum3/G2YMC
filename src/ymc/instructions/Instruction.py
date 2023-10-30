#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   Instruction class, encodes data about individual instructions
#
#######################################################################
from typing import Callable, Literal


class Instruction:
    def __init__(
        self,
        instruction: str,
        hexCode: str,
        width: int,
        argTypes: list[Literal["register", "register-register", "memory", "literal"]]
        | None,
        function: Callable[..., None],
        generalFlags: bool = False,
        carryFlag: bool = False,
    ) -> None:
        self.instruction = instruction # Actual code (e.g. mov, hlt)
        self.hexCode = hexCode # Hex code (A9, 04)
        self.width = width # Total width including arguments (found in encoding document)
        self.argTypes = argTypes    # Contains either array of argument types 
                                                                    # mapping to YMCCPU type-width dictionary, or value None
                                                                    # if No arguments are given
        self.function = function # Contains the name in asmFunctions.py for this instruction's function for the simulator
        self.generalFlags = generalFlags # Whether or not instruction sets OF, ZF, and SF flags
        self.carryFlag = carryFlag # Whether or not instruction sets CF flag

