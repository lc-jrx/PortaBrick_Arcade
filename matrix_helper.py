from pybricks.parameters import Color
from pybricks.pupdevices import ColorLightMatrix
from pybricks.tools import wait

from detect_devices import DetectDevices


class ResolutionException(Exception):
    def __init__(self, resolution):
        self.resolution = resolution


class MatrixHelper:
    """
    The MatrixHelper class controls the overall matrix consisting of 3x3 individual matrices.
    The number of matrices is freely selectable and is determined by the desired resolution.
    """
    __res_x = None
    __res_y = None

    def __init__(self, game_res_x, game_res_y):
        self.__matrix_id = None
        self.__new_y = None
        self.__new_x = None
        self.__res_x = game_res_x
        self.__res_y = game_res_y
        self.__pix_color = None

        detect_devices = DetectDevices()

        self.__matrix_available = detect_devices.matrix_available
        self.__matrix_ports = detect_devices.matrix_ports
        self.__matrix_count = int(self.__calc_matrix_count())

        # Check if available matrix modules fit to given resolution
        try:
            if self.__matrix_count > self.__matrix_available:
                print("\n"
                      "Given resolution does not match available matrix resolution.\n"
                      "Please adapt resolution or add",
                      self.__matrix_count - self.__matrix_available,
                      "more Spike ColorLightMatrix modules.\n")
                raise Exception
        except Exception:
            raise

        # Catch x or y equals 0, and x or y not multiples of 3
        try:
            if self.__res_x % 3 != 0 or self.__res_x == 0:
                raise ResolutionException(self.__res_x)
            elif self.__res_y % 3 != 0 or self.__res_y == 0:
                raise ResolutionException(self.__res_y)
        except ResolutionException as e:
            print('Resolution of ' + str(e) + ' pixel is not suitable for Spike ColorLightMatrix modules. '
                                              'Must not be 0 and must be a multiple of 3.')
            raise

        self.__pixels = []        # Empty list, will hold the lists of each module
        # self.pix_black = [[Color.NONE, Color.NONE, Color.NONE],
        #                   [Color.NONE, Color.NONE, Color.NONE],
        #                   [Color.NONE, Color.NONE, Color.NONE]]      # List with color info to turn module dark

        # Pre-set all pixels black (aka off), first initialize nested list
        for i in range(self.__matrix_count):
            # here each module get's its still empty pixel list linewise
            self.__pixels.append([[], [], []])
            # now fill the emty lists with default entries for black
            # self.pixels.append(self.pix_black.copy())
            # self.pixels.append(list(self.pix_black))
        self.matrix_off()

    def __recalc_coordinates(self, abs_x, abs_y):
        """Converts a coordinate of the given resolution to the coordinates of a
        single matrix of the display composed of matrix modules."""
        self.__new_x = abs_x - (abs_x // 3 * 3)
        self.__new_y = abs_y - (abs_y // 3 * 3)
        self.__matrix_id = (abs_y // 3 * self.__res_x / 3) + abs_x // 3
        return self.__new_x, self.__new_y, int(self.__matrix_id)

    def __calc_matrix_count(self):
        """Calculates the necessary number of individual modules from the given total resolution."""
        return (self.__res_x / 3) * (self.__res_y / 3)

    def __matrix2pixel(self, index):
        """Converts the given 'array' to a list"""
        dot = []
        for y in range(3):
            for x in range(3):
                dot.append(self.__pixels[index][y][x])
        return dot

    def pixel_on(self, input_x, input_y, input_color):
        temp = self.__recalc_coordinates(input_x, input_y)
        self.__pixels[temp[2]][temp[1]][temp[0]] = input_color
        ColorLightMatrix(self.__matrix_ports[temp[2]]).on(self.__matrix2pixel(temp[2]))

    def pixel_off(self, input_x, input_y):
        temp = self.__recalc_coordinates(input_x, input_y)
        self.__pixels[temp[2]][temp[1]][temp[0]] = Color.NONE
        ColorLightMatrix(self.__matrix_ports[temp[2]]).on(self.__matrix2pixel(temp[2]))

    def draw_pixel_graphic(self, picture, color):
        for i in range(len(picture)):
            self.pixel_on(picture[i][0], picture[i][1], color)

    def matrix_off(self):
        for i in range(self.__matrix_count):
            pix_black = [[Color.NONE, Color.NONE, Color.NONE],
                         [Color.NONE, Color.NONE, Color.NONE],
                         [Color.NONE, Color.NONE, Color.NONE]]
            self.__pixels[i] = pix_black.copy()
            ColorLightMatrix(self.__matrix_ports[i]).off()


if __name__ == "__main__":
    x_res = 6  # set resolution x
    y_res = 6  # set resolution y

    matrix = MatrixHelper(x_res, y_res)

    for y in range(y_res):
        for x in range(x_res):
            matrix.pixel_on(x, y, Color.RED)
            wait(150)

    for y in range(y_res):
        for x in range(x_res):
            matrix.pixel_off(x, y)
            wait(150)

    matrix.matrix_off()
