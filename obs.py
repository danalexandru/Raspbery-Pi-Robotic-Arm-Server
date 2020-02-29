"""
Description: This file has the OBS functionality (works alongside REST API)
"""

# region imports
from servo import dict_servo_motors, gpio_handler
from globals import console
# endregion imports


# region Methods
class Methods(object):
    """
    This is a class used for calling the methods from all the other scripts
    """
    def interpret_json(self, input_json):
        """
        This method interprets the json received from REST API

        :param input_json: (Dictionary) The JSON received that contains all the necessary data
        :return: Boolean (True or False)
        """
        try:
            mandatory_keys = {'motors'}
            if not mandatory_keys.issubset(input_json.keys()):
                console.log('Invalid keys. The JSON should contain the following keys: %s'
                            % str(mandatory_keys), console.LOG_WARNING)
                return False

            motors_list = input_json['motors']
            if self.validate_key('gpio_init', input_json) is True:
                if self.initialize_motors(motors_list) is False:
                    return False

            if self.validate_key('gpio_cleanup', input_json):
                if self.stop_motors(motors_list) is False:
                    return False

            if self.validate_key('duty_cycle', input_json):
                if self.change_duty_cycle(motors_list) is False:
                    return False

            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False

    def validate_key(self, key, input_json):
        """
        This method is used in order to validate whether or not a key exists and is True

        :param key: (String) The input_json key that is being validated
        :param input_json: (Dictionary) The JSON received that contains all the necessary data
        :return: Boolean (True or False)
        """
        try:
            return key in input_json.keys() and input_json[key] is True

        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)

    def initialize_motors(self, motors_list):
        """
        This method initializes the GPIO pins, the GPIO mode and all the motors with their own pwm_handler

        :param motors_list: (List) A list containing dictionaries with all the relevant information related to the motors
            [{
                'name': <String>,
                'duty_cycle': <Number>
            }]
        :return: Boolean (True or False)
        """
        try:
            gpio_handler.set_mode()
            for motor in motors_list:
                dict_servo_motors[motor['name']].initialize_gpio_pin_mode()
                dict_servo_motors[motor['name']].set_gpio_pin_pwn()

            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False

    def stop_motors(self, motors_list):
        """
        This method stops all the GPIO motors and clears the GPIO pins

        :param motors_list: (List) A list containing dictionaries with all the relevant information related to the motors
            [{
                'name': <String>,
                'duty_cycle': <Number>
            }]
        :return: Boolean (True or False)
        """
        try:
            for motor in motors_list:
                dict_servo_motors[motor['name']].stop_pwm_handler()

            gpio_handler.cleanup()
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False

    def change_duty_cycle(self, motors_list):
        """
        This method changes the duty cycles for all of the motors

        :param motor_list: (List) List of Dictionaries containing the motor key and duty cycle
        :return: Boolean (True or False)
        """
        try:
            for motor in motors_list:
                dict_servo_motors[motor['name']].set_gpio_pin_duty_cycle(motor['duty_cycle'])

            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR)
            return False


methods_handler = Methods()
# endregion Methods
