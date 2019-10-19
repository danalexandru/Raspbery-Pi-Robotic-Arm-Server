"""
This file deals with all the image processing part of the project
"""

# region imports
# noinspection PyUnresolvedReferences
# import picamera
import datetime
import cv2

from enum import Enum
from globals import *
# endregion imports


# region PiCameraHandler
picamera = None


class PiCameraHandler(object):
    """
    This class is used in order to take an image of the chessboard, or film the chessboard
    """
    class FileFormat(Enum):
        IMAGE = 1
        VIDEO = 2

    def __init__(self):
        try:
            self.camera_handler = picamera.PiCamera()
            self.camera_handler.vflip = True
            self.camera_handler.resolution = (1024, 768)
            self.entity_name = None
            self.file_format = self.FileFormat

        except Exception as error_message:
            console_log(error_message, LOG_ERROR, 'PiCamera')

    def set_entity_name(self, file_format):
        """
        Description: This method sets the name of the file that will be saved, either in the \"images\" or \"videos\"
                     folder, depending on the file format

        :param file_format: The file format (taken from the "self.file_format" enum)
        :return: Boolean (True or False)
        """
        try:
            current_time = str(datetime.datetime.now().strftime('%Y%m%d_%H%M'))

            if file_format == self.file_format.IMAGE:
                self.entity_name = ('./images/pic_%s.jpg' % current_time)
            elif file_format == self.file_format.VIDEO:
                self.entity_name = ('./videos/vid_%s.h264' % current_time)
            else:
                console_log('Unknown file format %s' % str(file_format), LOG_WARNING, self.set_entity_name.__name__)
                return False

            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.set_entity_name.__name__)
            return False

    def capture_image(self):
        """
        Description: This method takes a picture and in \"jpg\" format and saves it in the \"images\" folder

        :return: Boolean (True or False)
        """
        try:
            self.set_entity_name(self.file_format.IMAGE)
            self.camera_handler.capture(self.entity_name)
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.capture_image.__name__)
            return False

    def start_recording(self):
        """
        Description: This method starts the video recording in \"h264\" format

        :return: Boolean (True or False)
        """
        try:
            self.set_entity_name(self.file_format.VIDEO)
            self.camera_handler.start_recording(self.entity_name)
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.start_recording.__name__)
            return False

    def stop_recording(self):
        """
        Description: This method stops the video recording and saves it in the \"videos\" folder

        :return: Boolean (True or False)
        """
        try:
            self.camera_handler.stop_recording()
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.stop_recording.__name__)
            return False

    def set_recording_time_frame(self, seconds):
        """
        Description: This method sets the delay until a video recording should stop

        :param seconds: The amount of time the video recording should last (in seconds)
        :return: Boolean (True or False)
        """
        try:
            self.camera_handler.wait_recording(seconds)
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.set_recording_time_frame.__name__)
            return False


pi_camera_handler = PiCameraHandler()
# endregion PiCameraHandler


# region OpenCVHandler
class OpenCVHandler(object):
    """
    This class will determine the chess positions on the board
    """
    def __init__(self):
        try:
            self.width = 800
            self.height = 600

            self.image_path = None
            self.title = None
            self.is_RGB = False

            self.inner_corners = []

            self.image = None
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, 'OpenCVHandler')

    def set_debug_mode(self):
        """
        Description: This method is used for debug purposes. It calls an image from the \"images\" folder in grayscale
                     mode

        :return: Boolean (True of False)
        """
        try:
            self.image_path = './images/debug_chessboard.jpg'
            self.title = 'Debug chessboard'
            self.is_RGB = False

            self.image = cv2.imread(self.image_path, self.is_RGB)
            self.image = cv2.resize(self.image, (self.width, self.height))

            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.set_debug_mode.__name__)
            return False

    def show_image(self):
        """
        Description: This method is used to show an the image image uploaded into the "self.image" handler using openCV

        :return: Boolean (True or False)
        """
        try:
            for inner_corner in self.inner_corners:
                cv2.circle(self.image,
                           (inner_corner['y'], inner_corner['x']),
                           3,
                           (255, 0, 0),
                           -1)

            cv2.imshow(self.title, self.image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.show_image.__name__)
            return False

    def find_chessboard_inner_corners(self):
        """
        Description: This method finds the position of the inner chessboard corners

        :return: Boolean (True or False)
        """
        try:
            self.inner_corners = []
            (ret, corners) = cv2.findChessboardCorners(self.image, (7, 7))

            for corner in corners:
                (y, x) = corner.ravel()
                self.inner_corners.append({
                    'x': x,
                    'y': y
                })

            self.sort_chessboard_inner_corners(self.inner_corners)
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.find_chessboard_inner_corners.__name__)
            return False

    def sort_chessboard_inner_corners(self, inner_corners):
        """
        This function sorts the chessboard inner corners from the top-left corner to the bottom-right corner

        :return: Boolean (True or False)
        """
        try:
            # sort by rows
            k = False
            while k is False:
                k = True
                for index in range(0, len(inner_corners) - 1):
                    if inner_corners[index]['x'] > inner_corners[index + 1]['x']:
                        (inner_corners[index], inner_corners[index + 1]) = \
                            (inner_corners[index + 1], inner_corners[index])
                        k = False

            # sort by columns
            k = False
            while k is False:
                k = True
                for index in range(0, len(inner_corners) - 1):
                    if inner_corners[index]['x'] >= inner_corners[index + 1]['x'] and \
                            inner_corners[index]['y'] > inner_corners[index + 1]['y']:
                        (inner_corners[index], inner_corners[index + 1]) = \
                            (inner_corners[index + 1], inner_corners[index])
                        k = False

            self.inner_corners = inner_corners
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.sort_chessboard_inner_corners.__name__)
            return False


openCV_handler = OpenCVHandler()
# endregion OpenCVHandler
