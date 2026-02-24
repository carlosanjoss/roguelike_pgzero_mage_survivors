import math
from entities.projectile import Projectile
from entities.weapons.base_weapon import BaseWeapon
from pgzero.builtins import sounds

class SpreadWeapon(BaseWeapon):

    def __init__(self, game, owner):
        super().__init__(game, owner)
        self.cooldown = 1.2
        self.projectile_count = 3
        self.angle_spread = 25

    def attack(self):
        if not self.game.enemies:
            return

        nearest = min(
            self.game.enemies,
            key=lambda e: math.hypot(e.x - self.owner.x,
                                 e.y - self.owner.y)
        )

        base_angle = math.atan2(
            nearest.y - self.owner.y,
            nearest.x - self.owner.x
        )

        for i in range(self.projectile_count):
            offset = (
                (i - self.projectile_count // 2)
                * math.radians(self.angle_spread)
            )

            angle = base_angle + offset

            target_x = self.owner.x + math.cos(angle) * 100
            target_y = self.owner.y + math.sin(angle) * 100

            projectile = Projectile(
                self.game,
                self.owner.x,
                self.owner.y,
                target_x,
                target_y,
                self.owner.damage
            )

            self.game.projectiles.append(projectile)

        try:
            sounds.shoot.play()
        except:
            pass