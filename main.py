from RV32I_Instr import *

def main():
    x = JAL(1, 23423) # 1048577
    #print(x.gethex())
    print(x.getAssembly())
    print(x.gethex())
    print(x.getbinary())

    print()

    y = parseRV32I(x.getbinary())
    print(y.getAssembly())


if __name__ == '__main__':
    main()
