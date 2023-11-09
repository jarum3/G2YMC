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
        self.YMC_string: str = " " # this will be updated by our switch statement
        self.assembly_string: str = " "
        self.registers: dict[str, bool] = {"EDX": False, "ECX": False, "EBX": False, "EAX": False}
        self.flags: dict[str, bool] = {"OF": False, "SF": False, "CF": False, "ZF": False}
        arithmetic: list[str] = ["=", "+", "-", "*", "/"]

        if self.text.startswith("signed" or "unsigned"): # delclaration
            self.type = 1
            self.isParent = False
        elif self.text.startswith("if" or "else" or "while"): # relational
            self.type = 3
            self.isParent = True
        # Checks if any character from the arithmetic list is found in self.text
        elif any(x in self.text for x in arithmetic): # arithmetic
            self.type = 2
            self.isParent = False
        elif self.text.startswith("print"): # print
            self.type = 4
            self.isParent = False

    def set_register(self, reg:str):
        for key in self.registers:
            if reg == key:
                self.registers[reg] = True

    def set_flag(self, pflag:str):
        for key in self.flags:
            if pflag == key:
                self.registers[pflag] = True

    def set_YMC(self, ymc: str): # this is how we will store the YMC string
        self.YMC_string = ymc

    def append_YMC(self, ymc: str): # this is how we will store the YMC string
        self.YMC_string += ymc  + "\n"


    def add_parent(self, parent):
        self.parent: PLine = parent

    def set_address(self, address):
        self.address: int = address