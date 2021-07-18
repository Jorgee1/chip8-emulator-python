from random import randint

### CORE ########################
class Core:
	W = 64
	H = 32
	START_PC = 512

	def __init__(self):
		self.memory = [0 for i in range(8*512)]
		self.v      = [0 for i in range(8*2)]
		self.i      = 0
		self.pc     = self.START_PC
		self.sp     = 0
		self.stack  = [0 for i in range(8*2)]
		self.dt     = 0
		self.st     = 0
		self.key    = [0 for i in range(8*2)]
		self.screen = [[0 for x in range(self.W)] for y in range(self.H)]

	def __repr__(self):
		opcode = self.to_hex(self.fetch())
		pc_hex = self.to_hex(self.pc)
		return f'Core - PC:{pc_hex} OPCODE:{opcode}'

	def to_hex(self, value):
		return '0x{:04x}'.format(value).upper()

	def load(self, path, offset=0):
		with open(path, 'rb') as f:
			count = 0
			byte = f.read(1)
			while byte:
				self.memory[offset + count] = int.from_bytes(byte, byteorder='little')
				byte = f.read(1)
				count += 1

	def fetch(self):
		return (self.memory[self.pc] << 8) | self.memory[self.pc + 1]

	def next(self):
		self.pc += 2

	def stack_push(self):
		self.stack[self.sp] = self.pc
		self.sp = (self.sp + 1) & 0x000F

	def stack_pop(self):
		self.sp = (self.sp - 1) & 0x000F
		self.pc = self.stack[self.sp]
		self.stack[self.sp] = 0

	def clear_screen(self):
		for j in range(self.H):
			for i in range(self.W):
				self.screen[j][i] = 0

	def tic_timmer(self):
		if self.dt:
			self.dt -= 1

		if self.st:
			self.st -= 1

#################################

### Instructions ################

# Functions

def NOP(opcode, core):
	# 0000
	core.next()

def CLS(opcode, core):
	# 00E0
	core.clear_screen()
	core.next()

def RET(opcode, core):
	# 00EE
	core.stack_pop()
	core.next()


def JP_ADDR(opcode, core):
	# 1nnn
	core.pc = get_nnn(opcode)

def CALL_ADDR(opcode, core):
	# 2nnn
	core.stack_push()
	core.pc = get_nnn(opcode)

def SE_Vx_Byte(opcode, core):
	# 3xkk - Tested
	x, kk = get_x_kk(opcode)

	if core.v[x] == kk:
		core.next()
	core.next()

def SNE_Vx_Byte(opcode, core):
	# 4xkk - Tested
	x, kk = get_x_kk(opcode)

	if core.v[x] != kk:
		core.next()
	core.next()

def SE_Vx_Vy(opcode, core):
	# 5xy0 - test
	x, y = get_x_y(opcode)

	if(core.v[x] == core.v[y]):
		core.next()
	core.next()

def LD_Vx_Byte(opcode, core):
	# 6xkk
	x, kk = get_x_kk(opcode)
	core.v[x] = kk
	core.next()


def ADD_Vx_Byte(opcode, core):
	# 7xkk - tested
	x, kk = get_x_kk(opcode)
	core.v[x], _ = add_byte(core.v[x], kk)
	core.next()

def LD_Vx_Vy(opcode, core):
	# 8xy0
	x, y = get_x_y(opcode)
	core.v[x] = core.v[y]
	core.next()

def OR_Vx_Vy(opcode, core):
	# 8xy1
	x, y = get_x_y(opcode)
	core.v[x] = or_byte(core.v[x], core.v[y])
	core.next()

def AND_Vx_Vy(opcode, core):
	# 8xy2
	x, y = get_x_y(opcode)
	core.v[x] = and_byte(core.v[x], core.v[y])
	core.next()

def XOR_Vx_Vy(opcode, core):
	# 8xy3
	x, y = get_x_y(opcode)
	core.v[x] = xor_byte(core.v[x], core.v[y])
	core.next()

def ADD_Vx_Vy(opcode, core):
	# 8xy4
	x, y = get_x_y(opcode)
	core.v[x], core.v[0xF] = add_byte(core.v[x], core.v[y])
	core.next()

def SUB_Vx_Vy(opcode, core):
	# 8xy5
	x, y = get_x_y(opcode)
	core.v[x], core.v[0xF] = sub_byte(core.v[x], core.v[y])
	core.next()

def SHR_Vx(opcode, core):
	# 8xy6
	x = get_x_kk(opcode)

	core.v[x], core.v[0xF] = shift_right(core.v[x])
	core.next()

def SUBN_Vx_Vy(opcode, core):
	# 8xy7
	x, y = get_x_y(opcode)

	core.v[x], core.v[0xF] = sub_byte(core.v[y], core.v[x])
	core.next()

def SHL_Vx(opcode, core):
	# 8xyE
	x = get_x_kk(opcode)

	core.v[x], core.v[0xF] = shift_left(core.v[x])
	core.next()


