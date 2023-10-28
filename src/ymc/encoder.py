# Should use files asm.pkl to convert from assembly code to binary
# asm.pkl should contain object files for all instructions, with their assigned hex code and length being used to create binary data
import pickle
from instructions.Instruction import Instruction
with open("instructions/asm.pkl", "rb") as file:
    instructions: list[Instruction] = pickle.load(file)