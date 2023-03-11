from RV32I_Instr import *

def main():
    x = BEQ(31, 31, 12) # 1048577

    #print(x.gethex())

    y = parseRV32I(x.getbinary())
    print(y.getAssembly())


if __name__ == '__main__':
    main()
