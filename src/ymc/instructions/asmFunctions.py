import YMCCPU as cpu
import helpers.registerLookup as rl
import helpers.binaryConversion as bc
from helpers.setFlags import setFlags
import math


def outputSigned(register: str) -> None:
    # print the signed representation of the CPU register pointed to by the register byte
    print(bc.signedBinaryToInt(cpu.registers[rl.fourBitToRegister(register)]))


def outputUnsigned(register: str) -> None:
    # print the unsigned representation of the CPU register pointed to by the register byte
    print(bc.unsignedBinaryToInt(
        cpu.registers[rl.fourBitToRegister(register)]))


# print a newline
def outputNewline() -> None:
    print("\n")


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
    cpu.registers[0] = bc.unsignedIntToBinary(result)
    # Setting flags
    cpu.flags = setFlags(result, True)


def subRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    result = a - b
    cpu.registers[0] = bc.unsignedIntToBinary(result)
    cpu.flags = setFlags(result, False, (a < b))


def uMultRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    result = a * b
    cpu.registers[0] = bc.unsignedIntToBinary(result)
    cpu.flags = setFlags(result)


def sMultRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    result = a * b
    cpu.registers[0] = bc.signedIntToBinary(result)
    cpu.flags = setFlags(result)


def uDivRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    result = math.floor(a / b)
    cpu.registers[0] = bc.unsignedIntToBinary(result)
    cpu.flags = setFlags(result)


def sDivRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    a = bc.signedBinaryToInt(cpu.registers[regs[0]])
    b = bc.signedBinaryToInt(cpu.registers[regs[1]])
    result = math.floor(a / b)
    cpu.registers[0] = bc.signedIntToBinary(result)
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


#####################################################
# Three-argument arithmetic:
# 1. Parse arguments through registers (signed or unsigned for multiplication)
# 2. Perform arithmetic on all 3 ints
# 3. Store result to left operand
# 4. Set flags, add argument True for adding, subCF flag true if a < b (Borrow)
#    Flags should be set as they would be for only the right operation (a * b + c sets flags for adding, not multiplication)
#####################################################


def addsubRegisters(registers: str, extraRegister: str) -> None:
    regs: str = rl.eightBitToRegisters(registers)
    regs[2] = rl.fourBitToRegister(extraRegister)
    a = bc.unsignedBinaryToInt(cpu.registers[regs[0]])
    b = bc.unsignedBinaryToInt(cpu.registers[regs[1]])
    c = bc.unsignedBinaryToInt(cpu.registers[regs[2]])
    result = a + b - c
    cpu.registers[regs[0]] = bc.unsignedIntToBinary(result)
    setFlags(result, False, (b < c))