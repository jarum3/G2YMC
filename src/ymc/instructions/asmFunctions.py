import YMCCPU as cpu
import ymc.helpers.registerLookup as rl
import ymc.helpers.binaryConversion as bc


def outs(register) -> None:
    print(bc.signedBinaryToInt(rl.fourBitToRegister[register]))
