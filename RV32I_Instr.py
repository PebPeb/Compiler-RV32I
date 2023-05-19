"""
    A rudimentary compiler for my RV32I Single Cycle CPU 
    this is meant to compile the most basic Asembly for the
    processor.

    Created By: Bryce Keen
    Date: 02/04/2023

    www.brycekeen.com

"""
import re

class instruction:
    def __init__(self, opcode):
        self.opcode = opcode
        self.instr = None
        
    def getbinary(self, endian="big"):
        if endian == "big":
            return self.instr
        elif endian == "little":
            return self.instr[24:32] + self.instr[16:24] + self.instr[8:16] + self.instr[0:8]
        else:
            print("Invalid Endian: valid inputs \"big\" and \"little\"")
        
    def gethex(self, endian="big"):
        if endian == "big":
            return "{:08x}".format(int(self.instr, 2))[-8:]
        elif endian == "little":
            le = "{:08x}".format(int(self.instr, 2))[-8:]
            return le[6:8] + le[4:6] + le[2:4] + le[0:2]
        else:
            print("Invalid Endian: valid inputs \"big\" and \"little\"")

    def __str__(self):
        return self.getAssembly()

# These should hold the basic parsing abilities of a 
# instruction type. This should help reduce the need
# for copy and pasting parsing for each type

class R_type(instruction):
    def __init__(self, funct7, rs2, rs1, funct3, rd, opcode, instrName, upperCase=False):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.funct7 = funct7
        self.rs2 = "{:05b}".format(rs2)[-5:]
        self.rs1 = "{:05b}".format(rs1)[-5:]
        self.funct3 = funct3
        self.rd = "{:05b}".format(rd)[-5:]
        self.instr = self.funct7 + self.rs2 + self.rs1 + self.funct3 + self.rd + self.opcode

        self.upperCase = upperCase

    def getAssembly(self):
        if (self.upperCase):
            instrName = self.instrName.upper()
        else:
            instrName = self.instrName.lower()

        rd = "x" + str(int(self.rd, 2))
        rs1 = "x" + str(int(self.rs1, 2))
        rs2 = "x" + str(int(self.rs2, 2))

        return f"{instrName:<10}" + " " + rd + "," + rs1 + "," + rs2

class R_type_shift(R_type):
    def __init__(self, funct7, rs2, rs1, funct3, rd, opcode, instrName, upperCase=False):
        R_type.__init__(self, funct7, rs2, rs1, funct3, rd, opcode, instrName, upperCase=upperCase)

    def getAssembly(self):
        if (self.upperCase):
            instrName = self.instrName.upper()
        else:
            instrName = self.instrName.lower()

        rd = "x" + str(int(self.rd, 2))
        rs1 = "x" + str(int(self.rs1, 2))
        shamt = str(int(self.rs2, 2))

        return f"{instrName:<10}" + " " + rd + "," + rs1 + "," + shamt


class I_type (instruction):
    def __init__(self, rs1, funct3, rd, imm, opcode, instrName, signed=False, upperCase=False):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.imm = "{:032b}".format(imm)[-12:]
        self.rs1 = "{:05b}".format(rs1)[-5:]
        self.rd = "{:05b}".format(rd)[-5:]
        self.funct3 = funct3
        self.instr = self.imm + self.rs1 + self.funct3 + self.rd + self.opcode
        
        self.signed = signed
        self.upperCase = upperCase

    def getAssembly(self):
        if (self.upperCase):
            instrName = self.instrName.upper()
        else:
            instrName = self.instrName.lower()

        rd = "x" + str(int(self.rd, 2))
        rs1 = "x" + str(int(self.rs1, 2))
        if (self.signed):
            imm = str(twos_comp(int(self.imm, 2), 12)) 
        else:
            imm = str(int(self.imm, 2))

        return f"{instrName:<10}" + " " + rd + "," + rs1 + "," + imm

