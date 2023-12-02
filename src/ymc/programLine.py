#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   PLine class,  called it PLine so it wouldn't be confused with
#   the line keyword
#
#######################################################################

from typing import Literal
from program import Program


class programLine:
    def __init__(self, text: str, program: Program):
        self.text: str = text
        self.program: Program = program
        self.YMC_string: str | None = (
            None  # this will be updated by our switch statement
        )
        self.tabbed: bool = self.text.startswith("  ") or self.text.startswith("\t")
        self.text = self.text.strip()
        self.isParent = False
        self.type: Literal["declaration", "if", "else", "loop", "assignment", "output", "none"]
        self.determineType()
        self.generateYMC()

    def determineType(self) -> None:
        arithmetic: list[str] = ["=", "+", "-", "*", "/"]
        if self.text.startswith("signed") or self.text.startswith(
            "unsigned"
        ):  # declaration
            self.type = "declaration"
        elif self.text.startswith("if"):  # conditional
            self.type = "if"
            self.isParent = True
        elif self.text.startswith("else"):  # conditional
            self.type = "else"
            self.isParent = True
        elif self.text.startswith("while"):  # loop
            self.type = "loop"
            self.isParent = True
        # Checks if any character from the arithmetic list is found in self.text
        elif any(x in self.text for x in arithmetic):  # arithmetic
            self.type = "assignment"
        elif self.text.startswith("print"):  # print
            self.type = "output"
        else:
            self.type = "none"

    def generateYMC(self) -> None:
        self.checkTabs()
        match self.type:
            case "declaration":
                self.declarationGenerate()
            case "if":
                self.ifGenerate()
            case "else":
                self.elseGenerate()
            case "loop":
                self.loopGenerate()
            case "assignment":
                self.assignmentGenerate()
            case "output":
                self.outputGenerate()

    def declarationGenerate(self) -> None:
        line = self.text
        pieces = line.split(" ")
        sign = pieces[0] == "signed"
        pieces = pieces[1:]
        for i, _ in enumerate(pieces):
            self.program.varCount += 1
            self.program.variables[pieces[i]] = 1024 - self.program.varCount, sign

    def ifGenerate(self):
        line = self.text
        lineChunks = self.text.split(" ")[1:]
        left = lineChunks[0]
        relation = lineChunks[1]
        right = lineChunks[2]
        jmp = self.invertRelation(relation)
        self.move("eax", left)
        self.program.jmpAddress = self.program.address
        self.move("ecx", right)
        self.program.addLine("cmprr eax, ecx", self.text)
        if jmp:
            self.program.addLine(jmp + " [address]", self.text)
        self.program.tabCount = self.program.count
        self.program.tabParent = self.text
        self.program.tabParentType = "if"
        self.program.tabbed = True

    def elseGenerate(self):
        self.program.jmpAddress = self.program.address
        self.program.addLine("jmp [address]", self.text)
        self.program.tabParent = self.text
        self.program.tabParentType = "else"
        self.program.tabCount = self.program.count
    def loopGenerate(self):
        line = self.text
        lineChunks = line.split(" ")[1:]
        left = lineChunks[0]
        relation = lineChunks[1]
        right = lineChunks[2]
        jmp = self.invertRelation(relation)
        self.program.jmpAddress = self.program.address
        self.move("eax", left)
        self.move("ecx", right)
        self.program.addLine("cmprr eax, ecx", self.text)
        if jmp:
            self.program.addLine(jmp + " [address]", self.text)
        self.program.tabCount = self.program.count
        self.program.tabParent = self.text
        self.program.tabParentType = "loop"
        self.program.tabbed = True

    def assignmentGenerate(self) -> None:
        line = self.text
        lineChunks = line.split(" ")
        match len(lineChunks):
            case 3:
                ## Simple assignment
                self.move("eax", lineChunks[2])
                self.program.addLine(
                    "movmr " + str(self.program.variables[lineChunks[0]][0]) + ", eax", self.text
                )
            case 5:
                ## 2-arg
                signed = self.program.variables[lineChunks[0]][
                    1
                ]  ## Always used signed value of destination
                tmpOperand = self.operandCheck(lineChunks[3], signed)
                if tmpOperand:
                    operand: str = tmpOperand
                    self.move("eax", lineChunks[2])
                    self.move("ebx", lineChunks[4])
                    self.program.addLine(operand + " eax, ebx", self.text)
                    self.program.addLine(
                        "movmr " + str(self.program.variables[line[0]][0]) + ", eax", self.text
                    )
            case 7:
                ## 3 arg
                signed = self.program.variables[lineChunks[0]][
                    1
                ]  ## Always used signed value of destination
                tmpOperand1 = self.operandCheck(lineChunks[3], signed)
                tmpOperand2 = self.operandCheck(lineChunks[5], signed)
                if tmpOperand1 and tmpOperand2:
                    operand = tmpOperand1 + tmpOperand2
                    self.move("eax", lineChunks[2])
                    self.move("ebx", lineChunks[4])
                    self.move("ecx", lineChunks[6])
                    self.program.addLine(operand + " eax, ebx, ecx", self.text)
                    self.program.addLine(
                        "movmr " + str(self.program.variables[line[0]][0]) + ", eax", self.text
                    )

    def outputGenerate(self) -> None:
        line = self.text
        pieces = line.split(" ")
        var = pieces[1]
        if var == "\\n":
            self.program.addLine("outnl", self.text)
            return
        self.move("eax", var)
        sign = self.program.variables[var][1]
        if sign:
            signChar = "s"
        else:
            signChar = "u"
        self.program.addLine("out" + signChar + " eax", self.text)
        return

    def checkTabs(self) -> None:
        if self.program.tabbed and not self.tabbed:
            ## Before us is the last line in the block
            match self.program.tabParentType:
                case "loop":
                    if self.program.tabParent:
                        self.program.removeParent()
                        self.program.addLine(
                            "jmp " + str(self.program.jmpAddress), self.program.tabParent
                        )
                        self.program.replaceJump(self.program.address)
                case "if":  ## End of if
                    steps = 3
                    if not self.text.startswith(
                        "else"
                    ):  ## Else will insert an unconditional jump, we also want our if to skip over that
                        steps = 0
                        self.program.removeParent()
                    self.program.replaceJump(self.program.address+ steps)
                case "else":  ## End of else
                    self.program.removeParent()
                    self.program.replaceJump(self.program.address)

    def invertRelation(self, relation: str):
        match relation:
            case "==":
                return "jne"
            case "!=":
                return "je"
            case "<":
                return "jge"
            case "<=":
                return "jg"
            case ">":
                return "jle"
            case ">=":
                return "jl"

    def operandCheck(
        self, operand: str, signed: bool
    ) -> Literal["add", "sub", "smul", "mul", "sdiv", "div"] | None:
        signChar: str = ""
        if signed:
            signChar = "s"
        match operand:
            case "+":
                return "add"
            case "-":
                return "sub"
            case "*":
                return signChar + "mul"
            case "/":
                return signChar + "div"

    def move(self, register: str, value: str):
        memory: bool = False
        mov = "movr"
        if value.lstrip('-').isnumeric():
            mov += "l"
        else:
            memory = True
            mov += "m"
        if memory:
            self.program.addLine(
                mov + " " + register + ", " + str(self.program.variables[value][0]), self.text
            )
        else:
            self.program.addLine(mov + " " + register + ", " + value, self.text)
