from pygame import Rect
from pgzero.builtins import music


class Button:
    def __init__(self, text, rect, action):
        self.text = text
        self.rect = rect
        self.action = action

    def draw(self, screen):
        screen.draw.filled_rect(self.rect, (30, 30, 30))
        screen.draw.rect(self.rect, (180, 180, 180))

        screen.draw.text(
            self.text,
            center=self.rect.center,
            fontsize=36,
            color="white"
        )

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()


class MainMenu:
    def __init__(self, game):
        self.game = game

        self.background_image = "menu_background"  

        self.create_buttons()



    def create_buttons(self):
        center_x = self.game.width // 2
        start_y = self.game.height // 2 - 60

        music_text = self.get_music_text()

        self.start_button = Button(
            "Start Game",
            Rect(center_x - 150, start_y, 300, 60),
            self.start_game
        )

        self.music_button = Button(
            music_text,
            Rect(center_x - 150, start_y + 80, 300, 60),
            self.toggle_music
        )

        self.exit_button = Button(
            "Exit",
            Rect(center_x - 150, start_y + 160, 300, 60),
            self.exit_game
        )

        self.buttons = [
            self.start_button,
            self.music_button,
            self.exit_button
        ]



    def update(self, dt):
        pass



    def draw(self, screen):
        screen.clear()


        try:
            screen.blit(self.background_image, (0, 0))
        except:
            screen.fill((15, 15, 20))  


        screen.draw.text(
            "MAGE ROGUELIKE",
            center=(self.game.width // 2, 120),
            fontsize=70,
            color="white"
        )

        for button in self.buttons:
            button.draw(screen)



    def on_mouse_down(self, pos):
        for button in self.buttons:
            button.check_click(pos)



    def start_game(self):
        self.game.reset_entities()
        self.game.state = "playing"
        self.game.time_survived = 0

    def toggle_music(self):
        self.game.music_enabled = not self.game.music_enabled

        if self.game.music_enabled:
            try:
                music.play("background")
            except:
                pass
        else:
            music.stop()


        self.music_button.text = self.get_music_text()

    def get_music_text(self):
        return "Music: ON" if self.game.music_enabled else "Music: OFF"

    def exit_game(self):
        exit()