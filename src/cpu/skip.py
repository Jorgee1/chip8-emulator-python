class Skip:
	def SE_Vx_Byte(self, opcode):
		# 3xkk - Tested
		x = (opcode & int('0x0F00', 0)) >> 8
		kk = opcode & int('0x00FF', 0)

		if self.V[x] == kk:
			self.PC = self.PC +2
		self.PC = self.PC +2
		
	def SE_Vx_Vy(self, opcode):
		# 5xy0 - test
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		if(self.V[x]==self.V[y]):
			self.PC = self.PC + 2
		self.PC = self.PC + 2

	def SNE_Vx_Byte(self, opcode):
		# 4xkk - Tested
		x = (opcode & int('0x0F00', 0)) >> 8
		kk = opcode & int('0x00FF', 0)

		if self.V[x] != kk:
			self.PC = self.PC +2
		self.PC = self.PC +2

	def SNE_Vx_Vy(self, opcode):
		# 9xy0 - tested
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		if self.V[x] != self.V[y]:
			self.PC = self.PC + 2
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
