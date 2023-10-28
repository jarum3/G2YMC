import YMCCPU as cpu
import helpers.registerLookup as rl
import helpers.binaryConversion as bc
import math


def outputSigned(register: str) -> None:
    # print the signed representation of the CPU register pointed to by the register byte
    print(bc.signedBinaryToInt(cpu.registers[rl.fourBitToRegister(register)]))


def outputUnsigned(register: str) -> None:
    # print the unsigned representation of the CPU register pointed to by the register byte
    print(bc.unsignedBinaryToInt(
        cpu.registers[rl.fourBitToRegister(register)]))


def outputNewline() -> None:
    print("\n")


def movRegisterRegister(registers: str) -> None:
    args: list[str] = rl.eightBitToRegisters(registers)
    cpu.registers[args[0]] = cpu.registers[args[1]]


def movRegisterMemory(register: str, address: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr_int: int = bc.BinaryToAddr(address)
    cpu.registers[reg] = cpu.memory[addr_int]


def movRegisterLiteral(register: str, literal: str) -> None:
    reg = rl.fourBitToRegister(register)
    cpu.registers[reg] = literal[-8:]


def movMemoryRegister(address: str, register: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr_int = bc.BinaryToAddr(address)
    cpu.memory[addr_int] = cpu.registers[reg]


def addRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    result = int(bc.unsignedBinaryToInt(cpu.registers[0])) + int(
        bc.unsignedBinaryToInt(cpu.registers[1]))
    cpu.registers[0] = bc.unsignedIntToBinary(result)
    if (result == 0): cpu.flags["ZF"] = True
    if (bc.unsignedIntToBinary(result)[0] == "1"): cpu.flags["SF"] = True
    if (result > 127 or result < -128): cpu.flags["OF"] = True
    if (result > 255): cpu.flags["CF"] = True


def subRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    result = int(bc.unsignedBinaryToInt(cpu.registers[0])) - int(
        bc.unsignedBinaryToInt(cpu.registers[1]))
    cpu.registers[0] = bc.unsignedIntToBinary(result)
    if (result == 0): cpu.flags["ZF"] = True
    if (bc.unsignedIntToBinary(result)[0] == "1"): cpu.flags["SF"] = True
    if (result > 127 or result < -128): cpu.flags["OF"] = True
    if (result < 0): cpu.flags["CF"] = True


def uMultRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    result = int(bc.unsignedBinaryToInt(cpu.registers[0])) * int(
        bc.unsignedBinaryToInt(cpu.registers[1]))
    cpu.registers[0] = bc.unsignedIntToBinary(result)
    if (result == 0): cpu.flags["ZF"] = True
    if (bc.unsignedIntToBinary(result)[0] == "1"): cpu.flags["SF"] = True
    if (result > 127 or result < -128): cpu.flags["OF"] = True


def sMultRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    result = int(bc.signedBinaryToInt(cpu.registers[0])) * int(
        bc.signedBinaryToInt(cpu.registers[1]))
    cpu.registers[0] = bc.signedIntToBinary(result)
    if (result == 0): cpu.flags["ZF"] = True
    if (bc.unsignedIntToBinary(result)[0] == "1"): cpu.flags["SF"] = True
    if (result > 127 or result < -128): cpu.flags["OF"] = True


def uDivRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    result = math.floor(
        int(bc.unsignedBinaryToInt(cpu.registers[0])) /
        int(bc.unsignedBinaryToInt(cpu.registers[1])))
    cpu.registers[0] = bc.unsignedIntToBinary(result)
    if (result == 0): cpu.flags["ZF"] = True
    if (bc.unsignedIntToBinary(result)[0] == "1"): cpu.flags["SF"] = True
    if (result > 127 or result < -128): cpu.flags["OF"] = True


def sDivRegisters(registers: str) -> None:
    regs: list[str] = rl.eightBitToRegisters(registers)
    result = math.floor(
        int(bc.signedBinaryToInt(cpu.registers[0])) /
        int(bc.signedBinaryToInt(cpu.registers[1])))
    cpu.registers[0] = bc.signedIntToBinary(result)
    if (result == 0): cpu.flags["ZF"] = True
    if (bc.unsignedIntToBinary(result)[0] == "1"): cpu.flags["SF"] = True
    if (result > 127 or result < -128): cpu.flags["OF"] = True


def addRegisterMemory(register: str, memory: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr = bc.BinaryToAddr(memory)
    result = int(
        bc.unsignedBinaryToInt(cpu.registers[reg]) +
        int(bc.unsignedBinaryToInt(cpu.memory[addr])))
    cpu.registers[reg] = bc.unsignedIntToBinary(result)
    if (result == 0): cpu.flags["ZF"] = True
    if (bc.unsignedIntToBinary(result)[0] == "1"): cpu.flags["SF"] = True
    if (result > 127 or result < -128): cpu.flags["OF"] = True


def subRegisterMemory(register: str, memory: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr = bc.BinaryToAddr(memory)
    result = int(
        bc.unsignedBinaryToInt(cpu.registers[reg]) -
        int(bc.unsignedBinaryToInt(cpu.memory[addr])))
    cpu.registers[reg] = bc.unsignedIntToBinary(result)
    if (result == 0): cpu.flags["ZF"] = True
    if (bc.unsignedIntToBinary(result)[0] == "1"): cpu.flags["SF"] = True
    if (result > 127 or result < -128): cpu.flags["OF"] = True


def uMultRegisterMemory(register: str, memory: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr = bc.BinaryToAddr(memory)
    result = math.floor(
        int(
            bc.unsignedBinaryToInt(cpu.registers[reg]) *
            int(bc.unsignedBinaryToInt(cpu.memory[addr]))))
    cpu.registers[reg] = bc.unsignedIntToBinary(result)
    if (result == 0): cpu.flags["ZF"] = True
    if (bc.unsignedIntToBinary(result)[0] == "1"): cpu.flags["SF"] = True
    if (result > 127 or result < -128): cpu.flags["OF"] = True


def sMultRegisterMemory(register: str, memory: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr = bc.BinaryToAddr(memory)
    result = math.floor(
        int(
            bc.signedBinaryToInt(cpu.registers[reg]) *
            int(bc.signedBinaryToInt(cpu.memory[addr]))))
    cpu.registers[reg] = bc.signedIntToBinary(result)
    if (result == 0): cpu.flags["ZF"] = True
    if (bc.unsignedIntToBinary(result)[0] == "1"): cpu.flags["SF"] = True
    if (result > 127 or result < -128): cpu.flags["OF"] = True


def uDivRegisterMemory(register: str, memory: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr = bc.BinaryToAddr(memory)
    result = math.floor(
        int(
            bc.unsignedBinaryToInt(cpu.registers[reg]) /
            int(bc.unsignedBinaryToInt(cpu.memory[addr]))))
    cpu.registers[reg] = bc.unsignedIntToBinary(result)
    if (result == 0): cpu.flags["ZF"] = True
    if (bc.unsignedIntToBinary(result)[0] == "1"): cpu.flags["SF"] = True
    if (result > 127 or result < -128): cpu.flags["OF"] = True


def sDivRegisterMemory(register: str, memory: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr = bc.BinaryToAddr(memory)
    result = math.floor(
        int(
            bc.signedBinaryToInt(cpu.registers[reg]) /
            int(bc.signedBinaryToInt(cpu.memory[addr]))))
    cpu.registers[reg] = bc.signedIntToBinary(result)
    if (result == 0): cpu.flags["ZF"] = True
    if (bc.unsignedIntToBinary(result)[0] == "1"): cpu.flags["SF"] = True
    if (result > 127 or result < -128): cpu.flags["OF"] = True