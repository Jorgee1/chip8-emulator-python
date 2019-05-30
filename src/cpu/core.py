import unittest
from random import randint

class Chip8_Core:

	W = 64
	H = 32
	START_PC = 512

	def __init__(self, **kargs):
		self.memory = [0 for i in range(8*512)]
		self.V      = [0 for i in range(8*2)]
		self.I      = 0
		self.PC     = self.START_PC
		self.SP     = 0
		self.STACK  = [0 for i in range(8*2)]
		self.DT     = 0
		self.ST     = 0
		self.key    = [0 for i in range(8*2)]
		self.screen = [[0 for x in range(self.W)] for y in range(self.H)]

		self.load_font(kargs['font'])


	def load_font(self, path):
		with open(path, 'rb') as f:

			byte = f.read(1)
			count = 0
			while byte:
				data = int.from_bytes(byte, byteorder='little')
				if data:
					self.memory[count] = data
					byte = f.read(1)
					count = count + 1
				else:
					break

	def load_rom(self, path):
		with open(path, 'rb') as f:
			count = 512
			byte = f.read(1)
			while byte:
				self.memory[count] = int.from_bytes(byte, byteorder='little')
				byte = f.read(1)
				count = count + 1
		print('Last location:', count, 'Size', count - 512)

	def NOP(self, opcode):
		# 0000
		self.PC = self.PC + 2

	def CLS(self, opcode):
 		# 00E0
		for j in range(self.H):
			for i in range(self.W):
				self.screen[j][i] = 0
		self.PC += 2

	def RET(self, opcode):
		# 00EE
		self.SP = (self.SP - 1) & int('0x000F', 0)
		self.PC = self.STACK[self.SP]
		self.STACK[self.SP] = 0
		self.PC = self.PC + 2

	def JP_ADDR(self, opcode):
		# 1nnn - Tested
		self.PC = opcode & int('0x0FFF', 0)

	def CALL_ADDR(self, opcode):
		# 2nnn
		self.STACK[self.SP] = self.PC
		self.SP = (self.SP + 1) & int('0x000F', 0)
		self.PC = opcode & int('0x0FFF', 0)

	def SE_Vx_Byte(self, opcode):
		# 3xkk - Tested
		x = (opcode & int('0x0F00', 0)) >> 8
		kk = opcode & int('0x00FF', 0)

		if self.V[x] == kk:
			self.PC = self.PC +2
		self.PC = self.PC +2
		
	def SNE_Vx_Byte(self, opcode):
		# 4xkk - Tested
		x = (opcode & int('0x0F00', 0)) >> 8
		kk = opcode & int('0x00FF', 0)

		if self.V[x] != kk:
			self.PC = self.PC +2
		self.PC = self.PC +2

	def SE_Vx_Vy(self, opcode):
		# 5xy0 - test
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		if(self.V[x]==self.V[y]):
			self.PC = self.PC + 2
		self.PC = self.PC + 2

	def LD_Vx_Byte(self, opcode):
		# 6xkk
		kk = opcode & int('0x00FF', 0)
		x = (opcode & int('0x0F00', 0)) >> 8
		self.V[x] = kk
		self.PC = self.PC + 2

	def ADD_Vx_Byte(self, opcode):
		# 7xkk - tested
		x = (opcode & int('0x0F00', 0)) >> 8
		kk = opcode & int('0x00FF', 0)
		self.V[x] = (self.V[x] + kk) & int('0x00FF', 0)
		self.PC = self.PC + 2

	def LD_Vx_Vy(self, opcode):
		# 8xy0
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		self.V[x] = self.V[y]
		self.PC = self.PC + 2

	def OR_Vx_Vy(self, opcode):
		# 8xy1
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		self.V[x] = self.V[x] | self.V[y]
		self.PC = self.PC + 2

	def AND_Vx_Vy(self, opcode):
		# 8xy2 - tested
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		self.V[x] = self.V[x] & self.V[y]
		self.PC = self.PC + 2

	def XOR_Vx_Vy(self, opcode):
		# 8xy3
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		self.V[x] = self.V[x] ^ self.V[y]
		self.PC = self.PC + 2

	def ADD_Vx_Vy(self, opcode):
		# 8xy4
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		self.V[x] = self.V[x] + self.V[y]
		if self.V[x] > 256:
			self.V[int('0xF', 0)] = 1
		else:
			self.V[int('0xF', 0)] = 0
		self.V[x] = self.V[x] & int('0xFF',0)
		self.PC = self.PC + 2

	def SUB_Vx_Vy(self, opcode):
		# 8xy5
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4

		if self.V[x] > self.V[y]:
			self.V[int('0xF', 0)] = 1
		else:
			self.V[int('0xF', 0)] = 0
			
		if self.V[x] >= self.V[y]:
			self.V[x] = self.V[x] - self.V[y]
		else:
			self.V[x] = self.V[x] + ((~ self.V[y]) & int('0x00FF',0)) + 1
		self.PC = self.PC + 2

	def SHR_Vx(self, opcode):
		# 8xy6
		x = (opcode & int('0x0F00',0)) >> 8

		LSB = self.V[x] & int('0x0001',0)
		#Esto se puede reemplazar por
		#V[int('0xF', 0)] = LSB
		if LSB:
			self.V[int('0xF', 0)] = 1
		else:
			self.V[int('0xF', 0)] = 0

		# Esto se puede reemplazar por
		# V[x] = V[x] >> 1
		self.V[x] = int(self.V[x]/2)
		self.PC = self.PC + 2

	def SUBN_Vx_Vy(self, opcode):
		# 8xy7
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4

		if self.V[y] > self.V[x]:
			self.V[int('0xF', 0)] = 1
		else:
			self.V[int('0xF', 0)] = 0
			
		if self.V[y] >= self.V[x]:
			self.V[x] = self.V[y] - self.V[x]
		else:
			self.V[x] = self.V[y] + ((~ self.V[x]) & int('0x00FF',0)) + 1
		self.PC = self.PC + 2

	def SHL_Vx(self, opcode):
		# 8xyE
		x = (opcode & int('0x0F00',0)) >> 8

		# Esto se puede reemplazar por
		# V[int('0xF', 0)] = MSB
		MSB = (self.V[x] & int('0x8000',0)) >> 15
		if MSB:
			self.V[int('0xF', 0)] = 1
		else:
			self.V[int('0xF', 0)] = 0

		# Esto se puede reemplazar por
		# V[x] = V[x] << 1
		self.V[x] = self.V[x]*2
		self.PC = self.PC + 2

	def SNE_Vx_Vy(self, opcode):
		# 9xy0 - tested
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		if self.V[x] != self.V[y]:
			self.PC = self.PC + 2
		self.PC = self.PC + 2

	def LD_I_ADDR(self, opcode):
		#Annn
		self.I = opcode & int('0x0FFF', 0)
		self.PC = self.PC + 2

	def JP_V0_ADDR(self, opcode):
		# Bnnn Nunca se usa
		pass
		self.PC = self.PC + 2

	def RND_Vx_Byte(self, opcode):
		# Cxkk
		x = (opcode & int('0x0F00',0)) >> 8
		kk = opcode & int('0x00FF', 0)
		RND = randint(0, 255)
		self.V[x] = RND & kk
		self.PC = self.PC + 2

	def DRW_Vx_Vy_N(self, opcode):
		# Dxyn
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		n = opcode & int('0x000F',0)

		self.V[int('0x0F',0)] = 0

		x_cor = self.V[x]
		y_cor = self.V[y]
		for i in range(n):
			sprite = format(self.memory[self.I+i], '08b')
			x_cor = self.V[x]

			if (y_cor>=self.H):
				y_cor = y_cor - self.H*int((y_cor/(self.H-1)))

			for j in sprite:

				if ((x_cor)>=self.W):
					x_cor = x_cor - self.W*int((x_cor/(self.W-1)))

				if self.screen[y_cor][x_cor] == int(j):
					if self.screen[y_cor][x_cor]:
						self.V[int('0x0F',0)] = 1
					self.screen[y_cor][x_cor] = 0
				else:
					self.screen[y_cor][x_cor] = 1
				x_cor = x_cor + 1
			y_cor = y_cor + 1


		self.PC = self.PC + 2

	def SKP_Vx(self, opcode):
		#Ex9E
		x = (opcode & int('0x0F00', 0)) >> 8
		if self.key[self.V[x]]:
			self.PC = self.PC + 2
		self.PC = self.PC + 2

	def SKNP_Vx(self, opcode):
		#ExA1
		x = (opcode & int('0x0F00', 0)) >> 8
		if not self.key[self.V[x]]:
			self.PC = self.PC + 2
		self.PC = self.PC + 2

	def LD_Vx_DT(self, opcode):
		# Fx07
		x = (opcode & int('0x0F00', 0)) >> 8
		self.V[x] = self.DT
		self.PC = self.PC + 2

	def LD_Vx_K(self, opcode):
		# Fx0a
		x = (opcode & int('0x0F00', 0)) >> 8
		count = 0
		for i in self.key:
			if i:
				self.V[x] = count
				self.PC = self.PC + 2
				break
			count = count + 1

	def LD_DT_Vx(self, opcode):
		# Fx15
		x = (opcode & int('0x0F00', 0)) >> 8
		self.DT = self.V[x]
		self.PC = self.PC + 2

	def LD_ST_Vx(self, opcode):
		# Fx18
		x = (opcode & int('0x0F00', 0)) >> 8
		self.ST = self.V[x]
		self.PC = self.PC + 2

	def ADD_I_Vx(self, opcode):
		# Fx1E - test
		x = (opcode & int('0x0F00', 0)) >> 8
		self.I = (self.I + self.V[x]) & int('0xFFFF', 0)
		self.PC = self.PC + 2

	def LD_F_Vx(self, opcode):
		# Fx29
		x = (opcode & int('0x0F00', 0)) >> 8
		self.I = self.V[x]*5
		self.PC = self.PC + 2

	def LD_B_Vx(self, opcode):
		# Fx33
		x = (opcode & int('0x0F00', 0)) >> 8
		TEN = int(self.V[x]/100)
		HUN = int(self.V[x]/10) - TEN*10
		DEC = self.V[x] - HUN*10 - TEN*100
		self.memory[self.I]   = TEN
		self.memory[self.I+1] = HUN
		self.memory[self.I+2] = DEC
		self.PC = self.PC + 2

	def LD_I_Vx(self, opcode):
		# Fx55
		x = (opcode & int('0x0F00', 0)) >> 8
		for i in range(x+1):
			self.memory[self.I+i] = self.V[i]

		self.PC = self.PC + 2

	def LD_Vx_I(self, opcode):
		# Fx65
		x = (opcode & int('0x0F00', 0)) >> 8
		for i in range(x+1):
			self.V[i] = self.memory[self.I+i]

		self.PC = self.PC + 2



