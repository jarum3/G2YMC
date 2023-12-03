#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   HLC to YMC Compiler
#
#######################################################################
from __future__ import annotations      # It won't let me run the script without this in Compiler, CE, and CF
from PLine import PLine
import helpers.compiler_extension as ce
import helpers.compiler_functions as cf
from pathlib import Path

def main(file_path) -> list[PLine]:
    program_counter: int = 0
    pline_list: list[PLine] = []
    i: int = 0
    file_text: list[str] = []

    with open(file_path, 'r') as file:
        for line in file:
            if not file_text:
                file_text = [line]
            else:
                file_text.append(line)
        file_text.append("[End of Code]")

    for line_number, line in enumerate(file_text, start=0): # Process each line here
        if len(line.strip()) == 0: # skip the line if it is empty
            continue

        # Create a line object. It will set a flag telling us what category it belongs to (print, declaration, arithmetic operation, while or if)
        pline_instance = PLine(text = line) 

        if not pline_list:
            pline_list = [pline_instance]
        else:
            pline_list.append(pline_instance)

        pline_instance.set_address(program_counter)  # Set the address of the first YMC instruction associated with the pline
        pline_instance.set_type()
            
        # Setting the parent of the each line instance
        if pline_instance.text.startswith(' '):
            cf.set_parent(pline_instance, pline_list, i)
            next_line = file_text[line_number + 1]
            if (len(next_line.strip()) == 0 or not next_line.startswith(' ')) and (not pline_instance.parent.text.startswith("else")): # if next line is blank or not indented and it has a parent, then it is the last line in the code block
                    cf.set_last_child(pline_instance.parent, pline_instance)
                    program_counter += 3 # Always adds a jump of 3 bytes after the final child UNLESS it's at the end of an else statement

        i += 1

        # this line will execute the corresponding function based on the line type
        program_counter += ce.switch_dict.get(pline_instance.type, ce.default_case)(pline_instance)

    # Add jump locations to if, else, and while sections of pline_list
    pline_list = cf.add_jumps(file_text, i, pline_list)

    file_name = 'assembly.ymc'
    output_path = Path(__file__).with_name(file_name)
    output_path_str = output_path.absolute()
    # Write assembly to file r"C:\Users\jacob\OneDrive\Desktop\School\Fall 2023\CSC 365 CA\group project\test\src\ymc\test.ymc"
    with open(output_path_str, "w") as file:
        string = ""
        for pline in pline_list:
            if not pline.type == 1:     # don't include the signed/unsigned PLine types when writing YMC
                #string += str(pline.address) + "\t" # Added starting address of the YMC string groups inside the PLines
                string += pline.YMC_string
        file.write(string)
    print("HLC has been translated to YMC and stored in '" + file_name + "'")

    return pline_list

if __name__ == '__main__':
    input_path = Path(__file__).with_name('code.hlc')
    input_path_str = input_path.absolute()
    main(input_path_str)