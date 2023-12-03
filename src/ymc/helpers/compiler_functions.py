# Just some functions that I made to clean up the compiler and compiler_extension programs
# Jacob Duncan

from __future__ import annotations
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
def set_parent(pline_instance: PLine, pline_list: list[PLine], i: int):
    prev_line: PLine = pline_list[i - 1]
    if not prev_line.isParent:
        pline_instance.add_parent(prev_line.parent)
        return
    pline_instance.add_parent(prev_line)

def ymc_arithemtic_movs(vars: list[str], variables: dict[str, int], is3args: bool):
    mov_lines: str
    counter: int = 0
    # Process first line of ymc
    if any(char.isdigit() for char in vars[0]): # literal
        mov_lines = "movrl eax, " + vars[0] + "\n"
        counter += 3 # movrl is 3 bytes, so we increment the program_counter by 3
    else: # variable
        mov_lines = "movrm eax, " + str(variables[vars[0]]) + "\n"
        counter += 4 # movrm is 4 bytes, so we increment the program_counter by 4
    # Process second line of ymc
    if any(char.isdigit() for char in vars[2]): # literal
        mov_lines += "movrl ebx, " + vars[2] + "\n"
        counter += 3 # movrl is 3 bytes, so we increment the program_counter by 3
    else: # variable
        mov_lines += "movrm ebx, " + str(variables[vars[2]]) + "\n"
        counter += 4 # movrm is 4 bytes, so we increment the program_counter by 4

    # Process third line of ymc if necessary
    if is3args == True:
        if any(char.isdigit() for char in vars[4]): # literal
            mov_lines += "movrl ecx, " + vars[4] + "\n"
            counter += 3 # movrl is 3 bytes, so we increment the program_counter by 3
        else: # variable
            mov_lines += "movrm ecx, " + str(variables[vars[4]]) + "\n"
            counter += 4 # movrm is 4 bytes, so we increment the program_counter by 4
    
    return mov_lines, counter

def ymc_operation_2args(operator: str, isSigned: bool) -> str:
    operation_line: str = ""
    # Parse operators and process third line of ymc
    if operator == "+":
        operation_line = "add eax, ebx\n"
    elif operator == "-":
        operation_line = "sub eax, ebx\n"
    elif operator == "*":
        if isSigned == True:
            operation_line = "smul eax, ebx\n"
        else:
            operation_line = "mul eax, ebx\n"
    elif operator == "/":
        if isSigned == True:
            operation_line = "sdiv eax, ebx\n"
        else:
            operation_line = "div eax, ebx\n"
    
    return operation_line

def ymc_operation_3args(operators: list[str], isSigned: bool) -> str:
    operation_line: str = ""
    # Handle first operation.
    if operators[0] == "+":
        operation_line = "add"
    elif operators[0] == "-":
        operation_line = "sub"
    elif operators[0] == "*":
        if isSigned == True:
            operation_line = "smul"
        else:
            operation_line = "mul"
    elif operators[0] == "/":
        if isSigned == True:
            operation_line = "sdiv"
        else:
            operation_line = "div"
    # Handle second operation. Result of first op is stored in destination variable, so the operation is done on the variable and the third argument
    if operators[1] == "+":
        operation_line += "add"
    elif operators[1] == "-":
        operation_line += "sub"
    elif operators[1] == "*":
        if isSigned == True:
            operation_line += "smul"
        else:
            operation_line += "mul"
    elif operators[1] == "/":
        if isSigned == True:
            operation_line += "sdiv"
        else:
            operation_line += "div"
    if operation_line:
        operation_line += " eax, ebx, ecx\n"

    return operation_line

def create_hlt(hlc_text:str, address: int, YMC_Str: str):
    pline_hlt = PLine(hlc_text)         # text = "[End of Code]"
    pline_hlt.set_YMC(YMC_Str)          # set YMC_String to "hlt"
    pline_hlt.set_address(address)  # set address in PLine instance to final ce.program_counter value
    return pline_hlt

def add_jumps(file_text: list[str], i: int, pline_list: list[PLine]) -> list[PLine]:
    pi: int = 0 # Used to save index of parent for the incoming if statement
    lc_if = 0 # Save index of last child in if statement for when we add

    for p in pline_list: # For PLine in pline_list
        ci: int = 0     # store index of previous child (relevant to parent)
        if p.text.startswith("while"):  # check if pline is a While loop
            #t: PLine = p.last_child
            for tp in pline_list[pi + 1:]: # tp = trailing pLine from p_index onward
                if hasattr(tp, 'parent') == False: # Find first pline where its not a child
                    lc_index: int = (pi + ci) # set last child index to pi index + child index (relative to parent)
                    pline_list[pi].add_jump_loc(str(pline_list[lc_index + 1].address)) # add location outside of loop to the jmp instruction
                    pline_list[lc_index].append_YMC("jmp " + str(pline_list[pi].address))  # add jmp instruction to end of last child back to parent address
                    break           # break loop if reaching end
                ci += 1 # increase child index by 1
        elif p.text.startswith("if"):  # check if pline is an if
            for tp in pline_list[pi + 1:]:
                if hasattr(tp, 'parent') == False: # Find first pline where its not a child
                    lc_index: int = (pi + ci) # set last child index to pi index + child index (relative to parent)
                    pline_list[pi].add_jump_loc(str(pline_list[lc_index + 1].address)) # add location outside of loop to the jmp instruction
                    lc_if = lc_index
                    break           # break loop if reaching end
                ci += 1 # increase child index by 1
        elif p.text.startswith("else"):  # check if pline is an else
             for tp in pline_list[pi + 1:]:
                if hasattr(tp, 'parent') == False: # Find first pline where its not a child
                    lc_index: int = (pi + ci) # set last child index to pi index + child index (relative to parent)
                    pline_list[lc_if].append_YMC("jmp " + str(pline_list[lc_index + 1].address))  # add jmp instruction to end of last child of if statement with the address as the first instruction after else's children
                    break           # break loop if reaching end
                ci += 1 # increase child index by 1
        pi += 1    # increase parent index by one 
    return pline_list 

def print_pline_list(pline_list: list[PLine]):
    for p in pline_list:
        print (p.text)
        print (str(p.address)) 
        print (p.YMC_string)
        print ("")

def set_last_child(parent: PLine, pline_instance: PLine):
    parent.last_child = pline_instance