class Chip8_Pointer(Chip8_Core):
	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)

		self.inst_dic_global = {
			0: self.redirect_0,
			1: self.JP_ADDR,
			2: self.CALL_ADDR,
			3: self.SE_Vx_Byte,
			4: self.SNE_Vx_Byte,
			5: self.SE_Vx_Vy,
			6: self.LD_Vx_Byte,
			7: self.ADD_Vx_Byte,
			8: self.redirect_8,
			9: self.SNE_Vx_Vy,
			10:self.LD_I_ADDR,
			11:self.JP_V0_ADDR,
			12:self.RND_Vx_Byte,
			13:self.DRW_Vx_Vy_N,
			14:self.redirect_E,
			15:self.redirect_F
		}

		self.inst_dic_0 = {
			0: self.NOP,
			224: self.CLS,
			238: self. RET
		}

		self.inst_dic_8 = {
			0: self.LD_Vx_Vy,
			1: self.OR_Vx_Vy,
			2: self.AND_Vx_Vy,
			3: self.XOR_Vx_Vy,
			4: self.ADD_Vx_Vy,
			5: self.SUB_Vx_Vy,
			6: self.SHR_Vx,
			7: self.SUBN_Vx_Vy,
			14: self.SHL_Vx
		}

		self.inst_dic_E = {
			158: self.SKP_Vx,
			161: self.SKNP_Vx
		}

		self.inst_dic_F = {
			7: self.LD_Vx_DT,
			10: self.LD_Vx_K,
			21: self.LD_DT_Vx,
			24: self.LD_ST_Vx,
			30: self.ADD_I_Vx,
			41: self.LD_F_Vx,
			51: self.LD_B_Vx,
			85: self.LD_I_Vx,
			101: self.LD_Vx_I
		}

	def run_opcode(self, opcode):
		lead = opcode>>12
		self.inst_dic_global[lead](opcode)

		self.tic_timmer()

	def redirect_0(self, opcode):
		last = opcode & int('0x00FF', 0)
		self.inst_dic_0[last](opcode)

	def redirect_8(self, opcode):
		last = opcode & int('0x000F', 0)
		self.inst_dic_8[last](opcode)

	def redirect_E(self, opcode):
		last = opcode & int('0x00FF', 0)
		self.inst_dic_E[last](opcode)

	def redirect_F(self, opcode):
		last = opcode & int('0x00FF', 0)
		self.inst_dic_F[last](opcode)

	def tic_timmer(self):
		if self.DT:
			self.DT = self.DT - 1

		if self.ST:
			self.ST = self.ST - 1


