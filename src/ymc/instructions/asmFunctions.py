import ymc.YMCCPU as cpu
import ymc.helpers.registerLookup as rl
import ymc.helpers.binaryConversion as bc


def outs(register: str) -> None:
    # print the signed representation of the CPU register pointed to by the register byte
    print(bc.signedBinaryToInt(cpu.registers[rl.fourBitToRegister(register)]))
