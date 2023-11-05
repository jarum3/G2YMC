# Just some functions that I made to clean up the compiler and compiler_extension programs
# Jacob Duncan

from PLine import PLine

# Function to get the number of lines in a file, didn't feel big enough to make a new file for it
def get_number_of_lines(file_path) -> int:
    try:
        with open(file_path, 'r') as file:
            line_count: int = sum(1 for line in file)
        return line_count
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return 0

# Setting the parent of the each line instance
def set_parent(pline_instance, pline_list, i):
    prev_line = pline_list[i - 1]
    if not prev_line.isParent:
        pline_instance.add_parent(prev_line.parent)
        return
    pline_instance.add_parent(prev_line)

def set2args(vars, variables) -> list[int]:
    args = [0, 0]
    if any(char.isdigit() for char in vars[0]): # processing first argument
            args[0] = int(vars[0])
    else:
        args[0] = variables[vars[0]]
    if any(char.isdigit() for char in vars[2]): # processing second argument
        args[0] = int(vars[2])
    else:
        args[0] = variables[vars[2]]
    return args

def set3args(vars, variables) -> list[int]:
    args = [0, 0, 0]
    if any(char.isdigit() for char in vars[0]): # processing first argument
            args[0] = int(vars[0])
    else:
        args[0] = variables[vars[0]]
    if any(char.isdigit() for char in vars[2]): # processing second argument
        args[0] = int(vars[2])
    else:
        args[0] = variables[vars[2]]
    if any(char.isdigit() for char in vars[4]): # processing third argument
        args[0] = int(vars[4])
    else:
        args[0] = variables[vars[4]]
    return args