class Test_Chip8_Core_Operation(unittest.TestCase):
	def setUp(self):

		self.chip8 = Chip8_Core()

	def test_JP_ADDR(self):
		expected = '123'
		instruction = '0x1' + expected
		self.chip8.JP_ADDR(int(instruction, 0))
		self.assertEqual(self.chip8.PC, int('0x0'+expected, 0), 'Unexpeted Address: ' + instruction)

	def test_ADD_Vx_Byte(self):
		x     = '5'
		kk    = '77'
		value = '45'
		instruction = '0x7' + x + kk

		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+value, 0)

		self.chip8.ADD_Vx_Byte(int(instruction, 0))
		self.assertEqual(self.chip8.V[int('0x0'+x, 0)], int('0x0BC', 0), 'Operation Error: ' + instruction)

	def test_AND_Vx_Vy(self):
		x     = '5'
		y     = '6'
		value = '45'
		instruction = '0x8' + x + y + '2'

		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+value, 0)
		self.chip8.V[int('0x0'+y, 0)] = int('0x0'+value, 0)

		self.chip8.ADD_Vx_Vy(int(instruction, 0))
		self.assertEqual(self.chip8.V[int('0x0'+x, 0)], int('0x08A', 0), 'Operation Error: ' + instruction)

	def test_ADD_I_Vx(self):
		x = '5'
		self.chip8.I = 90
		base_I = self.chip8.I
		value = 65530

		instruction = '0xF' + x + '1E'

		self.chip8.V[int('0x0'+x, 0)] = value

		self.chip8.ADD_I_Vx(int(instruction, 0))
		self.assertEqual(self.chip8.I, (base_I + value) & int('0xFFFF', 0), 'Operation Error: ' + instruction)

