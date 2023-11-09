#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   Extension to the compiler to handle actual translation
#
#######################################################################

import math
from PLine import PLine
import helpers.compiler_functions as cf

program_counter: int = 0
registers: dict[str, int] = {"EDX": 0, "ECX": 0, "EBX": 0, "EAX": 0}
flags: dict[str, bool] = {"OF": False, "SF": False, "CF": False, "ZF": False}

variables: dict[str, int] = {}

size: int = 1024  # 1 kb is 1000 bytes
default_value = 0  # Define the default value.
memory = [default_value] * size
# This stuff is for the switch statement

####################################
# Variable Declaration
# Brad K
####################################
def declaration(pline_instance): # start by checking if signed or unsigned

    line_text = pline_instance.text # grab text from line instance
    vars = line_text.split()   # split words in str into list. Im not sure if there's going to be HLC with less than 3 variables
    del vars[0]                # delete signed/unsigned word from variables list. EX:del vars[0]="signed" --> vars[0]="a"  
    # I deleted if statement for signed or unsigned since it is only calculated during arithmetic/compare
    for v in vars:
            dec_count = len(variables) + 1                 # set declaration count to length of variables (0)  + 1 = 1
            variables[v] = len(memory) - dec_count       # set variables[v] equal to length of memory - declaration count
    return                          # EX: "Unsigned a b c" would have v = "a", len(memory) = 1024, len(variables) = 0, dec_count = 1, variables["x"] = 1024 - 1. Repeat for b and c.

##########################
# Arithmetic operations and Assignments
# Jacob Duncan
# TODO: Handle the memroy addresses. Will have to have a discussion about how we are handling memory
# TODO: Handle modified flags
# TODO: Finish 3-arg arithmetic. I don't think we specified what the YMC instruction would be if it were two of the same operators (i.e: a + b + c, we do not have an instruction to handle this)
##########################
def arithmetic(pline_instance): # assignment portion of flowchart
    line_text = pline_instance.text # grab text from line
    vars = line_text.split()   # split variables in line into list. Im not sure if there's going to be HLC with less than 3 variables

    assignment: str = vars[0]
    del vars[0]     # delete the variable being assiged cause its stored 
    del vars[0]     # delete the = sign

    temp_ymc: str

    # Handle assignments here
    # TODO: Handle memory
    if len(vars) == 1: # this means that this is just an assingment operation with no arithmetic
        if any(char.isdigit() for char in vars[0]): # literal
            variables[assignment] = int(vars[0]) # set varible to desired value
            temp_ymc = "movrl eax, " + vars[0] + "\n"
        else:
            variables[assignment] = variables[vars[0]] # variable
            temp_ymc = "movrm eax, " + "\n"# TODO: Add the address
        
        temp_ymc += "movmr , eax\n" # TODO: Add the address
        pline_instance.set_register("EAX")
        pline_instance.set_YMC(temp_ymc)
        return

    isSigned: bool = False

    # Handle 2-arg arithmetic
    # TODO: Handle memory and modified flags
    if len(vars) == 3: # this means it is a 2-arg operation, var[0] = arg1, var[1] = operator, var[2] = arg2
        arguments: list[int] = cf.set2args(vars, variables)
        operator: str = vars[1]
        if arguments[0] or arguments[1] < 0:
                isSigned = True

        # Process first line of ymc
        if any(char.isdigit() for char in vars[0]): # literal
            temp_ymc = "movrl eax, " + vars[0] + "\n"
        else: # variable
            temp_ymc = "movrm eax, " + "\n"# TODO: Add the address
        pline_instance.set_register("EAX")
        # Process second line of ymc
        if any(char.isdigit() for char in vars[2]): # literal
            temp_ymc += "movrl ebx, " + vars[2] + "\n"
        else: # variable
            temp_ymc += "movrm ebx, " + "\n"# TODO: Add the address
        pline_instance.set_register("EBX")

        # Parse operators and process third line of ymc
        if operator == "+":
            variables[assignment] = arguments[0] + arguments[1]
            temp_ymc += "add eax, ebx\n"
        elif operator == "-":
            variables[assignment] = arguments[0] - arguments[1]
            temp_ymc += "sub eax, ebx\n"
        elif operator == "*":
            variables[assignment] = arguments[0] * arguments[1]
            if isSigned == True:
                temp_ymc += "smul eax, ebx\n"
            else:
                temp_ymc += "mul eax, ebx\n"
        elif operator == "/":
            variables[assignment] = math.floor(arguments[0] / arguments[1])
            if isSigned == True:
                temp_ymc += "sdiv eax, ebx\n"
            else:
                temp_ymc += "div eax, ebx\n"

        temp_ymc += "movmr , eax\n" # TODO: Add the address
        pline_instance.set_YMC(temp_ymc)
        return

    # Handle 3-arg arithmetic
    # TODO: Handle memory and modified flags, finish translating to YMC
    elif len(vars) == 5: # this means it is 3-arg operation
        arguments: list[int] = cf.set3args(vars, variables)
        operators: list[str] = [vars[1], vars[3]]
        if arguments[0] or arguments[1] or arguments[2] < 0:
                isSigned = True

        # Process first line of ymc
        if any(char.isdigit() for char in vars[0]): # literal
            temp_ymc = "movrl eax, " + vars[0] + "\n"
        else: # variable
            temp_ymc = "movrm eax, " + "\n"# TODO: Add the address
        pline_instance.set_register("EAX")
        # Process second line of ymc
        if any(char.isdigit() for char in vars[2]): # literal
            temp_ymc += "movrl ebx, " + vars[2] + "\n"
        else: # variable
            temp_ymc += "movrm ebx, " + "\n"# TODO: Add the address
        pline_instance.set_register("EBX")
        # Process third line of ymc
        if any(char.isdigit() for char in vars[4]): # literal
            temp_ymc += "movrl ecx, " + vars[4] + "\n"
        else: # variable
            temp_ymc += "movrm ecx, " + "\n"# TODO: Add the address
        pline_instance.set_register("ECX")

        # Handle first operation. Operations are evaluated left to right, so we use the first two arguments here
        # When done, the result of the first operation will be stored in the destination variable for the time being
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
            variables[assignment] = math.floor(arguments[0] / arguments[1])
            if isSigned == True:
                print("Handle signed division here")
            else:
                print("Handle unsigned division here")

        # Handle second operation. Result of first op is stored in destination variable, so the operation is done on the variable and the third argument
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
            variables[assignment] = math.floor(variables[assignment] / arguments[2])
            if isSigned == True:
                print("Handle signed division here")
            else:
                print("Handle unsigned division here")

