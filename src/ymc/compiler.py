#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   HLC to YMC Compiler
#
#######################################################################

from PLine import PLine
import helpers.compiler_extension as ce
import helpers.compiler_functions as cf
from pathlib import Path

def main(file_path):
    program_counter: int = 0
    pline_list: list[PLine] = []
    i: int = 0

    with open(file_path, 'r') as file:
        # Iterate over each line in the file
        for line_number, line in enumerate(file, start=0): # Process each line here
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
            if pline_instance.text.startswith('   '):
                cf.set_parent(pline_instance, pline_list, i)
                is_last_line = line_number == cf.get_number_of_lines(file_path) - 1
                if not is_last_line:
                    next_line = next(file)
                    if (next_line.strip().isspace() or not next_line.startswith('   ')) and (not pline_instance.parent.text.startswith("Else")): # if next line is blank or not indented and it has a parent, then it is the last line in the code block
                        program_counter += 3 # Always adds a jump of 3 bytes after the final child UNLESS it's at the end of an else statement
                else:
                    program_counter += 3

            i += 1

            # this line will execute the corresponding function based on the line type
            program_counter += ce.switch_dict.get(pline_instance.type, ce.default_case)(pline_instance)
                
        pline_list.append(cf.create_hlt("[End of Code]", program_counter, "hlt")) # create hlt PLine Instance at end of the PLine list
        program_counter += 1                                                            # add 1 byte for HLT instruction

        # Add jump locations to if, else, and while sections of pline_list
        pline_list = cf.add_jumps(pline_list)

    output_path = Path(__file__).with_name('test.ymc')
    output_path_str = output_path.absolute()
    # Write assembly to file r"C:\Users\jacob\OneDrive\Desktop\School\Fall 2023\CSC 365 CA\group project\test\src\ymc\test.ymc"
    with open(output_path_str, "w") as file:
        string = ""
        for pline in pline_list:
            string += pline.YMC_string
        file.write(string)

if __name__ == '__main__':
    input_path = Path(__file__).with_name('test.hlc')
    input_path_str = input_path.absolute()
    main(input_path_str)