#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   Final main file
#
#######################################################################
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
    # Compile file.hlc, and save its list to a variable
    pline_list = cm.main("file.hlc")
    # Save both instruction dictionaries, one for the simulation, and one for encoding
    with open("instructions/instructionsByHex.pkl", "rb") as file:
        instructions: dict[str, Instruction] = pickle.load(file)
    with open("instructions/instructionsByName.pkl", "rb") as file:
        instructionsByName: dict[str, Instruction] = pickle.load(file)
    # Get range of addresses for each HLC line, to assign HLC lines to YMC lines
    ranges: list[tuple[int, int]] = []
    for i, line in enumerate(pline_list):
        minimum = line.address
        maximum = 1024
        if len(pline_list) > i + 1:
            maximum = pline_list[i + 1].address - 1
        ranges.append((minimum, maximum))
    en.main()  # Encode file.ymc to file.bin
    sm.loadFile("file.bin")  # Load in the binary file
    with open("output.csv", "w", newline="") as file:  # Open CSV to write to
        writer = csv.writer(file)  # Create CSV writer object
        # Headers for CSV
        fields = [
            "HLC Instruction",
            "YMC Address",
            "YMC Assembly",
            "YMC Encoding",
            "Output",
            "Modified Registers",
            "Modified Flags",
        ]
        writer.writerow(fields) # Writing headers
        while True: # Keep going until a halt is found
            address = sm.cpu.instructionPointer # Current address for instruction to read
            line = PLine("")
            lineText = ""
            # Find HLC Line with an address range matching our current address
            for i, potentialRange in enumerate(ranges):
                if address >= potentialRange[0] and address <= potentialRange[1]:
                    # Save matching HLC line, and its text formatted for the CSV
                    line = pline_list[i]
                    lineText = line.text.replace("\n", "").replace("  ", "")
            # Save starting flags and registers
            startFlags = sm.cpu.flags
            # We need to save strings as copies, since they'll be references otherwise
            # And those won't let us compare
            startRegs: dict[str, str] = {}
            for key in sm.cpu.registers:
              startRegs[key] = sm.cpu.registers[key]
            # Decode instruction into instr and arguments
            (instruction, args) = sm.decode(instructions, sm.cpu.instructionPointer)
            # Generate binary for current chunk of code
            instrBinary = bc.hexToBinary(instruction.hexCode)
            ymcBinary = instrBinary + "".join(args)
            ymcHex = instruction.hexCode
            ymc: str = ""
            # Match current chunk of code to YMC lines (Preserves negatives, etc)
            for ymcLine in line.YMC_string.splitlines():
                if en.getBinaryFromLine(ymcLine, instructionsByName) == ymcBinary:
                    ymc = ymcLine
            if args:
              # Convert binary to hex, fill it to multiple of 2, and make it uppercase
                ymcHex += (
                    hex(int(ymcBinary, 2))
                    .zfill(math.floor(len(ymcBinary) / 4))[2:]
                    .upper()
                )
            # Grab output, execute instruction
            output = sm.execute(instruction, args)  # Execute instruction
            output = output.replace("\n", "\\n") # Format output
            # Save ending state of flags/registers
            endFlags = sm.cpu.flags
            endRegs = sm.cpu.registers
            # Generate difference of flags/registers
            changedFlags: dict[str, bool] = {}
            changedRegs: dict[str, str] = {}
            # Loop through each flag and register to see if they changed, if they did, add them to the list
            for key in endFlags:
                if startFlags[key] != endFlags[key]:
                    changedFlags[key] = endFlags[key]
            for key in endRegs:
                if startRegs[key] != endRegs[key]:
                    changedRegs[key] = hex(int(endRegs[key], 2))[2:].zfill(2).upper()
            # Convert flags and registers into strings to be used in CSV
            changedFlagsStr = ""
            changedRegsStr = ""
            if changedFlags:
                changedFlagsStr = str(changedFlags)
            if changedRegs:
                changedRegsStr = str(changedRegs)
            # Write content to row of CSV
            writer.writerow(
                [lineText, address, ymc, ymcHex, output, changedRegsStr, changedFlagsStr]
            )


if __name__ == "__main__":
    main()
