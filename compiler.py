"""
    0000 - NOP
    00E0 - CLS
    00EE - RET
    0nnn - SYS addr
    1nnn - JP addr
    2nnn - CALL addr
    3xkk - SE Vx, byte
    4xkk - SNE Vx, byte
    5xy0 - SE Vx, Vy
    6xkk - LD Vx, byte
    7xkk - ADD Vx, byte
    8xy0 - LD Vx, Vy
    8xy1 - OR Vx, Vy
    8xy2 - AND Vx, Vy
    8xy3 - XOR Vx, Vy
    8xy4 - ADD Vx, Vy
    8xy5 - SUB Vx, Vy
    8xy6 - SHR Vx {, Vy}
    8xy7 - SUBN Vx, Vy
    8xyE - SHL Vx {, Vy}
    9xy0 - SNE Vx, Vy
    Annn - LD I, addr
    Bnnn - JP V0, addr
    Cxkk - RND Vx, byte
    Dxyn - DRW Vx, Vy, nibble
    Ex9E - SKP Vx
    ExA1 - SKNP Vx
    Fx07 - LD Vx, DT
    Fx0A - LD Vx, K
    Fx15 - LD DT, Vx
    Fx18 - LD ST, Vx
    Fx1E - ADD I, Vx
    Fx29 - LD F, Vx
    Fx33 - LD B, Vx
    Fx55 - LD [I], Vx
    Fx65 - LD Vx, [I]
"""

import re
import sys


if len(sys.argv)>=3:
    program = sys.argv[1]
    out_path = sys.argv[2]
else:
	print('Usage: python main.py path_to_program path_to_bin')
	exit()

print(program, out_path)

out = []

with open(program) as f:

    for line in f:
        line = line.replace('\n', '')
        if not line:
            out.append(0x00)
            out.append(0x00)
        elif line == 'CLS':
            out.append(0x00)
            out.append(0xE0)
        elif line == 'RET':
            out.append(0x00)
            out.append(0xEE)
        elif re.match('SYS [0-9A-F]{3}', line):
            index = line.replace('SYS ', '')
            opcode = 0x0000 + int(index, 16)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('JP [0-9A-F]{3}', line):
            index = line.replace('JP ', '')
            opcode = 0x1000 + int(index, 16)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('CALL [0-9A-F]{3}', line):
            index = line.replace('CALL ', '')
            opcode = 0x2000 + int(index, 16)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('SE V[0-9A-F], [0-9A-F]{2}', line):
            line = line.replace('SE ', '')
            x, kk = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0x3000 + (x << 8) + kk
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('SNE V[0-9A-F], [0-9A-F]{2}', line):
            line = line.replace('SNE ', '')
            x, kk = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0x4000 + (x << 8) + kk
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('SE V[0-9A-F], V[0-9A-F]', line):
            line = line.replace('SE ', '')
            x, y = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0x5000 + (x << 8) + (y << 4)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('LD V[0-9A-F], [0-9A-F]{2}', line):
            line = line.replace('LD ', '')
            x, kk = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0x6000 + (x << 8) + kk
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('ADD V[0-9A-F], [0-9A-F]{2}', line):
            line = line.replace('ADD ', '')
            x, kk = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0x7000 + (x << 8) + kk
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('LD V[0-9A-F], V[0-9A-F]', line):
            line = line.replace('LD ', '')
            x, y = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0x8000 + (x << 8) + (y << 4)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('OR V[0-9A-F], V[0-9A-F]', line):
            line = line.replace('OR ', '')
            x, y = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0x8001 + (x << 8) + (y << 4)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('AND V[0-9A-F], V[0-9A-F]', line):
            line = line.replace('AND ', '')
            x, y = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0x8002 + (x << 8) + (y << 4)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('XOR V[0-9A-F], V[0-9A-F]', line):
            line = line.replace('XOR ', '')
            x, y = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0x8003 + (x << 8) + (y << 4)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('ADD V[0-9A-F], V[0-9A-F]', line):
            line = line.replace('ADD ', '')
            x, y = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0x8004 + (x << 8) + (y << 4)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('SUB V[0-9A-F], V[0-9A-F]', line):
            line = line.replace('SUB ', '')
            x, y = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0x8005 + (x << 8) + (y << 4)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('SHR V[0-9A-F]', line):
            x = int(line.replace('SHR V', ''))
            opcode = 0x8006 + (x << 8)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('SUBN V[0-9A-F], V[0-9A-F]', line):
            line = line.replace('SUBN ', '')
            x, y = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0x8007 + (x << 8) + (y << 4)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('SHL V[0-9A-F]', line):
            x = int(line.replace('SHL V', ''))
            opcode = 0x800E + (x << 8)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('SNE V[0-9A-F], V[0-9A-F]', line):
            line = line.replace('SNE ', '')
            x, y = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0x9000 + (x << 8) + (y << 4)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('LD I, [0-9A-F]{3}', line):
            index = line.replace('LD I, ', '')
            opcode = 0xA000 + int(index, 16)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('JP V0, [0-9A-F]{3}', line):
            index = line.replace('JP V0, ', '')
            opcode = 0xB000 + int(index, 16)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('RND V[0-9A-F], [0-9A-F]{2}', line):
            line = line.replace('RND ', '')
            x, kk = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0xC000 + (x << 8) + kk
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('DRW V[0-9A-F], V[0-9A-F], [0-9A-F]', line):
            line = line.replace('DRW ', '')
            x, y, nn = [int(i, 16) for i in re.findall('[0-9A-F]+', line)]
            opcode = 0xD000 + (x << 8) + (y << 4) + nn
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('SKP V[0-9A-F]', line):
            x = int(line.replace('SKP V', ''))
            opcode = 0xE09E + (x << 8)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('SKNP V[0-9A-F]', line):
            x = int(line.replace('SKNP V', ''))
            opcode = 0xE0A1 + (x << 8)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('LD V[0-9A-F], DT', line):
            x = line.replace('LD V', '').replace(', DT', '')
            opcode = 0xF007 + (int(x, 16) << 8)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('LD V[0-9A-F], K', line):
            x = line.replace('LD V', '').replace(', K', '')
            opcode = 0xF00A + (int(x, 16) << 8)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('LD DT, V[0-9A-F]', line):
            x = line.replace('LD DT, V', '')
            opcode = 0xF015 + (int(x, 16) << 8)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('LD ST, V[0-9A-F]', line):
            x = line.replace('LD ST, V', '')
            opcode = 0xF018 + (int(x, 16) << 8)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('ADD I, V[0-9A-F]', line):
            x = line.replace('ADD I, V', '')
            opcode = 0xF01E + (int(x, 16) << 8)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('LD F, V[0-9A-F]', line):
            x = line.replace('LD F, V', '')
            opcode = 0xF029 + (int(x, 16) << 8)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('LD B, V[0-9A-F]', line):
            x = line.replace('LD B, V', '')
            opcode = 0xF033 + (int(x, 16) << 8)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('LD \[I\], V[0-9A-F]', line):
            x = line.replace('LD [I], V', '')
            opcode = 0xF055 + (int(x, 16) << 8)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        elif re.match('LD V[0-9A-F], \[I\]', line):
            x = line.replace('LD V', '').replace(', [I]', '')
            opcode = 0xF065 + (int(x, 16) << 8)
            out.append((opcode & 0xFF00) >> 8)
            out.append((opcode & 0x00FF))
        else:
            print('Error', line)

with open(out_path, 'wb') as f:
    f.write(bytes(out))


