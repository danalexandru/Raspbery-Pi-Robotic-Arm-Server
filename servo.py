# region imports
# noinspection PyUnresolvedReferences
import Rpi.GPIO as GPIO

from globals import *
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
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.set_mode.__name__)
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
            console_log(error_message, LOG_ERROR, self.cleanup.__name__)
            return False

    def setup_input_pin(self, pin):
        """
        Description: This method sets a pin to be an \"INPUT\" pin

        :param pin: The GPIO physical pin number
        :return: Boolean (True or False)
        """
        try:
            GPIO.setup(pin, GPIO.IN)
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.setup_input_pin.__name__)
            return False

    def setup_output_pin(self, pin):
        """
        Description: This method sets a pin to be an \"OUTPUT\" pin

        :param pin: The GPIO physical pin number
        :return: Boolean (True or False)
        """
        try:
            GPIO.setup(pin, GPIO.OUT)
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.setup_output_pin.__name__)
            return False

    def set_gpio_pin_pwm(self, pin, frequency):
        """
        Description: This method sets the pulse-width modulation frequency of the GPIO pin

        :param pin: The GPIO physical pin number
        :param frequency: The frequency in Hz
        :return: Object (The GPIO.PWM object for a certain pin)
        """
        try:
            return GPIO.PWM(pin, frequency)
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.set_gpio_pin_pwm.__name__)
            return False

# endregion GPIOHandler


# region ServoMotor
class ServoMotorHandler(object):
    """
    Description: This class controls the servo motor functions
    """
    def __init__(self, pin=0, frequency=0, duty_cycle=0):
        try:
            self.pin = pin
            self.frequency = frequency
            self.duty_cycle = duty_cycle
            self.pwn_handler = None
            return

        except Exception as error_message:
            console_log(error_message, LOG_ERROR, 'ServoMotorHandler')
            return

    def initialize_gpio_pin_mode(self):
        """
        Description: This method set the servo motor pin in output mode

        :return: Boolean (True or False)
        """
        try:
            GPIOHandler().setup_output_pin(self.pin)
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.initialize_gpio_pin_mode.__name__)
            return False

    def set_gpio_pin_pwn(self):
        """
        Description: This method sets the servo motor PWM (\"pulse-width modulation\") handler

        :return: Boolean (True or False)
        """
        try:
            self.pwn_handler = GPIOHandler().set_gpio_pin_pwm(self.pin, self.frequency)
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.set_gpio_pin_pwn.__name__)
            return False

    def set_gpio_pin_change_duty_cycle(self, duty_cycle):
        """
        Description: This method updates the PWM handler \"duty cycle\"

        :param duty_cycle: The PWM duty cycle (Integer: 0 - 100)
        :return: Boolean (True or False)
        """
        try:
            self.duty_cycle = duty_cycle
            self.pwn_handler.ChangeDutyCycle(duty_cycle)
            return True

        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.set_gpio_pin_change_duty_cycle.__name__)
            return False

    def set_gpio_pin_frequency(self, frequency):
        """
        Description: This method updates the PWM handler \"frequency\"

        :param frequency: The PWM frequency (Integer)
        :return: Boolean (True or False)
        """
        try:
            self.frequency = frequency
            self.pwn_handler.ChangeFrequency(frequency)
            return True

        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.set_gpio_pin_frequency.__name__)
            return False
# endregion ServoMotor


# region servos
dict_servo_motors = {}
# endregion servos
