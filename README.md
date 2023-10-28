# G2YMC

## HLC Compiler

Loop through each line.
Parse line into line object with category, switch statement based on category.
If line is tabbed, make the respective while / if line a parent of the line.
When tabs end, process addresses for the parent of the most recent tabbed line.
Store each line of assembly as [instr] [arg1], [arg2], [arg3] with commas, one instruction per line in the output file.
In the categories, parse assignment into a variable map. Parse arithmetic into arithmetic instructions (Similar to the flowchart). Parse print into out statement, etc.

## YMC Encoder
Go line-by-line of the asm file, parse instruction and arguments into binary. Total bytes should be equivalent to instruction width property.

## YMC Simulator
Go byte-by-byte, parse instruction, grab total width, grab next x bytes as arguments, parse each argument for their respective length, then pass to instruction’s function.

## HLC Line Class
Has line text, category, optional parent, optional children list, then has assembly string (with newlines, spaces, commas, etc).

## YMC Instruction Class
Has instruction name, hex code, total width, type of each argument (should be an array of strings). Should also contain one Callable function, which contains the code to execute for a given instruction. For example:

(NOT fully accurate, just for demonstration currently)
Name: addrr
Code: 0x91
Width: 2
argTypes = ["register-register"]
Def execute(arg1):
  registerTranslate(arg1.higher_4).value +=  registerTranslate(arg2.higher_4).value
  setFlags(arg1)
