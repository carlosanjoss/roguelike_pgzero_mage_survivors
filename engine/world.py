import random
import math
from entities.obstacle import Obstacle


class World:
    def __init__(self, game):
        self.game = game
        self.obstacles = []

        self.chunk_size = 600
        self.generated_chunks = set()



    def update(self):
        self.generate_chunks()



    def generate_chunks(self):
        px = int(self.game.player.x // self.chunk_size)
        py = int(self.game.player.y // self.chunk_size)

        for y in range(py - 2, py + 3):
            for x in range(px - 2, px + 3):
                if (x, y) not in self.generated_chunks:
                    self.generated_chunks.add((x, y))
                    self.generate_chunk(x, y)

    def generate_chunk(self, chunk_x, chunk_y):
        base_x = chunk_x * self.chunk_size
        base_y = chunk_y * self.chunk_size




        random.seed(chunk_x * 928371 + chunk_y * 123123)

        density_value = random.random()

        if density_value < 0.3:
            obstacle_count = random.randint(2, 5)      
        elif density_value < 0.7:
            obstacle_count = random.randint(6, 12)     
        else:
            obstacle_count = random.randint(15, 25)    

        for _ in range(obstacle_count):

            x = base_x + random.randint(40, self.chunk_size - 40)
            y = base_y + random.randint(40, self.chunk_size - 40)

            if self.is_valid_spawn(x, y):

                sprite = random.choice([
                    "map/tree",
                    "map/rock"
                ])

                obstacle = Obstacle(self.game, x, y, sprite)
                self.obstacles.append(obstacle)

        random.seed()  



    def is_valid_spawn(self, x, y):
 
        if math.hypot(x - self.game.player.x,
                      y - self.game.player.y) < 150:
            return False


        for obstacle in self.obstacles:
            if math.hypot(x - obstacle.x,
                          y - obstacle.y) < 50:
                return False

        return True 



    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)