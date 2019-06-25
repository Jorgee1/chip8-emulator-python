class Skip:
	def SE_Vx_Byte(self, opcode):
		# 3xkk - Tested
		x, kk = self.get_x_kk(opcode)

		if self.V[x] == kk:
			self.PC = self.PC +2
		self.PC = self.PC +2
		
	def SE_Vx_Vy(self, opcode):
		# 5xy0 - test
		x, y = self.get_x_y(opcode)

		if(self.V[x]==self.V[y]):
			self.PC = self.PC + 2
		self.PC = self.PC + 2

	def SNE_Vx_Byte(self, opcode):
		# 4xkk - Tested
		x, kk = self.get_x_kk(opcode)

		if self.V[x] != kk:
			self.PC = self.PC +2
		self.PC = self.PC +2

	def SNE_Vx_Vy(self, opcode):
		# 9xy0 - tested
		x, y = self.get_x_y(opcode)

		if self.V[x] != self.V[y]:
			self.PC = self.PC + 2
		self.PC = self.PC + 2

	def SKP_Vx(self, opcode):
		#Ex9E
		x, _ = self.get_x_kk(opcode)

		if self.key[self.V[x]]:
			self.PC = self.PC + 2
		self.PC = self.PC + 2

	def SKNP_Vx(self, opcode):
		#ExA1
		x, _ = self.get_x_kk(opcode)
		
		if not self.key[self.V[x]]:
			self.PC = self.PC + 2
		self.PC = self.PC + 2
