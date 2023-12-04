#######################################################################
#   CSC 365 Project Group 2
#   Jacob Duncan, Jakob Robinson, Terry Townsend, Brad Kivett
#
#   Final main file
#
#######################################################################
from ast import arg
from instructions.Instruction import Instruction
import helpers.registerLookup as rg
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
    pline_list: list[PLine] = cm.main("code.hlc")
    # Save both instruction dictionaries, one for the simulation, and one for encoding
    with open("instructions/instructionsByHex.pkl", "rb") as file:
        instructions: dict[str, Instruction] = pickle.load(file)
    with open("instructions/instructionsByName.pkl", "rb") as file:
        instructionsByName: dict[str, Instruction] = pickle.load(file)
    # Get range of addresses for each HLC line, to assign HLC lines to YMC lines
    ranges: list[tuple[int, int]] = []
    for i, line in enumerate(pline_list):
        minimum: int = line.address
        maximum: int = 1024
        if len(pline_list) > i + 1:
            maximum = pline_list[i + 1].address - 1
        ranges.append((minimum, maximum))
    en.main()  # Encode file.ymc to file.bin
    sm.loadFile("binary.bin")  # Load in the binary file
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
        while not sm.cpu.stopping: # Keep going until a halt is found
            address: int = sm.cpu.instructionPointer # Current address for instruction to read
            line = PLine("")
            lineText: str = ""
            # Find HLC Line with an address range matching our current address
            for i, potentialRange in enumerate(ranges):
                if address >= potentialRange[0] and address <= potentialRange[1]:
                    # Save matching HLC line, and its text formatted for the CSV
                    line = pline_list[i]
                    lineText = line.text.replace("\n", "").replace("  ", "")
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
            ymc: str = ""
            # Match current chunk of code to YMC lines (Preserves negatives, etc)
            
            # If we have literals of, for example, -1 and 255 in the same chunk, this will actually always assign to the latter one
            # However, they're equivalent binary! So they might as well be the same line of code
            # For example, 255 + 255 = 254 once you truncate to 8 bits
            # And obviously 255 + -1 is also 254.
            for ymcLine in line.YMC_string.splitlines():
                if en.getBinaryFromLine(ymcLine, instructionsByName) == ymcBinary:
                    ymc = ymcLine
            # If we didn't find a matching line, try to parse as 
            if not ymc:
                ymc = instruction.instruction
                if instruction.argTypes:
                    i = 0
                    for i, argType in enumerate(instruction.argTypes):
                        ymc += " "
                        match argType:
                            case "literal":
                                ymc += str(bc.unsignedBinaryToInt(args[i]))
                            case "register-register":
                                regs: list[str] = rg.eightBitToRegisters(args[i])
                                ymc += regs[0] + ", " + regs[1]
                            case "register":
                                ymc += rg.fourBitToRegister(args[i])
                            case "memory":
                                ymc += str(bc.BinaryToAddr(args[i]))
                            case _:
                                print(args[i])
                                ymc += "ERROR"
                        if len(args) > i - 1:
                            ymc += ","
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
            writer.writerow(
                [lineText, address, ymc, ymcHex, output, changedRegsStr, changedFlagsStr]
            )


if __name__ == "__main__":
    main()
