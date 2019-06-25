import unittest
from src.cpu import core

class Test_Chip8_Core_Operation(unittest.TestCase):
	def setUp(self):

		self.chip8 = core.Chip8_Core()

	def test_JP_ADDR(self):
		expected = '123'
		instruction = '0x1' + expected
		self.chip8.JP_ADDR(int(instruction, 0))
		self.assertEqual(self.chip8.PC, int('0x0'+expected, 0), 'Unexpeted Address: ' + instruction)

	def test_ADD_Vx_Byte(self):
		x     = '5'
		kk    = '77'
		value = '45'
		instruction = '0x7' + x + kk

		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+value, 0)

		self.chip8.ADD_Vx_Byte(int(instruction, 0))
		self.assertEqual(self.chip8.V[int('0x0'+x, 0)], int('0x0BC', 0), 'Operation Error: ' + instruction)

	def test_AND_Vx_Vy(self):
		x     = '5'
		y     = '6'
		value = '45'
		instruction = '0x8' + x + y + '2'

		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+value, 0)
		self.chip8.V[int('0x0'+y, 0)] = int('0x0'+value, 0)

		self.chip8.ADD_Vx_Vy(int(instruction, 0))
		self.assertEqual(self.chip8.V[int('0x0'+x, 0)], int('0x08A', 0), 'Operation Error: ' + instruction)

	def test_ADD_I_Vx(self):
		x = '5'
		self.chip8.I = 90
		base_I = self.chip8.I
		value = 65530

		instruction = '0xF' + x + '1E'

		self.chip8.V[int('0x0'+x, 0)] = value

		self.chip8.ADD_I_Vx(int(instruction, 0))
		self.assertEqual(self.chip8.I, (base_I + value) & int('0xFFFF', 0), 'Operation Error: ' + instruction)

class Test_Chip8_Core_Comparision(unittest.TestCase):

	def setUp(self):

		self.chip8 = core.Chip8_Core()

	def test_SE_Vx_Byte_True(self):
		x  =  '5'
		kk = '45'
		instruction = '0x3'+x+kk

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+kk, 0)
		self.chip8.SE_Vx_Byte(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+4, 'Incorrect comparison')

	def test_SE_Vx_Byte_False(self):
		x  =  '5'
		kk = '44'
		instruction = '0x3'+x+'45'

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+kk, 0)
		self.chip8.SE_Vx_Byte(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+2, 'Incorrect comparison')


	def test_SNE_Vx_Byte_True(self):
		x  =  '5'
		kk = '44'
		instruction = '0x4'+x+'45'


		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+kk, 0)
		self.chip8.SNE_Vx_Byte(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+4, 'Incorrect comparison: '+instruction)

	def test_SNE_Vx_Byte_False(self):
		x  =  '5'
		kk = '45'
		instruction = '0x4'+x+kk

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+kk, 0)
		self.chip8.SNE_Vx_Byte(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+2, 'Incorrect comparison: ' + instruction)


	def test_SE_Vx_Vy_True(self):
		x = '5'
		y = '6'
		kk = '45'

		instruction = '0x5'+x+y+'0'

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+kk, 0)
		self.chip8.V[int('0x0'+y, 0)] = int('0x0'+kk, 0)

		self.chip8.SE_Vx_Vy(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+4, 'Incorrect comparison: ' + instruction)

	def test_SE_Vx_Vy_Fase(self):
		x = '5'
		y = '6'

		instruction = '0x5'+x+y+'0'

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+'44', 0)
		self.chip8.V[int('0x0'+y, 0)] = int('0x0'+'45', 0)

		self.chip8.SE_Vx_Vy(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+2, 'Incorrect comparison: ' + instruction)


	def test_SNE_Vx_Vy_True(self):
		x = '5'
		y = '6'
		kk = 'A4'

		instruction = '0x9'+x+y+'0'

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+kk, 0)
		self.chip8.V[int('0x0'+y, 0)] = int('0x0'+kk, 0)

		self.chip8.SNE_Vx_Vy(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+2, 'Incorrect comparison: ' + instruction)

	def test_SNE_Vx_Vy_Fase(self):
		x = '5'
		y = '6'

		instruction = '0x9'+x+y+'0'

		# Set UP
		base_PC = self.chip8.PC
		self.chip8.V[int('0x0'+x, 0)] = int('0x0'+'A5', 0)
		self.chip8.V[int('0x0'+y, 0)] = int('0x0'+'00', 0)

		self.chip8.SNE_Vx_Vy(int(instruction, 0))

		# Run test
		self.assertEqual(self.chip8.PC, base_PC+4, 'Incorrect comparison: ' + instruction)



if __name__ == '__main__':
	unittest.main()