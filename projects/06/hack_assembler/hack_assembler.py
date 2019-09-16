import argparse
from pathlib import Path
import re


class HackAssembler():
    '''
    HackAssembler

    Example Usage:

    python hack_assembler.py ../add/Add.asm
    '''

    def __init__(self,*args,**kwargs):
        self.pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE)
        self.addressing_symbols = {
            'SP' : 0,
            'LCL' : 1,
            'ARG' : 2,
            'THIS' : 3,
            'THAT' : 4,
            'R0' : 0,
            'R1' : 1,
            'R2' : 2,
            'R3' : 3,
            'R4' : 4,
            'R5' : 5,
            'R6' : 6,
            'R7' : 7,
            'R8' : 8,
            'R9' : 9,
            'R10' : 10,
            'R11' : 11,
            'R12' : 12,
            'R13' : 13,
            'R14' : 14,
            'R15' : 15,
            'SCREEN' : 16384,
            'KBD' : 24576,
        }

        self.a_instruction = '0{value:>015b}'
        self.variable_number = 16

        self.comp_symbols = {
            '0' : '0101010',
            '1' : '0111111',
            '-1' : '0111010',
            'D' : '0001100',
            'A' : '0110000',
            '!D' : '0001101',
            '!A' : '0110001',
            '-D' : '0001111',
            '-A' : '0110011',
            'D+1' : '0011111',
            'A+1' : '0110111',
            'D-1' : '0001110',
            'A-1' : '0110010',
            'D+A' : '0000010',
            'D-A' : '0010011',
            'A-D' : '0000111',
            'D&A' : '0000000',
            'D|A' : '0010101',
            'M' : '1110000',
            '!M' : '1110001',
            '-M' : '1110011',
            'M+1' : '1110111',
            'M-1' : '1110010',
            'D+M' : '1000010',
            'D-M' : '1010011',
            'M-D' : '1000111',
            'D&M' : '1000000',
            'D|M' : '1010101',
        }
    def _remove_comments_and_whitespace(self,line):
        line = re.sub(self.pattern, '', line)
        line = line.strip()
        return line

    def assemble(self,asm_path):
        asm_path = Path(asm_path)
        with asm_path.open() as asm_file:
            asm = asm_file.readlines()

        # remove comments, whitespace, and blank lines
        asm = [self._remove_comments_and_whitespace(line) for line in asm]
        asm = [line for line in asm if len(line) > 0]

        # scan for labels
        linenum = 0
        for line in asm:
            first_char = line[0]
            if first_char == "(":
                label = re.search(r'\((.*?)\)',line).group(1)
                self.addressing_symbols[label] = linenum
            else:
                linenum += 1
        asm = [line for line in asm if line[0] != '(']

        hack_path = asm_path.with_suffix('.hack')
        print(hack_path)

        for line in asm:
            first_char = line[0]
            if first_char == "@":
                symbol = line[1:]
                try:
                    str = self.addressing_symbols[symbol]
                except KeyError:
                    str = symbol
                try:
                    value = int(str)
                except ValueError:
                    self.addressing_symbols.update({symbol : self.variable_number})
                    value = self.variable_number
                    self.variable_number += 1
                print(f'a | {value}')
                print(self.a_instruction.format(value=value))
            else:
                instruction = re.split('=|;', line)
                print(f'c | {instruction}')
        print(self.addressing_symbols)


# -----------------------------------------------------------------------------------------
if __name__ == '__main__':

    hack_assembler = HackAssembler()

    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        help='Path to asm file')
    args = parser.parse_args()
    hack_assembler.assemble(args.path)
