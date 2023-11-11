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

####################################
# Variable Declaration
# Brad K
####################################
def declaration(pline_instance: PLine): # start by checking if signed or unsigned
    line_text: str = pline_instance.text # grab text from line instance
    vars: list[str] = line_text.split()  # split words in str into list. Im not sure if there's going to be HLC with less than 3 variables
    del vars[0]                # delete signed/unsigned word from variables list. EX:del vars[0]="signed" --> vars[0]="a"  
    # I deleted if statement for signed or unsigned since it is only calculated during arithmetic/compare
    for v in vars:
            dec_count = len(variables) + 1                 # set declaration count to length of variables (0) + 1 = 1
            variables[v] = len(memory) - dec_count       # set variables[v] equal to length of memory - declaration count
    return                          # EX: "Unsigned a b c" would have v = "a", len(memory) = 1024, len(variables) = 0, dec_count = 1, variables["x"] = 1024 - 1. Repeat for b and c.

##########################
# Arithmetic operations and Assignments
# Jacob Duncan
##########################
def arithmetic(pline_instance: PLine): # assignment portion of flowchart
    line_text: str = pline_instance.text # grab text from line
    vars: list[str] = line_text.split()   # split variables in line into list.

    assignment: str = vars[0] # get variable we are assigning a value to
    del vars[0]     # delete the variable being assiged cause its stored 
    del vars[0]     # delete the = sign

    pline_instance.set_address(program_counter) # Set the address of the first YMC instruction associated with the pline

    temp_ymc: str

    # Handle assignments here
    if len(vars) == 1: # this means that this is just an assingment operation with no arithmetic
        address: str = str(variables[vars[0]])
        if any(char.isdigit() for char in vars[0]): # literal
            temp_ymc = "movrl eax, " + vars[0] + "\n"
            program_counter += 3 # movrl is 3 bytes, so we increment the program_counter by 3
        else:
            temp_ymc = "movrm eax, " + address + "\n"
            program_counter += 4 # movrm is 4 bytes, so we increment the program_counter by 4
        
        temp_ymc += "movmr " + str(variables[assignment]) + ", eax\n"
        program_counter += 4 # movmr is 4 bytes, so we increment the program_counter by 4

        # Set modified registers and ymc
        pline_instance.set_register("EAX")
        pline_instance.set_YMC(temp_ymc)
        return

    isSigned: bool = False

    # Handle 2-arg arithmetic
    if len(vars) == 3: # this means it is a 2-arg operation, var[0] = arg1, var[1] = operator, var[2] = arg2
        arguments: list[int] = cf.set2args(vars, variables)
        operator: str = vars[1]
        if arguments[0] or arguments[1] < 0:
                isSigned = True

        temp_counter: int
        # Process first 2 lines of ymc
        temp_ymc, temp_counter = cf.ymc_arithemtic_movs(vars, variables, False)
        program_counter += temp_counter # Increment program counter by number of bytes calculated in ymc_arithemtic_movs function

        # Parse operators and process third line of ymc
        temp_ymc += cf.ymc_operation_2args(operator, isSigned)
        program_counter += 2 # All 2 arg arithmetic operations are 2 bytes

        # Process fourth and final line of ymc
        temp_ymc += "movmr " + str(variables[assignment]) + ", eax\n" 
        program_counter += 4 # movmr is 4 bytes, so we increment the program_counter by 4

        # Set modified registers and ymc
        pline_instance.set_register("EAX")
        pline_instance.set_register("EBX")
        pline_instance.set_YMC(temp_ymc)
        return

    # Handle 3-arg arithmetic
    elif len(vars) == 5: # this means it is 3-arg operation
        arguments: list[int] = cf.set3args(vars, variables)
        operators: list[str] = [vars[1], vars[3]]
        if arguments[0] or arguments[1] or arguments[2] < 0:
                isSigned = True

        temp_counter: int = 0
        # Process first 3 lines of ymc
        temp_ymc, temp_counter = cf.ymc_arithemtic_movs(vars, variables, True)
        program_counter += temp_counter # Increment program counter by number of bytes calculated in ymc_arithemtic_movs function

        # Parse operators and process fourth line of ymc
        temp_ymc += cf.ymc_operation_3args(operators, isSigned)
        program_counter += 3 # All 3 arg arithmetic operations are 3 bytes

        # Process fifth and final line of ymc
        temp_ymc += "movmr " + str(variables[assignment]) + ", eax\n" 
        program_counter += 4 # movmr is 4 bytes, so we increment the program_counter by 4

        # Set modified registers and ymc
        pline_instance.set_register("EAX")
        pline_instance.set_register("EBX")
        pline_instance.set_register("ECX")
        pline_instance.set_YMC(temp_ymc)
        return