class I_type_load (I_type):
    def __init__(self, rs1, funct3, rd, imm, opcode, instrName, signed=False, upperCase=False):
        I_type.__init__(self, rs1, funct3, rd, imm, opcode, instrName, signed=signed, upperCase=upperCase)
    
    def getAssembly(self):
        if (self.upperCase):
            instrName = self.instrName.upper()
        else:
            instrName = self.instrName.lower()

        rs1 = "x" + str(int(self.rs1, 2))
        rd = "x" + str(int(self.rd, 2))
        if (self.signed):
            imm = str(twos_comp(int(self.imm, 2), 12)) 
        else:
            imm = str(int(self.imm, 2))

        return f"{instrName:<10}" + " " + rd + "," + imm + "(" + rs1 + ")" 


class S_type (instruction):
    def __init__(self, rs2, rs1, funct3, imm, opcode, instrName, signed=False, upperCase=False):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.imm = "{:032b}".format(imm)[-12:]
        self.rs2 = "{:05b}".format(rs2)[-5:]
        self.rs1 = "{:05b}".format(rs1)[-5:]
        self.funct3 = funct3
        self.instr = self.imm[0:7] + self.rs2 + self.rs1 + self.funct3 + self.imm[7:12] + self.opcode
        
        self.signed = signed
        self.upperCase = upperCase

    def getAssembly(self):
        if (self.upperCase):
            instrName = self.instrName.upper()
        else:
            instrName = self.instrName.lower()
        rs1 = "x" + str(int(self.rs1, 2))
        rs2 = "x" + str(int(self.rs2, 2))
        if (self.signed):
            imm = str(twos_comp(int(self.imm, 2), 12)) 
        else:
            imm = str(int(self.imm, 2))

        return f"{instrName:<10}" + " " + rs2 + "," + imm + "(" + rs1 + ")" 


class B_type (instruction):
    def __init__(self, rs2, rs1, funct3, imm, opcode, instrName, upperCase=False):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.imm = "{:032b}".format(imm)[-13:-1]
        self.rs2 = "{:05b}".format(rs2)[-5:]
        self.rs1 = "{:05b}".format(rs1)[-5:]
        self.funct3 = funct3
        self.instr = self.imm[0] + self.imm[2:8] + self.rs2 + self.rs1 + self.funct3 + self.imm[8:12] + self.imm[1] + self.opcode
    
        self.upperCase = upperCase

    def getAssembly(self):
        if (self.upperCase):
            instrName = self.instrName.upper()
        else:
            instrName = self.instrName.lower()

        rs1 = "x" + str(int(self.rs1, 2))
        rs2 = "x" + str(int(self.rs2, 2))
        imm = str(int(self.imm, 2) << 1)

        return f"{instrName:<10}" + " " + rs1 + "," + rs2 + "," + imm

class U_type (instruction):
    def __init__(self, rd, imm, opcode, instrName, upperCase=False):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.rd = "{:05b}".format(rd)[-5:]
        self.imm = "{:032b}".format(imm)[:20]
        self.instr = self.imm + self.rd + self.opcode

        self.upperCase = upperCase

    def getAssembly(self):
        if (self.upperCase):
            instrName = self.instrName.upper()
        else:
            instrName = self.instrName.lower()

        rd = "x" + str(int(self.rd, 2))
        imm = str(int(self.imm, 2) << 12)

        return f"{instrName:<10}" + " " + rd + "," + imm

class J_type (instruction):
    def __init__(self, rd, imm, opcode, instrName, upperCase=False):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.rd = "{:05b}".format(rd)[-5:]
        self.imm = "{:032b}".format(imm)[-21:]
        imm = "{:032b}".format(imm)[-21:-1]
        self.imm = imm + "0"
        imm = imm[0] + imm[10:20] + imm[9] + imm[1:9]
        self.instr = imm + self.rd + self.opcode
    
        self.upperCase = upperCase

    def getAssembly(self):
        if (self.upperCase):
            instrName = self.instrName.upper()
        else:
            instrName = self.instrName.lower()

        rd = "x" + str(int(self.rd, 2))
        imm = str(int(self.imm, 2))

        return f"{instrName:<10}" + " " + rd + "," + imm


# Each instruction should be a child of their specific type

class LUI (U_type):
    def __init__(self, rd, imm):
        U_type.__init__(self, rd, imm, '0110111', 'LUI')

class AUIPC (U_type):
    def __init__(self, rd, imm):
        U_type.__init__(self, rd, imm, '0010111', 'AUIPC')

