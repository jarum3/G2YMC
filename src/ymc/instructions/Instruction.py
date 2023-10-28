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
                 hex: str,
                 width: int,
                 argTypes: list[Literal["register", "register-register",
                                        "memory", "literal"]] | None,
                 function: Callable[..., None],
                 flags: bool = False) -> None:
        self.instruction = instruction
        self.hex = hex
        self.width = width
        self.assembly_string: str | None = None
        self.argTypes = argTypes
        self.function = function
        self.flags = flags