def relational(pline_instance: PLine): # if/else and while statements, start by checking what each line is
    line_text: str = pline_instance.text  # grab text from line
    line_list: list[str] = line_text.split()   # split line into list.
    type: str = line_list[0] 
    if type == "if":            # check if line is if/else statement or while loop                                                                 
        print("Code for if goes here") # TODO: Terry
    elif type == "else":                                                                 
        print("Code for else goes here") # TODO: Terry 
    elif type == "While":                                                                 
        variable = line_list[1]
        sign = line_list[2]
        limit = line_list[3]
        # TODO: Determine how to find location of jump and 
        if sign == '=':                                      
            print("Code for equal loop goes here")
        elif sign == '!=':                                                                 
            print("Code for not equal loop goes here")
        elif sign == '<':                                                                 
            print("Code for less than loop goes here")
        elif sign == '<=':                                                                 
            print("Code for less than or equal loop goes here")
        elif sign == '>':                                                                
            print("Code for greater than loop goes here")
        elif sign == '>=':                                                                 
            print("Code for greater than or equal loop goes here")
    # TODO: If/Else - Terry
    # TODO: While - Brad
    # Both of our parts should first be split up into 3 if/elif statements and one else statement checking for what kind of statement it is; 

####################################
# Print
# Brad K
# TODO: Convert -[hex value] to [hex signed] EX: 0x7F = 127 AND 0x80 = -128
#                   In other words, change str(hex(arg_value)) to a function I'll create in compiler functions to return correct signed hex
####################################

def printD(pline_instance: PLine):          # print statements
    line_text: str = pline_instance.text  # grab text from line
    statement: list[str] = line_text.split()   # split line into list.
    arg: str = statement[1]              # set arg to second item in split_line list
    unsigned: list[str] = ["a","b","c"]         # declare signed and unsigned lists for if statements below
    signed: list[str] = ["x","y","z"]
    
    pline_instance.set_address(program_counter)

    if arg in variables:            # Check if arg is in variables (It won't be if it's literal)
        arg_location: str = str(variables[arg])   # set location of arg to value in dictionary and convert to string

    if arg == "\n":                # check if new line
        pline_instance.set_YMC("outnl") 
        program_counter += 1                 # Increase program counter by 1 (outnl [1 byte])
    elif arg in unsigned:           # else if arg is an unsigned variable
        pline_instance.set_YMC("movrm eax, " + arg_location)   # set YMC instruction to first move arg_location to register eax, then outs eax 
        pline_instance.append_YMC("outs eax")
        program_counter += 6                 # Increase program counter by 4 bytes (movrm) + 2 bytes (outs)
    elif arg in signed:           # else if arg is a signed variable
        pline_instance.set_YMC("movrm eax, " + arg_location) # same as unsigned but with 'outu eax'
        pline_instance.append_YMC("outu eax")
        program_counter += 6       # Increase program counter by 4 bytes (movrm) + 2 bytes (outu)
    elif arg[0] is '-':           # check if literal is negative
        pline_instance.set_YMC("movrl eax, " + arg)      # set YMC instruction to move literal arg to register eax
        pline_instance.append_YMC("outs eax")                   # append YMC instruction to outs eax
        program_counter += 5       # Increase program counter by 3 bytes (movrl) + 2 bytes (outu)
    else:                       # else it is positive
        pline_instance.set_YMC("movrl eax, " + arg)       # set YMC instruction to move literal arg to register eax
        pline_instance.append_YMC("outu eax")                   # append YMC instruction to outu eax
        program_counter += 5       # Increase program counter by 3 bytes (movrl) + 2 bytes (outu)
def default_case(pline_instance: PLine):
    print("This is the default case. Something went very wrong")    

# Switch dictionary to call functions
switch_dict = {
    1: declaration,
    2: arithmetic,
    3: relational,
    4: printD
}