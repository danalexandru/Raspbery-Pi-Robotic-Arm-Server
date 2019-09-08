"""
This file is a debug file used in order to test the servo motor
"""


# region imports
# noinspection PyUnresolvedReferences
import Rpi.GPIO as GPIO
import atexit
from globals import *
# endregion imports


# region PwmHandler
class PwmHandler(object):
    """
    This class is used in order to call the PWM handler from the main function
    """
    def __init__(self):
        try:
            self.my_pwm = None
            self.pin = 0
            self.frequency = 0
            self.lower_limit = 1
            self.upper_limit = 2
            self.step = 0.01

            pulse_width_time_period = 1000 / self.frequency
            self.duty_cycle = (((self.lower_limit + self.upper_limit) / 2) * 100) / pulse_width_time_period

            return
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.__init__.__name__)
            return

    def start_my_pwm(self, pin=11, frequency=50):
        """
        Description: This method initializes the PWM handler

        :param pin: The GPIO servo pin number
        :param frequency: The GPIO PWM frequency
        :return: Boolean (True or False)
        """
        try:
            self.my_pwm = GPIO.PWM(pin, frequency)
            self.pin = pin
            self.frequency = frequency

            self.my_pwm.start(0)
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.start_my_pwm.__name__)
            return False

    def stop_my_pwm(self):
        """
        Description: This method stops the PWM method and cleans the GPIO pins setup

        :return: Boolean (True of False)
        """
        try:
            self.my_pwm.stop()
            GPIO.cleanup()
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.stop_my_pwm.__name__)
            return False

    def set_my_pwm_duty_cycle(self, direction):
        """
        Description: This methods rotates the servo motor to the left / right

        :param direction: (String) The direction of rotation (to the \"left\" / \"right\"
        :return: Boolean (True or False)
        """
        try:
            pulse_width_time_period = 1000 / self.frequency
            current_time_period = (self.duty_cycle * pulse_width_time_period) / 100

            if direction == 'left':
                new_position = current_time_period - self.step
                if new_position <= self.lower_limit:
                    console_log('The left limit has already been reached',
                                LOG_WARNING,
                                self.set_my_pwm_duty_cycle.__name__)
                    return False
            elif direction == 'right':
                new_position = current_time_period + self.step
                if new_position >= self.lower_limit:
                    console_log('The right limit has already been reached',
                                LOG_WARNING,
                                self.set_my_pwm_duty_cycle.__name__)
                    return False
            else:
                console_log('Unknown direction %s' % direction, LOG_WARNING, self.set_my_pwm_duty_cycle.__name__)
                return False

            duty_cycle = (new_position * 100) / pulse_width_time_period
            self.my_pwm.ChangeDutyCycle(duty_cycle)
            console_log('Duty cycle = %s) new_position = %s' % (str(self.duty_cycle), str(new_position)),
                        LOG_SUCCESS,
                        self.set_my_pwm_duty_cycle.__name__)
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.set_my_pwm_duty_cycle.__name__)
            return False


pwm_handler = PwmHandler()
# endregion PwmHandler


# region main
def main():
    """
    Description: This function has an infinite loop in which the user input is requested at any point in time in order
                change the servo motor position

    :return: Boolean (True or False)
    """
    try:
        pin = 11
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)

        pwm_handler.start_my_pwm()
        while True:
            # keyboard_input = input('Increment / Decrement servo? (\u2191, \u2193)')
            keyboard_input = input('%s\t Increment / Decrement servo? (w, s): %s' % (CODE_BLUE, CODE_WHITE))

            keyboard_input = keyboard_input.lower()
            console_log(keyboard_input, LOG_INFO, main.__name__)
            if keyboard_input == 'w':
                pwm_handler.set_my_pwm_duty_cycle('right')
            elif keyboard_input == 's':
                pwm_handler.set_my_pwm_duty_cycle('left')
            else:
                continue

    except Exception as error_message:
        console_log(error_message, LOG_WARNING, main.__name__)
        return False


@atexit.register
def at_exit_file():
    """
    Description: This function is called at the exit of the file

    :return: Boolean (True or False)
    """
    try:
        console_log('The debug file has been exited successfully.', LOG_SUCCESS, at_exit_file.__name__)
        pwm_handler.stop_my_pwm()

        return True
    except Exception as error_message:
        console_log(error_message, LOG_ERROR, at_exit_file.__name__)
        return False


if __name__ == '__main__':
    main()
# endregion main
