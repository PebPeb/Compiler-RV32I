from RV32I_Instr import *

def main():
    x = SLLI(5, 3, 1) # 1048577
    #print(x.gethex())
    print(x.getAssembly())


if __name__ == '__main__':
    main()
