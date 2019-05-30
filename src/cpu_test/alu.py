import unittest
from src.cpu import core

def run():
	class Test_Chip8_ALU_Operation(unittest.TestCase):
		def setUp(self):
			self.chip8 = core.Chip8_Core()

		def test_ADD_Vx_Byte_1(self):
			x = 1
			kk = 10
			self.V[x] = 10
			opcode = 0x7000 + x + kk

			self.chip8.ADD_Vx_Byte(opcode)

			self.assertEqual(V[x], 20, 'ALU error')



	unittest.main()