class JAL (J_type):
    def __init__(self, rd, imm):
        J_type.__init__(self, rd, imm, "1101111", "JAL")

class JALR (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "000", rd, imm, "1100111", "JALR")

class BEQ (B_type):
    def __init__(self, rs2, rs1, imm):
        B_type.__init__(self, rs2, rs1, "000", imm, "1100011", "BEQ")
    
class BNE (B_type):
    def __init__(self, rs2, rs1, imm):
        B_type.__init__(self, rs2, rs1, "001", imm, "1100011", "BNE")

class BLT (B_type):
    def __init__(self, rs2, rs1, imm):
        B_type.__init__(self, rs2, rs1, "100", imm, "1100011", "BLT")

class BGE (B_type):
    def __init__(self, rs2, rs1, imm):
        B_type.__init__(self, rs2, rs1, "101", imm, "1100011", "BGE")

class BLTU (B_type):
    def __init__(self, rs2, rs1, imm):
        B_type.__init__(self, rs2, rs1, "110", imm, "1100011", "BLTU")

class BGEU (B_type):
    def __init__(self, rs2, rs1, imm):
        B_type.__init__(self, rs2, rs1, "111", imm, "1100011", "BGEU")

class LB (I_type_load):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "000", rd, imm, "0000011", "LB", signed=True)

class LH (I_type_load):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "001", rd, imm, "0000011", "LH", signed=True)

class LW (I_type_load):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "010", rd, imm, "0000011", "LW", signed=True)

class LBU (I_type_load):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "100", rd, imm, "0000011", "LBU")

class LHU (I_type_load):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "101", rd, imm, "0000011", "LHU")

class SB (S_type):
    def __init__(self, rs2, rs1, imm):
        S_type.__init__(self, rs2, rs1, "000", imm, "0100011", "SB", signed=True)

class SH (S_type):
    def __init__(self, rs2, rs1, imm):
        S_type.__init__(self, rs2, rs1, "001", imm, "0100011", "SH", signed=True)

class SW (S_type):
    def __init__(self, rs2, rs1, imm):
        S_type.__init__(self, rs2, rs1, "010", imm, "0100011", "SW", signed=True)

class ADDI (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "000", rd, imm, "0010011", "ADDI", signed=True)

class SLTI (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "010", rd, imm, "0010011", "SLTI")

class SLTIU (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "011", rd, imm, "0010011", "SLTIU")

class XORI (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "100", rd, imm, "0010011", "XORI")

class ORI (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "110", rd, imm, "0010011", "ORI")

class ANDI (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "111", rd, imm, "0010011", "ANDI")

class SLLI (R_type_shift):
    def __init__(self, shamt, rs1, rd):
        R_type.__init__(self, "0000000", shamt, rs1, "001", rd, "0010011", "SLLI")

class SRLI (R_type_shift):
    def __init__(self, shamt, rs1, rd):
        R_type.__init__(self, "0000000", shamt, rs1, "101", rd, "0010011", "SRLI")

class SRAI (R_type_shift):
    def __init__(self, shamt, rs1, rd):
        R_type.__init__(self, "0100000", shamt, rs1, "101", rd, "0010011", "SRAI")

class ADD (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "000", rd, "0110011", "ADD")

