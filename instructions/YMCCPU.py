registers: dict[str, int] = {"EAX": 0, "EBX": 0, "ECX": 0, "EDX": 0}
flags: dict[str, bool] = {"OF": False, "SF": False, "CF": False, "ZF": False}
memory: list[str] = ["00000000"] * 1024
instructionPointer: int = 0
typeWidths: dict[str, int] = {
    "literal": 1,
    "register": 1,
    "register-register": 1,
    "memory": 2
}
