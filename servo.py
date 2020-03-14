"""
This file has all the methods used to control the servo motors (including all the GPIO handler)
"""

# region imports
# noinspection PyUnresolvedReferences
import RPi.GPIO as GPIO

from globals import console


# endregion imports


# region GPIOHandler
class GPIOHandler(object):
    """
    Description: This class is used in order to handle low level use of the GPIO pins
    """

    def set_mode(self):
        """
        Description: This method is used to set the GPIO pin mode (The way in which the GPIO pins are mapped and called)

        :return: Boolean (True or False)
        """
        try:
            GPIO.setmode(GPIO.BOARD)
            # GPIO.setmode(GPIO.BCM)
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.set_mode.__name__)
            return False

    def setup_input_pin(self, pin):
        """
        Description: This method sets a pin to be an \"INPUT\" pin

        :param pin: (Integer) The GPIO physical pin number
        :return: Boolean (True or False)
        """
        try:
            GPIO.setup(pin, GPIO.IN)
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.setup_input_pin.__name__)
            return False

    def cleanup(self):
        """
        Description This method cleans the memory allocation of any pins used throwout the project (required on exit)

        :return: Boolean (True or False)
        """
        try:
            GPIO.cleanup()
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.cleanup.__name__)
            return False

    def setup_output_pin(self, pin):
        """
        Description: This method sets a pin to be an \"OUTPUT\" pin

        :param pin: (Integer) The GPIO physical pin number
        :return: Boolean (True or False)
        """
        try:
            GPIO.setup(pin, GPIO.OUT)
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.setup_output_pin.__name__)
            return False

    def set_gpio_pin_pwm(self, pin, frequency):
        """
        Description: This method sets the pulse-width modulation frequency of the GPIO pin

        :param pin: (Integer) The GPIO physical pin number
        :param frequency: (Float) The frequency in Hz
        :return: Object (The GPIO.PWM object for a certain pin)
        """
        try:
            return GPIO.PWM(pin, frequency)
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.set_gpio_pin_pwm.__name__)
            return False


gpio_handler = GPIOHandler()


# endregion GPIOHandler


