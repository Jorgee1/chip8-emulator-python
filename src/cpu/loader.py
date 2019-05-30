from random import randint

class Loader:
	def LD_Vx_Byte(self, opcode):
		# 6xkk
		kk = opcode & int('0x00FF', 0)
		x = (opcode & int('0x0F00', 0)) >> 8
		self.V[x] = kk
		self.PC = self.PC + 2

	def LD_Vx_Vy(self, opcode):
		# 8xy0
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		self.V[x] = self.V[y]
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

	def LD_I_ADDR(self, opcode):
		#Annn
		self.I = opcode & int('0x0FFF', 0)
		self.PC = self.PC + 2

	def RND_Vx_Byte(self, opcode):
		# Cxkk
		x = (opcode & int('0x0F00',0)) >> 8
		kk = opcode & int('0x00FF', 0)
		RND = randint(0, 255)
		self.V[x] = RND & kk
		self.PC = self.PC + 2
