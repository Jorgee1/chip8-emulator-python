class Bit:
	def SHR_Vx(self, opcode):
		# 8xy6
		x = self.get_x_kk(opcode)

		self.V[0xF] = self.V[x] & 0x01
		self.V[x]   = self.V[x] >> 1
		self.PC     = self.PC + 2


	def SHL_Vx(self, opcode):
		# 8xyE
		x = self.get_x_kk(opcode)

		self.V[0xF] = (self.V[x] & 0x80) >> 7
		self.V[x]   = self.V[x] << 1
		self.PC     = self.PC + 2