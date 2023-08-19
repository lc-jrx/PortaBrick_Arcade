"""
Main program for PortaBrick Arcade project

Copyright <2023> <LC-jrx>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Icon, Button
from pybricks.tools import wait

# Import helper files (ColorMatrixDisplay driver, pixel pic library)
from matrix_helper import MatrixHelper
from pixel_pics import PixelPics

# Import games
from brick_pong import BrickPong
from brick_snake import BrickSnake


class PortaBrickArcade:
    """ Main Class of the PortaBrick Arcade. Controls the main menu and leads into the two games.
    """
    def __init__(self):
        self.display_resolution = (6, 6)

        self.hub = PrimeHub()
        self.matrix = MatrixHelper(self.display_resolution[0], self.display_resolution[1])
        self.pixel_pics = PixelPics()
        self.pressed = []
        # self.state = True

    def start_up(self):
        self.hub.display.text("PortaBrick Arcade", 200, 50)
        self.hub.display.icon(Icon.HEART)
        wait(1000)

    def game_snake(self):
        snake_game = BrickSnake(self.display_resolution[0], self.display_resolution[1])
        snake_game.gameplay()

    def game_pong(self):
        pong_game = BrickPong(self.display_resolution[0], self.display_resolution[1])
        pong_game.gameplay()

    def end_session(self):
        self.matrix.matrix_off()
        self.hub.display.off()

    def dialog(self):
        self.hub.display.text("SNAKE", 200, 50)
        wait(500)
        self.hub.display.icon(Icon.ARROW_LEFT_DOWN)
        wait(1000)
        self.hub.display.text("PONG", 200, 50)
        wait(500)
        self.hub.display.icon(Icon.ARROW_RIGHT_DOWN)
        wait(1000)
        self.hub.display.text("Quit", 200, 50)
        wait(500)
        self.hub.display.icon(Icon.ARROW_RIGHT_UP)
        wait(1000)
        self.hub.display.char("?")
        wait(1000)

    def dialog_input(self):
        action = False  # set input status
        sys_quit = False  # True closes game session

        while not sys_quit:
            self.dialog()
            while not action:
                pressed = self.hub.buttons.pressed()
                if Button.LEFT in pressed:
                    self.hub.display.char("S")
                    self.game_snake()
                    action = True
                elif Button.RIGHT in pressed:
                    self.hub.display.char("P")
                    self.game_pong()
                    action = True
                elif Button.BLUETOOTH in pressed:
                    self.hub.display.char("Q")
                    # self.state = False
                    sys_quit = True
                    action = True
            action = False
        self.end_session()


if __name__ == "__main__":

    game_session = PortaBrickArcade()
    game_session.start_up()
    # game_session.dialog()
    game_session.dialog_input()
    game_session.end_session()

# Leave the next line empty to fullfil PEP 8
