import argparse
import re

class Assembler():
    '''
    Assembler

    Example Usage:

    python assembler.py ../add/Add.asm
    '''

    def __init__(self,*args,**kwargs):
        self.pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE)
        self.symbols = {
            'SP' : '0',
            'LCL' : '1',
            'ARG' : '2',
            'THIS' : '3',
            'THAT' : '4',
            'R0' : '0',
            'R1' : '1',
            'R2' : '2',
            'R3' : '3',
            'R4' : '4',
            'R5' : '5',
            'R6' : '6',
            'R7' : '7',
            'R8' : '8',
            'R9' : '9',
            'R10' : '10',
            'R11' : '11',
            'R12' : '12',
            'R13' : '13',
            'R14' : '14',
            'R15' : '15',
            'SCREEN' : '16384',
            'KBD' : '24576',
        }

    def _remove_comments_and_whitespace(self,line):
        line = re.sub(self.pattern, '', line)
        line = line.strip()
        return line

    def assemble(self,asm_path):
        with open(asm_path,'r') as asm_file:
            asm = asm_file.readlines()
        asm = [self._remove_comments_and_whitespace(line) for line in asm]
        asm = [line for line in asm if len(line) > 0]
        linenum = 0
        for line in asm:
            first_char = line[0]
            if first_char == "(":
                label = re.search(r'\((.*?)\)',line).group(1)
                self.symbols[label] = linenum
            else:
                linenum += 1
        asm = [line for line in asm if line[0] != '(']

        for line in asm:
            first_char = line[0]
            if first_char == "@":
                value = re.split('@', line)
                print('a | {0}'.format(value))
            else:
                instruction = re.split('=|;', line)
                print('c | {0}'.format(instruction))


# -----------------------------------------------------------------------------------------
if __name__ == '__main__':

    assembler = Assembler()

    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        help='Path to asm file')
    args = parser.parse_args()
    assembler.assemble(args.path)
