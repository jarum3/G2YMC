#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   Final main file
#
#######################################################################
from programLine import programLine
from instructions.Instruction import Instruction
import helpers.registerLookup as rg
import helpers.binaryConversion as bc
import compiler as cm
import simulator as sm
import encoder as en
import csv
import pickle
import math

def main():
    # Compile file.hlc, and save its list to a variable
    (hlcDict, ymcDict) = cm.main("file.hlc", "file.ymc", False)
    # Save both instruction dictionaries, one for the simulation, and one for encoding
    with open("instructions/instructionsByHex.pkl", "rb") as file:
        instructions: dict[str, Instruction] = pickle.load(file)
    with open("instructions/instructionsByName.pkl", "rb") as file:
        instructionsByName: dict[str, Instruction] = pickle.load(file)
    # Get range of addresses for each HLC line, to assign HLC lines to YMC lines
    en.main()  # Encode file.ymc to file.bin
    sm.loadFile("file.bin")  # Load in the binary file
    with open("output.csv", "w", newline="") as file:  # Open CSV to write to
        writer = csv.writer(file)  # Create CSV writer object
        # Headers for CSV
        fields: list[str] = [
            "HLC Instruction",
            "YMC Address",
            "YMC Assembly",
            "YMC Encoding",
            "Output",
            "Modified Registers",
            "Modified Flags",
        ]
        writer.writerow(fields) # Writing headers
        while not sm.cpu.exiting: # Keep going until a halt is found
            address: int = sm.cpu.instructionPointer # Current address for instruction to read
            # Find HLC Line with an address range matching our current address
            line = hlcDict[address]
            if line:
                lineText = line.replace("\n", "").replace("  ", "")
            else:
                lineText = "compiler"
            # Save starting flags and registers
            startFlags: dict[str, bool] = sm.cpu.flags
            # We need to save strings as copies, since they'll be references otherwise
            # And those won't let us compare
            startRegs: dict[str, str] = {}
            for key in sm.cpu.registers:
                startRegs[key] = sm.cpu.registers[key]
            # Decode instruction into instr and arguments
            (instruction, args) = sm.decode(instructions, sm.cpu.instructionPointer)
            # Generate binary for current chunk of code
            instrBinary: str = bc.hexToBinary(instruction.hexCode)
            ymcBinary: str = instrBinary + "".join(args)
            ymcHex: str = instruction.hexCode
            print(address)
            ymc: str = ymcDict[address]
            print(ymc)
            # Match current chunk of code to YMC lines (Preserves negatives, etc)
            
            # If we have literals of, for example, -1 and 255 in the same chunk, this will actually always assign to the latter one
            # However, they're equivalent binary! So they might as well be the same line of code
            # For example, 255 + 255 = 254 once you truncate to 8 bits
            # And obviously 255 + -1 is also 254.
            if args:
                # Convert binary to hex, fill it to multiple of 2, and make it uppercase
                ymcHex += (
                    hex(int(ymcBinary, 2))
                    .zfill(math.floor(len(ymcBinary) / 4))[2:]
                    .upper()
                )
            # Grab output, execute instruction
            output: str = sm.execute(instruction, args)  # Execute instruction
            output = output.replace("\n", "\\n") # Format output
            # Save ending state of flags/registers
            endFlags: dict[str, bool] = sm.cpu.flags
            endRegs: dict[str, str] = sm.cpu.registers
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
            changedFlagsStr: str = ""
            changedRegsStr: str = ""
            if changedFlags:
                changedFlagsStr = str(changedFlags)
            if changedRegs:
                changedRegsStr = str(changedRegs)
            # Write content to row of CSV
            print([lineText, address, ymc, ymcHex, output, changedRegsStr, changedFlagsStr])
            writer.writerow(
                [lineText, address, ymc, ymcHex, output, changedRegsStr, changedFlagsStr]
            )


if __name__ == "__main__":
    main()
