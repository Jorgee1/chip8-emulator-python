from random import randint
import pygame
import sys
# to hex -> hex()
# to bin -> bin()
# 1 byte = 8 bit
# 1 char = 4 bit

black = (0,0,0)
white = (255,255,255)
W = 64
H = 32
upScale = 10

test = [0]*16

def byte_to_int(byte):
	return int.from_bytes(byte, byteorder='little')

memory = [0]*4096
V = [0]*16     #  8 bit
I = 0          # 16 bit
PC = 512       # 16 bit
SP = 0         #  8 bit
STACK = [0]*16 # 16 bit
DT = 0         # Delay timer
ST = 0         #Sound timer
screen = [[0 for x in range(W)] for y in range(H)]
key = [0]*16

# load font
with open('FONT', 'rb') as f:
	byte = f.read(1)
	count = 0
	while byte:
		data = byte_to_int(byte)
		if data:
			memory[count] = data
			byte = f.read(1)
			count = count + 1
		else:
			break

# load rom
if len(sys.argv)>=2:
	game = sys.argv[1]
else:
	print("No file selected")
	exit()

with open(game, 'rb') as f:
	count = 512
	byte = f.read(1)
	while byte:
		memory[count] = byte_to_int(byte)
		byte = f.read(1)
		count = count + 1

print('Last location:', count, 'Size', count - 512)
sw = True


pygame.init()
gameDisplay = pygame.display.set_mode((W*upScale + 400,H*upScale))
pygame.display.set_caption('Chip 8')
clock = pygame.time.Clock()
gameDisplay.fill(black)
font = pygame.font.Font('Lekton-Regular.ttf', 15)
controls = [
	pygame.K_KP0,
	pygame.K_KP1,
	pygame.K_KP2,
	pygame.K_KP3,
	pygame.K_KP4,
	pygame.K_KP5,
	pygame.K_KP6,
	pygame.K_KP7,
	pygame.K_KP8,
	pygame.K_KP9,
	pygame.K_a,
	pygame.K_b,
	pygame.K_c,
	pygame.K_d,
	pygame.K_e,
	pygame.K_f,
]

