from enum import Enum
from typing import Optional

class Instruction(Enum):
    HALT = 0
    LDAC = 1
    STAC = 2
    MVAC = 3
    MOVR = 4
    JMP = 5
    JMPZ = 6
    OUT = 7
    SUB = 8
    ADD = 9
    INC = 10
    CLAC = 11
    AND = 12
    OR = 13
    ASHR = 14
    NOT = 15
    CALL = 16
    MOVXA = 17 # mov address into register
    MOVXV = 18 # mov value into register
    MOVXX = 19 # move register into register
    MOVXI = 20 # move int into register aka runtime data
    MOVAX = 21 # mov register into address
    MOVAI = 22 # move int into address
    MOVAV = 23 # move value into address
    MOVAA = 24 # move address into address
    MOV = 25 # just mov
    CMPXX = 26 # compare 2 registers
    CMP = 30
    JE = 31 # jump if equal
    JNE = 32 # jump if not equal


class Register(Enum):
    S = 0
    Z = 1
    IR = 2
    AR = 3
    DR = 4
    PC = 5
    OUTR = 6
    ACC = 7
    R = 8
    x0 = 9
    x1 = 10
    x2 = 11
    x3 = 12
    x4 = 13
    x5 = 15
    
class Flag(Enum):
    ZF = 0 # zero flag for cmp
    OF = 1 # overflow flag
    PF = 2 # parity flag
     

def hello_asm():
    print("Hello world")
    
asm_env = {
    "HelloWorld": hello_asm
}

class Syscall(Enum):
    HELLO = 0

def toReg(source: str) -> Register | None:
    for reg in Register:
        if source == reg.name:
            return reg
    return None
