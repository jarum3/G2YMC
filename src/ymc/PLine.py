#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   PLine class,  called it PLine so it wouldn't be confused with
#   the line keyword
#
#######################################################################


class PLine:
    def __init__(self, text):
        self.text: str = text
        self.YMC_string: str = "" # this will be updated by our switch statement
        self.assembly_string: str = ""
        self.registers: dict[str, bool] = {"EDX": False, "ECX": False, "EBX": False, "EAX": False}
        self.arithmetic: list[str] = ["=", "+", "-", "*", "/"]
        self.type: int = self.set_type()
        self.isParent: bool
        self.parent: PLine
        self.last_child: PLine = PLine
        self.address: int = int

    def set_type(self) -> int:
        t: int = 0
        hlc_text: str = self.text.strip()
        if hlc_text.startswith("signed") or self.text.startswith("unsigned"): # delclaration
            t = 1
            self.isParent = False
        elif hlc_text.startswith("if") or self.text.startswith("else") or self.text.startswith("while"): # relational
            t = 3
            self.isParent = True
        elif hlc_text.startswith("print"): # print
            t = 4
            self.isParent = False
        # Checks if any character from the arithmetic list is found in self.text
        elif any(x in hlc_text for x in self.arithmetic): # arithmetic
            t = 2
            self.isParent = False
        elif hlc_text.startswith("[End of Code]"): # halt
            t = 5
            self.isParent = False
        return t

    def set_register(self, reg:str):
        for key in self.registers:
            if reg == key:
                self.registers[reg] = True

    def set_YMC(self, ymc: str): 
        self.YMC_string = ymc

    def add_YMC(self, ymc: str): 
        self.YMC_string += ymc

    def append_YMC(self, ymc: str): 
        self.YMC_string += ymc + "\n"

    def add_jump_loc(self, address: int): # this is used when adding locations to jumps.
        self.YMC_string += " " + str(address) + "\n"

    def add_parent(self, parent):
        self.parent: PLine = parent

    def set_address(self, address):
        self.address: int = address