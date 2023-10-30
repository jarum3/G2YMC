#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   HLC to YMC Compiler
#
#######################################################################

from PLine import PLine

program_counter = 0

            # EDX    ECX    EBX    EAX
registers =  [0, 0, 0, 0] # python is weird and won't let you define a boolean array with 0 and 1 so we have to use true and false here
        # ZF     SF     OF     CF
flags =  [False, False, False, False]     # maybe I'm wrong and one of you guys can figure out how to be able to use 0 and 1

# This is how chat GPT told me to make a list with a specified size. Not sure if there is a better way or not
size = 1000  # 1 kb is 1000 bytes
default_value = 0  # Define the default value.
# Memory array here. Not sure what type to make it
memory = [default_value] * size

### All of these have to be initialized before the switch_dict.get statement

# This stuff is for the switch statement
def declaration(): # start by checking if signed or unsigned
    print("This is case 1") # I left these print statments here to eliminate the error caused by having no code in the function
def arithmetic(): # start by checking if 2 arguments or 3 arguments
    print("This is case 2")
def relational(): # if/else and while statements, start by checking what each line is
    print("This is case 3")
def printD(): 
    print("This is case 4")
def default_case():
    print("This is the default case")    

switch_dict = {
    1: declaration,
    2: arithmetic,
    3: relational,
    4: printD
}

def main():
    # Open the file in read mode
    file_path = "path_to_your_file.txt"  # Replace with the actual path to txt file 
    try:
        with open(file_path, 'r') as file: # the r here means read only mode
            # Iterate over each line in the file
            for line in file: # Process each line here
                # Create a line object. The constructor for this class will check if it is an indented line and automatically set its parent line if so.
                # It will also set a flag telling us what category it belongs to (print, declaration, arithmetic operation, while or if)
                pline_instance = PLine(line) # the first parameter is the text of the line, the second is the type SEE SWITCH DICTIONARY
                
                if pline_instance.text.startswith('   '):  # Modify this condition based on the type of indentation you expect
                    # pline_instance.setParent([ITEM IN LINE ARRAY])
                    print("Line starts with indentation:")
                
                # this line will execute the corresponding function based on the line type
                switch_dict.get(pline_instance.type, default_case)()

    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()