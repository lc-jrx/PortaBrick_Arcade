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
from pybricks.parameters import Icon, Button, Color
from pybricks.tools import wait

# Import helper files (ColorMatrixDisplay driver, pixel library)
from matrix_helper import MatrixHelper
from pixel_library import PixelLibrary

# Import games (Add additional games here and initialize them in "__init__" section)
from brick_pong import BrickPong
from brick_snake import BrickSnake


class PortaBrickArcade:
    """ Main Class of the PortaBrick Arcade. Controls the main menu and leads into the games.
    """

    def __init__(self):
        # Basic variables
        self.display_resolution = (6, 6)
        self.pressed = []

        # Load available games (Must be initialized AND added to "available_games" dictionary!!!)
        self.snake_game = BrickSnake(self.display_resolution[0], self.display_resolution[1])
        self.pong_game = BrickPong(self.display_resolution[0], self.display_resolution[1])
        self.available_games = (self.snake_game, self.pong_game)

        # Initialize classes and Hardware
        self.hub = PrimeHub()
        self.matrix = MatrixHelper(self.display_resolution[0], self.display_resolution[1])
        self.pixel_lib = PixelLibrary()

        # Change functions of hub's buttons
        self.hub.system.set_stop_button(None)  # Disable Center button to be used as return button
        self.hub.system.set_stop_button(Button.BLUETOOTH)  # Set Bluetooth button as stop button for system

    def start_up(self):
        self.matrix.draw_pixel_graphic(self.pixel_lib.pixelpics("heart"), Color.RED)
        self.hub.display.text("PortaBrick Arcade", 200, 50)
        self.matrix.matrix_off()
        wait(1000)

    def end_session(self):
        self.matrix.matrix_off()
        self.hub.display.off()

    def dialog(self):
        counter = 0         # Counter for menu entries
        action = False      # True closes game session and restarts dialog
        sys_quit = False    # True closes program

        def show_menu_entry(i):
            self.matrix.matrix_off()
            self.matrix.draw_pixel_graphic(self.pixel_lib.pixelpics(self.available_games[i].app_icon),
                                           self.available_games[i].app_color)
            self.hub.display.text(self.available_games[i].app_name, 200, 50)

        # Show little Howto how to choose the entries
        self.hub.display.text("Choose game", 200, 100)
        wait(500)
        self.hub.display.text("Next", 200, 100)
        wait(500)
        self.hub.display.icon(Icon.ARROW_RIGHT_DOWN)
        wait(1000)
        self.hub.display.text("Previous", 200, 100)
        wait(500)
        self.hub.display.icon(Icon.ARROW_LEFT_DOWN)
        wait(1000)
        self.hub.display.text("Quit", 200, 100)
        wait(500)
        self.hub.display.icon(Icon.ARROW_RIGHT_UP)
        wait(1000)

        while not sys_quit:
            # Show the first menu entry
            show_menu_entry(counter)

            while not action:
                pressed = self.hub.buttons.pressed()
                if Button.LEFT in pressed:
                    if counter > 0:
                        counter -= 1
                        show_menu_entry(counter)
                elif Button.RIGHT in pressed:
                    if counter < len(self.available_games) - 1:
                        counter += 1
                        show_menu_entry(counter)
                elif Button.CENTER in pressed:
                    self.available_games[counter].gameplay()
                    action = True
                elif Button.BLUETOOTH in pressed:
                    self.end_session()
            action = False


if __name__ == "__main__":
    try:
        game_session = PortaBrickArcade()
        game_session.start_up()
        game_session.dialog()
    except SystemExit:
        game_session.end_session()

# Leave the next line empty to fullfil PEP 8
