import pgzrun
from engine.game import Game

WIDTH = 1280
HEIGHT = 720

game = Game(WIDTH, HEIGHT)


def update(dt):
    game.update(dt)


def draw():
    game.draw(screen)


def on_mouse_down(pos):
    game.on_mouse_down(pos)


def on_key_down(key):
    game.on_key_down(key)


pgzrun.go()