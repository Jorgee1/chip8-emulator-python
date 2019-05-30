class ALU:
	def ADD_Vx_Byte(self, opcode):
		# 7xkk - tested
		x = (opcode & int('0x0F00', 0)) >> 8
		kk = opcode & int('0x00FF', 0)
		self.V[x] = (self.V[x] + kk) & int('0x00FF', 0)
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

	def ADD_I_Vx(self, opcode):
		# Fx1E - test
		x = (opcode & int('0x0F00', 0)) >> 8
		self.I = (self.I + self.V[x]) & int('0xFFFF', 0)
		self.PC = self.PC + 2