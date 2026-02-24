import random
from entities.enemy import Enemy


class Spawner:
    def __init__(self, game):
        self.game = game
        self.spawn_timer = 0
        self.last_boss_minute = -1

    # ================= UPDATE =================

    def update(self, dt):
        self.spawn_timer += dt

        spawn_interval = max(
            0.3,
            2.0 - self.game.time_survived * 0.03
        )

        if self.spawn_timer >= spawn_interval:
            self.spawn_timer = 0
            self.spawn_enemy()

        self.check_boss_spawn()

    # ================= NORMAL SPAWN =================

    def spawn_enemy(self):
    

        enemy_pool = ["fast", "tank", "shooter", "exploder", "evader"]
        weights = [30, 25, 15, 15, 15]

        enemy_type = random.choices(enemy_pool, weights=weights, k=1)[0]

        self.game.enemies.append(
            Enemy(self.game, enemy_type)
        )

    # Spawn de boss separado (fora da roleta)
        if int(self.game.time_survived) > 0 and int(self.game.time_survived) % 60 == 0:
            self.game.enemies.append(
            Enemy(self.game, "boss")
        )

    # ================= BOSS SPAWN =================

    def check_boss_spawn(self):
        current_minute = int(self.game.time_survived // 60)

        if current_minute > 0 and current_minute != self.last_boss_minute:
            self.last_boss_minute = current_minute

            boss = Enemy(self.game, "boss")

            boss.max_hp += int(self.game.time_survived * 2)
            boss.hp = boss.max_hp

            self.game.enemies.append(boss)