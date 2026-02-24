import math


class BaseWeapon:
    def __init__(self, game, owner):
        self.game = game
        self.owner = owner
        self.cooldown = 0.25
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.cooldown:
            self.timer = 0
            self.attack()

    def attack(self):
        pass

    def draw(self, screen):
        pass