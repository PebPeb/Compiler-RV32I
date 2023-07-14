from rv32i.RV32I_Instr import *
import sys

def main():
    """
    lines = []
    with open("./Test.rv32i", 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:
                lines.append(line)

    for i in lines:
        i = parseAssembly_RV32I(i)
        sys.stdout.write(f"{i.gethex():<15}\n")
    """
    x = ["fe010113", "00812e23", "02010413", "00800793", "fef42623", "00200793", "fef42423", "fec42703", "fe842783", "00f707b3", "fef42223", "fe442783", "00078513", "01c12403", "02010113", "00008067"]
    
    for i in x:
        i = parseHex_RV32I(i)
        sys.stdout.write(f"{'':<8}{str(i):<15}\n")



def compareObj(x, y):
    sys.stdout.write(f"\n")
    sys.stdout.write(f"{'':<15}{'Input':^20}{'':>10}{'Output':^20}\n")
    sys.stdout.write(f"{'':<15}{x.getAssembly():<20}{'':>10}{y.getAssembly():<20}\n")
    sys.stdout.write(f"{'':<15}{x.gethex():<20}{'':>10}{y.gethex():<20}\n")
    sys.stdout.write(f"\n")


if __name__ == '__main__':
    main()
