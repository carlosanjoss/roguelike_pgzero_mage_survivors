import math
from entities.weapons.base_weapon import BaseWeapon


class OrbitalWeapon(BaseWeapon):

    def __init__(self, game, owner):
        super().__init__(game, owner)
        self.cooldown = 0  # sempre ativa
        self.angle = 0
        self.radius = 100
        self.damage = 10

    def update(self, dt):
        self.angle += 2 * dt

        orbit_x = self.owner.x + math.cos(self.angle) * self.radius
        orbit_y = self.owner.y + math.sin(self.angle) * self.radius

        for enemy in self.game.enemies:
            if math.hypot(enemy.x - orbit_x,
                          enemy.y - orbit_y) < 30:
                enemy.hp -= self.damage * dt

    def draw(self, screen):
        camera_x, camera_y = self.game.get_camera()

        orbit_x = self.owner.x + math.cos(self.angle) * self.radius
        orbit_y = self.owner.y + math.sin(self.angle) * self.radius

        screen.draw.filled_circle(
            (
                int(orbit_x - camera_x),
                int(orbit_y - camera_y)
            ),
            10,
            "yellow"
        )