# game cycle
while(sw):
	opcode = memory[PC]<<8 | memory[PC+1]
	lead = opcode>>12
	#print('OPCODE:', hex(opcode), '- First char:', hex(lead))

	# core
	if lead == int('0x0', 0):
		last = opcode & int('0x00FF', 0)
		if last == int('0xEE', 0):
			SP = SP - 1
			PC = STACK[SP]
			STACK[SP] = 0
		elif last == int('0xE0', 0):
			for j in range(32):
				for i in range(64):
					screen[j][i] = 0
		elif last == int('0x00', 0):
			# NOP
			pass
		else:
			sw = False
			print('Not programed', hex(opcode))
		PC = PC + 2

	elif lead == int('0x1', 0):
		location = opcode & int('0x0FFF', 0)
		PC = location
	elif lead == int('0x2', 0):
		location = opcode & int('0x0FFF', 0)
		STACK[SP] = PC
		SP = SP + 1
		PC = location
	elif lead == int('0x3', 0):
		x = (opcode & int('0x0F00', 0)) >> 8
		kk = opcode & int('0x00FF', 0)
		if V[x] == kk:
			PC = PC +2
		PC = PC +2
	elif lead == int('0x4', 0):
		x = (opcode & int('0x0F00', 0)) >> 8
		kk = opcode & int('0x00FF', 0)

		if V[x] != kk:
			PC = PC +2
		PC = PC +2
	elif lead == int('0x5', 0):
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		if(V[x]==V[y]):
			PC = PC + 2
		PC = PC + 2
	elif lead == int('0x6', 0):
		kk = opcode & int('0x00FF', 0)
		x = (opcode & int('0x0F00', 0)) >> 8
		V[x] = kk
		PC = PC + 2
	elif lead == int('0x7', 0):
		x = (opcode & int('0x0F00', 0)) >> 8
		kk = opcode & int('0x00FF', 0)
		V[x] = (V[x] + kk) & int('0x00FF', 0)
		PC = PC + 2
	elif lead == int('0x8', 0):
		last = opcode & int('0x000F', 0)
		if last == int('0x0', 0):
			x = (opcode & int('0x0F00',0)) >> 8
			y = (opcode & int('0x00F0',0)) >> 4
			V[x] = V[y]
			PC = PC + 2
		elif last == int('0x1', 0):
			x = (opcode & int('0x0F00',0)) >> 8
			y = (opcode & int('0x00F0',0)) >> 4
			V[x] = V[x] | V[y]
			PC = PC + 2
		elif last == int('0x2', 0):
			x = (opcode & int('0x0F00',0)) >> 8
			y = (opcode & int('0x00F0',0)) >> 4
			V[x] = V[x] & V[y]
			PC = PC + 2
		elif last == int('0x3', 0):
			x = (opcode & int('0x0F00',0)) >> 8
			y = (opcode & int('0x00F0',0)) >> 4
			V[x] = V[x] ^ V[y]
			PC = PC + 2
		elif last == int('0x4', 0):
			x = (opcode & int('0x0F00',0)) >> 8
			y = (opcode & int('0x00F0',0)) >> 4
			V[x] = V[x] + V[y]
			if V[x] > 256:
				V[int('0xF', 0)] = 1
			else:
				V[int('0xF', 0)] = 0
			V[x] = V[x] & int('0xFF',0)
			PC = PC + 2
		elif last == int('0x5', 0):
			x = (opcode & int('0x0F00',0)) >> 8
			y = (opcode & int('0x00F0',0)) >> 4

			if V[x] > V[y]:
				V[int('0xF', 0)] = 1
			else:
				V[int('0xF', 0)] = 0
				
			if V[x] >= V[y]:
				V[x] = V[x] - V[y]
			else:
				V[x] = V[x] + ((~ V[y]) & int('0x00FF',0)) + 1
			PC = PC + 2
		elif last == int('0x6', 0):
			x = (opcode & int('0x0F00',0)) >> 8
			y = (opcode & int('0x00F0',0)) >> 4

			LSB = V[x] & int('0x0001',0)
			#Esto se puede reemplazar por
			#V[int('0xF', 0)] = LSB
			if LSB:
				V[int('0xF', 0)] = 1
			else:
				V[int('0xF', 0)] = 0

			V[x] = int(V[x]/2)
			PC = PC + 2
		elif last == int('0x7', 0):
			x = (opcode & int('0x0F00',0)) >> 8
			y = (opcode & int('0x00F0',0)) >> 4

			if V[y] > V[x]:

				V[int('0xF', 0)] = 1
			else:
				V[int('0xF', 0)] = 0
				
			if V[y] >= V[x]:
				V[x] = V[y] - V[x]
			else:
				V[x] = V[y] + ((~ V[x]) & int('0x00FF',0)) + 1
			PC = PC + 2
		elif last == int('0xE', 0):
			x = (opcode & int('0x0F00',0)) >> 8
			y = (opcode & int('0x00F0',0)) >> 4

			MSB = (V[x] & int('0x8000',0)) >> 15
			if MSB:
				V[int('0xF', 0)] = 1
			else:
				V[int('0xF', 0)] = 0

			V[x] = V[x]*2

			PC = PC + 2
		else:
			print('Not programed', hex(opcode))
			sw = False
	elif lead == int('0x9', 0):
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		if V[x] != V[y]:
			PC = PC + 2
		PC = PC +2
	elif lead == int('0xA', 0):
		I = opcode & int('0x0FFF', 0)
		PC = PC + 2
	elif lead == int('0xC', 0):
		x = (opcode & int('0x0F00',0)) >> 8
		kk = opcode & int('0x00FF', 0)
		RND = randint(0, 255)
		V[x] = RND & kk
		PC = PC + 2
	elif lead == int('0xD', 0):
		x = (opcode & int('0x0F00',0)) >> 8
		y = (opcode & int('0x00F0',0)) >> 4
		n = opcode & int('0x000F',0)

		V[int('0x0F',0)] = 0

		x_cor = V[x]
		y_cor = V[y]
		for i in range(n):
			sprite = format(memory[I+i], '08b')
			x_cor = V[x]

			if (y_cor>=H):
				y_cor = y_cor - H*int((y_cor/(H-1)))

			for j in sprite:

				if ((x_cor)>=W):
					x_cor = x_cor - W*int((x_cor/(W-1)))

				if screen[y_cor][x_cor] == int(j):
					if screen[y_cor][x_cor]:
						V[int('0x0F',0)] = 1
					screen[y_cor][x_cor] = 0
				else:
					screen[y_cor][x_cor] = 1
				x_cor = x_cor + 1
			y_cor = y_cor + 1


		PC = PC + 2
	elif lead == int('0xE', 0):
		last = opcode & int('0x00FF', 0)
		if last == int('0x9E', 0):
			x = (opcode & int('0x0F00', 0)) >> 8
			if key[V[x]]:
				PC = PC + 2
		elif last == int('0xA1', 0):
			x = (opcode & int('0x0F00', 0)) >> 8
			if not key[V[x]]:
				PC = PC + 2
		else:
			sw = False
			print('Not programed', hex(opcode))
		PC = PC + 2
	elif lead == int('0xF', 0):
		last = opcode & int('0x00FF', 0)
		if last == int('0x07', 0):
			x = (opcode & int('0x0F00', 0)) >> 8
			V[x] = DT
			PC = PC + 2
		elif last == int('0x0A', 0):
			x = (opcode & int('0x0F00', 0)) >> 8
			count = 0
			for i in key:
				if i:
					V[x] = count
					PC = PC + 2
					break
				count = count + 1
		elif last == int('0x15', 0):
			x = (opcode & int('0x0F00', 0)) >> 8
			DT = V[x]
			PC = PC + 2
		elif last == int('0x18', 0):
			x = (opcode & int('0x0F00', 0)) >> 8
			ST = V[x]
			PC = PC + 2
		elif last == int('0x1E', 0):
			x = (opcode & int('0x0F00', 0)) >> 8
			I = (I + V[x]) & int('0x0FFF', 0)
			PC = PC + 2
		elif last == int('0x29', 0):
			x = (opcode & int('0x0F00', 0)) >> 8
			I = V[x]*5
			PC = PC + 2
		elif last == int('0x33', 0):
			x = (opcode & int('0x0F00', 0)) >> 8
			TEN = int(V[x]/100)
			HUN = int(V[x]/10) - TEN*10
			DEC = V[x] - HUN*10 - TEN*100
			memory[I]   = TEN
			memory[I+1] = HUN
			memory[I+2] = DEC
			PC = PC +2
		elif last == int('0x55', 0):
			x = (opcode & int('0x0F00', 0)) >> 8
			for i in range(x+1):
				memory[I+i] = V[i]

			PC = PC +2
		elif last == int('0x65', 0):
			x = (opcode & int('0x0F00', 0)) >> 8
			for i in range(x+1):
				V[i] = memory[I+i]

			PC = PC + 2
		else:
			print('Not programed', hex(opcode))
			sw = False
	else:
		print('Not programed', hex(opcode))
		sw = False

	if DT:
		DT = DT - 1

	if ST:
		ST = ST - 1
		#print("beep")

	# Draw

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sw = False

	gameDisplay.fill(black)

	for j in range(32):
		for i in range(64):
			if screen[j][i]:
				pygame.draw.rect(gameDisplay, white, (i*upScale,j*upScale,upScale,upScale))

	count = 0

	for i in controls:
		key[count] = pygame.key.get_pressed()[i]
		count = count + 1


	pygame.key.get_pressed()[i]

	ref = W*upScale + 15
	count = 0
	for i in V:
		textsurface = font.render("V["+('%0*X' % (1,count) ).upper()+"] = "+('0x%0*X' % (4,i) ).upper(), False, white)
		gameDisplay.blit(textsurface,(ref + 0, count*15))
		count = count + 1

	count = 0
	for i in key:
		textsurface = font.render("Key["+('%0*X' % (1,count) ).upper()+"] = "+str(i), False, white)
		gameDisplay.blit(textsurface,(ref + 120, count*15))
		count = count + 1

	count = 0
	for i in STACK:
		textsurface = font.render("STACK["+('%0*X' % (1,count) ).upper()+"] = "+('0x%0*X' % (4,i) ).upper(), False, white)
		gameDisplay.blit(textsurface,(ref + 210, count*15))
		count = count + 1

	textsurface = font.render("I  = "+('0x%0*X' % (4,I) ).upper(), False, white)
	gameDisplay.blit(textsurface,(ref + 0, count*15))
	count = count + 1
	textsurface = font.render("PC = "+('0x%0*X' % (4,PC) ).upper(), False, white)
	gameDisplay.blit(textsurface,(ref + 0, count*15))
	count = count + 1
	textsurface = font.render("SP = "+('0x%0*X' % (4,SP) ).upper(), False, white)
	gameDisplay.blit(textsurface,(ref + 0, count*15))

	textsurface = font.render("ST = "+('0x%0*X' % (4,ST) ).upper(), False, white)
	gameDisplay.blit(textsurface,(ref + 130, count*15))

	count = count + 1
	textsurface = font.render("OPCODE = "+('0x%0*X' % (4,opcode) ).upper(), False, white)
	gameDisplay.blit(textsurface,(ref + 0, count*15))

	textsurface = font.render("DT = "+('0x%0*X' % (4,DT) ).upper(), False, white)
	gameDisplay.blit(textsurface,(ref + 130, count*15))

	pygame.display.update()
	#input("Continue")

pygame.quit()
quit()