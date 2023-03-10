from RV32I_Instr import *

def main():
    x = SLLI(5, 3, 1) # 1048577
    #print(x.gethex())
    print(x.getAssembly())

    parseRV32I("00000000000000000000000000110111")


if __name__ == '__main__':
    main()
