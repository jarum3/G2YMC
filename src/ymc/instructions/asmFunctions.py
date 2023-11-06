###############################
# Contains a ton of functions that correspond to instructions
# and a rough outline of their funcitionality
# so the simulator can eventually use these (once-polished) to execute code.
# Necessary for encoder to properly debug
###############################

import instructions.YMCCPU as cpu # Using CPU registers/flags/memory
import helpers.registerLookup as rl # Using register lookups
import helpers.binaryConversion as bc # Using binary conversions
from helpers.setFlags import setFlags # Setting flags in arithmetic instructions
import math # For rounding from division

## Special instructions

# print the signed representation of the CPU register pointed to by the register byte
def outputSigned(register: str) -> None:
    print(bc.signedBinaryToInt(cpu.registers[rl.fourBitToRegister(register)]))

# print the unsigned representation of the CPU register pointed to by the register byte
def outputUnsigned(register: str) -> None:
    print(bc.unsignedBinaryToInt(cpu.registers[rl.fourBitToRegister(register)]))


# print a newline, empty body accomplishes this
def outputNewline() -> None:
    print("")

## Mov instructions

# Grabs value from right register, puts it into left register
def movRegisterRegister(registers: str) -> None:
    args: list[str] = rl.eightBitToRegisters(registers)
    cpu.registers[args[0]] = cpu.registers[args[1]]


