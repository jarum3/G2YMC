#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   Final main file
#
#######################################################################
import enum
from hmac import new
from instructions.Instruction import Instruction
import helpers.binaryConversion as bc
from PLine import PLine
import compiler as cm
import simulator as sm
import encoder as en
import csv
import pickle
import math

def main():
  pline_list = cm.main("file.hlc")
  with open("instructions/instructionsByHex.pkl", "rb") as file:
      instructions: dict[str, Instruction] = pickle.load(file)
  with open("instructions/instructionsByName.pkl", "rb") as file:
    instructionsByName: dict[str, Instruction] = pickle.load(file)
  ranges: list[tuple[int, int]] = []
  for i, line in enumerate(pline_list):
    minimum = line.address
    maximum = 1024
    if (len(pline_list) > i + 1):
      maximum = pline_list[i+1].address - 1
    ranges.append((minimum, maximum))
  en.main()
  sm.loadFile("file.bin") # Load in the binary file
  with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    fields = ["HLC Instruction", "YMC Address", "YMC Assembly", "YMC Encoding", "Modified Registers", "Modified Flags"]
    writer.writerow(fields)
    while True:
      address = sm.cpu.instructionPointer
      line = PLine("")
      lineText = ""
      for i, potentialRange in enumerate(ranges):
        if address > potentialRange[0] and address < potentialRange[1]:
          line = pline_list[i]
          lineText = line.text.replace("\n", "").replace("  ", "")
      startFlags = sm.cpu.flags
      startRegs = sm.cpu.registers
      startAddr = sm.cpu.instructionPointer
      (instruction, args) = sm.decode(instructions, sm.cpu.instructionPointer) # Decode instruction
      instrBinary = bc.hexToBinary(instruction.hexCode)
      ymcBinary = instrBinary + "".join(args)
      ymc: str = ""
      for ymcLine in line.YMC_string.splitlines():
        if en.getBinaryFromLine(ymcLine, instructionsByName) == ymcBinary:
          ymc = ymcLine
      ymcHex = instruction.hexCode
      if (args):
        ymcHex += hex(int(ymcBinary, 2)).zfill(math.floor(len(ymcBinary) / 4))[2:].upper()
      output = sm.execute(instruction, args) # Execute instruction
      endFlags = sm.cpu.flags
      endRegs = sm.cpu.registers
      changedFlags: dict[str, bool] = {}
      changedRegs: dict[str, str] = {}
      # Loop through each flag and register to see if they changed, if they did, add them to the list
      for key in endFlags:
        if startFlags[key] != endFlags[key]:
          changedFlags[key] = endFlags[key]
      for key in endRegs:
        if startRegs[key] != endRegs[key]:
          changedRegs[key] = hex(int(endRegs[key], 2))[2:].zfill(2).upper()
      changedFlagsStr = " "
      changedRegsStr = " "
      if changedFlags:
        changedFlagsStr = str(changedFlags)
      if changedRegs:
        changedRegsStr = str(changedRegs)
      writer.writerow([lineText, startAddr, ymc, ymcHex, changedRegsStr, changedFlagsStr])
if __name__ == "__main__":
  main()