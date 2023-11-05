#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   Extension to the compiler to handle actual translation
#
#######################################################################

from PLine import PLine
import helpers.compiler_functions as cf

program_counter: int = 0
registers: dict[str, int] = {"EDX": 0, "ECX": 0, "EBX": 0, "EAX": 0}
flags: dict[str, bool] = {"OF": False, "SF": False, "CF": False, "ZF": False}  # I'm getting a runtime error here. It's goes away by adding ' ' around dict[str, bool] --Brad

variables: dict[str, int] = {"a": 0, "b": 0, "c": 0, "x": 0, "y": 0, "z": 0}
variables_declared: dict[str, bool] = {"a": False, "b": False, "c": False, "x": False, "y": False, "z": False}

size: int = 1024  # 1 kb is 1000 bytes
default_value = 0  # Define the default value.
memory = [default_value] * size

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

##########################
# Arithmetic operations and Assignments
# Jacob Duncan
##########################
def arithmetic(pline_instance): # assignment portion of flowchart
    line_text = pline_instance.text # grab text from line
    vars = line_text.split()   # split variables in line into list. Im not sure if there's going to be HLC with less than 3 variables

    assignment: str = vars[0]
    del vars[0]     # delete the variable being assiged cause its stored 
    del vars[0]     # delete the = sign

    # Handle assignments here
    if len(vars) == 1: # this means that this is just an assingment operation with no arithmetic
        if any(char.isdigit() for char in vars[0]):
            variables[assignment] = int(vars[0]) # set varible to desired value
        else:
            variables[assignment] = variables[vars[0]]
        # TODO: Add code to handle memory and translate into YMC, then return

    isSigned: bool = False

    # Handle 2-arg arithmetic
    if len(vars) == 3: # this means it is a 2-arg operation, var[0] = arg1, var[1] = operator, var[2] = arg2
        arguments: int = cf.set2args(vars, variables)
        operator: str = vars[1]
        if arguments[0] or arguments[1] < 0:
                isSigned = True

        # TODO: Add code to handle memory and translate to YMC, then return
        if operator == "+":
            variables[assignment] = arguments[0] + arguments[1]
        elif operator == "-":
            variables[assignment] = arguments[0] - arguments[1]
        elif operator == "*":
            variables[assignment] = arguments[0] * arguments[1]
            if isSigned == True:
                print("Handle signed multiplication here")
            else:
                print("Handle unsigned multiplication here")
        elif operator == "/":
            variables[assignment] = arguments[0] / arguments[1]
            if isSigned == True:
                print("Handle signed division here")
            else:
                print("Handle unsigned division here")

    # Handle 3-arg arithmetic
    elif len(vars) == 5: # this means it is 3-arg operation
        arguments: int = cf.set3args(vars, variables)
        operators: str = [vars[1], vars[3]]
        if arguments[0] or arguments[1] or arguments[2] < 0:
                isSigned = True

        # Handle first operation. Operations are evaluated left to right, so we use the first two arguments here
        # When done, the result of the first operation will be stored in the destination variable for the time being
        # TODO: Add code to handle memory and translate to YMC, then return
        if operators[0] == "+":
            variables[assignment] = arguments[0] + arguments[1]
        elif operators[0] == "-":
            variables[assignment] = arguments[0] - arguments[1]
        elif operators[0] == "*":
            variables[assignment] = arguments[0] * arguments[1]
            if isSigned == True:
                print("Handle signed multiplication here")
            else:
                print("Handle unsigned multiplication here")
        elif operators[0] == "/":
            variables[assignment] = arguments[0] / arguments[1]
            if isSigned == True:
                print("Handle signed division here")
            else:
                print("Handle unsigned division here")

        # Handle second operation. Result of first op is stored in destination variable, so the operation is done on the variable and the third argument
        # TODO: Add code to handle memory and translate to YMC, then return
        if operators[1] == "+":
            variables[assignment] = variables[assignment] + arguments[2]
        elif operators[1] == "-":
            variables[assignment] = variables[assignment] - arguments[2]
        elif operators[1] == "*":
            variables[assignment] = variables[assignment] * arguments[2]
            if isSigned == True:
                print("Handle signed multiplication here")
            else:
                print("Handle unsigned multiplication here")
        elif operators[1] == "/":
            variables[assignment] = variables[assignment] / arguments[2]
            if isSigned == True:
                print("Handle signed division here")
            else:
                print("Handle unsigned division here")

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