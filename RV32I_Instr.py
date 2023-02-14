"""
    A rudimentary compiler for my RV32I Single Cycle CPU 
    this is meant to compile the most basic Asembly for the
    processor.

    Created By: Bryce Keen
    Date: 02/04/2023

    www.brycekeen.com

"""

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

# These should hold the basic parsing abilities of a 
# instruction type. This should help reduce the need
# for copy and pasting parsing for each type

class R_type(instruction):
    def __init__(self, funct7, rs2, rs1, funct3, rd, opcode):
        instruction.__init__(self, opcode)
        self.funct7 = funct7
        self.rs2 = "{:05b}".format(rs2)[-5:]
        self.rs1 = "{:05b}".format(rs1)[-5:]
        self.funct3 = funct3
        self.rd = "{:05b}".format(rd)[-5:]
        self.instr = self.funct7 + self.rs2 + self.rs1 + self.funct3 + self.rd + self.opcode

class I_type (instruction):
    def __init__(self, rs1, funct3, rd, imm, opcode):
        instruction.__init__(self, opcode)
        self.imm = "{:032b}".format(imm)[-12:]
        self.rs1 = "{:05b}".format(rs1)[-5:]
        self.rd = "{:05b}".format(rd)[-5:]
        self.funct3 = funct3
        self.instr = self.imm + self.rs1 + self.funct3 + self.rd + self.opcode

class S_type (instruction):
    def __init__(self, rs2, rs1, funct3, imm, opcode):
        instruction.__init__(self, opcode)
        self.imm = "{:032b}".format(imm)[-12:]
        self.rs2 = "{:05b}".format(rs2)[-5:]
        self.rs1 = "{:05b}".format(rs1)[-5:]
        self.funct3 = funct3
        self.instr = self.imm[0:7] + self.rs2 + self.rs1 + self.funct3 + self.imm[7:12] + self.opcode


class B_type (instruction):
    def __init__(self, rs2, rs1, funct3, imm, opcode):
        instruction.__init__(self, opcode)
        self.imm = "{:032b}".format(imm)[-13:-1]
        self.rs2 = "{:05b}".format(rs2)[-5:]
        self.rs1 = "{:05b}".format(rs1)[-5:]
        self.funct3 = funct3
        self.instr = self.imm[0] + self.imm[2:8] + self.rs2 + self.rs1 + self.funct3 + self.imm[8:12] + self.imm[1] + self.opcode

class U_type (instruction):
    def __init__(self, rd, imm, opcode, instrName):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.rd = "{:05b}".format(rd)[-5:]
        self.imm = "{:032b}".format(imm)[:20]
        self.instr = self.imm + self.rd + self.opcode

    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd)) + ", " + str(int(self.imm, 2) << 12)

class J_type (instruction):
    def __init__(self, rd, imm, opcode, instrName):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.rd = "{:05b}".format(rd)[-5:]
        self.imm = "{:032b}".format(imm)[-21:]
        imm = "{:032b}".format(imm)[-21:-1]
        imm = imm[0] + imm[10:20] + imm[9] + imm[1:9]
        self.instr = imm + self.rd + self.opcode
    
    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd)) + ", " + str(int(self.imm, 2) << 1)


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
        I_type.__init__(self, rs1, "000", rd, imm, "1100111")

class BEQ (B_type):
    def __init__(self, rs2, rs1, imm):
        B_type.__init__(self, rs2, rs1, "000", imm, "1100011")

class BNE (B_type):
    def __init__(self, rs2, rs1, imm):
        B_type.__init__(self, rs2, rs1, "001", imm, "1100011")

class BLT (B_type):
    def __init__(self, rs2, rs1, imm):
        B_type.__init__(self, rs2, rs1, "100", imm, "1100011")

class BGE (B_type):
    def __init__(self, rs2, rs1, imm):
        B_type.__init__(self, rs2, rs1, "101", imm, "1100011")

class BLTU (B_type):
    def __init__(self, rs2, rs1, imm):
        B_type.__init__(self, rs2, rs1, "110", imm, "1100011")

class BGEU (B_type):
    def __init__(self, rs2, rs1, imm):
        B_type.__init__(self, rs2, rs1, "111", imm, "1100011")

class LB (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "000", rd, imm, "0000011")

class LH (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "001", rd, imm, "0000011")

class LW (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "010", rd, imm, "0000011")

class LBU (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "100", rd, imm, "0000011")

class LHU (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "101", rd, imm, "0000011")

class SB (S_type):
    def __init__(self, rs2, rs1, imm):
        S_type.__init__(self, rs2, rs1, "000", imm, "0100011")

class SH (S_type):
    def __init__(self, rs2, rs1, imm):
        S_type.__init__(self, rs2, rs1, "001", imm, "0100011")

class SW (S_type):
    def __init__(self, rs2, rs1, imm):
        S_type.__init__(self, rs2, rs1, "010", imm, "0100011")

class ADDI (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "000", rd, imm, "0010011")

class SLTI (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "010", rd, imm, "0010011")

class SLTIU (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "011", rd, imm, "0010011")

class XORI (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "100", rd, imm, "0010011")

class ORI (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "110", rd, imm, "0010011")

class ANDI (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "111", rd, imm, "0010011")

class SLLI (R_type):
    def __init__(self, shamt, rs1, rd):
        R_type.__init__(self, "0000000", shamt, rs1, "001", rd, "0010011")

class SRLI (R_type):
    def __init__(self, shamt, rs1, rd):
        R_type.__init__(self, "0000000", shamt, rs1, "101", rd, "0010011")

class SRAI (R_type):
    def __init__(self, shamt, rs1, rd):
        R_type.__init__(self, "0100000", shamt, rs1, "101", rd, "0010011")

class ADD (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "000", rd, "0110011")

class SUB (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0100000", rs2, rs1, "000", rd, "0110011")

class SLL (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "001", rd, "0110011")

class SLT (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "010", rd, "0110011")

class SLTU (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "011", rd, "0110011")

class XOR (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "100", rd, "0110011")

class SRL (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "101", rd, "0110011")

class SRA (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0100000", rs2, rs1, "101", rd, "0110011")

class OR (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "110", rd, "0110011")

class AND (R_type):
    def __init__(self, rs2, rs1, rd):
        R_type.__init__(self, "0000000", rs2, rs1, "111", rd, "0110011")


