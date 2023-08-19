"""
Arcade Game BrickPong for PortaBrick Arcade

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
from pybricks.pupdevices import ForceSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait as blocking_wait, StopWatch
from matrix_helper import MatrixHelper
from game_control import GameControl
from pixel_pics import PixelPics
from urandom import randint


class BrickPong:
    """Implementation of the classic game "Pong" for the PortaBrick Arcade
    based on the Pybricks framework. As a template or inspiration the
    code of the game was generated by chat.openai.com and then adapted."""

    def __init__(self, display_res_x, display_res_y):
        self.__screen_width = display_res_x
        self.__screen_height = display_res_y

        # Set up game variables
        self.__ball_x, self.__ball_y = None, None
        self.__ball_x_velocity, self.__ball_y_velocity = 1, 1
        self.__render_off = []
        self.__game_speed = 300
        self.__hardgame_factor = 2
        self.__score = None
        self.__gameover = None
        self.__quit = False
        self.__reset = True

        self.__paddle_A = self.__Paddle("A", self.__screen_width, self.__screen_height, self.__hardgame_factor)
        self.__paddle_B = self.__Paddle("B", self.__screen_width, self.__screen_height, self.__hardgame_factor)

        # Initialize software and hardware
        self.__gamecontrol = GameControl(self.__screen_width, self.__screen_height, self.__game_speed)
        self.__matrix = MatrixHelper(self.__screen_width, self.__screen_height)  # initialize driver for matrix
        self.__pixel_pics = PixelPics()  # initialize pixel drawings library
        self.__hub = PrimeHub()  # initialize LEGO Spike Prime Hub
        self.__button_L = ForceSensor(Port.E)  # initialize LEGO Spike Prime Force Sensor as left button
        self.__button_R = ForceSensor(Port.F)  # initialize LEGO Spike Prime Force Sensor as right button
        self.__hub_buttons = []  # initialize variable that holds info about pressed button

    class __Paddle:
        def __init__(self, player, screen_width, screen_height, difficulty):
            """ This class generates the players paddles. Input needed:
            - player (character): "A" or "B"
            - screen_witdh (integer): in pixel; must be 6 or bigger
            - screen_height (integer): in pixel; must be 6 or bigger
            - difficulty (integer): must be 2 or greater; the greater the factor, the smaller the paddles

            Readable from outside:
            - paddle_pix(nested list): list of the paddles coordinates
            - paddle_pix_off(nested list): list of those coordinates, that will be switched off (after paddles movement)
            - paddle_length(integer): length of the paddle
            """
            self.paddle_pix = []  # initial list for y-coordinates of paddle
            self.paddle_pix_off = []
            self.__screen_width = screen_width
            self.__screen_height = screen_height
            self.paddle_length = self.__screen_height // difficulty

            if player == "A":
                for i in range(self.paddle_length):
                    self.paddle_pix.append([0, i + 1])

            elif player == "B":
                x = screen_width - 1
                for i in range(self.paddle_length):
                    self.paddle_pix.append([x, self.__screen_height - 1 - self.paddle_length + i])

        def move_paddle(self, direction, speed):
            pix_off = []

            def move_one():
                for i in range(len(self.paddle_pix)):
                    pix_off.append(self.paddle_pix[i].copy())
                    self.paddle_pix[i][1] += direction

            def move_many(factor):
                for i in range(len(self.paddle_pix)):
                    pix_off.append(self.paddle_pix[i].copy())
                    self.paddle_pix[i][1] += direction * factor

            if direction == 1:
                if self.paddle_pix[-1][1] < self.__screen_height - speed and speed > 1:
                    move_many(speed)
                elif self.paddle_pix[-1][1] < self.__screen_height - 1:
                    move_one()
                else:
                    self.paddle_pix_off = []
                    # print("No move")
            elif direction == -1:
                if self.paddle_pix[0][1] > speed:
                    move_many(speed)
                elif self.paddle_pix[0][1] > 0:
                    move_one()
                else:
                    self.paddle_pix_off = []
                    # print("No move")
            self.__compare(self.paddle_pix, pix_off)

        def __compare(self, new_pix, off_pix):
            diff = [i for i in off_pix if i not in new_pix]
            # print("Diff: ", diff)
            if len(diff) > 0:
                self.paddle_pix_off = diff.copy()

    @staticmethod
    def __wait(time):
        """ Part of generator function for using parallel computing without threads.
            Source: https://github.com/orgs/pybricks/discussions/356 """
        timer = StopWatch()
        while timer.time() < time:
            yield

    def __render_game(self):
        # Render the current game state.
        while True:
            # First read those pixels from paddles to be shut off and add them to the render_off-list
            if len(self.__paddle_A.paddle_pix_off) > 0:
                for i in self.__paddle_A.paddle_pix_off:
                    self.__render_off.append(i)
            if len(self.__paddle_B.paddle_pix_off) > 0:
                for i in self.__paddle_B.paddle_pix_off:
                    self.__render_off.append(i)
            # Then switch off former active pixels
            if len(self.__render_off) > 0:
                for i in range(len(self.__render_off)):
                    self.__matrix.pixel_off(self.__render_off[i][0], self.__render_off[i][1])
                self.__render_off = []
            # Now switch on pixels for both players and ball
            for i in range(len(self.__paddle_A.paddle_pix)):
                self.__matrix.pixel_on(self.__paddle_A.paddle_pix[i][0], self.__paddle_A.paddle_pix[i][1], Color.WHITE)
            for i in range(len(self.__paddle_B.paddle_pix)):
                self.__matrix.pixel_on(self.__paddle_B.paddle_pix[i][0], self.__paddle_B.paddle_pix[i][1], Color.WHITE)
            self.__matrix.pixel_on(self.__ball_x, self.__ball_y, Color.RED)

            yield

    def __update_ball(self):
        while True:
            yield from self.__wait(self.__game_speed)
            # Update ball position
            self.__render_off.insert(0, [self.__ball_x, self.__ball_y])
            self.__ball_x += self.__ball_x_velocity
            self.__ball_y += self.__ball_y_velocity

    def __handle_ball_collisions(self):
        while True:
            # Handle ball collisions with player and computer paddles
            if self.__ball_x_velocity == -1 and self.__ball_x == 1:
                for i in range(len(self.__paddle_A.paddle_pix)):
                    if self.__ball_y_velocity == 1:
                        if self.__ball_y + 1 == self.__paddle_A.paddle_pix[i][1]:
                            # print("Paddle A contact")
                            self.__ball_x_velocity = -self.__ball_x_velocity
                            self.__score += 1
                    elif self.__ball_y_velocity == -1:
                        if self.__ball_y - 1 == self.__paddle_A.paddle_pix[i][1]:
                            # print("Paddle A contact")
                            self.__ball_x_velocity = -self.__ball_x_velocity
                            self.__score += 1
            elif self.__ball_x_velocity == 1 and self.__ball_x == self.__screen_width - 2:
                for i in range(len(self.__paddle_B.paddle_pix)):
                    if self.__ball_y + 1 == self.__paddle_B.paddle_pix[i][1]:
                        # print("Paddle B contact")
                        self.__ball_x_velocity = -self.__ball_x_velocity

            # Handle ball collisions with upper and lower walls
            if self.__ball_y == 0 or self.__ball_y == self.__screen_height - 1:
                self.__ball_y_velocity = -self.__ball_y_velocity

            # Handle ball collisions with left and right walls
            if self.__ball_x == 0 or self.__ball_x == self.__screen_width:
                # print("Ball x {}, y {}, Paddle {}".format(self.__ball_x, self.__ball_y, self.__paddle_A.paddle_pix))
                self.__gameover = True

            yield

    def __update_computer_paddle(self):
        while True:
            # Move computer paddle towards ball
            if self.__ball_x_velocity > 0:
                factor = randint(0, 2)
                if self.__paddle_B.paddle_pix[-1][1] - 2 < self.__ball_y:
                    self.__paddle_B.move_paddle(1, factor)
                elif self.__paddle_B.paddle_pix[0][1] > self.__ball_y:
                    self.__paddle_B.move_paddle(-1, factor)
            else:
                self.__paddle_B.paddle_pix_off = []
            yield

    def __update_player_paddle(self):
        while True:
            if self.__button_L.force() > 6 and self.__paddle_A.paddle_pix[0][1] > 1:
                self.__paddle_A.move_paddle(-1, 2)
            elif self.__button_L.force() > 2 and self.__paddle_A.paddle_pix[0][1] > 0:
                self.__paddle_A.move_paddle(-1, 1)
            elif self.__button_R.force() > 6 and self.__paddle_A.paddle_pix[-1][1] < self.__screen_height - 1:
                self.__paddle_A.move_paddle(1, 2)
            elif self.__button_R.force() > 2 and self.__paddle_A.paddle_pix[-1][1] < self.__screen_height:
                self.__paddle_A.move_paddle(1, 1)
            yield

    def __show_something_on_hub(self):
        while True:
            self.__hub.display.number(self.__score)
            yield

    def __init_game(self):
        self.__matrix.matrix_off()
        self.__hub.display.text("PONG", 200, 50)
        blocking_wait(1000)

        self.__hub.speaker.volume(35)  # set volume to non deafening

        # Ask for game settings
        setting = self.__gamecontrol.set_game_settings()
        if setting[0]:
            self.__hardgame_factor = 3
        else:
            self.__hardgame_factor = 2
        self.__game_speed = setting[1]

    def __init_pong(self):
        # Initialize game parameters
        self.__ball_x, self.__ball_y = self.__screen_width // 2, self.__screen_height // 2

        # Initialize or reset the control variables
        self.__score = 0
        self.__gameover = False

    def gameplay(self):
        self.__init_game()
        while self.__reset:
            self.__init_pong()
            while not self.__quit:
                tasks = [
                    self.__render_game(),
                    self.__update_player_paddle(),
                    self.__update_computer_paddle(),
                    self.__update_ball(),
                    self.__handle_ball_collisions(),
                    self.__show_something_on_hub()
                ]

                while not self.__gameover:
                    for t in tasks:
                        next(t)
                    blocking_wait(100)
                # Here starts gameover action
                self.__gamecontrol.gameover()
                blocking_wait(1500)  # wait one and a half seconds

                self.__quit = True
                blocking_wait(self.__game_speed)
            reset_values = self.__gamecontrol.reset_game()
            self.__quit = reset_values[0]
            self.__reset = reset_values[1]
        self.__matrix.matrix_off()


# Test the class
if __name__ == "__main__":
    ponggame = BrickPong(6, 6)
    ponggame.gameplay()

# Leave the next line empty to fullfil PEP 8
