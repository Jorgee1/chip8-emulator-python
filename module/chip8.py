from random import randint

# Utils

def get_x_y(byte):
    return (byte & 0x0F00) >> 8, (byte & 0x00F0) >> 4

def get_x_y_n(byte):
    return (byte & 0x0F00) >> 8, (byte & 0x00F0) >> 4, byte & 0x000F

def get_x_kk(byte):
    return (byte & 0x0F00) >> 8, byte & 0x00FF

def get_nnn(value):
    return value & 0x0FFF


def add_check_carry(value_1, value_2):
    return int((value_1 + value_2) > 0xFF)

def sub_check_carry(value_1, value_2):
    return int(value_1 > value_2)

def add_values_8bit(value_1, value_2):
    return (value_1 + value_2) & 0x00FF, add_check_carry(value_1, value_2)

def add_values_16bit(value_1, value_2):
    return (value_1 + value_2) & 0xFFFF

def sub_values(value_1, value_2):
    if value_1 >= value_2:
        return value_1 - value_2, sub_check_carry(value_1, value_2)
    else:
        return value_1 + ((~ value_2) & 0x00FF) + 1, sub_check_carry(value_1, value_2)

# Font

font = [
	0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
    0x20, 0x60, 0x20, 0x20, 0x70, # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
    0x90, 0x90, 0xF0, 0x10, 0x10, # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
    0xF0, 0x10, 0x20, 0x40, 0x40, # 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90, # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
    0xF0, 0x80, 0x80, 0x80, 0xF0, # C
    0xE0, 0x90, 0x90, 0x90, 0xE0, # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
    0xF0, 0x80, 0xF0, 0x80, 0x80  # F
]

