from entities.projectile import Projectile
from entities.weapons.base_weapon import BaseWeapon


class PiercingWeapon(BaseWeapon):

    def __init__(self, game, owner):
        super().__init__(game, owner)
        self.cooldown = 2.0

    def attack(self):
        projectile = Projectile(
            self.game,
            self.owner.x,
            self.owner.y,
            self.owner.x + 1,
            self.owner.y,
            self.owner.damage * 2
        )

        projectile.piercing = True
        projectile.speed = 500

        self.game.projectiles.append(projectile)