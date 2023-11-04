# Just some functions that I made to clean up the compiler program
# Jacob Duncan

from PLine import PLine

program_counter = 0

registers: dict[str, int] = {"EDX": 0, "ECX": 0, "EBX": 0, "EAX": 0}

flags: dict[str, bool] = {"OF": False, "SF": False, "CF": False, "ZF": False}  # I'm getting a runtime error here. It's goes away by adding ' ' around dict[str, bool] --Brad

size = 1024  # 1 kb is 1000 bytes
default_value = 0  # Define the default value.
memory = [default_value] * size

# Function to get the number of lines in a file, didn't feel big enough to make a new file for it
def get_number_of_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            line_count = sum(1 for line in file)
        return line_count
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Setting the parent of the each line instance
def set_parent(pline_instance, pline_list, i):
    prev_line = pline_list[i - 1]
    if not prev_line.isParent:
        pline_instance.add_parent(prev_line.parent)
        return
    pline_instance.add_parent(prev_line)


# This stuff is for the switch statement

##########################
# Variable Declaration
# Brad K
##########################
def declaration(pline_instance): # start by checking if signed or unsigned
    line_text = pline_instance.text # grab text from line
    variables = line_text.split()   # split variables in line into list. Im not sure if there's going to be HLC with less than 3 variables
    del variables[0]                # delete signed/unsigned word from variables list

    if line_text.startswith("signed"):  # start by checking if signed or unsigned
        flags["SF"] = True                        # set flag to True if signed
        for v in variables:               # go through each variable and assign to location in storage
            print(v)
    elif pline_instance.text.startswith("unsigned"):
        flags["SF"] = False # set flag to False if unsigned
        for v in variables:               # go through each variable and assign to location in storage
            print(v)                      # Currently just printing

def arithmetic(pline_instance): # assignment portion of flowchart
    print("This is case 2")
def relational(pline_instance): # if/else and while statements, start by checking what each line is
    print("This is case 3")
def printD(pline_instance): # print statements
    print("This is case 4")
def default_case(pline_instance):
    print("This is the default case. Something went very wrong")    

switch_dict = {
    1: declaration,
    2: arithmetic,
    3: relational,
    4: printD
}