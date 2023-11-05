# Just some functions that I made to clean up the compiler program
# Jacob Duncan

from PLine import PLine

program_counter = 0
registers: dict[str, int] = {"EDX": 0, "ECX": 0, "EBX": 0, "EAX": 0}
flags: dict[str, bool] = {"OF": False, "SF": False, "CF": False, "ZF": False}  # I'm getting a runtime error here. It's goes away by adding ' ' around dict[str, bool] --Brad

variables: dict[str, int] = {"a": 0, "b": 0, "c": 0, "x": 0, "y": 0, "z": 0}
variables_declared: dict[str, bool] = {"a": False, "b": False, "c": False, "x": False, "y": False, "z": False}

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

    line_text = pline_instance.text # grab text from line instance
    vars = line_text.split()   # split words in str into list. Im not sure if there's going to be HLC with less than 3 variables
    del vars[0]                # delete signed/unsigned word from variables list. EX:del vars[0]="signed" --> vars[0]="a"
                                        
    if line_text.startswith("signed"):    # start by checking if signed or unsigned
        flags["SF"] = True                # set flag to True if signed
        for v in vars:               # go through each variable 
            variables_declared[v] = True  #set a variable in 
    elif line_text.startswith("unsigned"):
        flags["SF"] = False               # set flag to False if unsigned
        for v in vars:                     # go through each variable in variables list
            variables_declared[v] = True    #
    return

def arithmetic(pline_instance): # assignment portion of flowchart
    print("This is case 2")
def relational(pline_instance): # if/else and while statements, start by checking what each line is
    print("This is case 3")
def printD(pline_instance): # print statements
    line_text = pline_instance.text # grab text from line
    split_line = line_text.split()   # split variables in line into list. Im not sure if there's going to be HLC with less than 3 variables
    arg = split_line[1]             # delete signed/unsigned word from variables list
    if arg is "/nl": 
        pline_instance.set_YMC("outnl")
    elif arg in variables:
        pline_instance.set_YMC(arg) # still need to write code past this point

def default_case(pline_instance):
    print("This is the default case. Something went very wrong")    

switch_dict = {
    1: declaration,
    2: arithmetic,
    3: relational,
    4: printD
}