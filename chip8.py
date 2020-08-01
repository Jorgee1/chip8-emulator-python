import sys
from random import randint

### VARS  ######################
W = 64
H = 32
START_PC = 512
FONT = 'font/chip8_Font.bin'
#################################

### REGISTERS ###################
memory = [0 for i in range(8*512)]
v      = [0 for i in range(8*2)]
i      = 0
pc     = START_PC
sp     = 0
stack  = [0 for i in range(8*2)]
dt     = 0
st     = 0
key    = [0 for i in range(8*2)]
screen = [[0 for x in range(W)] for y in range(H)]
#################################

### Instructions ################

# Functions

def NOP(opcode):
	# 0000
	pc += 2

def CLS(opcode):
	# 00E0
	for j in range(H):
		for i in range(W):
			screen[j][i] = 0
	pc += 2

def RET(opcode):
	# 00EE
	sp = (sp - 1) & 0x000F
	pc = stack[sp]
	stack[sp] = 0
	pc = pc + 2


def JP_ADDR(opcode):
	# 1nnn
	pc = get_nnn(opcode)

def CALL_ADDR(opcode):
	# 2nnn
	stack[sp] = pc
	sp = (sp + 1) & 0x000F
	pc = get_nnn(opcode)

def SE_Vx_Byte(opcode):
	# 3xkk - Tested
	x, kk = get_x_kk(opcode)

	if v[x] == kk:
		pc = pc + 2
	pc = pc + 2

def SNE_Vx_Byte(opcode):
	# 4xkk - Tested
	x, kk = get_x_kk(opcode)

	if v[x] != kk:
		pc = pc + 2 
	pc = pc + 2

def SE_Vx_Vy(opcode):
	# 5xy0 - test
	x, y = get_x_y(opcode)

	if(v[x]==v[y]):
		pc = pc + 2
	pc = pc + 2

def LD_Vx_Byte(opcode):
	# 6xkk
	x, kk = get_x_kk(opcode)
	v[x] = kk
	pc = pc + 2


def ADD_Vx_Byte(opcode):
	# 7xkk - tested
	x, kk = get_x_kk(opcode)
	v[x], _ = add_byte(v[x], kk)
	pc += 2

def LD_Vx_Vy(opcode):
	# 8xy0
	x, y = get_x_y(opcode)
	v[x] = v[y]
	pc = pc + 2

def OR_Vx_Vy(opcode):
	# 8xy1
	x, y = get_x_y(opcode)
	v[x] = or_byte(v[x], v[y])
	pc += 2

def AND_Vx_Vy(opcode):
	# 8xy2
	x, y = get_x_y(opcode)
	v[x] = and_byte(v[x], v[y])
	pc += 2

def XOR_Vx_Vy(opcode):
	# 8xy3
	x, y = get_x_y(opcode)
	v[x] = xor_byte(v[x], v[y])
	pc += 2

def ADD_Vx_Vy(opcode):
	# 8xy4
	x, y = get_x_y(opcode)
	v[x], v[0xF] = add_byte(v[x], v[y])
	pc += 2

def SUB_Vx_Vy(opcode):
	# 8xy5
	x, y = get_x_y(opcode)
	v[x], v[0xF] = sub_byte(v[x], v[y])
	pc += 2

def SHR_Vx(opcode):
	# 8xy6
	x = get_x_kk(opcode)

	v[x], v[0xF] = shift_right(v[x])
	pc = pc + 2

def SUBN_Vx_Vy(opcode):
	# 8xy7
	x, y = get_x_y(opcode)

	v[x], v[0xF] = sub_byte(v[y], v[x])
	pc += 2

def SHL_Vx(opcode):
	# 8xyE
	x = get_x_kk(opcode)

	v[x], v[0xF] = shift_left(v[x])
	pc = pc + 2


def SNE_Vx_Vy(opcode):
	# 9xy0
	x, y = get_x_y(opcode)

	if v[x] != v[y]:
		pc = pc + 2
	pc = pc + 2

def LD_I_ADDR(opcode):
	# Annn
	i = opcode & 0x0FFF
	pc = pc + 2

def JP_V0_ADDR(opcode):
	# Bnnn
	nnn = self.get_nnn(opcode)
	pc = (nnn + v[0]) & 0xFFF

def RND_Vx_Byte(opcode):
	# Cxkk
	x, kk = get_x_kk(opcode)
	RND = randint(0, 255)
	v[x] = RND & kk
	pc = pc + 2

def DRW_Vx_Vy_N(opcode):
	# Dxyn
	x, y, n = get_x_y_n(opcode)

	v[0x0F] = 0

	x_cor = v[x]
	y_cor = v[y]

	for index in range(n):
		sprite = format(memory[i + index], '08b')
		x_cor = v[x]

		if y_cor >= H:
			y_cor = y_cor - H*int((y_cor/(H-1)))

		for j in sprite:

			if x_cor >= W:
				x_cor = x_cor - W*int((x_cor/(W-1)))

			if screen[y_cor][x_cor] == int(j):
				if screen[y_cor][x_cor]:
					v[0x0F] = 1
				screen[y_cor][x_cor] = 0
			else:
				screen[y_cor][x_cor] = 1
			x_cor = x_cor + 1
		y_cor = y_cor + 1

	pc = pc + 2


def SKP_Vx(opcode):
	#Ex9E
	x, _ = get_x_kk(opcode)

	if key[V[x]]:
		pc = pc + 2
	pc = pc + 2

def SKNP_Vx(opcode):
	#ExA1
	x, _ = get_x_kk(opcode)
	
	if not key[v[x]]:
		pc = pc + 2
	pc = pc + 2


