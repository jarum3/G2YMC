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
def set_parent(pline_instance: PLine, pline_list: list[PLine], i: int):
    prev_line: PLine = pline_list[i - 1]
    if not prev_line.isParent:
        pline_instance.add_parent(prev_line.parent)
        return
    pline_instance.add_parent(prev_line)

def set2args(vars: list[str], variables: dict[str, int]) -> list[int]:
    args = [0, 0]
    if any(char.isdigit() for char in vars[0]): # processing first argument
            args[0] = int(vars[0])
    else:
        args[0] = variables[vars[0]]
    if any(char.isdigit() for char in vars[2]): # processing second argument
        args[1] = int(vars[2])
    else:
        args[1] = variables[vars[2]]
    return args

def set3args(vars: list[str], variables: dict[str, int]) -> list[int]:
    args = [0, 0, 0]
    if any(char.isdigit() for char in vars[0]): # processing first argument
            args[0] = int(vars[0])
    else:
        args[0] = variables[vars[0]]
    if any(char.isdigit() for char in vars[2]): # processing second argument
        args[1] = int(vars[2])
    else:
        args[1] = variables[vars[2]]
    if any(char.isdigit() for char in vars[4]): # processing third argument
        args[2] = int(vars[4])
    else:
        args[2] = variables[vars[4]]
    return args

def ymc_arithemtic_movs(vars: list[str], variables: dict[str, int], is3args: bool):
    mov_lines: str
    counter: int = 0
    address: list[str] = [str(variables[vars[0]]), str(variables[vars[2]])] # This is one of the ugliest things I have ever seen.
    # Process first line of ymc
    if any(char.isdigit() for char in vars[0]): # literal
        mov_lines = "movrl eax, " + vars[0] + "\n"
        counter += 3 # movrl is 3 bytes, so we increment the program_counter by 3
    else: # variable
        mov_lines = "movrm eax, " + address[0] + "\n"
        counter += 4 # movrm is 4 bytes, so we increment the program_counter by 4
    # Process second line of ymc
    if any(char.isdigit() for char in vars[2]): # literal
        mov_lines += "movrl ebx, " + vars[2] + "\n"
        counter += 3 # movrl is 3 bytes, so we increment the program_counter by 3
    else: # variable
        mov_lines += "movrm ebx, " + address[1] + "\n"
        counter += 4 # movrm is 4 bytes, so we increment the program_counter by 4

    # CProcess third line of ymc if necessary
    if is3args == True:
        address.append(str(variables[vars[4]]))
        if any(char.isdigit() for char in vars[4]): # literal
            mov_lines += "movrl ecx, " + vars[4] + "\n"
            counter += 3 # movrl is 3 bytes, so we increment the program_counter by 3
        else: # variable
            mov_lines += "movrm ecx, " + address[2] + "\n"
            counter += 4 # movrm is 4 bytes, so we increment the program_counter by 4
    
    return mov_lines, counter

def ymc_operation_2args(operator: str, isSigned: bool) -> str:
    operation_line: str
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
    operation_line: str
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
        operation_line += "add eax, ebx, ecx\n"
    elif operators[1] == "-":
        operation_line += "sub eax, ebx, ecx\n"
    elif operators[1] == "*":
        if isSigned == True:
            operation_line += "smul eax, ebx, ecx\n"
        else:
            operation_line += "mul eax, ebx, ecx\n"
    elif operators[1] == "/":
        if isSigned == True:
            operation_line += "sdiv eax, ebx, ecx\n"
        else:
            operation_line += "div eax, ebx, ecx\n"

    return operation_line