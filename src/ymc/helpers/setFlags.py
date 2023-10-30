from helpers.binaryConversion import unsignedIntToBinary


def setFlags(result: int, add: bool = False, subCF: bool = False) -> dict[str, bool]:
    flags: dict[str, bool] = {"OF": False, "SF": False, "CF": False, "ZF": False}
    if result == 0:
        flags["ZF"] = True
    if unsignedIntToBinary(result)[0] == "1":
        flags["SF"] = True
    if result > 127 or result < -128:
        flags["OF"] = True
    if result > 255 and add:
        flags["CF"] = True
    if subCF:
        flags["CF"] = True
    return flags