# Chip8 Class
class Chip8:

    w = 64
    h = 32
    START_PC = 512

    def __init__(self):
        self.memory = [0 for i in range(8*512)]
        self.V      = [0 for i in range(8*2)]
        self.I      = 0
        self.PC     = self.START_PC
        self.SP     = 0
        self.STACK  = [0 for i in range(8*2)]
        self.DT     = 0
        self.ST     = 0
        self.key    = [0 for i in range(8*2)]
        self.screen = [[0 for x in range(self.w)] for y in range(self.h)]

        # Load Font
        for index, byte in enumerate(font):
            self.memory[index] = byte
        
        # Instructions addresing
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

    def _load_file(self, path, offset):
        with open(path, 'rb') as f:
            count = offset
            byte = f.read(1)
            while byte:
                self.memory[count] = int.from_bytes(byte, byteorder='little')
                byte = f.read(1)
                count = count + 1

    def load_rom(self, path):
        self._load_file(path, self.START_PC)

    def run(self):
        if not self.DT:
            opcode = (self.memory[self.PC] << 8) | self.memory[self.PC+1]
            self.inst_dic_global[opcode>>12](opcode)

        if self.ST:
            self.ST = self.ST - 1
        
        if self.DT:
            self.DT = self.DT - 1


    def redirect_0(self, opcode):
        self.inst_dic_0[opcode & 0x00FF](opcode)

    def redirect_8(self, opcode):
        self.inst_dic_8[opcode & 0x000F](opcode)

    def redirect_E(self, opcode):
        self.inst_dic_E[opcode & 0x00FF](opcode)

    def redirect_F(self, opcode):
        self.inst_dic_F[opcode & 0x00FF](opcode)

    ## Instructions

    def NOP(self, opcode):
        # 0000
        self.PC = self.PC + 2

    # Jump

    def RET(self, opcode):
        # 00EE
        self.SP = (self.SP - 1) & 0x000F
        self.PC = self.STACK[self.SP]
        self.STACK[self.SP] = 0
        self.PC = self.PC + 2

    def CALL_ADDR(self, opcode):
        # 2nnn
        self.STACK[self.SP] = self.PC
        self.SP = (self.SP + 1) & 0x000F
        self.PC = get_nnn(opcode)

    def JP_ADDR(self, opcode):
        # 1nnn - Tested
        self.PC = get_nnn(opcode)

    def JP_V0_ADDR(self, opcode):
        # Bnnn - Nunca se usa
        nnn = get_nnn(opcode)
        self.PC = (nnn + self.V[0]) & 0xFFF

    # Skip

    def SE_Vx_Byte(self, opcode):
        # 3xkk - Tested
        x, kk = get_x_kk(opcode)

        if self.V[x] == kk:
            self.PC = self.PC +2
        self.PC = self.PC +2
        
    def SE_Vx_Vy(self, opcode):
        # 5xy0 - test
        x, y = get_x_y(opcode)

        if(self.V[x]==self.V[y]):
            self.PC = self.PC + 2
        self.PC = self.PC + 2

    def SNE_Vx_Byte(self, opcode):
        # 4xkk - Tested
        x, kk = get_x_kk(opcode)

        if self.V[x] != kk:
            self.PC = self.PC +2
        self.PC = self.PC +2

    def SNE_Vx_Vy(self, opcode):
        # 9xy0 - tested
        x, y = get_x_y(opcode)

        if self.V[x] != self.V[y]:
            self.PC = self.PC + 2
        self.PC = self.PC + 2

    def SKP_Vx(self, opcode):
        #Ex9E
        x, _ = get_x_kk(opcode)

        if self.key[self.V[x]]:
            self.PC = self.PC + 2
        self.PC = self.PC + 2

    def SKNP_Vx(self, opcode):
        #ExA1
        x, _ = get_x_kk(opcode)
        
        if not self.key[self.V[x]]:
            self.PC = self.PC + 2
        self.PC = self.PC + 2

    # Loader

    def LD_Vx_Byte(self, opcode):
        # 6xkk
        x, kk = get_x_kk(opcode)
        self.V[x] = kk
        self.PC = self.PC + 2

    def LD_Vx_Vy(self, opcode):
        # 8xy0
        x, y = get_x_y(opcode)
        self.V[x] = self.V[y]
        self.PC = self.PC + 2

    def LD_Vx_DT(self, opcode):
        # Fx07
        x, _ = get_x_y(opcode)
        self.V[x] = self.DT
        self.PC = self.PC + 2

    def LD_Vx_K(self, opcode):
        # Fx0a
        x, _ = get_x_y(opcode)

        for i in range(len(self.key)):
            if self.key[i]:
                self.V[x] = i
                self.PC = self.PC + 2
                break

    def LD_DT_Vx(self, opcode):
        # Fx15
        x, _ = get_x_y(opcode)
        self.DT = self.V[x]
        self.PC = self.PC + 2

    def LD_ST_Vx(self, opcode):
        # Fx18
        x, _ = get_x_y(opcode)
        self.ST = self.V[x]
        self.PC = self.PC + 2

    def LD_F_Vx(self, opcode):
        # Fx29
        x, _ = get_x_y(opcode)
        self.I = self.V[x]*5
        self.PC = self.PC + 2

    def LD_B_Vx(self, opcode):
        # Fx33
        x, _ = get_x_y(opcode)
        TEN = int(self.V[x]/100)
        HUN = int(self.V[x]/10) - TEN*10
        DEC = self.V[x] - HUN*10 - TEN*100
        self.memory[self.I]   = TEN
        self.memory[self.I+1] = HUN
        self.memory[self.I+2] = DEC
        self.PC = self.PC + 2

    def LD_I_Vx(self, opcode):
        # Fx55
        x, _ = get_x_y(opcode)
        for i in range(x+1):
            self.memory[self.I+i] = self.V[i]

        self.PC = self.PC + 2

    def LD_Vx_I(self, opcode):
        # Fx65
        x, _ = get_x_y(opcode)
        for i in range(x+1):
            self.V[i] = self.memory[self.I+i]

        self.PC = self.PC + 2

    def LD_I_ADDR(self, opcode):
        #Annn
        self.I = opcode & 0x0FFF
        self.PC = self.PC + 2

    def RND_Vx_Byte(self, opcode):
        # Cxkk
        x, kk = get_x_kk(opcode)
        RND = randint(0, 255)
        self.V[x] = RND & kk
        self.PC = self.PC + 2

    # Grafics
    def CLS(self, opcode):
        # 00E0
        for j in range(self.h):
            for i in range(self.w):
                self.screen[j][i] = 0
        self.PC += 2

    def DRW_Vx_Vy_N(self, opcode):
        x, y, n = get_x_y_n(opcode)

        self.V[0x0F] = 0

        x_cor = self.V[x]
        y_cor = self.V[y]
        for i in range(n):
            sprite = format(self.memory[self.I+i], '08b')
            x_cor = self.V[x]

            if (y_cor>=self.h):
                y_cor = y_cor - self.h*int((y_cor/(self.h-1)))

            for j in sprite:

                if ((x_cor)>=self.w):
                    x_cor = x_cor - self.w*int((x_cor/(self.w-1)))

                if self.screen[y_cor][x_cor] == int(j):
                    if self.screen[y_cor][x_cor]:
                        self.V[0x0F] = 1
                    self.screen[y_cor][x_cor] = 0
                else:
                    self.screen[y_cor][x_cor] = 1
                x_cor = x_cor + 1
            y_cor = y_cor + 1

        self.PC = self.PC + 2

    # Bit

    def SHR_Vx(self, opcode):
        # 8xy6
        x = get_x_kk(opcode)

        self.V[0xF] = self.V[x] & 0x01
        self.V[x]   = self.V[x] >> 1
        self.PC     = self.PC + 2


    def SHL_Vx(self, opcode):
        # 8xyE
        x = get_x_kk(opcode)

        self.V[0xF] = (self.V[x] & 0x80) >> 7
        self.V[x]   = self.V[x] << 1
        self.PC     = self.PC + 2

    # ALU


    # ADD
    def ADD_Vx_Byte(self, opcode):
        # 7xkk - tested
        x, kk = get_x_kk(opcode)
        self.V[x], _ = add_values_8bit(self.V[x], kk)
        self.PC += 2

    def ADD_I_Vx(self, opcode):
        # Fx1E - test
        x, _ = get_x_y(opcode)
        self.I = add_values_16bit(self.I, self.V[x])
        self.PC += 2

    def ADD_Vx_Vy(self, opcode):
        # 8xy4
        x, y = get_x_y(opcode)
        self.V[x], self.V[0xF] = add_values_8bit(self.V[x], self.V[y])
        self.PC += 2


    # SUB
    def SUB_Vx_Vy(self, opcode):
        # 8xy5
        x, y = get_x_y(opcode)
        self.V[x], self.V[0xF] = sub_values(self.V[x], self.V[y])
        self.PC += 2

    def SUBN_Vx_Vy(self, opcode):
        # 8xy7
        x, y = get_x_y(opcode)
        self.V[x], self.V[0xF] = sub_values(self.V[y], self.V[x])
        self.PC += 2


    # Logical Operations
    def AND_Vx_Vy(self, opcode):
        # 8xy2 - tested
        x, y = get_x_y(opcode)
        self.V[x] = self.V[x] & self.V[y]
        self.PC += 2

    def OR_Vx_Vy(self, opcode):
        # 8xy1
        x, y = get_x_y(opcode)
        self.V[x] = self.V[x] | self.V[y]
        self.PC += 2

    def XOR_Vx_Vy(self, opcode):
        # 8xy3
        x, y = get_x_y(opcode)
        self.V[x] = self.V[x] ^ self.V[y]
        self.PC += 2


