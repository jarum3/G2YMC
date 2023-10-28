#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   PLine class,  called it PLine so it wouldn't be confused with
#   the line keyword
#
#######################################################################
from typing import Callable, Literal


class Instruction:

    def __init__(self,
                 instruction: str,
                 hexCode: str,
                 width: int,
                 argTypes: list[Literal["register", "register-register",
                                        "memory", "literal"]] | None,
                 function: Callable[..., None],
                 carryFlag: bool = False,
                 otherFlags: bool = False) -> None:
        self.instruction = instruction
        self.hexCode = hexCode
        self.width = width
        self.assembly_string: str | None = None
        self.argTypes = argTypes
        self.function = function
        self.carryFlag = carryFlag
        self.otherFlags = otherFlags