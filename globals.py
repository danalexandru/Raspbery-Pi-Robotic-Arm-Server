"""
This file has flags and methods that are used all throwout the project
"""

# region global variables
import sys

# region console log flags
LOG_ERROR = 0x00
LOG_WARNING = 0x01
LOG_SUCCESS = 0x02
LOG_INFO = 0x03
# endregion console log flags


# region messages color codes
CODE_RED = '\033[1;31;40m'
CODE_YELLOW = '\033[1;33;40m'
CODE_GREEN = '\033[1;32;40m'
CODE_BLUE = '\033[1;34;40m'
CODE_WHITE = '\033[1;37;40m'


# endregion


# endregion global variables


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


# region global functions
def console_log(message, priority=None, location=None):
    """
    Description: Function used to return color coded error messages, along with the location

    :param message: message (String)
    :param location:  message location (String)
    :param priority: the message type (Integer)
    :return: Boolean (True of False)
    """
    try:
        message = str(message)
        line_number = str(sys.exc_info()[-1].tb_lineno)

        if location is None:
            location = ''

        rest_error_message = '{rest_error_message}'
        if priority == LOG_ERROR:
            print('%s\t Error (%s:%s):%s %s' % (CODE_RED, location, line_number, CODE_WHITE, message))
            rest_error_message = ('Error(%s): %s' % (location, message))
        elif priority == LOG_WARNING:
            print('%s\t Warning (%s:%s):%s %s' % (CODE_YELLOW, location, line_number, CODE_WHITE, message))
            rest_error_message = ('Warning(%s): %s' % (location, message))

        elif priority == LOG_SUCCESS:
            print('%s\t Success (%s:%s):%s %s' % (CODE_GREEN, location, line_number, CODE_WHITE, message))
            rest_error_message = ('Success(%s): %s' % (location, message))

        elif priority == LOG_INFO:
            print('%s\t Info (%s:%s):%s %s' % (CODE_BLUE, location, line_number, CODE_WHITE, message))
            rest_error_message = ('Info(%s): %s' % (location, message))

        elif priority is None:
            print('%s\t %s' % (CODE_WHITE, message))
            rest_error_message = message

        rest_error_message_handler.set_last_error_message(rest_error_message)
        return True

    except Exception as error_message:
        print('%s\t Error: %s %s' % (CODE_RED, CODE_WHITE, str(error_message)))
        rest_error_message = ('Error (console_log): %s' % error_message)
        rest_error_message_handler.set_last_error_message(rest_error_message)
        return False
# endregion global functions
