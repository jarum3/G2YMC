#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   HLC to YMC Compiler
#
#######################################################################

from programLine import programLine
from program import Program

def main(input: str, output: str, lineNumber: bool):
    # Open the file in read mode
    file_path = input  # Replace with the actual path to txt file 
    ymc_path = output
    # Creation of line list, i.e. list that contains a PLine object for every line in the file
    pline_list: list[programLine] = []
    program: Program = Program(lineNumber=lineNumber)
    with open("file.hlc", 'r') as file: # the r here means read only mode
        # Iterate over each line in the file
        count: int = 0
        for i, line in enumerate(file): # Process each line here
            # Create a line object. It will set a flag telling us what category it belongs to (print, declaration, arithmetic operation, while or if)
            pline_instance = programLine(line, program)
        programLine("\n", program)
        program.addLine("hlt", "compiler")
    with open(ymc_path, "w") as file:
        file.write("\n".join(program.bodyList))
    return (program.hlcLines, program.bodyDict)


if __name__ == '__main__':
    main("file.hlc", "file.ymc", True)