# region ServoMotor
class ServoMotorHandler(object):
    """
    This class controls the servo motor functions
    """

    def __init__(self, pin=0, frequency=50, duty_cycle=5, lower_limit=2, upper_limit=10, step=0.1):
        """
        This constructor initializes the servo motor object

        :param pin: (Integer) The GPIO physical pin number
        :param frequency: (Float) The PWM frequency
        :param duty_cycle: (Integer: 0 - 100) The PWM duty cycle
        :param lower_limit: (Float) The lower limit of the PWM time period limit
        :param upper_limit: (Float) The upper limit of the PWM time period limit
        :param step: (Float) The step for incrementing / decrementing the PWM duty cycle
        """
        try:
            self.pin = pin
            self.frequency = frequency
            self.duty_cycle = duty_cycle
            self.pwn_handler = None

            self.lower_limit = lower_limit
            self.upper_limit = upper_limit
            self.step = step

            self.dict_duty_cycle_xy_consts = {
                'upper': {
                    'left': {
                        'x': 0,
                        'y': 0
                    },
                    'right': {
                        'x': 0,
                        'y': 0
                    }
                },
                'lower': {
                    'left': {
                        'x': 0,
                        'y': 0
                    },
                    'right': {
                        'x': 0,
                        'y': 0
                    }
                },
                'percentage': 1 / 7
            }

            self.duty_cycle_z_consts = {
                'upper': 0,
                'lower': 0
            }

            return

        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, 'ServoMotorHandler')
            return

    def initialize_gpio_pin_mode(self):
        """
        This method set the servo motor pin in output mode

        :return: Boolean (True or False)
        """
        try:
            gpio_handler.setup_output_pin(self.pin)
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.initialize_gpio_pin_mode.__name__)
            return False

    def set_gpio_pin_pwn(self):
        """
        This method sets the servo motor PWM (\"pulse-width modulation\") handler

        :return: Boolean (True or False)
        """
        try:
            self.pwn_handler = gpio_handler.set_gpio_pin_pwm(self.pin, self.frequency)
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.set_gpio_pin_pwn.__name__)
            return False

    def set_gpio_pin_duty_cycle(self, duty_cycle):
        """
        This method updates the PWM handler \"duty cycle\"

        :param duty_cycle: (Integer: 0 - 100) The PWM duty cycle
        :return: Boolean (True or False)
        """
        try:
            self.duty_cycle = duty_cycle
            self.pwn_handler.ChangeDutyCycle(duty_cycle)
            return True

        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.set_gpio_pin_duty_cycle.__name__)
            return False

    def set_gpio_pin_frequency(self, frequency):
        """
        This method updates the PWM handler \"frequency\"

        :param frequency: (Float) The PWM frequency
        :return: Boolean (True or False)
        """
        try:
            self.frequency = frequency
            self.pwn_handler.ChangeFrequency(frequency)
            return True

        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.set_gpio_pin_frequency.__name__)
            return False

    def set_gpio_pwm_limits(self, lower_limit=None, upper_limit=None):
        """
        This method sets the PWM time period limits

        :param lower_limit: (Float) The lower limit of the PWM time period
        :param upper_limit: (Float) The upper limit of the PWM time period
        :return: Boolean (True or False)
        """
        try:
            if lower_limit is not None:
                self.lower_limit = lower_limit

            if upper_limit is not None:
                self.upper_limit = upper_limit

            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.set_gpio_pwm_limits.__name__)
            return False

    def rotate_left(self):
        """
        This method rotated the servo motor to the left side

        :return: Boolean (True or False)
        """
        try:
            pulse_width_time_period = 1000 / self.frequency
            current_time_period = (self.duty_cycle * pulse_width_time_period) / 100

            if current_time_period - self.step <= self.lower_limit:
                console.log('The left limit has already been reached', console.LOG_WARNING, self.rotate_left.__name__)
                return False

            duty_cycle = ((current_time_period - self.step) * 100) / pulse_width_time_period
            self.set_gpio_pin_duty_cycle(duty_cycle)

            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.rotate_left.__name__)
            return False

    def rotate_right(self):
        """
        This method rotated the servo motor to the right side

        :return: Boolean (True or False)
        """
        try:
            pulse_width_time_period = 1000 / self.frequency
            current_time_period = (self.duty_cycle * pulse_width_time_period) / 100

            if current_time_period + self.step <= self.lower_limit:
                console.log('The right limit has already been reached', console.LOG_WARNING, self.rotate_right.__name__)
                return False

            duty_cycle = ((current_time_period + self.step) * 100) / pulse_width_time_period
            self.set_gpio_pin_duty_cycle(duty_cycle)

            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.rotate_left.__name__)
            return False

    def stop_pwm_handler(self):
        """
        This method stops the PWM handler and cleans the memory allocation of any pins used throwout the
                     project (required on exit)

        :return: Boolean (True or False)
        """
        try:
            self.pwn_handler.stop()
            gpio_handler.cleanup()

            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_WARNING, self.stop_pwm_handler.__name__)
            return False

    def set_dict_duty_cycle__xy_consts(self, dict_duty_cycle_xy_consts):
        """
        This method initializes the duty cycle constants necessary in order to reach the extreme corners of the
        chessboard

        :param dict_duty_cycle_xy_consts: (Dictionary) A dictionary containing the (x, y) values of the upper corners
                'upper': {
                    'left': {
                        'x': <Number>,
                        'y': <Number>
                    },
                    'right': {
                        'x': <Number>,
                        'y': <Number>
                    }
                },
                'lower': {
                    'left': {
                        'x': <Number>,
                        'y': <Number>
                    },
                    'right': {
                        'x': <Number>,
                        'y': <Number>
                    }
                },
                'percentage': <Number>
            }
        :return: Boolean (True or False)
        """
        try:
            vertical_mandatory_keys = {'upper', 'lower'}
            horizontal_mandatory_keys = {'left', 'right'}

            if not vertical_mandatory_keys.issubset(dict_duty_cycle_xy_consts) or \
                    not horizontal_mandatory_keys.issubset(dict_duty_cycle_xy_consts['upper']) or \
                    not horizontal_mandatory_keys.issubset(dict_duty_cycle_xy_consts['lower']):
                console.log('Invalid dictionary keys. It should contain %s. Also, each key should contain another'
                            'dictionary with the %s keys.' % (
                                str(vertical_mandatory_keys),
                                str(horizontal_mandatory_keys)
                            ),
                            console.LOG_WARNING)
                return False

            self.dict_duty_cycle_xy_consts = dict_duty_cycle_xy_consts
            if 'percentage' not in self.dict_duty_cycle_xy_consts.keys():
                self.dict_duty_cycle_xy_consts['percentage'] = 1.7
                
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False

    def get_dict_duty_cycle_xy_consts_values(self):
        """
        This method returns the values of dict_duty_cycle_xy_consts in a more easily accessible format

        :return: (List) a list containing the dict_duty_cycle_xy_consts values in the following order
        [
            upper_left_x,
            upper_left_y,
            upper_right_x,
            upper_right_y,
            lower_left_x,
            lower_left_y,
            lower_right_x,
            lower_right_y
        ]
        """
        try:
            return [
                self.dict_duty_cycle_xy_consts['upper']['left']['x'],
                self.dict_duty_cycle_xy_consts['upper']['left']['y'],

                self.dict_duty_cycle_xy_consts['upper']['right']['x'],
                self.dict_duty_cycle_xy_consts['upper']['right']['y'],

                self.dict_duty_cycle_xy_consts['lower']['left']['x'],
                self.dict_duty_cycle_xy_consts['lower']['left']['y'],

                self.dict_duty_cycle_xy_consts['lower']['right']['x'],
                self.dict_duty_cycle_xy_consts['lower']['right']['y']
            ]
        except Exception as error_message:
            console.log(error_message, console.LOG_WARNING)
            return False

    @staticmethod
    def rule_of_three(initial_value, final_value, x):
        """
        This method used the rule of three in order to determine the value for x. It is assumed that there is a
        linear correlation between x and y of the form: a*x + b = y, where x = [1 - 8] and y = [initial_value,
        final_value].

        :param initial_value: (Number) The y value for x = 1
        :param final_value: (Number) The y value for x = 8
        :param x: (Integer) The current x value (Default: [1 - 8])
        :return: (Number) The y value for x
        """
        try:
            a = (final_value - initial_value) / 7
            b = initial_value - a

            return a*x + b
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False

    def find_duty_cycles(self, position):
        """
        This method determines the duty cycle necessary to reach the current position, both for horizontal and vertical
        movement. Only one of these values will actually be used in the movement sync (depending on the motor location),
        but for universality both cases will be calculated.

        :param position: (Dictionary) A dictionary containing the chess piece position on the chessboard
        {
            'x': <Integer> (Default: [1 - 8]),
            'y': <Integer> (Default: [1 - 8])
        }
        :return: (Dictionary) The 2 calculated duty cycles for cet motor
        {
            'x': <Number>,
            'y': <Number>
        }
        """
        try:
            mandatory_keys = {'x', 'y'}
            if not mandatory_keys.issubset(position):
                console.log('Invalid dictionary keys. They should be %s.' % str(mandatory_keys), console.LOG_WARNING)
                return False

            # retrieve the dict_duty_cycle_xy_consts values
            [xul, yul, xur, yur, xll, yll, xlr, ylr] = self.get_dict_duty_cycle_xy_consts_values()
            p = self.dict_duty_cycle_xy_consts['percentage']

            [x, y] = [position['x'], position['y']]
            dict_upper = {
                'x': self.rule_of_three(xul, xur, x),
                'y': self.rule_of_three(yul, yur, y)
            }

            dict_lower = {
                'x': self.rule_of_three(xll, xlr, x),
                'y': self.rule_of_three(yll, ylr, y)
            }

            return {
                'x': (p * (x - 1) * dict_upper['x']) + ((1 - p) * (x - 1) * dict_lower['x']),
                'y': (p * (y - 1) * dict_upper['y']) + ((1 - p) * (y - 1) * dict_lower['y'])
            }

        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False

    def set_duty_cycle_z_consts(self, duty_cycle_z_consts):
        """
        This method initializes the duty cycle constants necessary in order to lift or lower a chesspiece

        :param duty_cycle_z_consts: (Dictionary) A dictionary containing the (x, y) values of the upper corners
                'upper': <Number>
                'lower': <Number>
            }
        :return: Boolean (True or False)
        """
        try:
            mandatory_keys = {'upper', 'lower'}

            if not mandatory_keys.issubset(duty_cycle_z_consts):
                console.log('Invalid dictionary keys. It should contain %s.' % str(mandatory_keys), console.LOG_WARNING)
                return False

            self.duty_cycle_z_consts = duty_cycle_z_consts
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False
# endregion ServoMotor


# region servos
dict_servo_motors = {
    'base': ServoMotorHandler(pin=13, frequency=50, duty_cycle=5, lower_limit=2, upper_limit=10, step=0.1),
    'bottom_left': ServoMotorHandler(pin=3, frequency=50, duty_cycle=5, lower_limit=2, upper_limit=10, step=0.1),
    'bottom_right': ServoMotorHandler(pin=15, frequency=50, duty_cycle=5, lower_limit=2, upper_limit=10, step=0.1),
    'bottom_vertical': ServoMotorHandler(pin=11, frequency=50, duty_cycle=5, lower_limit=2, upper_limit=10, step=0.1),
    'claw_vertical': ServoMotorHandler(pin=7, frequency=50, duty_cycle=5, lower_limit=2, upper_limit=10, step=0.1),
    'claw_left': ServoMotorHandler(pin=5, frequency=50, duty_cycle=5, lower_limit=2, upper_limit=10, step=0.1),
    'claw': ServoMotorHandler(pin=0, frequency=50, duty_cycle=5, lower_limit=2, upper_limit=10, step=0.1)
}
# endregion servos