# Grabs value from memory at right address, puts it into left register
def movRegisterMemory(register: str, address: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr_int: int = bc.BinaryToAddr(address)
    cpu.registers[reg] = cpu.memory[addr_int]


# Grabs value from right literal, puts it into left register
def movRegisterLiteral(register: str, literal: str) -> None:
    reg = rl.fourBitToRegister(register)
    cpu.registers[reg] = literal[-8:]


# Grabs value from right register, puts it into memory at left address
def movMemoryRegister(address: str, register: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr_int = bc.BinaryToAddr(address)
    cpu.memory[addr_int] = cpu.registers[reg]


#####################################################
# Two-argument arithmetic:
# 1. Parse arguments through register or memory into ints (signed or unsigned for multiplication)
# 2. Perform arithmetic on both ints
# 3. Store result to left operand
# 4. Set flags, add argument True for adding, subCF flag true if a < b (Borrow)
#####################################################


def addRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    result = a + b
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    # Setting flags
    cpu.flags = setFlags(result, True)


def subRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    result = a - b
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    cpu.flags = setFlags(result, False, (a < b))


def uMultRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    result = a * b
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    cpu.flags = setFlags(result)


def sMultRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    result = a * b
    cpu.registers[regs[0]] = bc.signedIntToBinary(result)
    cpu.flags = setFlags(result)


def uDivRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    result = math.floor(a / b)
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    cpu.flags = setFlags(result)


def sDivRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    result = math.floor(a / b)
    cpu.registers[regs[0]] = bc.signedIntToBinary(result)
    cpu.flags = setFlags(result)


def addRegisterMemory(register: str, memory: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr = bc.BinaryToAddr(memory)
    a = bc.unsignedBinaryToInt(cpu.registers[reg])
    b = bc.unsignedBinaryToInt(cpu.memory[addr])
    result = a + b
    cpu.registers[reg] = bc.unsignedIntToBinary(result)
    cpu.flags = setFlags(result, True)


def subRegisterMemory(register: str, memory: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr = bc.BinaryToAddr(memory)
    a = bc.unsignedBinaryToInt(cpu.registers[reg])
    b = bc.unsignedBinaryToInt(cpu.memory[addr])
    result = a - b
    cpu.registers[reg] = bc.unsignedIntToBinary(result)
    cpu.flags = setFlags(result, False, (a < b))


def uMultRegisterMemory(register: str, memory: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr = bc.BinaryToAddr(memory)
    a = bc.unsignedBinaryToInt(cpu.registers[reg])
    b = bc.unsignedBinaryToInt(cpu.memory[addr])
    result = a * b
    cpu.registers[reg] = bc.unsignedIntToBinary(result)
    cpu.flags = setFlags(result)


def sMultRegisterMemory(register: str, memory: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr = bc.BinaryToAddr(memory)
    a = bc.signedBinaryToInt(cpu.registers[reg])
    b = bc.signedBinaryToInt(cpu.memory[addr])
    result = a * b
    cpu.registers[reg] = bc.signedIntToBinary(result)
    cpu.flags = setFlags(result)


def uDivRegisterMemory(register: str, memory: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr = bc.BinaryToAddr(memory)
    a = bc.unsignedBinaryToInt(cpu.registers[reg])
    b = bc.unsignedBinaryToInt(cpu.memory[addr])
    result = math.floor(a / b)
    cpu.registers[reg] = bc.unsignedIntToBinary(result)
    cpu.flags = setFlags(result)


def sDivRegisterMemory(register: str, memory: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr = bc.BinaryToAddr(memory)
    a = bc.signedBinaryToInt(cpu.registers[reg])
    b = bc.signedBinaryToInt(cpu.memory[addr])
    result = math.floor(a / b)
    cpu.registers[reg] = bc.signedIntToBinary(result)
    cpu.flags = setFlags(result)



## Compare instructions

# Compares are exactly the same as subtracts, but don't store their values.


def compareRegisterRegister(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    result = a - b
    cpu.flags = setFlags(result, False, (a < b))


def compareRegisterMemory(register: str, memory: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr = bc.BinaryToAddr(memory)
    a = bc.unsignedBinaryToInt(cpu.registers[reg])
    b = bc.unsignedBinaryToInt(cpu.memory[addr])
    result = a - b
    cpu.flags = setFlags(result, False, (a < b))


#####################################################
# Jumps
# All take one memory address, instruction pointer gets set here
# Only if the conditional is met. Conditional is verified using flags
#####################################################

# No check
def unconditionalJump(address: str) -> None:
    cpu.instructionPointer = bc.BinaryToAddr(address)

# Not SF and not ZF -> Greater
def jumpGreater(address: str) -> None:
    if cpu.flags["SF"] == False and cpu.flags["ZF"] == False:
        cpu.instructionPointer = bc.BinaryToAddr(address)

# Not SF -> Greater than or equal to
def jumpGreaterEqual(address: str) -> None:
    if cpu.flags["SF"] == False:
        cpu.instructionPointer = bc.BinaryToAddr(address)

# SF = less-than
def jumpLess(address: str) -> None:
    if cpu.flags["SF"]:
        cpu.instructionPointer = bc.BinaryToAddr(address)

# SF or ZF -> less-than or equal
def JumpLessEqual(address: str) -> None:
    if cpu.flags["SF"] or cpu.flags["ZF"]:
        cpu.instructionPointer = bc.BinaryToAddr(address)

# Not ZF -> not equal
def jumpNotEqual(address: str) -> None:
    if cpu.flags["ZF"] == False:
        cpu.instructionPointer = bc.BinaryToAddr(address)

# ZF -> Equal
def jumpEqual(address: str) -> None:
    if cpu.flags["ZF"]:
        cpu.instructionPointer = bc.BinaryToAddr(address)


#####################################################
# Three-argument arithmetic:
# 1. Parse arguments through registers (signed or unsigned for multiplication)
# 2. Perform arithmetic on all 3 ints
# 3. Store result to left operand
# 4. Set flags, add argument True for adding, subCF flag true if b < c for subtracting (Borrow)
#    Flags should be set as they would be for only the right operation (a * b + c sets flags for adding, not multiplication)
#####################################################

## All of these are almost identical except for:
# Signed vs. Unsigned (mul vs smul, div vs sdiv)
# Arithmetic operators (specific to instruction)
# Flags set for right operation, args should be (result, [True if addition, False if subtraction], [(b <c) if subtraction])

def addSubRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers) # Grab registers
    regs[2] = rl.fourBitToRegister(extraRegister) # Grab third register
    # Assign each register to a variable
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    c = bc.unsignedBinaryToInt(cpu.registers[regs[2]])
    result = a + b # Do the first arithmetic operation
    result -= c         # Do the second arithmetic operation (Preserves lack of order-of-operations)
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result) # Store the result
    setFlags(result, False, (b < c)) # Set the flags for the rightmost operation

# All of these are exactly the same save the exceptions marked above
def addMulRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    c = bc.unsignedBinaryToInt(cpu.registers[regs[2]])
    result = a + b
    result *= c
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    setFlags(result)


def addsMulRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    c = bc.signedBinaryToInt(cpu.registers[regs[2]])
    result = a + b
    result *= c
    cpu.registers[regs[0]] = bc.signedIntToBinary(result)
    setFlags(result)


def addDivRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    c = bc.unsignedBinaryToInt(cpu.registers[regs[2]])
    result = a + b
    result = math.floor(result / c)
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    setFlags(result)


def addsDivRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    c = bc.signedBinaryToInt(cpu.registers[regs[2]])
    result = a + b
    result = math.floor(result / c)
    cpu.registers[regs[0]] = bc.signedIntToBinary(result)
    setFlags(result)


def subAddRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    c = bc.unsignedBinaryToInt(cpu.registers[regs[2]])
    result = a - b
    result += c
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    setFlags(result, True)


def subMulRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    c = bc.unsignedBinaryToInt(cpu.registers[regs[2]])
    result = a - b
    result *= c
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    setFlags(result)


def subsMulRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    c = bc.signedBinaryToInt(cpu.registers[regs[2]])
    result = a - b
    result *= c
    cpu.registers[regs[0]] = bc.signedIntToBinary(result)
    setFlags(result)


def subDivRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    c = bc.unsignedBinaryToInt(cpu.registers[regs[2]])
    result = a - b
    result = math.floor(result / c)
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    setFlags(result)


def subsDivRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    c = bc.signedBinaryToInt(cpu.registers[regs[2]])
    result = a - b
    result = math.floor(result / c)
    cpu.registers[regs[0]] = bc.signedIntToBinary(result)
    setFlags(result)


def mulAddRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    c = bc.unsignedBinaryToInt(cpu.registers[regs[2]])
    result = a * b
    result += c
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    setFlags(result, True)


def mulSubRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    c = bc.unsignedBinaryToInt(cpu.registers[regs[2]])
    result = a * b
    result -= c
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    setFlags(result, False, (b < c))


def mulDivRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    c = bc.unsignedBinaryToInt(cpu.registers[regs[2]])
    result = a * b
    result = math.floor(result / c)
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    setFlags(result)


def smulAddRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    c = bc.signedBinaryToInt(cpu.registers[regs[2]])
    result = a * b
    result += c
    cpu.registers[regs[0]] = bc.signedIntToBinary(result)
    setFlags(result, True)


def smulSubRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    c = bc.signedBinaryToInt(cpu.registers[regs[2]])
    result = a * b
    result -= c
    cpu.registers[regs[0]] = bc.signedIntToBinary(result)
    setFlags(result, False, (b < c))


def smulsDivRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    c = bc.signedBinaryToInt(cpu.registers[regs[2]])
    result = a * b
    result = math.floor(result / c)
    cpu.registers[regs[0]] = bc.signedIntToBinary(result)
    setFlags(result)


def divAddRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    c = bc.unsignedBinaryToInt(cpu.registers[regs[2]])
    result = math.floor(a / b)
    result += c
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    setFlags(result, True)


def divSubRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    c = bc.unsignedBinaryToInt(cpu.registers[regs[2]])
    result = math.floor(a / b)
    result -= c
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    setFlags(result, False, (b < c))


def divMulRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    c = bc.unsignedBinaryToInt(cpu.registers[regs[2]])
    result = math.floor(a / b)
    result *= c
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    setFlags(result)


def sdivAddRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    c = bc.signedBinaryToInt(cpu.registers[regs[2]])
    result = math.floor(a / b)
    result += c
    cpu.registers[regs[0]] = bc.signedIntToBinary(result)
    setFlags(result, True)


def sdivSubRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    c = bc.signedBinaryToInt(cpu.registers[regs[2]])
    result = math.floor(a / b)
    result -= c
    cpu.registers[regs[0]] = bc.signedIntToBinary(result)
    setFlags(result, False, (b < c))


def sdivsMulRegisters(registers: str, extraRegister: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    regs.append(rl.fourBitToRegister(extraRegister))
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    c = bc.signedBinaryToInt(cpu.registers[regs[2]])
    result = math.floor(a / b)
    result *= c
    cpu.registers[regs[0]] = bc.signedIntToBinary(result)
    setFlags(result)

## End of instructions