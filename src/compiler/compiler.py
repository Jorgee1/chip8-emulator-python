import binascii
import re

class Compiler:
	num_match = '[0-9a-f]'
	output_folder = 'Out'

	def __init__(self):
		self.tokens = {
			"CLS" : self.CLS,  "RET": self.RET, "JP"  : self.JP,   "NOP" : self.NOP,
			"CALL": self.CALL, "SE" : self.SE,  "SNE" : self.SNE,  "LD"  : self.LD,
			"ADD" : self.ADD,  "OR" : self.OR,  "AND" : self.AND,  "XOR" : self.XOR,
			"SUB" : self.SUB,  "SHR": self.SHR, "SUBN": self.SUBN, "SHL" : self.SHL,
			"RND" : self.RND,  "DRW": self.DRW, "SKP" : self.SKP,  "SKNP": self.SKNP,
		}

	def compile(self, cmd):
		words = cmd.split(' ', 1)

		token = words[0]
		parms = ''
		

		if len(words) > 1:
			token = words[0]
			parms = words[1]



		print("Token  :", token, parms)


		out = self.tokens[token](parms)
		print(hex(int.from_bytes(out, byteorder='little')))

		return out



	def type_addr(self, code, cmd):
		addr = re.search(self.num_match+'{3}', cmd).group(0)
		return code+addr


	def NOP(self, cmd):

		return binascii.unhexlify('0000')

	def CLS(self, cmd):

		return binascii.unhexlify('00E0')

	def RET(self, cmd):

		return binascii.unhexlify('00EE')

	def JP(self, cmd):
		"""
			JP addr     -> JP 0xNNN
			JP V0, addr -> JP VX, 0xNNN
		"""
		single_word = re.match(r'^0x[0-9a-fA-F]{3}', cmd)
		v_parm = re.match(r'^V[0-9a-fA-F], 0x[0-9a-fA-F]{3}', cmd)

		if single_word:
			addr = single_word.group(0).replace('0x','')
			return binascii.unhexlify('1'+addr)

		return binascii.unhexlify('0000')

	def CALL(self, cmd):
		single_word = re.match(r'^0x[0-9a-fA-F]{3}', cmd)

		if single_word:
			addr = single_word.group(0).replace('0x','')
			return binascii.unhexlify('2'+addr)

		return binascii.unhexlify('0000')

	def SE(self, cmd):

		return binascii.unhexlify('0000')

	def SNE(self, cmd):

		return binascii.unhexlify('0000')

	def LD(self, cmd):

		return binascii.unhexlify('0000')

	def ADD(self, cmd):

		return binascii.unhexlify('0000')

	def OR(self, cmd):

		return binascii.unhexlify('0000')

	def AND(self, cmd):

		return binascii.unhexlify('0000')

	def XOR(self, cmd):

		return binascii.unhexlify('0000')

	def SUB(self, cmd):

		return binascii.unhexlify('0000')

	def SHR(self, cmd):

		return binascii.unhexlify('0000')

	def SUBN(self, cmd):

		return binascii.unhexlify('0000')

	def SHL(self, cmd):

		return binascii.unhexlify('0000')

	def RND(self, cmd):

		return binascii.unhexlify('0000')

	def DRW(self, cmd):

		return binascii.unhexlify('0000')

	def SKP(self, cmd):

		return binascii.unhexlify('0000')

	def SKNP(self, cmd):

		return binascii.unhexlify('0000')
