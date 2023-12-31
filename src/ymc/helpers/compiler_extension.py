#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   Extension to the compiler to handle actual translation
#
#######################################################################
from __future__ import annotations
from PLine import PLine
import helpers.compiler_functions as cf

registers: dict[str, int] = {"EDX": 0, "ECX": 0, "EBX": 0, "EAX": 0}
flags: dict[str, bool] = {"OF": False, "SF": False, "CF": False, "ZF": False}
variables: dict[str, int] = {}

####################################
# Variable Declaration
# Brad K
####################################
def declaration(pline_instance: PLine) -> int: # start by checking if signed or unsigned
    line_text: str = pline_instance.text # grab text from line instance
    vars: list[str] = line_text.split()  # split words in str into list. Im not sure if there's going to be HLC with less than 3 variables
    del vars[0]                # delete signed/unsigned word from variables list. EX:del vars[0]="signed" --> vars[0]="a"  
    
    for v in vars:              # for variables being declared in vars
            dec_count = len(variables) + 1        # set declaration count to length of variables (0) + 1 = 1
            variables[v] = 1024 - dec_count       # set variables[v] equal to length of memory - declaration count
    print("Declaration line processed") 
    return 0                     # counter shouldn't go up yet, return 0

##########################
# Arithmetic operations and Assignments
# Jacob Duncan
##########################
def arithmetic(pline_instance: PLine) -> int: # assignment portion of flowchart
    line_text: str = pline_instance.text # grab text from line
    vars: list[str] = line_text.split()   # split variables in line into list.
    counter: int = 0
    temp_ymc: str
    isSigned: bool
    signed: list[str] = ["x", "y", "z"]
    assignment: str = vars[0] # get variable we are assigning a value to
    del vars[0]     # delete the variable being assiged cause its stored 
    del vars[0]     # delete the = sign

    if assignment in signed:
        isSigned = True
    else:
        isSigned = False

    # Handle assignments here
    if len(vars) == 1: # this means that this is just an assingment operation with no arithmetic
        if any(char.isdigit() for char in vars[0]): # literal
            temp_ymc = "movrl eax, " + vars[0] + "\n" 
            counter += 3 # movrl is 3 bytes, so we increment the program_counter by 3
        else:
            address: str = str(variables[vars[0]])
            temp_ymc = "movrm eax, " + address + "\n"
            counter += 4 # movrm is 4 bytes, so we increment the program_counter by 4
        
        temp_ymc += "movmr " + str(variables[assignment]) + ", eax\n"
        counter += 4 # movmr is 4 bytes, so we increment the program_counter by 4

        # Set modified registers and ymc
        pline_instance.set_register("EAX")
        pline_instance.set_YMC(temp_ymc)

    # Handle 2-arg arithmetic
    elif len(vars) == 3: # this means it is a 2-arg operation, var[0] = arg1, var[1] = operator, var[2] = arg2
        operator: str = vars[1]
        temp_counter: int
        # Process first 2 lines of ymc
        temp_ymc, temp_counter = cf.ymc_arithemtic_movs(vars, variables, False)
        counter += temp_counter # Increment program counter by number of bytes calculated in ymc_arithemtic_movs function

        # Parse operators and process third line of ymc
        temp_ymc += cf.ymc_operation_2args(operator, isSigned)
        counter += 2 # All 2 arg arithmetic operations are 2 bytes

        # Process fourth and final line of ymc
        temp_ymc += "movmr " + str(variables[assignment]) + ", eax\n" 
        counter += 4 # movmr is 4 bytes, so we increment the program_counter by 4

        # Set modified registers and ymc
        pline_instance.set_register("EAX")
        pline_instance.set_register("EBX")
        pline_instance.set_YMC(temp_ymc)

    # Handle 3-arg arithmetic
    elif len(vars) == 5: # this means it is 3-arg operation
        operators: list[str] = [vars[1], vars[3]]
        # Process first 3 lines of ymc
        temp_ymc, temp_counter = cf.ymc_arithemtic_movs(vars, variables, True)
        counter += temp_counter # Increment program counter by number of bytes calculated in ymc_arithemtic_movs function

        # Parse operators and process fourth line of ymc
        temp_ymc += cf.ymc_operation_3args(operators, isSigned)
        counter += 3 # All 3 arg arithmetic operations are 3 bytes

        # Process fifth and final line of ymc
        temp_ymc += "movmr " + str(variables[assignment]) + ", eax\n" 
        counter += 4 # movmr is 4 bytes, so we increment the program_counter by 4

        # Set modified registers and ymc
        pline_instance.set_register("EAX")
        pline_instance.set_register("EBX")
        pline_instance.set_register("ECX")
        pline_instance.set_YMC(temp_ymc)
    
    print("Arithmetic line processed") 
    return counter

