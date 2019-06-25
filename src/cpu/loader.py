from random import randint

class Loader:
	def LD_Vx_Byte(self, opcode):
		# 6xkk
		x, kk = self.get_x_kk(opcode)
		self.V[x] = kk
		self.PC = self.PC + 2

	def LD_Vx_Vy(self, opcode):
		# 8xy0
		x, y = self.get_x_y(opcode)
		self.V[x] = self.V[y]
		self.PC = self.PC + 2

	def LD_Vx_DT(self, opcode):
		# Fx07
		x, _ = self.get_x_y(opcode)
		self.V[x] = self.DT
		self.PC = self.PC + 2

	def LD_Vx_K(self, opcode):
		# Fx0a
		x, _ = self.get_x_y(opcode)

		for i in range(len(self.key)):
			if self.key[i]:
				self.V[x] = i
				self.PC = self.PC + 2
				break


	def LD_DT_Vx(self, opcode):
		# Fx15
		x, _ = self.get_x_y(opcode)
		self.DT = self.V[x]
		self.PC = self.PC + 2

	def LD_ST_Vx(self, opcode):
		# Fx18
		x, _ = self.get_x_y(opcode)
		self.ST = self.V[x]
		self.PC = self.PC + 2

	def LD_F_Vx(self, opcode):
		# Fx29
		x, _ = self.get_x_y(opcode)
		self.I = self.V[x]*5
		self.PC = self.PC + 2

	def LD_B_Vx(self, opcode):
		# Fx33
		x, _ = self.get_x_y(opcode)
		TEN = int(self.V[x]/100)
		HUN = int(self.V[x]/10) - TEN*10
		DEC = self.V[x] - HUN*10 - TEN*100
		self.memory[self.I]   = TEN
		self.memory[self.I+1] = HUN
		self.memory[self.I+2] = DEC
		self.PC = self.PC + 2

	def LD_I_Vx(self, opcode):
		# Fx55
		x, _ = self.get_x_y(opcode)
		for i in range(x+1):
			self.memory[self.I+i] = self.V[i]

		self.PC = self.PC + 2

	def LD_Vx_I(self, opcode):
		# Fx65
		x, _ = self.get_x_y(opcode)
		for i in range(x+1):
			self.V[i] = self.memory[self.I+i]

		self.PC = self.PC + 2

	def LD_I_ADDR(self, opcode):
		#Annn
		self.I = opcode & 0x0FFF
		self.PC = self.PC + 2

	def RND_Vx_Byte(self, opcode):
		# Cxkk
		x, kk = self.get_x_kk(opcode)
		RND = randint(0, 255)
		self.V[x] = RND & kk
		self.PC = self.PC + 2
