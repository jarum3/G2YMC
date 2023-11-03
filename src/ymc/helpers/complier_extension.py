# Just some functions that I made to clean up the compiler program
# Jacob Duncan

from PLine import PLine

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
def set_parent(pline_instance, pline_list, iter):
    if pline_instance.text.startswith('   '):  
        for j in range(iter - 1, -1, -1):
            if not pline_list[j].text.startswith('  '):
                pline_instance.add_parent(pline_list[j])

# This stuff is for the switch statement
def declaration(pline_instance): # start by checking if signed or unsigned
    print("This is case 1") # I left these print statments here to eliminate the error caused by having no code in the function
def arithmetic(pline_instance): # start by checking if 2 arguments or 3 arguments
    print("This is case 2")
def relational(pline_instance): # if/else and while statements, start by checking what each line is
    print("This is case 3")
def printD(pline_instance): 
    print("This is case 4")
def default_case(pline_instance):
    print("This is the default case. Something went very wrong")    

switch_dict = {
    1: declaration,
    2: arithmetic,
    3: relational,
    4: printD
}