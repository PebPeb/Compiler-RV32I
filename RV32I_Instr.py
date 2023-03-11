"""
    A rudimentary compiler for my RV32I Single Cycle CPU 
    this is meant to compile the most basic Asembly for the
    processor.

    Created By: Bryce Keen
    Date: 02/04/2023

    www.brycekeen.com

"""

def parseRV32I(instr):
    opcode = instr[25:32]
    rd = instr[20:25]
    funct3 = instr[17:20]
    rs1 = instr[12:17]

    imm_U = instr[0:20]
    imm_J = instr[0] + instr[12:20] + instr[11] + instr[1:11]
    imm_I = inst[0:12]
    

    match opcode:
        case "0110111":         # LUI
            return LUI(int(rd, 2), int(imm_U, 2) << 12)
        case "0010111":         # AUIPC
            return AUIPC(int(rd, 2), int(imm_U, 2) << 12)
        case "1101111":         # JAL
            return JAL(int(rd, 2), int(imm_J, 2) << 1)
        case "1100111":         # JALR, BEQ, BNE, BLT, BGE, BLTU, BGEU
            match funct3:
                case "000":     # JALR
                    return JALR(int(rs1, 2), int(rd, 2), int(imm_I, 2))
                case "000":
                    pass
                case "001":
                    pass
                case "100":
                    pass
                case "101":
                    pass
                case "110":
                    pass
                case "111":
                    pass


        case "1100011":
            pass
        case "0000011":
            pass
        case "0100011":
            pass
        case "0010011":
            pass
        case "0110011":
            pass
        case "0001111":
            pass
        case "1110011":
            pass

        case _:
            print("Invalid Opcode")
            return



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
    def __init__(self, funct7, rs2, rs1, funct3, rd, opcode, instrName):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.funct7 = funct7
        self.rs2 = "{:05b}".format(rs2)[-5:]
        self.rs1 = "{:05b}".format(rs1)[-5:]
        self.funct3 = funct3
        self.rd = "{:05b}".format(rd)[-5:]
        self.instr = self.funct7 + self.rs2 + self.rs1 + self.funct3 + self.rd + self.opcode

    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd, 2))  + ", x" + str(int(self.rs1, 2))  + ", x" + str(int(self.rs2, 2))

class I_type (instruction):
    def __init__(self, rs1, funct3, rd, imm, opcode, instrName):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.imm = "{:032b}".format(imm)[-12:]
        self.rs1 = "{:05b}".format(rs1)[-5:]
        self.rd = "{:05b}".format(rd)[-5:]
        self.funct3 = funct3
        self.instr = self.imm + self.rs1 + self.funct3 + self.rd + self.opcode
 
    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd, 2)) + ", x" + str(int(self.rs1, 2)) + ", " + str(int(self.imm, 2))

class S_type (instruction):
    def __init__(self, rs2, rs1, funct3, imm, opcode, instrName):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.imm = "{:032b}".format(imm)[-12:]
        self.rs2 = "{:05b}".format(rs2)[-5:]
        self.rs1 = "{:05b}".format(rs1)[-5:]
        self.funct3 = funct3
        self.instr = self.imm[0:7] + self.rs2 + self.rs1 + self.funct3 + self.imm[7:12] + self.opcode

    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rs2, 2)) + ", " + str(int(self.imm, 2)) + "(" + str(int(self.rs1, 2)) + ")"


class B_type (instruction):
    def __init__(self, rs2, rs1, funct3, imm, opcode, instrName):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.imm = "{:032b}".format(imm)[-13:-1]
        self.rs2 = "{:05b}".format(rs2)[-5:]
        self.rs1 = "{:05b}".format(rs1)[-5:]
        self.funct3 = funct3
        self.instr = self.imm[0] + self.imm[2:8] + self.rs2 + self.rs1 + self.funct3 + self.imm[8:12] + self.imm[1] + self.opcode
    
    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rs1, 2)) + ", x" + str(int(self.rs2, 2)) + ", " + str(int(self.imm, 2) << 1)

class U_type (instruction):
    def __init__(self, rd, imm, opcode, instrName):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.rd = "{:05b}".format(rd)[-5:]
        self.imm = "{:032b}".format(imm)[:20]
        self.instr = self.imm + self.rd + self.opcode

    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd, 2)) + ", " + str(int(self.imm, 2) << 12)

class J_type (instruction):
    def __init__(self, rd, imm, opcode, instrName):
        instruction.__init__(self, opcode)
        self.instrName = instrName
        self.rd = "{:05b}".format(rd)[-5:]
        self.imm = "{:032b}".format(imm)[-21:]
        imm = "{:032b}".format(imm)[-21:-1]
        self.imm = imm + "0"
        imm = imm[0] + imm[10:20] + imm[9] + imm[1:9]
        self.instr = imm + self.rd + self.opcode
    
    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd, 2)) + ", " + str(int(self.imm, 2))


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

class LB (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "000", rd, imm, "0000011", "LB")

    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd, 2)) + ", " + str(int(self.imm, 2)) + "(x" + str(int(self.rs1, 2)) + ")"

class LH (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "001", rd, imm, "0000011", "LH")

    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd, 2)) + ", " + str(int(self.imm, 2)) + "(x" + str(int(self.rs1, 2)) + ")"

class LW (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "010", rd, imm, "0000011", "LW")

    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd, 2)) + ", " + str(int(self.imm, 2)) + "(x" + str(int(self.rs1, 2)) + ")"

class LBU (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "100", rd, imm, "0000011", "LBU")

    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd, 2)) + ", " + str(int(self.imm, 2)) + "(x" + str(int(self.rs1, 2)) + ")"

class LHU (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "101", rd, imm, "0000011", "LHU")

    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd, 2)) + ", " + str(int(self.imm, 2)) + "(x" + str(int(self.rs1, 2)) + ")"

class SB (S_type):
    def __init__(self, rs2, rs1, imm):
        S_type.__init__(self, rs2, rs1, "000", imm, "0100011", "SB")

class SH (S_type):
    def __init__(self, rs2, rs1, imm):
        S_type.__init__(self, rs2, rs1, "001", imm, "0100011", "SH")

class SW (S_type):
    def __init__(self, rs2, rs1, imm):
        S_type.__init__(self, rs2, rs1, "010", imm, "0100011", "SW")

class ADDI (I_type):
    def __init__(self, rs1, rd, imm):
        I_type.__init__(self, rs1, "000", rd, imm, "0010011", "ADDI")

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

class SLLI (R_type):
    def __init__(self, shamt, rs1, rd):
        R_type.__init__(self, "0000000", shamt, rs1, "001", rd, "0010011", "SLLI")

    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd, 2))  + ", x" + str(int(self.rs1, 2))  + ", " + str(int(self.rs2, 2))

class SRLI (R_type):
    def __init__(self, shamt, rs1, rd):
        R_type.__init__(self, "0000000", shamt, rs1, "101", rd, "0010011", "SRLI")

    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd, 2))  + ", x" + str(int(self.rs1, 2))  + ", " + str(int(self.rs2, 2))

class SRAI (R_type):
    def __init__(self, shamt, rs1, rd):
        R_type.__init__(self, "0100000", shamt, rs1, "101", rd, "0010011", "SRAI")

    def getAssembly(self):
        return self.instrName + " x" + str(int(self.rd, 2))  + ", x" + str(int(self.rs1, 2))  + ", " + str(int(self.rs2, 2))

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


