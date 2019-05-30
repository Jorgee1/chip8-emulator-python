from random import randint
from src.cpu.core import Chip8_Pointer
import pygame
import sys


# to hex -> hex()
# to bin -> bin()
# 1 byte = 8 bit
# 1 char = 4 bit

chip8 = Chip8_Pointer(font='font/chip8_Font.bin')


# load rom
if len(sys.argv)>=2:
	game = sys.argv[1]
	chip8.load_rom(game)
else:
	print("No file selected")
	exit()




#Init pygame

black_color = (0,0,0)
white_color = (255,255,255)
upScale = 10
gui_space = 400

pygame.init()
pygame.display.set_caption('Chip 8')

gameDisplay = pygame.display.set_mode((chip8.W*upScale + gui_space, chip8.H*upScale))
gameDisplay.fill(black_color)


font = pygame.font.Font('font/UbuntuMono-R.ttf', 15)

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
sw = True
while(sw):
	opcode = chip8.memory[chip8.PC]<<8 | chip8.memory[chip8.PC+1]

	print(hex(opcode))
	#input()
	chip8.run_opcode(opcode)


	
	# Events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sw = False


	# Draw
	gameDisplay.fill(black_color)

	for j in range(32):
		for i in range(64):
			if chip8.screen[j][i]:
				pygame.draw.rect(gameDisplay, white_color, (i*upScale,j*upScale,upScale,upScale))

	# Draw GUI
	count = 0

	for i in controls:
		chip8.key[count] = pygame.key.get_pressed()[i]
		count = count + 1


	ref = chip8.W*upScale + 15
	count = 0
	for i in chip8.V:
		textsurface = font.render("V["+('%0*X' % (1,count) ).upper()+"] = "+('0x%0*X' % (4,i) ).upper(), False, white_color)
		gameDisplay.blit(textsurface,(ref + 0, count*15))
		count = count + 1

	count = 0
	for i in chip8.key:
		textsurface = font.render("Key["+('%0*X' % (1,count) ).upper()+"] = "+str(i), False, white_color)
		gameDisplay.blit(textsurface,(ref + 120, count*15))
		count = count + 1

	count = 0
	for i in chip8.STACK:
		textsurface = font.render("STACK["+('%0*X' % (1,count) ).upper()+"] = "+('0x%0*X' % (4,i) ).upper(), False, white_color)
		gameDisplay.blit(textsurface,(ref + 210, count*15))
		count = count + 1

	textsurface = font.render("I  = "+('0x%0*X' % (4,chip8.I) ).upper(), False, white_color)
	gameDisplay.blit(textsurface,(ref + 0, count*15))
	count = count + 1
	textsurface = font.render("PC = "+('0x%0*X' % (4,chip8.PC) ).upper(), False, white_color)
	gameDisplay.blit(textsurface,(ref + 0, count*15))
	count = count + 1
	textsurface = font.render("SP = "+('0x%0*X' % (4,chip8.SP) ).upper(), False, white_color)
	gameDisplay.blit(textsurface,(ref + 0, count*15))

	textsurface = font.render("ST = "+('0x%0*X' % (4,chip8.ST) ).upper(), False, white_color)
	gameDisplay.blit(textsurface,(ref + 130, count*15))
	count = count + 1
	
	textsurface = font.render("OPCODE = "+('0x%0*X' % (4,opcode) ).upper(), False, white_color)
	gameDisplay.blit(textsurface,(ref + 0, count*15))

	textsurface = font.render("DT = "+('0x%0*X' % (4,chip8.DT) ).upper(), False, white_color)
	gameDisplay.blit(textsurface,(ref + 130, count*15))

	pygame.display.update()



pygame.quit()
