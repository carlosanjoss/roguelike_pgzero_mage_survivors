import math
from pygame import Rect
from pgzero.builtins import sounds

from entities.weapons.spread_weapon import SpreadWeapon


class Player:
    def __init__(self, game, x, y):
        self.game = game


        self.x = x
        self.y = y


        self.sprite_width = 64
        self.sprite_height = 64


        self.speed = 220
        self.velocity_x = 0
        self.velocity_y = 0


        self.max_hp = 100
        self.hp = 100


        self.level = 1
        self.xp = 0
        self.xp_to_next = 10


        self.damage = 25


        self.weapons = []
        self.add_start_weapon()


        self.animation_timer = 0
        self.animation_speed = 0.15
        self.frame_index = 0
        self.state = "idle"

        self.idle_frames = [
            "player/player_idle_0",
            "player/player_idle_1",
        ]

        self.walk_frames = [
            "player/player_walk_0",
            "player/player_walk_1",
            "player/player_walk_2",
            "player/player_walk_3",
        ]



    def add_start_weapon(self):
        weapon = SpreadWeapon(self.game, self)
        self.weapons.append(weapon)



    def update(self, dt, keyboard):
        self.handle_input(keyboard)
        self.move(dt)
        self.animate(dt)

        for weapon in self.weapons:
            weapon.update(dt)



    def handle_input(self, keyboard):
        self.velocity_x = 0
        self.velocity_y = 0

        if keyboard.w:
            self.velocity_y = -1
        if keyboard.s:
            self.velocity_y = 1
        if keyboard.a:
            self.velocity_x = -1
        if keyboard.d:
            self.velocity_x = 1

        if self.velocity_x != 0 or self.velocity_y != 0:
            self.state = "walk"
        else:
            self.state = "idle"



    def move(self, dt):
        length = math.hypot(self.velocity_x, self.velocity_y)

        if length != 0:
            self.velocity_x /= length
            self.velocity_y /= length

        next_x = self.x + self.velocity_x * self.speed * dt
        next_y = self.y + self.velocity_y * self.speed * dt

        hitbox_size = int(self.sprite_width * 0.6)

        future_rect = Rect(
            int(next_x - hitbox_size // 2),
            int(next_y - hitbox_size // 2),
            hitbox_size,
            hitbox_size
        )

        collision = False

        for obstacle in self.game.world.obstacles:
            if future_rect.colliderect(obstacle.rect):
                collision = True
                break

        if not collision:
            self.x = next_x
            self.y = next_y



    def animate(self, dt):
        frames = self.get_current_frames()

        if not frames:
            return

        self.animation_timer += dt

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

    def get_current_frames(self):
        if self.state == "walk":
            return self.walk_frames
        return self.idle_frames



    def draw(self, screen):
        frames = self.get_current_frames()

        if not frames:
            return

        if self.frame_index >= len(frames):
            self.frame_index = 0

        image_name = frames[self.frame_index]

        screen.blit(
            image_name,
            (
                int(self.game.width // 2 - self.sprite_width // 2),
                int(self.game.height // 2 - self.sprite_height // 2)
            )
        )

        self.draw_hp_bar(screen)



    def draw_hp_bar(self, screen):
        bar_width = 50
        bar_height = 6

        hp_ratio = self.hp / self.max_hp

        center_x = self.game.width // 2
        center_y = self.game.height // 2

        screen.draw.filled_rect(
            Rect(center_x - bar_width // 2,
                 center_y - 45,
                 bar_width,
                 bar_height),
            (60, 0, 0)
        )

        screen.draw.filled_rect(
            Rect(center_x - bar_width // 2,
                 center_y - 45,
                 int(bar_width * hp_ratio),
                 bar_height),
            (0, 200, 0)
        )



    def gain_xp(self, amount):
        self.xp += amount

        if self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.5)

            self.game.level_up()