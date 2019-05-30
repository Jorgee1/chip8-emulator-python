class Jump:
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

	def JP_V0_ADDR(self, opcode):
		# Bnnn Nunca se usa
		pass
		self.PC = self.PC + 2