"""
Arcade Game BrickSnake for PortaBrick Arcade

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
from urandom import randint


class BrickSnake:
    """Implementation of the classic game "Snake" for the PortaBrick Arcade
    based on the Pybricks framework. As inspiration minor parts of the
    code of the game was generated by chat.openai.com and then adapted."""

    def __init__(self, display_res_x, display_res_y):
        # Basic variables
        self.__resolution = (display_res_x, display_res_y)
        self.__game_speed = 300  # work speed itself
        self.app_icon = "snake"
        self.app_name = "Snake"
        self.app_color = Color.ORANGE

        # Variables for game SNAKE
        self.__hardgame = False  # If True hitting the wall ends the game
        self.__direction = ()  # initial direction of snake
        self.__snake_head = ()  # snake head at game start
        self.__snake_body = []  # snake body at game start
        self.__lunch = ()
        self.__render_on = ()
        self.__render_off = []
        self.__snake_had_lunch = None

        self.loop = None  # Prevents a 180 degree turn on same.
        self.__game_counter = None
        self.__gameover = None
        self.__quit = False
        self.__reset = True

        # Initialize software and hardware
        self.__gamecontrol = GameControl(self.__resolution[0], self.__resolution[1], self.__game_speed)
        self.__matrix = MatrixHelper(self.__resolution[0], self.__resolution[1])  # initialize driver for matrix
        self.__hub = PrimeHub()  # initialize LEGO Spike Prime Hub
        self.__button_L = ForceSensor(Port.E)  # initialize LEGO Spike Prime Force Sensor as left button
        self.__button_R = ForceSensor(Port.F)  # initialize LEGO Spike Prime Force Sensor as right button
        self.__hub_buttons = []  # initialize variable that holds info about pressed button

    @staticmethod
    def __wait(time):
        """ Part of generator function for using parallel computing without threads.
            Source: https://github.com/orgs/pybricks/discussions/356 """
        timer = StopWatch()
        while timer.time() < time:
            yield

    def __input_buttons(self):
        # print("Get input")
        while True:
            # turn button taps to self.direction change
            if self.loop:
                if self.__button_L.touched():
                    # turn snake self.direction counter-clockwise
                    if self.__direction == (1, 0):  # from left to right
                        self.__direction = (0, -1)
                    elif self.__direction == (0, -1):  # from bottom to top
                        self.__direction = (-1, 0)
                    elif self.__direction == (-1, 0):  # from right to left
                        self.__direction = (0, 1)
                    elif self.__direction == (0, 1):  # from top to bottom
                        self.__direction = (1, 0)
                elif self.__button_R.touched():
                    # turn snake self.direction clockwise
                    if self.__direction == (1, 0):  # from left to right
                        self.__direction = (0, 1)
                    elif self.__direction == (0, 1):  # from top to bottom
                        self.__direction = (-1, 0)
                    elif self.__direction == (-1, 0):  # from right to left
                        self.__direction = (0, -1)
                    elif self.__direction == (0, -1):  # from bottom to top
                        self.__direction = (1, 0)
                self.loop = False
            yield

    def __show_something_on_hub(self):
        while True:
            self.__hub.display.number(self.__game_counter)
            yield

    def __overule_hardgame(self):
        if not self.__hardgame:
            if self.__snake_head[0] == 6 and self.__direction == (1, 0):
                # from left to right reaching screen boarder
                self.__snake_head = (self.__snake_head[0] - 6, self.__snake_head[1])
            elif self.__snake_head[1] == 6 and self.__direction == (0, 1):
                # from top to bottom reaching screen boarder
                self.__snake_head = (self.__snake_head[0], self.__snake_head[1] - 6)
            elif self.__snake_head[0] == -1 and self.__direction == (-1, 0):
                # from right to left reaching screen boarder
                self.__snake_head = (self.__snake_head[0] + 6, self.__snake_head[1])
            elif self.__snake_head[1] == -1 and self.__direction == (0, -1):
                # from bottom to top reaching screen boarder
                self.__snake_head = (self.__snake_head[0], self.__snake_head[1] + 6)

    def __check_gameover(self):
        while True:
            # print("Check gameover")
            if self.__snake_head[0] == -1 or \
                    self.__snake_head[1] == -1 or \
                    self.__snake_head[0] == self.__resolution[0] or \
                    self.__snake_head[1] == self.__resolution[1]:
                self.__gameover = True
                print(self.__gameover)
            yield

    def __check_snake_eats_itself(self):
        if self.__snake_head in self.__snake_body[1:]:
            self.__gameover = True

    def __check_snake_had_lunch(self):
        if self.__lunch == self.__snake_head:
            self.__hub.speaker.play_notes(["D2/8"], 200)
            self.__game_counter += 1
            self.__snake_had_lunch = True
            self.__lunch = (randint(0, self.__resolution[0] - 1), randint(0, self.__resolution[1] - 1))
        else:
            self.__snake_had_lunch = False

    def __snake_movement(self):
        while True:
            yield from self.__wait(self.__game_speed)
            self.__snake_head = (self.__snake_head[0] + self.__direction[0], self.__snake_head[1] + self.__direction[1])
            self.__overule_hardgame()
            self.__snake_body.insert(0, self.__snake_head)
            self.__check_snake_had_lunch()
            if not self.__snake_had_lunch:
                self.__render_off = list(self.__snake_body.pop())
            else:
                self.__render_off.clear()
            self.__render_on = self.__snake_body.copy()
            self.__check_snake_eats_itself()
            # prevent snake to make u-turn. Locks input for one movement cycle
            self.loop = True

    def __render_matrix_display(self):
        while True:
            # render lunch
            self.__matrix.pixel_on(self.__lunch[0], self.__lunch[1], Color.ORANGE)
            # render specific pixels off
            if self.__render_off:
                self.__matrix.pixel_off(self.__render_off[0], self.__render_off[1])
                self.__render_off.clear()
            # render snake's head
            self.__matrix.pixel_on(self.__render_on[0][0], self.__render_on[0][1], Color(h=235, s=80, v=60))
            # render snake's body
            for i in range(len(self.__render_on[1:])):
                self.__matrix.pixel_on(self.__render_on[i + 1][0], self.__render_on[i + 1][1], Color(h=235, s=80, v=50))
            yield

    def __init_game(self):
        self.__matrix.matrix_off()
        self.__hub.display.text("Snake", 200, 50)
        blocking_wait(1000)

        self.__hub.speaker.volume(35)  # set volume to non deafening

        # Ask for game settings
        setting = self.__gamecontrol.set_game_settings()
        self.__hardgame = setting[0]
        self.__game_speed = setting[1]

    def __init_snake(self):
        # Initialize snake and it's lunch
        self.__snake_head = (2, 2)  # snake head at game start
        self.__snake_body = [(1, 2), (0, 2)]  # snake body at game start
        self.__snake_body.insert(0, self.__snake_head)
        self.__render_on = self.__snake_body.copy()
        self.__lunch = (randint(0, self.__resolution[0] - 1),
                        randint(0, self.__resolution[1] - 1))  # initial position of lunch
        self.__direction = (1, 0)  # initial direction of snake
        self.__snake_had_lunch = False

        # Initialize or reset the control variables
        self.__game_counter = 0
        self.__gameover = False
        self.loop = True

    def gameplay(self):
        self.__init_game()
        while self.__reset:
            self.__init_snake()

            while not self.__quit:
                tasks = [
                    self.__render_matrix_display(),
                    self.__show_something_on_hub(),
                    self.__input_buttons(),
                    self.__snake_movement(),
                    self.__check_gameover()
                ]

                while not self.__gameover:
                    for t in tasks:
                        next(t)
                    blocking_wait(100)
                # Here starts gameover action
                self.__gamecontrol.gameover()
                blocking_wait(1500)  # wait one and a half seconds
                self.__matrix.matrix_off()  # clear the matrix
                self.__quit = True  # leave game loop
                blocking_wait(self.__game_speed)
            reset_values = self.__gamecontrol.reset_game()
            self.__quit = reset_values[0]
            self.__reset = reset_values[1]
        self.__matrix.matrix_off()


# Test the class
if __name__ == "__main__":
    snakegame = BrickSnake(6, 6)
    snakegame.gameplay()

# Leave the next line empty to fullfil PEP 8