def relational(pline_instance: PLine) -> int: # if/else and while statements, start by checking what each line is
    line_text: str = pline_instance.text  # grab text from line
    line_list: list[str] = line_text.split()   # split line into list.
    type: str = line_list[0]   
    counter = 0

    if type == "if" or type == "while":            # check if line is if/else statement or while loop                                                        
        first_operand: str = line_list[1]
        sign: str = line_list[2]
        limit = line_list[3]                                                              
        if str(first_operand) in variables:      # check if first operand is a variable
            pline_instance.append_YMC("movrm eax, " + str(variables[first_operand]))     # ADD YMC Instruction
            counter += 4            # ADD 4 bytes for movrm
        else:
            pline_instance.append_YMC("movrl eax, " + limit)     # ADD YMC Instruction
            counter += 3            # ADD 3 bytes for movrl

        if str(limit) in variables:      # check if second operand is a variable
            pline_instance.append_YMC("movrm ecx, " + str(variables[limit]))     # ADD YMC Instruction
            counter += 4            # ADD 4 bytes for movrm
        else:
            pline_instance.append_YMC("movrl ecx, " + limit)     # ADD YMC Instruction
            counter += 3            # ADD 3 bytes for movrl

        pline_instance.append_YMC("cmprr eax, ecx")
        counter += 2            # ADD 2 bytes for cmprr
        pline_instance.set_register("EAX")  # set registers EAX and ECX
        pline_instance.set_register("ECX")

        if sign == '==':
            pline_instance.add_YMC("jne")
        elif sign == '!=':                             
            pline_instance.add_YMC("je")
        elif sign == '<':                              
            pline_instance.add_YMC("jge")
        elif sign == '<=':                                     
            pline_instance.add_YMC("jg")
        elif sign == '>':                                   
            pline_instance.add_YMC("jle")
        elif sign == '>=':                                         
            pline_instance.add_YMC("jl")
        
        counter += 3 # ADD 3 bytes to counter for jump
    else:
        pline_instance.set_YMC("")

    print("Relational line processed") 
    return counter

####################################
# Print
# Brad K
####################################

def printD(pline_instance: PLine) -> int:          # print statements
    line_text: str = pline_instance.text  # grab text from line
    statement: list[str] = line_text.split()   # split line into list.
    arg: str = statement[1]              # set arg to second item in split_line list
    unsigned: list[str] = ["a","b","c"]         # declare signed and unsigned lists for if statements below
    signed: list[str] = ["x","y","z"]
    counter: int = 0


    if arg == "\\n":                # check if new line
        pline_instance.set_YMC("outnl\n") 
        counter += 1                 # Increase program counter by 1 (outnl [1 byte])
        return counter
    if arg in variables:            # Check if arg is in variables (It won't be if it's literal)
        arg_location: str = str(variables[arg])   # set location of arg to value in dictionary and convert to string
        if arg in unsigned:           # else if arg is an unsigned variable
            pline_instance.set_YMC("movrm eax, " + arg_location + "\n")   # set YMC instruction to first move arg_location to register eax, then outs eax 
            pline_instance.append_YMC("outu eax")
            counter += 6                 # Increase program counter by 4 bytes (movrm) + 2 bytes (outs)
        elif arg in signed:           # else if arg is a signed variable
            pline_instance.set_YMC("movrm eax, " + arg_location + "\n") # same as unsigned but with 'outu eax'
            pline_instance.append_YMC("outs eax")
            counter += 6       # Increase program counter by 4 bytes (movrm) + 2 bytes (outu)
    elif arg.startswith('-'):           # check if literal is negative
        pline_instance.set_YMC("movrl eax, " + arg + "\n")      # set YMC instruction to move literal arg to register eax
        pline_instance.append_YMC("outs eax")                   # append YMC instruction to outs eax
        counter += 5       # Increase program counter by 3 bytes (movrl) + 2 bytes (outu)
    else:                       # else it is positive
        pline_instance.set_YMC("movrl eax, " + arg + "\n")       # set YMC instruction to move literal arg to register eax
        pline_instance.append_YMC("outu eax")                   # append YMC instruction to outu eax
        counter += 5       # Increase program counter by 3 bytes (movrl) + 2 bytes (outu)

    # Set modified registers
    pline_instance.set_register("EAX")

    print("Print line processed") 
    return counter

def halt(pline_instance: PLine) -> int:
    pline_instance.set_YMC("hlt")
    return 1

def default_case(pline_instance: PLine) -> int:
    print("Default case processed. Something went very wrong")  
    return 0 

# Switch dictionary to call functions
switch_dict = {
    1: declaration,
    2: arithmetic,
    3: relational,
    4: printD,
    5: halt
}