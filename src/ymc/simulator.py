from __future__ import annotations
from contextlib import redirect_stdout
import io
import pickle
from instructions.Instruction import Instruction
import instructions.YMCCPU as cpu

## Takes in a file, loads it into memory
def loadFile(binaryFile: str):
  with open(binaryFile, "r") as file: # Grab passed file
      data = file.read() # Put file data into data variable
      byteString = [data[i:i+8] for i in range(0, len(data), 8)] # Split file into 1-byte chunks
      for i, chunk in enumerate(byteString): # Add every chunk into memory, starting at position 0
        cpu.memory[i] = chunk
      cpu.instructionPointer = 0 # Set instruction pointer properly

## Decodes an instruction, outputs the instruction and its arugments (if any)
def decode(instructions: dict[str, Instruction], instructionPointer: int) -> tuple[Instruction, list[str]]:
  instr = cpu.memory[instructionPointer] # Grab instruction from memory
  if instr == "00000000": # Default if EOF hit, we could make this an error but its more useful to just halt
    print("No halt at end of file, halting anyways!")
    exit() # Halt
  # Convert instruction binary into hex code, then map to instructions dictionary to find the right instruction
  instruction: Instruction = instructions[hex(int(instr, 2))[2:].zfill(2).upper()]
  args: list[str] = [] # Return an empty list if no arguments were found
  if instruction.argTypes: # We don't want to read arguments if there are none
    i = instructionPointer + 1 # Location of first argument
    for arg in instruction.argTypes: # Loop over each argument
      if (arg == "memory"): # Memory takes two bytes
        args.append((cpu.memory[i] + cpu.memory[i+1]))
        i += 2
      else: # Everything else is only one byte
        args.append(cpu.memory[i])
        i += 1
  return (instruction, args) # Return a tuple of the instruction and the list of arguments

## Execute an instruction's function with the arguments passed
def execute(instruction: Instruction, args: list[str]) -> str | None:
  cpu.instructionPointer += instruction.width # Increment instruction pointer BEFORE function, in case function is a jump
  with redirect_stdout(io.StringIO()) as output:
    if len(args) > 0: # If we have args, use them
      instruction.function(*args) # Args get unrolled into function arguments (Look up the spread operator for info on this)
    else:
      instruction.function() # Execute with no arguments
    if output.getvalue():
      return output.getvalue()

def main():
    # Should use files asm.pkl to convert from assembly code to binary
    # asm.pkl should contain object files for all instructions, with their assigned hex code and length being used to create binary data
    with open("instructions/instructionsByHex.pkl", "rb") as file:
        instructions: dict[str, Instruction] = pickle.load(file)
    loadFile("file.bin") # Load in the binary file
    while (True): # Loop until we find a halt
      (instruction, args) = decode(instructions, cpu.instructionPointer) # Decode instruction
      output = execute(instruction, args) # Execute instruction
      if output:
        print(output, end="")
if __name__ == "__main__":
  main()