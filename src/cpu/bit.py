class Bit:
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