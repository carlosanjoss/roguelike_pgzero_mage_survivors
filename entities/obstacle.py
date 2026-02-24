from pygame import Rect


class Obstacle:
    def __init__(self, game, x, y, sprite):
        self.game = game

        # CENTRO REAL
        self.x = x
        self.y = y

        self.sprite = sprite

        # TAMANHO REAL DA ROCK
        self.sprite_width = 31
        self.sprite_height = 41

        # HITBOX CENTRALIZADA
        self.rect = Rect(
            int(self.x - self.sprite_width // 2),
            int(self.y - self.sprite_height // 2),
            self.sprite_width,
            self.sprite_height
        )

    def draw(self, screen):
        camera_x, camera_y = self.game.get_camera()

        screen.blit(
            self.sprite,
            (
                int(self.x - camera_x - self.sprite_width // 2),
                int(self.y - camera_y - self.sprite_height // 2)
            )
        )