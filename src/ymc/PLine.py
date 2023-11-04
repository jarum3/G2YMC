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
        

        if self.text.startswith("signed" or "unsigned"): # delclaration
            self.type = 1
            self.isParent = False

        elif self.text.startswith("if" or "else" or "while"): # relational
            self.type = 3
            self.isParent = True

        elif self.text.includes("=" or"+" or "-" or "*" or "/"): # arithmetic
            self.type = 2
            self.isParent = False

        elif self.text.startswith("print"): # print
            self.type = 4
            self.isParent = False

    def set_YMC(self, ymc): # this is how we will store the YMC string
        self.YMC_string = ymc

    def add_parent(self, parent):
        self.parent = parent