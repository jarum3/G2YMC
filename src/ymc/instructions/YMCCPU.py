##############################
# Stores global values relating to CPU data that can be used across instruction functions
##############################

# Stores register values as single bytes, starting as all 0s
registers: dict[str, str] = {
    "EAX": "0" * 8,
    "EBX": "0" * 8,
    "ECX": "0" * 8,
    "EDX": "0" * 8,
}
# Stores flag values as booleans
flags: dict[str, bool] = {"OF": False, "SF": False, "CF": False, "ZF": False}
# Creates memory as a 1024-length list (1kb)
memory: list[str] = ["00000000"] * 1024
# Instruction pointer will start at 0, first instruction should be at address 0 in memory.
instructionPointer: int = 0
# Dictionary of type widths, in bytes
typeWidths: dict[str, int] = {
    "literal": 1,
    "register": 1,
    "register-register": 1,
    "memory": 2,
}
exiting: bool = False