def SNE_Vx_Vy(opcode, core):
	# 9xy0
	x, y = get_x_y(opcode)

	if core.v[x] != core.v[y]:
		core.next()
	core.next()

def LD_I_ADDR(opcode, core):
	# Annn
	core.i = get_nnn(opcode)
	core.next()

def JP_V0_ADDR(opcode, core):
	# Bnnn
	nnn = get_nnn(opcode)
	core.pc = (nnn + core.v[0]) & 0xFFF

def RND_Vx_Byte(opcode, core):
	# Cxkk
	x, kk = get_x_kk(opcode)
	RND = randint(0, 255)
	core.v[x] = RND & kk
	core.next()

def DRW_Vx_Vy_N(opcode, core):
	# Dxyn
	x, y, n = get_x_y_n(opcode)

	core.v[0x0F] = 0

	x_cor = core.v[x]
	y_cor = core.v[y]

	for index in range(n):
		sprite = format(core.memory[core.i + index], '08b')
		x_cor = core.v[x]

		if y_cor >= core.H:
			y_cor = y_cor - core.H*int((y_cor/(core.H-1)))

		for j in sprite:

			if x_cor >= core.W:
				x_cor = x_cor - core.W*int((x_cor/(core.W-1)))

			if core.screen[y_cor][x_cor] == int(j):
				if core.screen[y_cor][x_cor]:
					core.v[0x0F] = 1
				core.screen[y_cor][x_cor] = 0
			else:
				core.screen[y_cor][x_cor] = 1
			x_cor = x_cor + 1
		y_cor = y_cor + 1

	core.next()


def SKP_Vx(opcode, core):
	#Ex9E
	x, _ = get_x_kk(opcode)

	if core.key[core.v[x]]:
		core.next()
	core.next()

def SKNP_Vx(opcode, core):
	#ExA1
	x, _ = get_x_kk(opcode)
	
	if not core.key[core.v[x]]:
		core.next()
	core.next()


def LD_Vx_DT(opcode, core):
	# Fx07
	x, _ = get_x_y(opcode)
	core.v[x] = core.dt
	core.next()

def LD_Vx_K(opcode, core):
	# Fx0a
	x, _ = get_x_y(opcode)

	for i in range(len(core.key)):
		if key[i]:
			core.v[x] = core.i
			core.next()
			break

def LD_DT_Vx(opcode, core):
	# Fx15
	x, _ = get_x_y(opcode)
	core.dt = core.v[x]
	core.next()

def LD_ST_Vx(opcode, core):
	# Fx18
	x, _ = get_x_y(opcode)
	core.st = core.v[x]
	core.next()

def ADD_I_Vx(opcode, core):
	# Fx1E - test
	x, _ = get_x_y(opcode)
	core.i = add_2byte(core.i, core.v[x])
	core.next()

def LD_F_Vx(opcode, core):
	# Fx29
	x, _ = get_x_y(opcode)
	core.i = core.v[x] * 5
	core.next()

def LD_B_Vx(opcode, core):
	# Fx33
	x, _ = get_x_y(opcode)
	TEN = int(core.v[x]/100)
	HUN = int(core.v[x]/10) - TEN*10
	DEC = core.v[x] - HUN*10 - TEN*100

	core.memory[core.i]     = TEN
	core.memory[core.i + 1] = HUN
	core.memory[core.i + 2] = DEC

	core.next()

def LD_I_Vx(opcode, core):
	# Fx55
	x, _ = get_x_y(opcode)
	for index in range(x + 1):
		core.memory[core.i + index] = core.v[index]

	core.next()

def LD_Vx_I(opcode, core):
	# Fx65
	x, _ = get_x_y(opcode)
	for index in range(x + 1):
		core.v[index] = core.memory[core.i + index]

	core.next()

# Index

inst_global = {
	0 : lambda opcode, core: inst_0[opcode & 0x00FF](opcode, core),
	1 : JP_ADDR,
	2 : CALL_ADDR,
	3 : SE_Vx_Byte,
	4 : SNE_Vx_Byte,
	5 : SE_Vx_Vy,
	6 : LD_Vx_Byte,
	7 : ADD_Vx_Byte,
	8 : lambda opcode, core: inst_8[opcode & 0x000F](opcode, core),
	9 : SNE_Vx_Vy,
	10: LD_I_ADDR,
	11: JP_V0_ADDR,
	12: RND_Vx_Byte,
	13: DRW_Vx_Vy_N,
	14: lambda opcode, core: inst_E[opcode & 0x00FF](opcode, core),
	15: lambda opcode, core: inst_F[opcode & 0x00FF](opcode, core)
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

def load_file(path, offset):
	with open(path, 'rb') as f:
		count = offset
		byte = f.read(1)
		while byte:
			memory[count] = int.from_bytes(byte, byteorder='little')
			byte = f.read(1)
			count = count + 1

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
