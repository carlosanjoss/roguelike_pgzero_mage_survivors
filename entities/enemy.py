import math
import random
from pygame import Rect
from entities.projectile import Projectile


class Enemy:

    def __init__(self, game, enemy_type):
        self.game = game
        self.type = enemy_type

        self.x, self.y = self.spawn_outside_player()



        if enemy_type == "fast":
            self.speed = 180
            self.base_hp = 30
            self.base_damage = 10
            self.frames = ["enemies/fast_0", "enemies/fast_1"]
            self.sprite_size = 64

        elif enemy_type == "tank":
            self.speed = 80
            self.base_hp = 120
            self.base_damage = 20
            self.frames = ["enemies/tank_0", "enemies/tank_1"]
            self.sprite_size = 64

        elif enemy_type == "shooter":
            self.speed = 90
            self.base_hp = 60
            self.base_damage = 15
            self.frames = ["enemies/shooter_0", "enemies/shooter_1"]
            self.sprite_size = 64
            self.shoot_timer = 0
            self.shoot_rate = 2.0

        elif enemy_type == "exploder":
            self.speed = 120
            self.base_hp = 40
            self.base_damage = 40
            self.frames = ["enemies/exploder_0", "enemies/exploder_1"]
            self.sprite_size = 64

        elif enemy_type == "evader":
            self.speed = 220
            self.base_hp = 50
            self.base_damage = 12
            self.frames = ["enemies/evader_0", "enemies/evader_1"]
            self.sprite_size = 64

        elif enemy_type == "boss":
            self.speed = 70
            self.base_hp = 800
            self.base_damage = 30
            self.frames = ["enemies/boss_0", "enemies/boss_1"]
            self.sprite_size = 96
            self.shoot_timer = 0
            self.shoot_rate = 1.2



        self.scale_with_time()



        self.is_elite = False

        if self.type != "boss" and random.random() < 0.10:
            self.make_elite()



        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.2



    def scale_with_time(self):
        minutes = self.game.time_survived / 60
        difficulty_multiplier = 1 + (minutes * 0.25)

        self.max_hp = self.base_hp * difficulty_multiplier
        self.hp = self.max_hp

        self.damage = self.base_damage * difficulty_multiplier
        self.speed *= 1 + (minutes * 0.05)



    def make_elite(self):
        self.is_elite = True
        self.max_hp *= 2
        self.hp = self.max_hp
        self.damage *= 1.5
        self.speed *= 1.5



    def spawn_outside_player(self):
        distance = 900
        angle = random.uniform(0, 2 * math.pi)

        x = self.game.player.x + math.cos(angle) * distance
        y = self.game.player.y + math.sin(angle) * distance

        return x, y



    def update(self, dt):
        self.move_towards_player(dt)

        if self.type in ["shooter", "boss"]:
            self.shoot(dt)

        self.animate(dt)
        self.check_collision_with_player(dt)



    def move_towards_player(self, dt):
        dx = self.game.player.x - self.x
        dy = self.game.player.y - self.y

        distance = math.hypot(dx, dy)

        if distance != 0:
            dx /= distance
            dy /= distance

        next_x = self.x + dx * self.speed * dt
        next_y = self.y + dy * self.speed * dt

        hitbox_size = int(self.sprite_size * 0.6)

        future_rect_x = Rect(
            int(next_x - hitbox_size // 2),
            int(self.y - hitbox_size // 2),
            hitbox_size,
            hitbox_size
        )

        if not any(future_rect_x.colliderect(ob.rect)
                   for ob in self.game.world.obstacles):
            self.x = next_x

        future_rect_y = Rect(
            int(self.x - hitbox_size // 2),
            int(next_y - hitbox_size // 2),
            hitbox_size,
            hitbox_size
        )

        if not any(future_rect_y.colliderect(ob.rect)
                   for ob in self.game.world.obstacles):
            self.y = next_y



    def shoot(self, dt):
        self.shoot_timer += dt

        if self.shoot_timer >= self.shoot_rate:
            self.shoot_timer = 0

            projectile = Projectile(
                self.game,
                self.x,
                self.y,
                self.game.player.x,
                self.game.player.y,
                self.damage,
                speed=250,
                from_enemy=True
            )

            self.game.projectiles.append(projectile)



    def check_collision_with_player(self, dt):
        if math.hypot(self.x - self.game.player.x,
                      self.y - self.game.player.y) < self.sprite_size * 0.4:

            if self.type == "exploder":
                self.game.player.hp -= self.damage
                self.hp = 0
            else:
                self.game.player.hp -= self.damage * dt



    def on_death(self):


        if self.is_elite:
            from entities.health_pickup import HealthPickup
            self.game.health_pickups.append(
                HealthPickup(self.game, self.x, self.y)
            )

        if self.type == "boss":
            self.drop_random_weapon()

    def drop_random_weapon(self):
        from entities.weapons.orbital_weapon import OrbitalWeapon
        from entities.weapons.spread_weapon import SpreadWeapon
        from entities.weapons.piercing_weapon import PiercingWeapon

        weapon_pool = [
            OrbitalWeapon,
            SpreadWeapon,
            PiercingWeapon
        ]

        weapon_class = random.choice(weapon_pool)
        new_weapon = weapon_class(self.game, self.game.player)

        self.game.player.weapons.append(new_weapon)



    def animate(self, dt):
        self.animation_timer += dt

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)



    def draw(self, screen):
        camera_x, camera_y = self.game.get_camera()

        screen_x = self.x - camera_x
        screen_y = self.y - camera_y


        if self.is_elite:
            screen.draw.filled_circle(
                (int(screen_x), int(screen_y)),
                int(self.sprite_size * 0.7),
                (120, 0, 180)
            )

        screen.blit(
            self.frames[self.frame_index],
            (
                int(screen_x - self.sprite_size // 2),
                int(screen_y - self.sprite_size // 2)
            )
        )

        hp_ratio = max(0, self.hp / self.max_hp)

        bar_width = self.sprite_size
        bar_height = 6

        screen.draw.filled_rect(
            Rect(
                int(screen_x - bar_width // 2),
                int(screen_y - self.sprite_size // 2 - 12),
                bar_width,
                bar_height
            ),
            (60, 0, 0)
        )

        screen.draw.filled_rect(
            Rect(
                int(screen_x - bar_width // 2),
                int(screen_y - self.sprite_size // 2 - 12),
                int(bar_width * hp_ratio),
                bar_height
            ),
            (0, 200, 0)
        )