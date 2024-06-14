from typing import List, Dict
import struct
from .classes import Instruction
from .classes import asm_env, Syscall,Register

class Assembler():
    def __init__(self, fn):
        self.ln = 0
        self.opcodes: List[int | str] = []
        self.symbol_table: Dict[str, int] = {}
        self.label_table: Dict[str, int] = {}
        self.tokenizer(fn)
        self.replaced_instructions = {count : instr for count, instr in enumerate(self.opcodes) if isinstance(instr, str)}
        self.instructions = [self.symbol_table[instruction] if instruction in self.symbol_table.keys() else instruction for instruction in self.opcodes]
        self.memory_layout = {count:instruction for count, instruction in enumerate(self.instructions)}


    """ Each line of the file is delimited by a space and checked if it is empty, then passed to the token parser. """
    def tokenizer(self, fn):
        try:
            with open(fn, 'r') as file:
                for line in file.readlines():
                    self.ln += 1
                    tokens : List[str] = line.strip().replace("\t", ' ').split(' ')
                    if tokens and tokens != ['']:
                        self.parse_tokens(tokens)
        except FileNotFoundError:
            print(f"The file {fn} is not in scope.")
            exit()


    """ Converts a token into an InstructionSet """
    def converter(self, token) -> int:
        for tType in Instruction:
            if tType.name == token:
                return tType.value


    """ Checks if a token is part of InstructionSet or not """
    def checker(self, token) -> bool:
        for tType in Instruction:
            if tType.name == token:
                return True
        return False
    
    def token2syscall(self, token):
        if token in asm_env:
            index = list(asm_env.keys()).index(token)
            return index
        else:
            raise KeyError(f"Token '{token}' not found in asm_env")
    
    def isregister(self, token) -> bool:
        if token in Register.__members__:
            return True
        else:
            return False
    """ Check if the given symbol is an address or the value of an address
    address -> = address
    [address] -> value inside
    """
    def isvalue(self, symbol):
        return (symbol[0] == "[" and symbol[-1] == "]")
    
    """ is this token really a symbol ?"""
    def issymbol(self, symbol):
        if self.isvalue(symbol):
            symbol = self.nakevalue(symbol) # nake the value to allow checking for string like this [symbol]
        return symbol in self.symbol_table
    
    """remove the [] around the value to search in symbol table"""
    def nakevalue(self, token):
        if self.isvalue(token):
            return token[1:-1]
        else:
            raise TypeError("Expected value")
    
    def token2register(self, token):
        if self.isregister(token):
            return Register[token].value
        else:
            raise KeyError(f"Token '{token}' not found in registers list")

    """ 
        Parses the given tokens from each line and generates a scaffolding of instructions stored in self.opcodes 
        Additionally, the function fills symbol table and label table for later use and replacement.
    """
    def parse_tokens(self, tokens: List[str]):
        t1 : str = tokens[0]
        if self.checker(t1):
            if t1 in ["LDAC", "STAC", "JMP", "JMPZ"]:
                try:
                    self.opcodes.extend([self.converter(t1), tokens[1]]) # Named addresses
                except IndexError:
                    print("Expected an operand for", t1,"at line", self.ln)
                    exit()
            elif t1 == "CALL":
                try:
                    self.opcodes.extend([self.converter(t1), self.token2syscall(tokens[1])])
                except IndexError:
                    print("Missing function for CALL ", self.ln)
                    exit()
            elif t1 in ["MOV"]:
                try:
                    if len(tokens[1].split(",", 1)) > 1:
                        tokens = [item for elem in tokens for item in elem.split(',') if item]
                        print(tokens)
                        if self.isregister(tokens[1]): #MOVX*
                            if self.isregister(tokens[2]): #MOVXX
                                self.opcodes.extend([Instruction.MOVXX.value, self.token2register(tokens[1]), self.token2register(tokens[2])])
                            elif self.issymbol(tokens[2]): #MOVXV or MOVXA
                                if self.isvalue(tokens[2]):
                                    self.opcodes.extend([Instruction.MOVXV.value, self.token2register(tokens[1]), self.symbol_table[self.nakevalue(tokens[2])]]) #MOVXV
                                else:
                                    self.opcodes.extend([Instruction.MOVXA.value], self.token2register(tokens[1]), self.symbol_table[tokens[2]])
                            elif tokens[2].isdigit(): #MOVXI
                                self.opcodes.extend([Instruction.MOVXI.value, self.token2register(tokens[1]), int(tokens[2])])
                            else:
                                raise IndexError("LMAO idk what to do rn")
                        elif self.issymbol(tokens[1]): #MOVA*
                            if self.issymbol(tokens[2]): #MOVAA or MOVAV
                                if self.isvalue(tokens[2]): #MOVAV
                                    self.opcodes.extend([Instruction.MOVAV.value, self.symbol_table[tokens[1]], self.symbol_table[tokens[2]]])
                                else: #MOVAA
                                    self.opcodes.extend([Instruction.MOVAA.value, self.symbol_table[tokens[1]], self.symbol_table[tokens[2]]])
                            elif self.isregister(tokens[2]): #MOVAX
                                self.opcodes.extend([Instruction.MOVAX.value, self.symbol_table[tokens[1]], self.token2register(tokens[2])])
                            elif tokens[2].isdigit(): #MOVAI
                                self.opcodes.extend([Instruction.MOVAI.value, self.symbol_table[tokens[1]], int(tokens[2])])
                            else:
                                print("2nd token is off")
                        else:
                            print("incorrect operands")
                    else:
                        raise print("Missing nigga")
                except IndexError:
                    print("kys")
                """
                try:
                    if len(tokens[1].split(",", 1)) > 1: # make sure we have a comma
                        tokens = [item for elem in tokens for item in elem.split(',') if item]
                        if self.isregister(tokens[1]):
                            self.opcodes.append(self.converter(t1))
                            self.opcodes.append(self.token2register(tokens[1]))
                        elif self.issymbol(tokens[1]):
                            self.opcodes.append(Instruction.MOVA.value) # specific instruction to move values inside a data
                            self.opcodes.append(self.symbol_table[tokens[1]]) # append the address of the symbol instead to mova
                        else:
                            print("ERROR NOT A REGISTER NOR AN ADDRESS")
                            raise NotImplementedError()
                        if self.isvalue(tokens[2]):
                            self.opcodes.append(self.opcodes[self.symbol_table[self.nakevalue(tokens[2])]])
                        elif tokens[2].isdigit(): # handle the case where you just want to move a value
                            self.opcodes.append(int(tokens[2]))
                        else:
                            self.opcodes.append(self.symbol_table[tokens[2]])
                    else:
                        raise IndexError("Missing ,")
                except IndexError:
                    print("Expected an operand for", t1,"at line", self.ln)
                    """
            else:
                self.opcodes.append(self.converter(t1))
        elif ':' in t1:
            if len(tokens) > 1 and tokens[1] != '':
                try:
                    self.symbol_table.update({tokens[0][:-1] : len(self.opcodes)})
                    righthand_side: int = int(tokens[1], base=16)
                    self.opcodes.append(righthand_side)
                    if righthand_side < 0:
                        print("Unexpected negative sign before hexadecimal number", tokens[1][1:], "at line", self.ln)
                        exit()
                except ValueError:
                    print("Expected a hexadecimal number after declaration", tokens[0][:-1], "at line", self.ln)
                    exit()
            else:
                self.symbol_table.update({tokens[0][:-1] : len(self.opcodes)})
                self.label_table.update({tokens[0][:-1] : len(self.opcodes)})
        elif ';' in t1:
            pass
        else:
            print("Unknown keyword", t1 ,"used at line", self.ln)
            exit()


    """ Dirty function to output in the binary format for Logisim """
    def logisim_format(self, fn):
        with open(fn, "w") as file:
            file.write("v2.0 raw\n")
            for instruction in self.instructions:
                file.write(hex(int(instruction))[2:].zfill(8)+"\n")

    """ Binary ninja formatted output """
    " The most amazing refactor happened here, you gotta check the commit history to believe it. "
    def bn_format(self, fn):
        bn_format = [self.symbol_table[instruction]*4 if instruction in self.symbol_table.keys() else instruction for instruction in self.opcodes]
        with open(fn, "wb") as file:
            for instruction in bn_format:
                assert(type(instruction) == int)
                file.write(struct.pack("i", instruction))