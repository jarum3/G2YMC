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
        self.text = text
        self.YMC_string = None # this will be updated by our switch statement
        self.assembly_string = None
        self.isParent = False

        if self.text.startswith("signed" or "unsigned"): # delclaration
            self.type = 1

        elif self.text.startswith("if" or "else" or "while"): # relational
            self.type = 3
            self.isParent = True

        elif self.text.includes("=" or"+" or "-" or "*" or "/"): # arithmetic
            self.type = 2

        elif self.text.startswith("print"): # print
            self.type = 4

    def setYMC(self, ymc): # this is how we will store the YMC string
        self.YMC_string = ymc

    def setParent(self, parent):
        self.parent = parent