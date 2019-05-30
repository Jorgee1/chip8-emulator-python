from src.cpu import pointer, alu, loader, skip, grafics, jump, bit

class Chip8_Core(pointer.Pointer, alu.ALU, loader.Loader, skip.Skip, grafics.Grafics, jump.Jump, bit.Bit):

	W = 64
	H = 32
	START_PC = 512

	def __init__(self, *args, **kargs):
		self.memory = [0 for i in range(8*512)]
		self.V      = [0 for i in range(8*2)]
		self.I      = 0
		self.PC     = self.START_PC
		self.SP     = 0
		self.STACK  = [0 for i in range(8*2)]
		self.DT     = 0
		self.ST     = 0
		self.key    = [0 for i in range(8*2)]
		self.screen = [[0 for x in range(self.W)] for y in range(self.H)]

		self.load_font(kargs['font'])
		
		super(Chip8_Core, self).__init__()

	def load_font(self, path):
		with open(path, 'rb') as f:

			byte = f.read(1)
			count = 0
			while byte:
				data = int.from_bytes(byte, byteorder='little')
				if data:
					self.memory[count] = data
					byte = f.read(1)
					count = count + 1
				else:
					break

	def load_rom(self, path):
		with open(path, 'rb') as f:
			count = 512
			byte = f.read(1)
			while byte:
				self.memory[count] = int.from_bytes(byte, byteorder='little')
				byte = f.read(1)
				count = count + 1
		print('Last location:', count, 'Size', count - 512)


	def NOP(self, opcode):
		# 0000
		self.PC = self.PC + 2


	def run(self):
		opcode = self.memory[self.PC]<<8 | self.memory[self.PC+1]

		#print(hex(opcode))
		#input()
		self.run_opcode(opcode)