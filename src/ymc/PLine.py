#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   PLine class,  called it PLine so it wouldn't be confused with
#   the line keyword
#
#######################################################################


class PLine:

    def __init__(self, text, type):
        self.text = text
        self.type = type
        self.YMC_string = None  # this will be updated by our switch statement
        self.assembly_string = None

        if self.text.startswith(
                '   '
        ):  # Modify this condition based on the type of indentation you expect
            # define parent here
            # self.parent = [PARENT LINE]
            print("Line starts with indentation:")