def relational(pline_instance): # if/else and while statements, start by checking what each line is
    print("This is case 3")

####################################
# Print
# Brad K
# TODO: Convert -[hex value] to [hex signed] EX: 0x7F = 127 AND 0x80 = -128
#                   In other words, change str(hex(arg_value)) to a function I'll create in compiler functions to return correct signed hex
####################################

def printD(pline_instance):          # print statements
    line_text = pline_instance.text  # grab text from line
    split_line = line_text.split()   # split line into list.
    arg = split_line[1]              # set arg to second item in split_line list
    arg_value = memory[variables[arg]]     # grab memory location from variables dictionary and get value from memory list
    unsigned = ["a","b","c"]         # declare signed and unsigned lists for if statements below
    signed = ["x","y","z"]

    if arg is "/nl":                # check if new line
        pline_instance.set_YMC("outnl")
    elif arg in unsigned:
        pline_instance.set_YMC("movrm eax, " + str(hex(arg_value)) + "\n" + "outs eax" )   # set YMC instruction to first move hex(arg_value) to register eax, then outs eax 
    elif arg in signed:
        pline_instance.set_YMC("movrm eax, " + str(hex(arg_value)) + "\n" + "outu eax") # set YMC instruction to first move hex(arg_value) to register eax, then outu eax


def default_case(pline_instance):
    print("This is the default case. Something went very wrong")    

# Switch dictionary to call functions
switch_dict = {
    1: declaration,
    2: arithmetic,
    3: relational,
    4: printD
}