class Grafics:
	def CLS(self, opcode):
 		# 00E0
		for j in range(self.H):
			for i in range(self.W):
				self.screen[j][i] = 0
		self.PC += 2

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