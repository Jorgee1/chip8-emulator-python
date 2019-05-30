from random import randint
from src.cpu.core import Chip8_Core
import pygame
import sys


# to hex -> hex()
# to bin -> bin()
# 1 byte = 8 bit
# 1 char = 4 bit

chip8 = Chip8_Core(font='font/chip8_Font.bin')


# load rom
if len(sys.argv)>=2:
	game = sys.argv[1]
	chip8.load_rom(game)
else:
	print("No file selected")
	exit()




# Init pygame

black_color = (0,0,0)
white_color = (255,255,255)
text_size = 18


window_w = 800
window_h = 600
upScale = 5

pygame.init()
pygame.display.set_caption('PyChip8')
gameDisplay = pygame.display.set_mode((window_w, window_h))
font = pygame.font.Font('font/UbuntuMono-R.ttf', text_size)

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


game_screen_x = 0
game_screen_y = 0

# PC Draw Variabels

pc_draw_x = chip8.W*upScale + text_size
pc_draw_y = 0

# Stack Pointer Draw Variabels

sp_draw_x = chip8.W*upScale + text_size
sp_draw_y = text_size

# I Draw Variabels

i_draw_x = chip8.W*upScale + text_size
i_draw_y = text_size*2

# ST Draw Variabels

st_draw_x = chip8.W*upScale + text_size
st_draw_y = text_size*3

# DT Draw Variabels

dt_draw_x = chip8.W*upScale + text_size
dt_draw_y = text_size*4

# Register Draw Variables

register_draw_x = 0
register_draw_y = chip8.H*upScale + text_size

# Stack Draw Variables

stack_draw_x = 100
stack_draw_y = chip8.H*upScale + text_size

# Key Draw Variables

key_draw_x = 230
key_draw_y = chip8.H*upScale + text_size

# Memory Draw Variables
memory_draw_x = 350
memory_draw_y = chip8.H*upScale + text_size
memory_draw_padding = text_size/4

memory_draw_col = 10
memory_draw_row = 20

memory_draw_start = 0

memory_draw_move_up        = False 
memory_draw_move_down      = False
memory_draw_move_left      = False
memory_draw_move_right     = False
memory_draw_move_step      = 5
memory_draw_move_fast_step = memory_draw_move_step*10

# game cycle
chip8_cylce = True
while(chip8_cylce):

	chip8.run()
	
	# Events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			chip8_cylce = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				chip8_cylce = False
			elif event.key == pygame.K_LEFT:
				memory_draw_move_left = True
			elif event.key == pygame.K_RIGHT:
				memory_draw_move_right = True
			elif event.key == pygame.K_DOWN:
				memory_draw_move_down = True
			elif event.key == pygame.K_UP:
				memory_draw_move_up = True
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				memory_draw_move_left = False
			elif event.key == pygame.K_RIGHT:
				memory_draw_move_right = False
			elif event.key == pygame.K_DOWN:
				memory_draw_move_down = False
			elif event.key == pygame.K_UP:
				memory_draw_move_up = False


	if memory_draw_move_up:
		if memory_draw_start - memory_draw_move_step > 0:
			memory_draw_start -= memory_draw_move_step
		else:
			memory_draw_start = 0
	elif memory_draw_move_down:
		if memory_draw_start + memory_draw_move_step < 0x0FFF - memory_draw_col*(memory_draw_row-1):
			memory_draw_start += memory_draw_move_step
		else:
			memory_draw_start = 0x0FFF - memory_draw_col*(memory_draw_row-1)
	elif memory_draw_move_left:
		if memory_draw_start - memory_draw_move_fast_step > 0:
			memory_draw_start -= memory_draw_move_fast_step
		else:
			memory_draw_start = 0
	elif memory_draw_move_right:
		if memory_draw_start + memory_draw_move_fast_step <  0x0FFF - memory_draw_col*(memory_draw_row-1):
			memory_draw_start += memory_draw_move_fast_step
		else:
			memory_draw_start = 0x0FFF - memory_draw_col*(memory_draw_row-1)

	count = 0
	for i in controls:
		chip8.key[count] = pygame.key.get_pressed()[i]
		count = count + 1

	# Draw
	gameDisplay.fill(black_color)

	# Screen
	for j in range(32):
		for i in range(64):
			if chip8.screen[j][i]:
				pygame.draw.rect(gameDisplay, white_color, (game_screen_x + i*upScale, game_screen_y + j*upScale,upScale,upScale))


	# PC
	textsurface = font.render(' '.join(['PC:', '0x{:04x}'.format(chip8.PC).upper()]), False, white_color)
	gameDisplay.blit(textsurface,(pc_draw_x, pc_draw_y))

	# SP
	textsurface = font.render(' '.join(['SP:', '0x{:01x}'.format(chip8.SP).upper()]), False, white_color)
	gameDisplay.blit(textsurface,(sp_draw_x, sp_draw_y))

	# I
	textsurface = font.render(' '.join(['I :', '0x{:04x}'.format(chip8.I ).upper()]), False, white_color)
	gameDisplay.blit(textsurface,(i_draw_x, i_draw_y))

	# ST
	textsurface = font.render(' '.join(['ST:', '0x{:01x}'.format(chip8.ST).upper()]), False, white_color)
	gameDisplay.blit(textsurface,(st_draw_x, st_draw_y))

	# DT
	textsurface = font.render(' '.join(['DT:', '0x{:01x}'.format(chip8.DT).upper()]), False, white_color)
	gameDisplay.blit(textsurface,(dt_draw_x, dt_draw_y))

	# V register
	for i in range(len(chip8.V)):
		text = ' '.join(['V{:01x}'.format(i).upper() + ':', '0x{:02x}'.format(chip8.V[i]).upper()])
		textsurface = font.render(text, False, white_color)
		gameDisplay.blit(textsurface,(register_draw_x + 0, register_draw_y + i*text_size))

	# Stack
	for i in range(len(chip8.STACK)):
		text = ' '.join(['Stack', '{:01x}'.format(i).upper() + ':', '0x{:02x}'.format(chip8.STACK[i]).upper()])
		textsurface = font.render(text, False, white_color)
		gameDisplay.blit(textsurface,(stack_draw_x, stack_draw_y + i*text_size))

	# Key
	for i in range(len(chip8.key)):
		text = ' '.join(['Key', '{:01x}'.format(i).upper()+':', str(chip8.key[i])])
		textsurface = font.render(text, False, white_color)
		gameDisplay.blit(textsurface,(key_draw_x, key_draw_y + i*15))

	# Memory
	y = 0
	for i in range(memory_draw_start, memory_draw_start + memory_draw_row*memory_draw_col, memory_draw_col):
		x = 0
		textsurface = font.render('0x{:03x}'.format(i) + ':', False, white_color)
		gameDisplay.blit(textsurface,(x + memory_draw_x, y + memory_draw_y))
		x = textsurface.get_width() + memory_draw_padding
		for j in range(memory_draw_col):
			if i+j <= 0x0FFF:
				text = "{:02x}".format(chip8.memory[i+j])
				textsurface = font.render(text, False, white_color)
				gameDisplay.blit(textsurface,(x + memory_draw_x, y + memory_draw_y))
			else:
				textsurface = font.render('XX', False, white_color)
				gameDisplay.blit(textsurface, (x + memory_draw_x, y + memory_draw_y))
			x = x + textsurface.get_width() + memory_draw_padding
		y = y + text_size

	pygame.display.update()



pygame.quit()
