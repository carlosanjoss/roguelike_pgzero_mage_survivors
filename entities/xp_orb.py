import math


class XPOrb:
    def __init__(self, game, x, y, value):
        self.game = game
        self.x = x
        self.y = y
        self.value = value

        self.speed = 0
        self.alive = True



    def update(self, dt):
        dx = self.game.player.x - self.x
        dy = self.game.player.y - self.y

        distance = math.hypot(dx, dy)


        if distance < 150:
            self.speed = 250
        else:
            self.speed = 0

        if distance != 0:
            dx /= distance
            dy /= distance

        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt


        if distance < 20:
            self.game.player.gain_xp(self.value)
            self.alive = False


    def draw(self, screen):
        camera_x, camera_y = self.game.get_camera()

        screen.draw.filled_circle(
            (
                self.x - camera_x,
                self.y - camera_y
            ),
            4,
            "blue"
        )