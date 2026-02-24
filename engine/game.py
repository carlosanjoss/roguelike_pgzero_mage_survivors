import random
import math
from pygame import Rect
from pgzero.builtins import music, keyboard

from ui.menu import MainMenu
from entities.player import Player
from engine.spawner import Spawner
from engine.map import GameMap
from engine.world import World
from entities.health_pickup import HealthPickup


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.music_enabled = False
        self.state = "menu"

        self.menu = MainMenu(self)

        self.reset_game()

    # ================= RESET =================

    def reset_entities(self):
        self.player = Player(self, 0, 0)
        self.enemies = []
        self.projectiles = []
        self.xp_orbs = []
        self.particles = []

        self.health_pickups = []
        self.health_spawn_timer = 0
        self.health_spawn_rate = 12

    def reset_game(self):
        self.reset_entities()

        self.world = World(self)
        self.map = GameMap(self)
        self.spawner = Spawner(self)

        self.time_survived = 0
        self.level_choices = []
        self.state = "menu"

    # ================= UPDATE =================

    def update(self, dt):

        if self.state == "menu":
            self.menu.update(dt)
            return

        if self.state in ["paused", "level_up"]:
            return

        if self.state == "playing":

            self.time_survived += dt

            self.player.update(dt, keyboard)
            self.world.update()
            self.spawner.update(dt)

            # VIDA ALEATÓRIA
            self.health_spawn_timer += dt

            if self.health_spawn_timer >= self.health_spawn_rate:
                self.health_spawn_timer = 0
                self.spawn_health_pickup()

            for item in self.health_pickups:
                item.update(dt)

            self.health_pickups = [i for i in self.health_pickups if i.alive]

            # ENEMIES
            for enemy in self.enemies:
                enemy.update(dt)
            self.enemies = [e for e in self.enemies if e.hp > 0]

            # PROJECTILES
            for projectile in self.projectiles:
                projectile.update(dt)
            self.projectiles = [p for p in self.projectiles if p.alive]

            # XP
            for orb in self.xp_orbs:
                orb.update(dt)
            self.xp_orbs = [o for o in self.xp_orbs if o.alive]

            # PARTICLES
            for particle in self.particles:
                particle.update(dt)
            self.particles = [p for p in self.particles if p.alive]

            if self.player.hp <= 0:
                self.state = "game_over"

    # ================= SPAWN HEALTH =================

    def spawn_health_pickup(self):
        distance = random.randint(400, 900)
        angle = random.uniform(0, 2 * math.pi)

        x = self.player.x + math.cos(angle) * distance
        y = self.player.y + math.sin(angle) * distance

        self.health_pickups.append(
            HealthPickup(self, x, y)
        )

    # ================= DRAW =================

    def draw(self, screen):
        screen.clear()

        if self.state == "menu":
            self.menu.draw(screen)
            return

        if self.state in ["playing", "paused", "level_up"]:

            self.map.draw(screen)
            self.world.draw(screen)

            self.draw_playing(screen)

            if self.state == "paused":
                screen.draw.text(
                    "PAUSED",
                    center=(self.width // 2, self.height // 2),
                    fontsize=70,
                    color="white"
                )

            if self.state == "level_up":
                self.draw_level_up(screen)

            return

        if self.state == "game_over":
            self.draw_game_over(screen)

    # ================= DRAW PLAYING =================

    def draw_playing(self, screen):

        for item in self.health_pickups:
            item.draw(screen)

        for orb in self.xp_orbs:
            orb.draw(screen)

        for particle in self.particles:
            particle.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        for projectile in self.projectiles:
            projectile.draw(screen)

        self.player.draw(screen)

        for weapon in self.player.weapons:
            if hasattr(weapon, "draw"):
                weapon.draw(screen)

        self.draw_ui(screen)

    # ================= UI =================

    def draw_ui(self, screen):

        panel = Rect(10, 10, 260, 150)
        screen.draw.filled_rect(panel, (20, 20, 20))
        screen.draw.rect(panel, (150, 150, 150))

        hp_ratio = self.player.hp / self.player.max_hp
        xp_ratio = self.player.xp / self.player.xp_to_next

        screen.draw.text("HP", (20, 25), fontsize=20, color="white")
        screen.draw.filled_rect(Rect(60, 30, 180, 15), (60, 0, 0))
        screen.draw.filled_rect(Rect(60, 30, 180 * hp_ratio, 15), (200, 0, 0))

        screen.draw.text("XP", (20, 55), fontsize=20, color="white")
        screen.draw.filled_rect(Rect(60, 60, 180, 15), (50, 50, 50))
        screen.draw.filled_rect(Rect(60, 60, 180 * xp_ratio, 15), (0, 150, 255))

        screen.draw.text(f"Level {self.player.level}", (20, 85), fontsize=20, color="white")
        screen.draw.text(f"Time: {int(self.time_survived)}", (20, 110), fontsize=20, color="white")

        music_status = "ON" if self.music_enabled else "OFF"
        screen.draw.text(f"Music: {music_status}", (20, 135), fontsize=20, color="white")

    # ================= GAME OVER =================

    def draw_game_over(self, screen):
        screen.draw.text(
            "GAME OVER",
            center=(self.width // 2, self.height // 2 - 40),
            fontsize=60,
            color="red"
        )

        screen.draw.text(
            f"Time Survived: {int(self.time_survived)}s",
            center=(self.width // 2, self.height // 2 + 10),
            fontsize=30,
            color="white"
        )

        screen.draw.text(
            "Press ESC to return to Menu",
            center=(self.width // 2, self.height // 2 + 60),
            fontsize=25,
            color="white"
        )

    # ================= LEVEL UP =================

    def level_up(self):
        self.state = "level_up"

        upgrades = [
            ("+10 Damage", "damage"),
            ("Faster Attack", "fire_rate"),
            ("Move Speed +30", "speed"),
            ("Max HP +20", "max_hp"),
        ]

        self.level_choices = random.sample(upgrades, 3)

    def apply_upgrade(self, upgrade_type):

        if upgrade_type == "damage":
            self.player.damage += 10

        elif upgrade_type == "fire_rate":
            for weapon in self.player.weapons:
                if hasattr(weapon, "cooldown"):
                    weapon.cooldown *= 0.8

        elif upgrade_type == "speed":
            self.player.speed += 30

        elif upgrade_type == "max_hp":
            self.player.max_hp += 20
            self.player.hp += 20

        self.state = "playing"

    def draw_level_up(self, screen):

        overlay = Rect(0, 0, self.width, self.height)
        screen.draw.filled_rect(overlay, (0, 0, 0))

        screen.draw.text(
            "LEVEL UP!",
            center=(self.width // 2, 100),
            fontsize=60,
            color="white"
        )

        for i, choice in enumerate(self.level_choices):

            rect = Rect(self.width // 2 - 200, 200 + i * 100, 400, 70)

            screen.draw.filled_rect(rect, (50, 50, 50))
            screen.draw.rect(rect, "white")

            screen.draw.text(
                choice[0],
                center=rect.center,
                fontsize=30,
                color="white"
            )

    # ================= INPUT =================

    def on_mouse_down(self, pos):

        if self.state == "menu":
            self.menu.on_mouse_down(pos)

        elif self.state == "level_up":

            for i, choice in enumerate(self.level_choices):

                rect = Rect(
                    self.width // 2 - 200,
                    200 + i * 100,
                    400,
                    70
                )

                if rect.collidepoint(pos):
                    self.apply_upgrade(choice[1])

    def on_key_down(self, key):

        if key.name == "ESCAPE":

            if self.state == "playing":
                self.state = "paused"

            elif self.state == "paused":
                self.state = "playing"

            elif self.state == "game_over":
                self.reset_game()

        if key.name == "M":
            self.toggle_music()

    # ================= AUDIO =================

    def toggle_music(self):
        self.music_enabled = not self.music_enabled

        if self.music_enabled:
            try:
                music.play("background")
            except:
                pass
        else:
            music.stop()

    # ================= CAMERA =================

    def get_camera(self):
        return (
            self.player.x - self.width // 2,
            self.player.y - self.height // 2
        )