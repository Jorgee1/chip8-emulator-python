class Jump:

	def get_nnn(self, value):
		return value & 0x0FFF

	def RET(self, opcode):
		# 00EE
		self.SP = (self.SP - 1) & 0x000F
		self.PC = self.STACK[self.SP]
		self.STACK[self.SP] = 0
		self.PC = self.PC + 2

	def JP_ADDR(self, opcode):
		# 1nnn - Tested
		self.PC = self.get_nnn(opcode)

	def CALL_ADDR(self, opcode):
		# 2nnn
		self.STACK[self.SP] = self.PC
		self.SP = (self.SP + 1) & 0x000F
		self.PC = self.get_nnn(opcode)

	def JP_V0_ADDR(self, opcode):
		# Bnnn - Nunca se usa
		nnn = self.get_nnn(opcode)
		self.PC = (nnn + self.V[0]) & 0xFFF