def LD_Vx_DT(opcode):
	# Fx07
	x, _ = get_x_y(opcode)
	v[x] = dt
	pc = pc + 2

def LD_Vx_K(opcode):
	# Fx0a
	x, _ = get_x_y(opcode)

	for i in range(len(key)):
		if key[i]:
			v[x] = i
			pc = pc + 2
			break

def LD_DT_Vx(opcode):
	# Fx15
	x, _ = get_x_y(opcode)
	dt = v[x]
	pc = pc + 2

def LD_ST_Vx(opcode):
	# Fx18
	x, _ = get_x_y(opcode)
	st = v[x]
	pc = pc + 2

def ADD_I_Vx(opcode):
	# Fx1E - test
	x, _ = get_x_y(opcode)
	i = add_2byte(i, v[x])
	pc = pc + 2

def LD_F_Vx(opcode):
	# Fx29
	x, _ = get_x_y(opcode)
	i = v[x] * 5
	pc = pc + 2

def LD_B_Vx(opcode):
	# Fx33
	x, _ = get_x_y(opcode)
	TEN = int(v[x]/100)
	HUN = int(v[x]/10) - TEN*10
	DEC = v[x] - HUN*10 - TEN*100

	memory[i]     = TEN
	memory[i + 1] = HUN
	memory[i + 2] = DEC

	pc = pc + 2

def LD_I_Vx(opcode):
	# Fx55
	x, _ = get_x_y(opcode)
	for index in range(x + 1):
		memory[i + index] = v[index]

	pc = pc + 2

def LD_Vx_I(opcode):
	# Fx65
	x, _ = get_x_y(opcode)
	for index in range(x + 1):
		v[i] = memory[i + index]

	pc = pc + 2

# Index

inst_global = {
	0 : lambda opcode: inst_0[opcode & 0x00FF](opcode),
	1 : JP_ADDR,
	2 : CALL_ADDR,
	3 : SE_Vx_Byte,
	4 : SNE_Vx_Byte,
	5 : SE_Vx_Vy,
	6 : LD_Vx_Byte,
	7 : ADD_Vx_Byte,
	8 : lambda opcode: inst_8[opcode & 0x000F](opcode),
	9 : SNE_Vx_Vy,
	10: LD_I_ADDR,
	11: JP_V0_ADDR,
	12: RND_Vx_Byte,
	13: DRW_Vx_Vy_N,
	14: lambda opcode: inst_E[opcode & 0x00FF](opcode),
	15: lambda opcode: inst_F[opcode & 0x00FF](opcode)
}

inst_0 = {
	0  : NOP,
	224: CLS,
	238: RET
}

inst_8 = {
	0 : LD_Vx_Vy,
	1 : OR_Vx_Vy,
	2 : AND_Vx_Vy,
	3 : XOR_Vx_Vy,
	4 : ADD_Vx_Vy,
	5 : SUB_Vx_Vy,
	6 : SHR_Vx,
	7 : SUBN_Vx_Vy,
	14: SHL_Vx
}

inst_E = {
	158: SKP_Vx,
	161: SKNP_Vx
}

inst_F = {
	7  : LD_Vx_DT,
	10 : LD_Vx_K,
	21 : LD_DT_Vx,
	24 : LD_ST_Vx,
	30 : ADD_I_Vx,
	41 : LD_F_Vx,
	51 : LD_B_Vx,
	85 : LD_I_Vx,
	101: LD_Vx_I
}

#################################

### UTILS #######################


def get_nnn(opcode):
	return opcode & 0x0FFF

def get_x_y(opcode):
	return (opcode & 0x0F00) >> 8, (opcode & 0x00F0) >> 4

def get_x_kk(opcode):
	return (opcode & 0x0F00) >> 8, opcode & 0x00FF

def get_x_y_n(opcode):
	return (opcode & 0x0F00) >> 8, (opcode & 0x00F0) >> 4, opcode & 0x000F

def load_file(self, path, offset):
	with open(path, 'rb') as f:
		count = offset
		byte = f.read(1)
		while byte:
			memory[count] = int.from_bytes(byte, byteorder='little')
			byte = f.read(1)
			count = count + 1

#################################

### Main Functions ##############

def fetch():
	return (memory[pc] << 8) | memory[pc + 1]

def tic_timmer():
	if dt:
		dt = dt - 1

	if st:
		st = st - 1

def run(opcode):
	opcode = fetch()

	inst_global[opcode>>12](opcode)

	tic_timmer()

#################################

### ALU #########################

# ADD

def add_byte(value_1, value_2):
	result = value_1 + value_2
	return result & 255, (result & 256) >> 8

def add_2byte(value_1, value_2):
	result = value_1 + value_2
	return result & 0xFFFF, (result & 0x10000) >> 16

# SUB

def sub_byte(value_1, value_2):
	result = value_1 - value_2
	borrow = 0

	if result < 0:
		borrow = 1
		
	return result & 255, borrow

# AND

def and_byte(value_1, value_2):
	return (value_1 & value_2) & 255

# OR

def or_byte(value_1, value_2):
	return (value_1 | value_2) & 255

# XOR

def xor_byte(value_1, value_2):
	return (value_1 ^ value_2) & 255

# Shift Left

def shift_left(value):
	LSB = value & 1
	return (value >> 1) & 255, LSB

# Shift Right

def shift_right(value):
	MSB = (value & 0x80) >> 7
	return (value << 1) & 255, MSB

#################################



if __name__ == '__main__':
	if len(sys.argv) >= 2:
		game = sys.argv[1]

		load_file(FONT, 0)
		load_file(path, START_PC)

		# Implementation
	else:
		print("No file selected")
		exit()
