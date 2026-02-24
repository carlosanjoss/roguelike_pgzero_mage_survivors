import math
import random
from pgzero.builtins import sounds
from entities.xp_orb import XPOrb
from entities.particle import Particle


class Projectile:
    def __init__(
        self,
        game,
        x,
        y,
        target_x,
        target_y,
        damage,
        speed=400,
        piercing=False,
        from_enemy=False,
        lifetime=3.0
    ):
        self.game = game

        self.x = x
        self.y = y

        self.damage = damage
        self.speed = speed
        self.piercing = piercing
        self.from_enemy = from_enemy

        self.hit_enemies = set()
        self.alive = True

        self.lifetime = lifetime
        self.timer = 0

        dx = target_x - x
        dy = target_y - y

        length = math.hypot(dx, dy)

        if length != 0:
            dx /= length
            dy /= length

        self.vx = dx
        self.vy = dy



    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifetime:
            self.alive = False
            return

        self.x += self.vx * self.speed * dt
        self.y += self.vy * self.speed * dt

        if self.from_enemy:
            self.check_player_collision()
        else:
            self.check_enemy_collision()

        if math.hypot(self.x - self.game.player.x,
                      self.y - self.game.player.y) > 2000:
            self.alive = False



    def check_enemy_collision(self):
        for enemy in self.game.enemies:

            if enemy in self.hit_enemies:
                continue

            if math.hypot(self.x - enemy.x,
                          self.y - enemy.y) < enemy.sprite_size * 0.5:

                enemy.hp -= self.damage
                self.hit_enemies.add(enemy)

                if enemy.hp <= 0:
                    enemy.on_death()
                    self.handle_enemy_death(enemy)

                if not self.piercing:
                    self.alive = False
                    return



    def check_player_collision(self):
        player = self.game.player

        if math.hypot(self.x - player.x,
                      self.y - player.y) < 28:

            player.hp -= self.damage
            self.alive = False



    def handle_enemy_death(self, enemy):
        try:
            sounds.enemy_die.play()
        except:
            pass

        # XP padrão
        orb = XPOrb(self.game, enemy.x, enemy.y, 5)
        self.game.xp_orbs.append(orb)

        # Partículas
        for _ in range(6):
            self.game.particles.append(
                Particle(self.game, enemy.x, enemy.y)
            )



        roll = random.random()

        # 5% vida
        if roll < 0.05:
            from entities.health_pickup import HealthPickup
            self.game.health_pickups.append(
                HealthPickup(self.game, enemy.x, enemy.y)
            )

        # 3% arma
        elif roll < 0.08:
            enemy.drop_random_weapon()

        # 1% level up instantâneo
        elif roll < 0.09:
            self.game.level_up()



    def draw(self, screen):
        camera_x, camera_y = self.game.get_camera()

        if self.from_enemy:
            color = "orange"
        elif self.piercing:
            color = "cyan"
        else:
            color = "red"

        screen.draw.filled_circle(
            (
                int(self.x - camera_x),
                int(self.y - camera_y)
            ),
            5,
            color
        )