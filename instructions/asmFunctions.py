import YMCCPU as ymc
import helpers.registerLookup as rl
import helpers.binaryConversion as bc


def outs(register) -> None:
    print(bc.signedBinaryToInt(rl.fourBitToRegister[register]))
