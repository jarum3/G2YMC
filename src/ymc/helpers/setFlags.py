from helpers.binaryConversion import unsignedIntToBinary


def setFlags(result: int, add: bool = False, subCF: bool = False) -> dict[str, bool]:
    flags: dict[str, bool] = {"OF": False, "SF": False, "CF": False, "ZF": False}
    if result == 0: # Zero flag true if result is 0
        flags["ZF"] = True
    if unsignedIntToBinary(result)[0] == "1": # Sign flag true if most-significant bit is 1
        flags["SF"] = True
    if result > 127 or result < -128: # Overflow flag true if result out of range for signed representation
        flags["OF"] = True
    if result > 255 and add: # Carry flag true if result of addition is greater than 255
        flags["CF"] = True
    if subCF:
        flags["CF"] = True # Carry flag also true if a > b in sub a, b (Bool passed by caller)
    return flags
