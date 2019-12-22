"""
This file is a debug file used in order to test the servo motor and the image processing
"""

# region imports
# noinspection PyUnresolvedReferences
# import RPi.GPIO as GPIO
import atexit
import time

from camera import pi_camera_handler, openCV_handler
from globals import console

# endregion imports


# region PwmHandler
GPIO = None


class PwmHandler(object):
    """
    This class is used in order to call the PWM handler from the main function
    """

    def __init__(self):
        try:
            self.my_pwm = None
            self.pin = 11
            self.frequency = 50
            self.lower_limit = 1
            self.upper_limit = 2
            self.step = 0.01

            pulse_width_time_period = 1000 / self.frequency
            self.duty_cycle = (((self.lower_limit + self.upper_limit) / 2) * 100) / pulse_width_time_period
            console.log('duty cycle = %s' % str(self.duty_cycle), console.LOG_INFO, self.__init__.__name__)
            return
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.__init__.__name__)
            return

    def start_my_pwm(self, pin=11, frequency=50):
        """
        This method initializes the PWM handler

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
            console.log(error_message, console.LOG_ERROR, self.start_my_pwm.__name__)
            return False

    def stop_my_pwm(self):
        """
        This method stops the PWM method and cleans the GPIO pins setup

        :return: Boolean (True of False)
        """
        try:
            self.my_pwm.stop()
            GPIO.cleanup()
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.stop_my_pwm.__name__)
            return False

    def set_my_pwm_duty_cycle(self, direction):
        """
        This methods rotates the servo motor to the left / right

        :param direction: (String) The direction of rotation (to the \"left\" / \"right\"
        :return: Boolean (True or False)
        """
        try:
            pulse_width_time_period = 1000 / self.frequency
            current_time_period = (self.duty_cycle * pulse_width_time_period) / 100

            if direction == 'left':
                new_position = current_time_period - self.step
                if new_position <= self.lower_limit:
                    console.log('The left limit has already been reached',
                                console.LOG_WARNING,
                                self.set_my_pwm_duty_cycle.__name__)
                    return False
            elif direction == 'right':
                new_position = current_time_period + self.step
                if new_position >= self.upper_limit:
                    console.log('The right limit has already been reached',
                                console.LOG_WARNING,
                                self.set_my_pwm_duty_cycle.__name__)
                    return False
            else:
                console.log('Unknown direction %s' % direction, console.LOG_WARNING,
                            self.set_my_pwm_duty_cycle.__name__)
                return False

            duty_cycle = (new_position * 100) / pulse_width_time_period
            self.duty_cycle = duty_cycle

            self.my_pwm.ChangeDutyCycle(duty_cycle)
            console.log('Duty cycle = %s) new_position = %s' % (str(self.duty_cycle), str(new_position)),
                        console.LOG_SUCCESS,
                        self.set_my_pwm_duty_cycle.__name__)
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.set_my_pwm_duty_cycle.__name__)
            return False


pwm_handler = PwmHandler()


# endregion PwmHandler


# region servo
def servo():
    """
    This function has an infinite loop in which the user input is requested at any point in time in order
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
            keyboard_input = input('%s\t Increment / Decrement servo? (\"w\", \"s\"): %s' %
                                   (
                                       console.get_color_code(console.LOG_INFO),
                                       console.get_color_code(console.LOG_DEFAULT)
                                   )
                                   )

            keyboard_input = keyboard_input.lower()
            console.log(keyboard_input, console.LOG_INFO, main.__name__)
            if keyboard_input == 'w':
                pwm_handler.set_my_pwm_duty_cycle('right')
            elif keyboard_input == 's':
                pwm_handler.set_my_pwm_duty_cycle('left')
            else:
                continue

    except Exception as error_message:
        console.log(error_message, console.LOG_ERROR, servo.__name__)
        return False


# endregion servo


# region camera
def camera():
    """
    This function is used to test the functionality of the \"camera\" module

    :return: Boolean (True or False)
    """
    try:
        while True:
            keyboard_input = input('%s\t Camera functionality (\"image\" / \"video\"): %s' %
                                   (
                                       console.get_color_code(console.LOG_INFO),
                                       console.get_color_code(console.LOG_DEFAULT)
                                   )
                                   )
            keyboard_input = str(keyboard_input).lower()

            if keyboard_input == 'image':
                pi_camera_handler.capture_image()
            elif keyboard_input == 'video':
                pi_camera_handler.start_recording()
                pi_camera_handler.set_recording_time_frame(10)
                pi_camera_handler.stop_recording()
            else:
                continue

    except Exception as error_message:
        console.log(error_message, console.LOG_ERROR, camera.__name__)
        return False


# endregion camera


# region openCV
def openCV():
    """
    This function tests the functionality of the openCV functionality which looks at the chess board in order to find the
    desired squares

    :returns: Boolean (True or False)
    """
    try:
        # openCV_handler = OpenCVHandler()
        openCV_handler.set_debug_mode()
        openCV_handler.find_chessboard_inner_corners()
        openCV_handler.find_chessboard_outer_corners()
        openCV_handler.show_image()

        return True
    except Exception as error_message:
        console.log(error_message, console.LOG_ERROR, main.__name__)
        return False


# endregion openCV


# region main
def main():
    """
    This function is used in order to select the component that is going to be debugged

    :return: Boolean (True or False)
    """
    try:
        keyboard_input = input('%s\t Debug Component ('
                               '\"servo\" / '
                               '\"camera\" / '
                               '\"opencv\"): %s' % (
                                   console.get_color_code(console.LOG_INFO),
                                   console.get_color_code(console.LOG_DEFAULT)
                               )
                               )

        keyboard_input = str(keyboard_input).lower()

        if keyboard_input == 'servo':
            servo()
        elif keyboard_input == 'camera':
            camera()
        elif keyboard_input == 'opencv':
            openCV()
        else:
            return False

        return True
    except Exception as error_message:
        console.log(error_message, console.LOG_ERROR, main.__name__)
        return False


@atexit.register
def at_exit_file():
    """
    This function is called at the exit of the file

    :return: Boolean (True or False)
    """
    try:
        console.log('The debug file has been exited successfully.', console.LOG_SUCCESS, at_exit_file.__name__)
        pwm_handler.stop_my_pwm()
        return True
    except Exception as error_message:
        console.log(error_message, console.LOG_ERROR, at_exit_file.__name__)
        return False


if __name__ == '__main__':
    main()
# endregion main