class SUB (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0100000", rs2, rs1, "000", rd, "0110011", "SUB")

class SLL (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "001", rd, "0110011", "SLL")

class SLT (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "010", rd, "0110011", "SLT")

class SLTU (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "011", rd, "0110011", "SLTU")

class XOR (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "100", rd, "0110011", "XOR")

class SRL (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "101", rd, "0110011", "SRL")

class SRA (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0100000", rs2, rs1, "101", rd, "0110011", "SRA")

class OR (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "110", rd, "0110011", "OR")

class AND (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "111", rd, "0110011", "AND")




def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is


def parseHex_RV32I(instr):
    if (instr[:2] == '0x'):
        instr = instr[2:]

    if (len(instr) != 8):
        print("Error Instruction needs to be 32 bits long")
        exit()

    return __parse_RV32I_bin("{:032b}".format(int(instr, 16)))

def parseBin_RV32I(instr):
    if (instr[:2] == '0b'):
        instr = instr[2:]

    if (len(instr) != 32):
        print("Error Instruction needs to be 32 bits long")
        exit()

    return __parse_RV32I_bin(instr)


def __parse_RV32I_bin(instr):
    opcode = instr[25:32]
    rd = int(instr[20:25], 2)
    funct3 = instr[17:20]
    rs1 = int(instr[12:17], 2)
    rs2 = int(instr[7:12], 2)
    funct7 = instr[0:7]
    shamt = rs2

    imm_U = int(instr[0:20], 2) << 12
    imm_J = int(instr[0] + instr[12:20] + instr[11] + instr[1:11], 2) << 1
    imm_I = int(instr[0:12], 2)
    imm_B = int(instr[0] + instr[24] + instr[1:7] + instr[20:24], 2) << 1
    imm_S = int(instr[0:7] + instr[20:25], 2)

    match opcode:
        case "0110111":         # LUI
            return LUI(rd, imm_U)
        case "0010111":         # AUIPC
            return AUIPC(rd, imm_U)
        case "1101111":         # JAL
            return JAL(rd, imm_J)
        case "1100111":         # JALR
            match funct3:
                case "000":         # JALR
                    return JALR(rs1, rd, imm_I)
        case "1100011":         # BEQ, BNE, BLT, BGE, BLTU, BGEU
            match funct3:
                case "000":         # BEQ
                    return BEQ(rs2, rs1, imm_B)
                case "001":         # BNE
                    return BNE(rs2, rs1, imm_B)
                case "100":         # BLT
                    return BLT(rs2, rs1, imm_B)
                case "101":         # BGE
                    return BGE(rs2, rs1, imm_B)
                case "110":         # BLTU
                    return BLTU(rs2, rs1, imm_B)
                case "111":         # BGEU
                    return BGEU(rs2, rs1, imm_B)
        case "0000011":
            match funct3:
                case "000":         # LB
                    return LB(rs1, rd, imm_I)
                case "001":         # LH
                    return LH(rs1, rd, imm_I)
                case "010":         # LW
                    return LW(rs1, rd, imm_I)
                case "100":         # LBU
                    return LBU(rs1, rd, imm_I)
                case "101":         # LHU
                    return LHU(rs1, rd, imm_I)
        case "0100011":
            match funct3:
                case "000":         #SB
                    return SB(rs2, rs1, imm_S)
                case "001":         #SH
                    return SH(rs2, rs1, imm_S)
                case "010":         #SW
                    return SW(rs2, rs1, imm_S)
        case "0010011":
            match funct3:
                case "000":         #ADDI
                    return ADDI(rs1, rd, imm_I)
                case "010":         #SLTI
                    return SLTI(rs1, rd, imm_I)
                case "011":         #SLTIU
                    return SLTIU(rs1, rd, imm_I)
                case "100":         #XORI
                    return XORI(rs1, rd, imm_I)
                case "110":         #ORI
                    return ORI(rs1, rd, imm_I)
                case "111":         #ANDI
                    return ANDI(rs1, rd, imm_I)
                case "001":
                    match funct7:
                        case "0000000":     # SLLI
                            return SLLI(shamt, rs1, rd)
                case "101":         
                    match funct7:      
                        case "0000000":     # SRLI
                            return SRLI(shamt, rs1, rd)
                        case "0100000":     # SRAI
                            return SRAI(shamt, rs1, rd)
        case "0110011":
            match funct3:
                case "000":         #ADD
                    match funct7:
                        case "0000000":
                            return ADD(rs2, rs1, rd)
                case "000":         #SUB
                    match funct7:
                        case "0100000":
                            return SUB(rs2, rs1, rd)
                case "001":         #SLL
                    match funct7:
                        case "0000000":
                            return SLL(rs2, rs1, rd)
                case "010":         #SLT
                    match funct7:
                        case "0000000":
                            return SLT(rs2, rs1, rd)
                case "011":         #SLTU
                    match funct7:
                        case "0000000":
                            return SLTU(rs2, rs1, rd)
                case "100":         #XOR
                    match funct7:
                        case "0000000":
                            return XOR(rs2, rs1, rd)
                case "101":         #SRL
                    match funct7:
                        case "0000000":
                            return SRL(rs2, rs1, rd)
                case "101":         #SRA
                    match funct7:
                        case "0100000":
                            return SRA(rs2, rs1, rd)
                case "110":         #OR
                    match funct7:
                        case "0000000":
                            return OR(rs2, rs1, rd)
                case "111":         #AND
                    match funct7: 
                        case "0000000":
                            return AND(rs2, rs1, rd)
        case _:
            print("Invalid Opcode")
            return


def parseAssembly_RV32I(instr):
    return __parse_RV32I_assembly_raw(instr)



# Does not handle register aliases right now 
def __parse_RV32I_assembly_raw(instr):
    instr = re.sub(r'[\(\)\n]+', ' ', instr)
    instr = re.split(r'[,\s]+', instr)          # Split up mnemonic and registers
    mnemonic = instr[0].upper()

    # Currently does not handle register aliases just 0x-31x
    def parse_R_type(instr):
        return { "rd" : int(instr[1][1:]), 
                 "rs1" : int(instr[2][1:]),
                 "rs2" : int(instr[3][1:])}

    def parse_R_type_shamt(instr):
        return { "rd" : int(instr[1][1:]), 
                 "rs1" : int(instr[2][1:]),
                 "shamt" : int(instr[3])}

    def parse_I_type(instr):
        if (int(instr[3]) < 0):
            instr[3] = int(decimal_to_twos_complement(int(instr[3]), 12), 2)
        else:
            instr[3] = int(instr[3])

        return { "rd" : int(instr[1][1:]), 
                 "rs1" : int(instr[2][1:]),
                 "imm" : instr[3]}       

    def parse_S_type(instr):
        return { "rs2" : int(instr[1][1:]), 
                 "imm" : int(instr[2]),
                 "rs1" : int(instr[3][1:])}           

    def parse_B_type(instr):
        if (int(instr[3]) < 0):
            instr[3] = int(decimal_to_twos_complement(int(instr[3]), 13), 2)
        else:
            instr[3] = int(instr[3])

        return { "rs2" : int(instr[1][1:]), 
                 "rs1" : int(instr[2][1:]),
                 "imm" : int(instr[3])}    

    def parse_J_type(instr):
        return { "rd" : int(instr[1][1:]), 
                "imm" : int(instr[2])}  

    def parse_U_type(instr):
        return { "rd" : int(instr[1][1:]), 
                "imm" : int(instr[2])}  

    match mnemonic:
        case "LUI":
            operands = parse_U_type(instr)
            return LUI(operands["rd"], operands["imm"])
        case "AUIPC":
            operands = parse_U_type(instr)
            return AUIPC(operands["rd"], operands["imm"])
        case "JAL":
            operands = parse_J_type(instr)
            return JAL(operands["rd"], operands["imm"])
        case "JALR":
            operands = parse_I_type(instr)
            return JALR(operands["rs1"], operands["rd"], operands["imm"])
        case "BEQ":
            operands = parse_B_type(instr)
            return BEQ(operands["rs2"], operands["rs1"], operands["imm"])
        case "BNE":
            operands = parse_B_type(instr)
            return BNE(operands["rs2"], operands["rs1"], operands["imm"])
        case "BLT":
            operands = parse_B_type(instr)
            return BLT(operands["rs2"], operands["rs1"], operands["imm"])
        case "BGE":
            operands = parse_B_type(instr)
            return BGE(operands["rs2"], operands["rs1"], operands["imm"])
        case "BLTU":
            operands = parse_B_type(instr)
            return BLTU(operands["rs2"], operands["rs1"], operands["imm"])
        case "BGEU":
            operands = parse_B_type(instr)
            return BGEU(operands["rs2"], operands["rs1"], operands["imm"])
        case "LB":
            operands = parse_I_type(instr)
            return LB(operands["rs1"], operands["rd"], operands["imm"])
        case "LH":
            operands = parse_I_type(instr)
            return LH(operands["rs1"], operands["rd"], operands["imm"])
        case "LW":
            operands = parse_I_type(instr)
            return LW(operands["rs1"], operands["rd"], operands["imm"])
        case "LBU":
            operands = parse_I_type(instr)
            return LBU(operands["rs1"], operands["rd"], operands["imm"])
        case "LHU":
            operands = parse_I_type(instr)
            return LHU(operands["rs1"], operands["rd"], operands["imm"])
        case "SB":
            operands = parse_S_type(instr)
            return SB(operands["rs2"], operands["rs1"], operands["imm"])
        case "SH":
            operands = parse_S_type(instr)
            return SH(operands["rs2"], operands["rs1"], operands["imm"])
        case "SW":
            operands = parse_S_type(instr)
            return SW(operands["rs2"], operands["rs1"], operands["imm"])
        case "ADDI":
            operands = parse_I_type(instr)
            return ADDI(operands["rs1"], operands["rd"], operands["imm"])
        case "SLTI":
            operands = parse_I_type(instr)
            return SLTI(operands["rs1"], operands["rd"], operands["imm"])
        case "SLTIU":
            operands = parse_I_type(instr)
            return SLTIU(operands["rs1"], operands["rd"], operands["imm"])
        case "XORI":
            operands = parse_I_type(instr)
            return XORI(operands["rs1"], operands["rd"], operands["imm"])
        case "ORI":
            operands = parse_I_type(instr)
            return ORI(operands["rs1"], operands["rd"], operands["imm"])
        case "ANDI":
            operands = parse_I_type(instr)
            return ANDI(operands["rs1"], operands["rd"], operands["imm"])
        case "SLLI":
            operands = parse_R_type_shamt(instr)
            return SLLI(operands["shamt"], operands["rs1"], operands["rd"])
        case "SRLI":
            operands = parse_R_type_shamt(instr)
            return SRLI(operands["shamt"], operands["rs1"], operands["rd"])
        case "SRAI":
            operands = parse_R_type_shamt(instr)
            return SRAI(operands["shamt"], operands["rs1"], operands["rd"])
        case "ADD":
            operands = parse_R_type(instr)
            return ADD(operands["rs2"], operands["rs1"], operands["rd"])
        case "SUB":
            operands = parse_R_type(instr)
            return SUB(operands["rs2"], operands["rs1"], operands["rd"])
        case "SLL":
            operands = parse_R_type(instr)
            return SLL(operands["rs2"], operands["rs1"], operands["rd"])
        case "SLT":
            operands = parse_R_type(instr)
            return SLT(operands["rs2"], operands["rs1"], operands["rd"])
        case "SLTU":
            operands = parse_R_type(instr)
            return SLTU(operands["rs2"], operands["rs1"], operands["rd"])
        case "XOR":
            operands = parse_R_type(instr)
            return XOR(operands["rs2"], operands["rs1"], operands["rd"])
        case "SRL":
            operands = parse_R_type(instr)
            return SRL(operands["rs2"], operands["rs1"], operands["rd"])
        case "SRA":
            operands = parse_R_type(instr)
            return SRA(operands["rs2"], operands["rs1"], operands["rd"])
        case "OR":
            operands = parse_R_type(instr)
            return OR(operands["rs2"], operands["rs1"], operands["rd"])
        case "AND":
            operands = parse_R_type(instr)
            return AND(operands["rs2"], operands["rs1"], operands["rd"])

        # Pseudo-Mnemonic
        case "NOP":
            return ADDI(0, 0, 0)    
        case "MV":
            return ADDI(int(instr[2][1:]), int(instr[1][1:]),  0)    
        case "CLR":     
            return ADDI(0, int(instr[1][1:]), 0)


def decimal_to_twos_complement(number, num_bits):
    if number >= 0:
        raise ValueError("Input number must be negative.")
    
    max_value = 2 ** (num_bits - 1)
    if number < -max_value:
        raise ValueError(f"Input number is too small for {num_bits} bits.")

    positive_value = abs(number)
    complement_value = (2 ** num_bits) - positive_value
    binary = bin(complement_value)[2:]  # Convert to binary string, remove '0b' prefix

    # Zero-pad the binary string to ensure it has the desired number of bits
    padded_binary = binary.zfill(num_bits)

    return padded_binary
