class GameMap:
    def __init__(self, game):
        self.game = game
        self.tile_size = 64

    def draw(self, screen):
        tile = self.tile_size

        camera_x, camera_y = self.game.get_camera()

        # Quantos tiles precisamos cobrir a tela inteira
        cols = self.game.width // tile + 3
        rows = self.game.height // tile + 3

        # Tile inicial baseado na câmera
        start_col = int(camera_x // tile) - 1
        start_row = int(camera_y // tile) - 1

        for row in range(start_row, start_row + rows):
            for col in range(start_col, start_col + cols):

                world_x = col * tile
                world_y = row * tile

                screen_x = world_x - camera_x
                screen_y = world_y - camera_y

                screen.blit("map/grass", (screen_x, screen_y))