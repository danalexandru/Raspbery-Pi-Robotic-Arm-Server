# region global variables


# region console log flags
LOG_ERROR       =   0x00
LOG_WARNING     =   0x01
LOG_SUCCESS     =   0x02
LOG_INFO        =   0x03
# endregion console log flags


# region messages color codes
CODE_RED        =   "\033[1;31;40m"
CODE_YELLOW     =   "\033[1;33;40m"
CODE_GREEN      =   "\033[1;32;40m"
CODE_BLUE       =   "\033[1;34;40m"
CODE_WHITE      =   "\033[1;37;40m"
# endregion


# endregion global variables


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

        if location is None:
            location = ""

        if priority == LOG_ERROR:
            print("%s\t Error (%s):%s %s" % (CODE_RED, location, CODE_WHITE, message))

        elif priority == LOG_WARNING:
            print("%s\t Warning (%s):%s %s" % (CODE_YELLOW, location, CODE_WHITE, message))

        elif priority == LOG_SUCCESS:
            print("%s\t Success (%s):%s %s" % (CODE_GREEN, location, CODE_WHITE, message))

        elif priority == LOG_INFO:
            print("%s\t Info (%s):%s %s" % (CODE_BLUE, location, CODE_WHITE, message))

        elif priority is None:
            print("%s\t %s" % (CODE_WHITE, message))

        return True

    except Exception as error_message:
        print("%s\t Error: %s %s" % (CODE_RED, CODE_WHITE, str(error_message)))
        return False
