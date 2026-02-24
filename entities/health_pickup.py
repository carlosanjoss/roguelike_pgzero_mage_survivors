import math


class HealthPickup:

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y

        # Caminho relativo à pasta images/
        self.sprite = "items/health"
        self.size = 48

        self.heal_amount = 30
        self.alive = True

    # ================= UPDATE =================

    def update(self, dt):
        player = self.game.player

        if math.hypot(self.x - player.x,
                      self.y - player.y) < 32:

            player.hp = min(
                player.max_hp,
                player.hp + self.heal_amount
            )

            self.alive = False

    # ================= DRAW =================

    def draw(self, screen):
        camera_x, camera_y = self.game.get_camera()

        screen.blit(
            self.sprite,
            (
                int(self.x - camera_x - self.size // 2),
                int(self.y - camera_y - self.size // 2)
            )
        )