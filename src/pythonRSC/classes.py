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
     
import pyray as pr
def hello_asm(emulator):
    print("Hello world")
    result = int(input("Stop the loop ? "))
    if result == 1:
        emulator.regs[Register.x0] = 1
    else:
        emulator.regs[Register.x0] = 0
    

def init_window(emulator):
    print("Creating a new window")
    width = emulator.regs[Register.x0]
    height = emulator.regs[Register.x1]
    pr.init_window(width, height, "Hello asm")

# should window close
def window_close(emulator):
    emulator.regs[Register.x0] = pr.window_should_close()
    
def begin_drawing(emulator):
    pr.begin_drawing()

def clear_bckground(emulator):
    color = emulator.regs[Register.x0]
    pr.clear_background([color, color, color, color])
    
def draw_reactangle(emulator):
    posx = emulator.regs[Register.x0]
    posy = emulator.regs[Register.x1]
    width = emulator.regs[Register.x2]
    height = emulator.regs[Register.x3]
    color = emulator.regs[Register.x4]
    pr.draw_rectangle(posx, posy, width, height, [255,color, 0, 255])
    
def end_drawing(emulator):
    pr.end_drawing()

def close_window(emulator):
    pr.close_window()

asm_env = {
    "HelloWorld": hello_asm,
    "InitWindow" : init_window,
    "CloseWindow" : close_window,
    "WindowShouldClose" : window_close,
    "BeginDrawing" : begin_drawing,
    "EndDrawing" : end_drawing,
    "ClearBackground" : clear_bckground,
    "DrawRectangle" : draw_reactangle
}

class Syscall(Enum):
    HELLO = 0
    INITWINDOW = 1
    CLOSEWINDOW = 2
    WINDOWSHOULDCLOSE = 3
    BEGINDRAWING = 4
    ENDDRAWING = 5
    CLEARBACKGROUND = 6
    DRAWRECT = 7

def toReg(source: str) -> Register | None:
    for reg in Register:
        if source == reg.name:
            return reg
    return None
