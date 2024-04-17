from classes import VendingMachine
from lexer import lexer, errors
import sys

def main(argv):
    file = "initial.json" if len(argv) < 2 else argv[1]
    machine = VendingMachine(file, lexer, errors)
    
    while machine.running:
        data = input(">> ")
        machine.execute(data)

if __name__ == '__main__':
    main(sys.argv)
