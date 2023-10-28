registers: dict[str, int] = {"eax": 0, "ebx": 0, "ecx": 0, "edx": 0}
flags: dict[str, bool] = {"OF": False, "SF": False, "CF": False, "ZF": False}
memory: list[str] = ["00000000"] * 1024
instructionPointer: int = 0