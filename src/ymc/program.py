import pickle
from typing import Literal

from instructions.Instruction import Instruction


class Program:
    def __init__(self, lineNumber: bool = False) -> None:
        self.lineNumber = lineNumber
        self.variables: dict[str, tuple[int, bool]] = {}
        self.address: int = 0
        self.count = 0
        self.varCount: int = 0
        self.tabbed: bool = False
        self.tabParent: str | None = None
        self.tabParentType: Literal["if", "else", "loop"] | None = None
        self.tabCount: int
        self.bodyList: list[str] = []
        self.bodyDict: dict[int, str] = {}
        self.hlcLines: dict[int, str] = {}
        self.jmpAddress = 0
        with open("instructions/instructionsByName.pkl", "rb") as file:
            self.instructions: dict[str, Instruction] = pickle.load(file)

    def addLine(self, text: str, hlc: str) -> None:
        line = text
        if (self.lineNumber):
            line = str(self.address) + "\t" + text
        self.bodyList.append(line)
        self.bodyDict[self.address] = line
        self.hlcLines[self.address] = hlc
        self.address += self.instructions[text.split(" ")[0]].width
        self.count += 1

    def replaceJump(self, address: int) -> None:
        line = self.bodyList[self.tabCount - 1]
        lineChunks = line.split("[")
        newLine = lineChunks[0] + str(address)
        self.bodyList[self.tabCount - 1] = newLine
        for key in self.bodyDict:
            if self.bodyDict[key] == line:
                lineAddr = key
                self.bodyDict[lineAddr] = newLine
                break
    def removeParent(self) -> None:
        self.tabbed = False
        self.tabParent = None
        self.tabParentType = None
