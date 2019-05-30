class Pointer:
	def __init__(self):
		self.inst_dic_global = {
			0 : self.redirect_0,
			1 : self.JP_ADDR,
			2 : self.CALL_ADDR,
			3 : self.SE_Vx_Byte,
			4 : self.SNE_Vx_Byte,
			5 : self.SE_Vx_Vy,
			6 : self.LD_Vx_Byte,
			7 : self.ADD_Vx_Byte,
			8 : self.redirect_8,
			9 : self.SNE_Vx_Vy,
			10: self.LD_I_ADDR,
			11: self.JP_V0_ADDR,
			12: self.RND_Vx_Byte,
			13: self.DRW_Vx_Vy_N,
			14: self.redirect_E,
			15: self.redirect_F
		}

		self.inst_dic_0 = {
			0  : self.NOP,
			224: self.CLS,
			238: self. RET
		}

		self.inst_dic_8 = {
			0 : self.LD_Vx_Vy,
			1 : self.OR_Vx_Vy,
			2 : self.AND_Vx_Vy,
			3 : self.XOR_Vx_Vy,
			4 : self.ADD_Vx_Vy,
			5 : self.SUB_Vx_Vy,
			6 : self.SHR_Vx,
			7 : self.SUBN_Vx_Vy,
			14: self.SHL_Vx
		}

		self.inst_dic_E = {
			158: self.SKP_Vx,
			161: self.SKNP_Vx
		}

		self.inst_dic_F = {
			7  : self.LD_Vx_DT,
			10 : self.LD_Vx_K,
			21 : self.LD_DT_Vx,
			24 : self.LD_ST_Vx,
			30 : self.ADD_I_Vx,
			41 : self.LD_F_Vx,
			51 : self.LD_B_Vx,
			85 : self.LD_I_Vx,
			101: self.LD_Vx_I
		}

	def run_opcode(self, opcode):
		self.inst_dic_global[opcode>>12](opcode)

		self.tic_timmer()

	def redirect_0(self, opcode):
		self.inst_dic_0[opcode & 0x00FF](opcode)

	def redirect_8(self, opcode):
		self.inst_dic_8[opcode & 0x000F](opcode)

	def redirect_E(self, opcode):
		self.inst_dic_E[opcode & 0x00FF](opcode)

	def redirect_F(self, opcode):
		self.inst_dic_F[opcode & 0x00FF](opcode)

	def tic_timmer(self):
		if self.DT:
			self.DT = self.DT - 1

		if self.ST:
			self.ST = self.ST - 1