class ALU:

	def __add_values_8bit(self, value_1, value_2):
		return (value_1 + value_2) & 0x00FF, self.__add_check_carry(value_1, value_2)

	def __add_values_16bit(self, value_1, value_2):
		return (value_1 + value_2) & 0xFFFF

	def __add_check_carry(self, value_1, value_2):
		if (value_1 + value_2) > 0xFF:
			return 1
		else:
			return 0

	def __sub_values(self, value_1, value_2):
		if value_1 >= value_2:
			return value_1 - value_2, self.__sub_check_carry(value_1, value_2)
		else:
			return value_1 + ((~ value_2) & 0x00FF) + 1, self.__sub_check_carry(value_1, value_2)

	def __sub_check_carry(self, value_1, value_2):
		if value_1 > value_2:
			return 1
		else:
			return 0


	# ADD
	def ADD_Vx_Byte(self, opcode):
		# 7xkk - tested
		x, kk = self.get_x_kk(opcode)

		self.V[x], _ = self.__add_values_8bit(self.V[x], kk)
		self.PC += 2

	def ADD_I_Vx(self, opcode):
		# Fx1E - test
		x, _ = self.get_x_y(opcode)

		self.I = self.__add_values_16bit(self.I, self.V[x])
		self.PC += 2

	def ADD_Vx_Vy(self, opcode):
		# 8xy4
		x, y = self.get_x_y(opcode)
		self.V[x], self.V[0xF] = self.__add_values_8bit(self.V[x], self.V[y])
		self.PC += 2


	# SUB
	def SUB_Vx_Vy(self, opcode):
		# 8xy5
		x, y = self.get_x_y(opcode)
		self.V[x], self.V[0xF] = self.__sub_values(self.V[x], self.V[y])
		self.PC += 2

	def SUBN_Vx_Vy(self, opcode):
		# 8xy7
		x, y = self.get_x_y(opcode)
		self.V[x], self.V[0xF] = self.__sub_values(self.V[y], self.V[x])
		self.PC += 2


	# Logical Operations
	def AND_Vx_Vy(self, opcode):
		# 8xy2 - tested
		x, y = self.get_x_y(opcode)
		self.V[x] = self.V[x] & self.V[y]
		self.PC += 2

	def OR_Vx_Vy(self, opcode):
		# 8xy1
		x, y = self.get_x_y(opcode)
		self.V[x] = self.V[x] | self.V[y]
		self.PC += 2

	def XOR_Vx_Vy(self, opcode):
		# 8xy3
		x, y = self.get_x_y(opcode)
		self.V[x] = self.V[x] ^ self.V[y]
		self.PC += 2