class Test_Chip8_Core_Comparision(unittest.TestCase):

	def setUp(self):

		self.chip8 = Chip8_Core()

	def test_SE_Vx_Byte_True(self):
		x  =  '5'
		kk = '45'
		instruction = '0x3'+x+kk

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+kk, 0)
		self.chip8.SE_Vx_Byte(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+4, 'Incorrect comparison')

	def test_SE_Vx_Byte_False(self):
		x  =  '5'
		kk = '44'
		instruction = '0x3'+x+'45'

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+kk, 0)
		self.chip8.SE_Vx_Byte(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+2, 'Incorrect comparison')


	def test_SNE_Vx_Byte_True(self):
		x  =  '5'
		kk = '44'
		instruction = '0x4'+x+'45'


		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+kk, 0)
		self.chip8.SNE_Vx_Byte(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+4, 'Incorrect comparison: '+instruction)

	def test_SNE_Vx_Byte_False(self):
		x  =  '5'
		kk = '45'
		instruction = '0x4'+x+kk

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+kk, 0)
		self.chip8.SNE_Vx_Byte(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+2, 'Incorrect comparison: ' + instruction)


	def test_SE_Vx_Vy_True(self):
		x = '5'
		y = '6'
		kk = '45'

		instruction = '0x5'+x+y+'0'

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+kk, 0)
		self.chip8.V[int('0x0'+y, 0)] = int('0x0'+kk, 0)

		self.chip8.SE_Vx_Vy(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+4, 'Incorrect comparison: ' + instruction)

	def test_SE_Vx_Vy_Fase(self):
		x = '5'
		y = '6'

		instruction = '0x5'+x+y+'0'

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+'44', 0)
		self.chip8.V[int('0x0'+y, 0)] = int('0x0'+'45', 0)

		self.chip8.SE_Vx_Vy(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+2, 'Incorrect comparison: ' + instruction)


	def test_SNE_Vx_Vy_True(self):
		x = '5'
		y = '6'
		kk = 'A4'

		instruction = '0x9'+x+y+'0'

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+kk, 0)
		self.chip8.V[int('0x0'+y, 0)] = int('0x0'+kk, 0)

		self.chip8.SNE_Vx_Vy(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+2, 'Incorrect comparison: ' + instruction)

	def test_SNE_Vx_Vy_Fase(self):
		x = '5'
		y = '6'

		instruction = '0x9'+x+y+'0'

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+'A5', 0)
		self.chip8.V[int('0x0'+y, 0)] = int('0x0'+'00', 0)

		self.chip8.SNE_Vx_Vy(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+4, 'Incorrect comparison: ' + instruction)



if __name__ == '__main__':
	unittest.main()