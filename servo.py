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
    def __init__(self, pin=0, frequency=50, duty_cycle=0, lower_limit=0, upper_limit=0, step=0):
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
# endregion ServoMotor


# region servos
dict_servo_motors = {
    'base': ServoMotorHandler(0, 50),
    'bottom_left': ServoMotorHandler(0, 50),
    'bottom_right': ServoMotorHandler(0, 50),
    'bottom_vertical': ServoMotorHandler(0, 50),
    'claw_vertical': ServoMotorHandler(0, 50),
    'claw_horizontal': ServoMotorHandler(0, 50),
    'claw': ServoMotorHandler(0, 50)
}
# endregion servos
