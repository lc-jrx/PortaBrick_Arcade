from pybricks.iodevices import PUPDevice
from pybricks.parameters import Port
from uerrno import ENODEV


class NotRunException(Exception):
    def __init__(self):
        print("Before detecting devices run port scan.")


class DetectDevices:
    """ Class to detect which devices are connected to which port.
        Basis taken from: https://docs.pybricks.com/en/latest/iodevices/pupdevice.html#detecting-devices"""

    def __init__(self):
        self.matrix_available = 0
        self.matrix_ports = []
        self.device_names = None
        self.__ports = None
        self.__scan_ports()
        self.__detect_matrixes()

    def __scan_ports(self):
        # Dictionary of device identifiers along with their name.
        self.device_names = {
            # pybricks.pupdevices.DCMotor
            1: "Wedo 2.0 Medium Motor",
            2: "Powered Up Train Motor",
            # pybricks.pupdevices.Light
            8: "Powered Up Light",
            # pybricks.pupdevices.Motor
            38: "BOOST Interactive Motor",
            46: "Technic Large Motor",
            47: "Technic Extra Large Motor",
            48: "SPIKE Medium Angular Motor",
            49: "SPIKE Large Angular Motor",
            65: "SPIKE Small Angular Motor",
            75: "Technic Medium Angular Motor",
            76: "Technic Large Angular Motor",
            # pybricks.pupdevices.TiltSensor
            34: "Wedo 2.0 Tilt Sensor",
            # pybricks.pupdevices.InfraredSensor
            35: "Wedo 2.0 Infrared Motion Sensor",
            # pybricks.pupdevices.ColorDistanceSensor
            37: "BOOST Color Distance Sensor",
            # pybricks.pupdevices.ColorSensor
            61: "SPIKE Color Sensor",
            # pybricks.pupdevices.UltrasonicSensor
            62: "SPIKE Ultrasonic Sensor",
            # pybricks.pupdevices.ForceSensor
            63: "SPIKE Force Sensor",
            # pybricks.pupdevices.ColorLightMatrix
            64: "SPIKE 3x3 Color Light Matrix",
        }

        # Make a list of known ports.
        self.__ports = [Port.A, Port.B]

        # On hubs that support it, add more ports.
        try:
            self.__ports.append(Port.C)
            self.__ports.append(Port.D)
        except AttributeError:
            pass

        # On hubs that support it, add more ports.
        try:
            self.__ports.append(Port.E)
            self.__ports.append(Port.F)
        except AttributeError:
            pass

        # print("Detected Ports", self.ports)
        # print("Matrixes: ", self.matrix_available)
        # print("Matrix Ports: ", self.matrix_ports)

    def __detect_matrixes(self):
        try:
            if self.__ports is None:
                raise NotRunException
            elif self.device_names is None:
                raise NotRunException
        except NotRunException:
            raise

        # Go through all available ports.
        for port in self.__ports:

            # Try to get the device, if it is attached.
            try:
                device = PUPDevice(port)
            except OSError as ex:
                if ex.args[0] == ENODEV:
                    # No device found on this port.
                    # print(port, ": ---")
                    continue
                else:
                    raise

            # Get the device id
            device_id = device.info()["id"]

            # Look up the name.
            # try:
            #     print(port, ":", self.device_names[device_id], 'ID:', device_id)
            # except KeyError:
            #     print(port, ":", "Unknown device with ID", device_id)

            # Register the count of ColorLightMatrix modules and its ports
            if device_id == 64:
                self.matrix_available += 1
                # ColorLightMatrix(port).on(Color.YELLOW)
                # print("Matrixes: ", self.matrix_available)
                self.matrix_ports.append(port)
                # wait(500)
                # ColorLightMatrix(port).off()


if __name__ == "__main__":
    testrun = DetectDevices()
    print("Matrixes: ", testrun.matrix_available)
    print("Matrix Ports: ", testrun.matrix_ports)
