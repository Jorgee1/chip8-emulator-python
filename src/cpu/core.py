from src.cpu import pointer, alu, loader, skip, grafics, jump, bit

class Chip8_Core(
		pointer.Pointer,
		alu.ALU,
		loader.Loader,
		skip.Skip,
		grafics.Grafics,
		jump.Jump,
		bit.Bit
	):

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

	# Utils functions

	def load_file(self, path, offset):
		with open(path, 'rb') as f:
			count = offset
			byte = f.read(1)
			while byte:
				self.memory[count] = int.from_bytes(byte, byteorder='little')
				byte = f.read(1)
				count = count + 1

	def load_font(self, path):
		self.load_file(path, 0)

	def load_rom(self, path):
		self.load_file(path, self.START_PC)

	def get_x_y(self, byte):
		return (byte & 0x0F00) >> 8, (byte & 0x00F0) >> 4

	def get_x_kk(self, byte):
		return (byte & 0x0F00) >> 8, byte & 0x00FF

	def run(self):
		opcode = (self.memory[self.PC] << 8) | self.memory[self.PC+1]
		self.run_opcode(opcode)

	# Instructions
	
	def NOP(self, opcode):
		# 0000
		self.PC = self.PC + 2

