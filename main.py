import sys

from enum import Enum
from dataclasses import field
from dataclasses import astuple
from dataclasses import dataclass

import pygame as pg
from pygame.font import Font

from module.chip8  import Chip8


@dataclass
class Color:
    r: int
    g: int
    b: int

class Colors:
    black = Color(0, 0, 0)
    gray  = Color(50, 50, 50)
    white = Color(255, 255, 255)

@dataclass(init=False)
class Key:
    state: bool = False
    press: bool = False
    _lock: bool = False

    def _is_key_pressed_and_not_locked(self):
        return self.state and not self._lock 

    def _is_key_not_pressed_and_locked(self):
        return not self.state and self._lock

    def update(self, state):
        self.state = bool(state)

        if self._is_key_pressed_and_not_locked():
            self.press = True
            self._lock = True
        elif self._is_key_not_pressed_and_locked():
            self.press = False
            self._lock = False
        else:
            self.press = False

class Input:
    def __init__(self):
        self.keys = dict()

        # Maps to Chip8 key memory address
        self.keys_address = [
            pg.K_KP0, # 0x0
            pg.K_KP1, # 0x1
            pg.K_KP2, # 0x2
            pg.K_KP3, # 0x3
            pg.K_KP4, # 0x4
            pg.K_KP5, # 0x5
            pg.K_KP6, # 0x6
            pg.K_KP7, # 0x7
            pg.K_KP8, # 0x8
            pg.K_KP9, # 0x9
            pg.K_a,   # 0xA
            pg.K_b,   # 0xB
            pg.K_c,   # 0xC
            pg.K_d,   # 0xD
            pg.K_e,   # 0xE
            pg.K_f    # 0xF
        ]

        for key in self.keys_address:
            self.keys[key] = Key()

    def update(self):
        keys = pg.key.get_pressed()

        for name, key in self.keys.items():
            value = keys[name]

            key.update(value)

@dataclass
class Screen:
    w: int
    h: int
    x: int = 0
    y: int = 0
    surface: pg.Surface = field(init=False)

    def __post_init__(self):
        self.surface = pg.display.set_mode((self.w, self.h))

    def rect(self, scale=1):
        return pg.Rect(
            self.x,
            self.y,
            self.w * scale,
            self.h * scale
        )


if len(sys.argv)>=2:
    rom = sys.argv[1]
else:
	print('Usage: python main.py path_to_game')
	exit()


# Pygame init
game_exit = False

pg.init()
screen = Screen(w=800, h=600)
font = Font('font/UbuntuMono-R.ttf', 18)
controller = Input()

# Chip8 init
chip8 = Chip8(font='font/chip8_Font.bin')
chip8.load_rom(rom)

while not game_exit:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    controller.update()

    for index, key in enumerate(controller.keys_address):
        chip8.key[index] = int(controller.keys[key].state)

    chip8.run()

    # Render
    surface = pg.display.get_surface()
    surface.fill(astuple(Colors.gray))

    # Screen
    pg.draw.rect(
        surface,
        astuple(Colors.black),
        pg.Rect(0, 0, chip8.w*10, chip8.h*10)
    )
    for j in range(chip8.h):
        for i in range(chip8.w):
            if chip8.screen[j][i]:
                rect = pg.Rect(i*10, j*10, 10, 10)
                pg.draw.rect(surface, astuple(Colors.white), rect)

    pg.display.flip()

pg.quit()
