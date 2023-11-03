#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   HLC to YMC Compiler
#
#######################################################################

from PLine import PLine
import ymc.helpers.compiler_extension as ce

program_counter = 0

registers: dict[str, int] = {"EDX": 0, "ECX": 0, "EBX": 0, "EAX": 0}

flags: dict[str, bool] = {"OF": False, "SF": False, "CF": False, "ZF": False}

size = 1024  # 1 kb is 1000 bytes
default_value = 0  # Define the default value.
memory = [default_value] * size

def main():
    # Open the file in read mode
    file_path = "path_to_your_file.txt"  # Replace with the actual path to txt file 

    line_count = ce.get_number_of_lines(file_path)
    default_value1 = None
    # Creation of line list, i.e. list that contains a PLine object for every line in the file
    pline_list = [default_value1] * line_count

    i = 0
    try:
        with open(file_path, 'r') as file: # the r here means read only mode
            # Iterate over each line in the file
            for line in file: # Process each line here
                # Create a line object. It will set a flag telling us what category it belongs to (print, declaration, arithmetic operation, while or if)
                pline_instance = PLine(line) 
                pline_list[i] = pline_instance
                i += 1
                
                # Setting the parent of the each line instance
                ce.set_parent(pline_instance, pline_list, i)

                # this line will execute the corresponding function based on the line type
                ce.switch_dict.get(pline_instance.type, ce.default_case)(pline_instance)

    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()