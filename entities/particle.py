import random
import math


class Particle:
    def __init__(self, game, x, y):
        self.game = game

        self.x = x
        self.y = y

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(50, 150)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = 0.5
        self.alive = True



    def update(self, dt):
        self.life -= dt

        if self.life <= 0:
            self.alive = False
            return

        self.x += self.vx * dt
        self.y += self.vy * dt



    def draw(self, screen):
        camera_x, camera_y = self.game.get_camera()

        screen.draw.filled_circle(
            (
                self.x - camera_x,
                self.y - camera_y
            ),
            2,
            "orange"
        )