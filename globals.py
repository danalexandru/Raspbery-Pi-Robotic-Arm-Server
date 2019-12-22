"""
This file has flags and methods that are used all throwout the project
"""
# region imports
import traceback
import sys
import ntpath


# endregion imports


# region RestErrorMessageHandler
class RestErrorMessageHandler(object):
    """
    This class is used in order to send the error_message back to the client throw the REST server
    """

    def __init__(self):
        self.last_error_message = None

    def set_last_error_message(self, error_message):
        """
        Description: This method sets saves the last given error message into the \'last_error_message\' local variable

        :param error_message: The last error message given
        :return: Boolean (True or False)
        """
        self.last_error_message = error_message

    def get_last_error_message(self):
        """
        Description: This method returns the last given error_message

        :return: Boolean (True or False)
        """
        return self.last_error_message


rest_error_message_handler = RestErrorMessageHandler()


# endregion RestErrorMessageHandler


# region class Console
class Console(object):
    """
    This class is used in order to print color coded messages:
    -
    """

    def __init__(self):
        self._traceback_step = -2

        # region console log flags
        self.LOG_ERROR = 0x00
        self.LOG_WARNING = 0x01
        self.LOG_SUCCESS = 0x02
        self.LOG_INFO = 0x03
        self.LOG_DEFAULT = 0x04
        # endregion console log flags

        # region messages color codes
        self._CODE_RED = '\033[1;31;49m'
        self._CODE_YELLOW = '\033[1;33;49m'
        self._CODE_GREEN = '\033[1;32;49m'
        self._CODE_BLUE = '\033[1;34;49m'
        self._CODE_WHITE = '\033[1;39;49m'
        self._CODE_HIGHLIGHT = '\033[1;95;49m'
        self._CODE_DEFAULT = '\033[1;39;49m'
        # endregion messages color codes

    def log(self, message, priority=None, location=None):
        """
        Function used to return color coded error messages, along with the location

        :param message: message (String)
        :param location:  message location (String)
        :param priority: the message type (Integer)
        :return: Boolean (True of False)
        """
        try:
            message = str(message).capitalize()

            if sys.exc_info()[-1] is not None:
                line_number = str(sys.exc_info()[-1].tb_lineno)
            else:
                line_number: ''

            if location is None:
                location = ''

            rest_error_message = '{rest_error_message}'
            if priority == self.LOG_ERROR:
                print('%s\t Error (%s:%s):%s %s' % (self._CODE_RED, location, line_number, self._CODE_WHITE, message))
                rest_error_message = ('Error(%s): %s' % (location, message))
            elif priority == self.LOG_WARNING:
                print('%s\t Warning (%s:%s):%s %s' % (
                    self._CODE_YELLOW, location, line_number, self._CODE_WHITE, message))
                rest_error_message = ('Warning(%s): %s' % (location, message))

            elif priority == self.LOG_SUCCESS:
                print(
                    '%s\t Success (%s:%s):%s %s' % (self._CODE_GREEN, location, line_number, self._CODE_WHITE, message))
                rest_error_message = ('Success(%s): %s' % (location, message))

            elif priority == self.LOG_INFO:
                print('%s\t Info (%s:%s):%s %s' % (self._CODE_BLUE, location, line_number, self._CODE_WHITE, message))
                rest_error_message = ('Info(%s): %s' % (location, message))

            elif priority is None:
                print('%s\t %s' % (self._CODE_WHITE, message))
                rest_error_message = message

            rest_error_message_handler.set_last_error_message(rest_error_message)
            return True

        except Exception as error_message:
            print('%s\t Error: %s %s' % (self._CODE_RED, self._CODE_WHITE, str(error_message)))
            rest_error_message = ('Error (console_log): %s' % error_message)
            rest_error_message_handler.set_last_error_message(rest_error_message)
            return False

    def get_color_code(self, priority=None):
        """
        This method returns the color code for a certain LOG priority

        :param priority: The log priority (LOG_DEFAULT by default)
        :returns: (String) The color code
        """
        try:
            if priority is None or priority == self.LOG_DEFAULT:
                return self._CODE_WHITE

            if priority == self.LOG_ERROR:
                return self._CODE_RED
            elif priority == self.LOG_WARNING:
                return self._CODE_YELLOW
            elif priority == self.LOG_SUCCESS:
                return self._CODE_GREEN
            elif priority == self.LOG_INFO:
                return self._CODE_BLUE
            else:
                return self._CODE_DEFAULT

        except Exception as error_message:
            self.log(error_message, self.LOG_ERROR, self.get_color_code.__name__)
            return False


console = Console()
# endregion class Console
