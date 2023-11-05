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

def main():
    # Open the file in read mode
    file_path = "path_to_your_file.txt"  # Replace with the actual path to txt file 

    line_count: int = cf.get_number_of_lines(file_path)
    default_value1: PLine = None
    # Creation of line list, i.e. list that contains a PLine object for every line in the file
    pline_list: PLine = [default_value1] * line_count

    i = 0
    try:
        with open(file_path, 'r') as file: # the r here means read only mode
            # Iterate over each line in the file
            for line in file: # Process each line here
                # Create a line object. It will set a flag telling us what category it belongs to (print, declaration, arithmetic operation, while or if)
                pline_instance = PLine(line) 
                pline_list[i] = pline_instance
                
                # Setting the parent of the each line instance
                if pline_instance.text.startswith('   '):
                    cf.set_parent(pline_instance, pline_list, i)
                i += 1

                # this line will execute the corresponding function based on the line type
                ce.switch_dict.get(pline_instance.type, ce.default_case)(pline_instance)

    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()