import ymc.YMCCPU as cpu
import ymc.helpers.registerLookup as rl
import ymc.helpers.binaryConversion as bc


def outs(register: str) -> None:
    # print the signed representation of the CPU register pointed to by the register byte
    print(bc.signedBinaryToInt(cpu.registers[rl.fourBitToRegister(register)]))


def outu(register: str) -> None:
    # print the unsigned representation of the CPU register pointed to by the register byte
    print(bc.unsignedBinaryToInt(
        cpu.registers[rl.fourBitToRegister(register)]))


def outnl() -> None:
    print("\n")


def movrr(registers: str) -> None:
    args: list[str] = rl.eightBitToRegisters(registers)
    cpu.registers[args[0]] = cpu.registers[args[1]]


def movmrm(register: str, address: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr_int: int = bc.BinaryToAddr(address)
    cpu.registers[reg] = cpu.memory[addr_int]


def movrl(register: str, literal: str) -> None:
    reg = rl.fourBitToRegister(register)
    cpu.registers[reg] = literal[-8:]


def movmr(address: str, register: str) -> None:
    reg = rl.fourBitToRegister(register)
    addr_int = bc.BinaryToAddr(address)
    cpu.memory[addr_int] = cpu.registers[reg]