from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Color
from pybricks.tools import wait
from matrix_helper import MatrixHelper
from pixel_pics import PixelPics


class GameControl:
    def __init__(self, display_res_x, display_res_y, default_gamespeed):
        # Basic variables
        self.__resolution = (display_res_x, display_res_y)

        # Variables for game
        self.__hardgame = True
        self.__game_speed = default_gamespeed

        # Initialize software and hardware
        self.__matrix = MatrixHelper(self.__resolution[0], self.__resolution[1])  # initialize driver for matrix
        self.__pixel_pics = PixelPics()  # initialize pixel drawings library
        self.__hub = PrimeHub()  # initialize LEGO Spike Prime Hub
        self.__hub_buttons = []  # initialize variable that holds info about pressed button

    def set_game_settings(self):
        action = False  # set input status

        # Let's ask for how hard to play
        self.__hub.display.text("Hard game?", 200, 50)
        while not action:
            pressed = self.__hub.buttons.pressed()
            if Button.RIGHT in pressed:
                self.__hub.display.char("Y")
                self.__hardgame = True
            elif Button.LEFT in pressed:
                self.__hub.display.char("N")
                self.__hardgame = False
            elif Button.BLUETOOTH in pressed:
                action = True

        action = False  # reset input status

        # Let's ask for how fast to play
        self.__hub.display.text("Difficulty?", 200, 50)
        difficulty = 3  # set game speed to mid (1 - 5)

        while not action:
            pressed = self.__hub.buttons.pressed()
            self.__hub.display.char(str(difficulty))

            if Button.RIGHT in pressed:
                if difficulty < 5:
                    difficulty += 1
                    self.__game_speed -= 50
            elif Button.LEFT in pressed:
                if difficulty > 1:
                    difficulty -= 1
                    self.__game_speed += 50
            elif Button.BLUETOOTH in pressed:
                action = True
            wait(250)

        return self.__hardgame, self.__game_speed

    def reset_game(self):
        action = False  # set input status
        game_quit = None
        game_reset = None
        self.__matrix.matrix_off()
        self.__matrix.draw_pixel_graphic(self.__pixel_pics.smiley, Color.GREEN)
        self.__hub.display.text("Play again?", 200, 50)
        while not action:
            pressed = self.__hub.buttons.pressed()
            if Button.RIGHT in pressed:
                self.__hub.display.char("Y")
                game_quit = False
                game_reset = True
            elif Button.LEFT in pressed:
                self.__hub.display.char("N")
                game_reset = False
            elif Button.BLUETOOTH in pressed:
                self.__matrix.matrix_off()
                action = True

        return game_quit, game_reset

    def gameover(self):
        self.__matrix.matrix_off()
        self.__hub.speaker.play_notes(["B3/2", "B2/2"], 160)  # make a sad sound
        self.__matrix.draw_pixel_graphic(self.__pixel_pics.smiley_sad, Color.RED)  # show a grafik for game over
        self.__hub.display.text("Game Over", 200, 50)
