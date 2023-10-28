#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   PLine class,  called it PLine so it wouldn't be confused with
#   the line keyword
#
#######################################################################
from typing import Callable


class Instruction:

    def __init__(self, instruction: str, hex: str, width: int,
                 argTypes: list[str], function: Callable[..., None]) -> None:
        self.instruction = instruction
        self.hex = hex
        self.width = width
        self.assembly_string: str | None = None
        self.argTypes = argTypes
        self.function = function