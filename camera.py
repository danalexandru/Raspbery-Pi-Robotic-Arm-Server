"""
This file deals with all the image processing part of the project
"""

# region imports
# noinspection PyUnresolvedReferences
# import picamera
import datetime
import cv2

from enum import Enum
from globals import console
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
            console.log(error_message, console.LOG_ERROR, 'PiCamera')

    def set_entity_name(self, file_format):
        """
        This method sets the name of the file that will be saved, either in the \"images\" or \"videos\"
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
                console.log('Unknown file format %s' % str(file_format), console.LOG_WARNING, self.set_entity_name.__name__)
                return False

            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.set_entity_name.__name__)
            return False

    def capture_image(self):
        """
        This method takes a picture and in \"jpg\" format and saves it in the \"images\" folder

        :return: Boolean (True or False)
        """
        try:
            self.set_entity_name(self.file_format.IMAGE)
            self.camera_handler.capture(self.entity_name)
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.capture_image.__name__)
            return False

    def start_recording(self):
        """
        This method starts the video recording in \"h264\" format

        :return: Boolean (True or False)
        """
        try:
            self.set_entity_name(self.file_format.VIDEO)
            self.camera_handler.start_recording(self.entity_name)
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.start_recording.__name__)
            return False

    def stop_recording(self):
        """
        This method stops the video recording and saves it in the \"videos\" folder

        :return: Boolean (True or False)
        """
        try:
            self.camera_handler.stop_recording()
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.stop_recording.__name__)
            return False

    def set_recording_time_frame(self, seconds):
        """
        This method sets the delay until a video recording should stop

        :param seconds: The amount of time the video recording should last (in seconds)
        :return: Boolean (True or False)
        """
        try:
            self.camera_handler.wait_recording(seconds)
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.set_recording_time_frame.__name__)
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

            self.image = None

            self.inner_corners = []
            self.outer_corners = []
            self.all_corners = []

            self.chessboard_positions = []

            self.sort_tolerance = 1
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, 'OpenCVHandler')

    def set_debug_mode(self):
        """
        This method is used for debug purposes. It calls an image from the \"images\" folder in grayscale
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
            console.log(error_message, console.LOG_ERROR, self.set_debug_mode.__name__)
            return False

    def show_image(self):
        """
        This method is used to show an the image image uploaded into the "self.image" handler using openCV

        :return: Boolean (True or False)
        """
        try:
            for corner in self.all_corners:
                cv2.circle(self.image,
                           (int(corner['x']), int(corner['y'])),
                           3,
                           (255, 0, 0),
                           -1)

            while True:
                cv2.imshow(self.title, self.image)
                cv2.setMouseCallback(self.title, get_mouse_position)
                k = cv2.waitKey(0)
                if k == -1:
                    break

            cv2.destroyAllWindows()
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.show_image.__name__)
            return False

    def find_chessboard_inner_corners(self):
        """
        This method finds the position of the inner chessboard corners

        :return: Boolean (True or False)
        """
        try:
            self.inner_corners = []
            (ret, corners) = cv2.findChessboardCorners(self.image, (7, 7))

            for corner in corners:
                (x, y) = corner.ravel()
                self.inner_corners.append({
                    'x': x,
                    'y': y
                })

            self.sort_chessboard_corners(self.inner_corners, 'inner_corners')
            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.find_chessboard_inner_corners.__name__)
            return False

    def find_chessboard_outer_corners(self):
        """
        This method finds the position of the outer corners chessboard corners

        :return: Boolean (True or False)
        """
        try:
            self.outer_corners = []

            x_mean = []
            y_mean = []

            first_index = 0
            last_index = 6

            for i in range(7):
                x = []
                y = []

                x_dif = []
                y_dif = []

                for j in range(7):
                    x.append(self.inner_corners[i*7 + j]['x'])
                    y.append(self.inner_corners[i + j*7]['y'])

                for j in range(6):
                    x_dif.append(abs(x[j + 1] - x[j]))
                    y_dif.append(abs(y[j + 1] - y[j]))

                x_mean.append(sum(x_dif)/len(x_dif))
                y_mean.append(sum(y_dif)/len(y_dif))

            # append the 4 extreme corners of the board
            self.outer_corners.append({
                'x': self.inner_corners[first_index]['x'] - x_mean[first_index],
                'y': self.inner_corners[first_index]['y'] - y_mean[first_index]
            })
            self.outer_corners.append({
                'x': self.inner_corners[first_index + last_index]['x'] + x_mean[first_index],
                'y': self.inner_corners[first_index + last_index]['y'] - y_mean[last_index]
            })
            self.outer_corners.append({
                'x': self.inner_corners[last_index*7]['x'] - x_mean[last_index],
                'y': self.inner_corners[last_index*7]['y'] + y_mean[first_index]
            })
            self.outer_corners.append({
                'x': self.inner_corners[last_index*8]['x'] + x_mean[last_index],
                'y': self.inner_corners[last_index*8]['y'] + y_mean[last_index]
            })

            # append the first row
            for i in range(7):
                self.outer_corners.append({
                    'x': self.inner_corners[i]['x'],
                    'y': self.inner_corners[i]['y'] - y_mean[i]
                })
                self.outer_corners.append({
                    'x': self.inner_corners[i*7]['x'] - x_mean[i],
                    'y': self.inner_corners[i*7]['y']
                })
                self.outer_corners.append({
                    'x': self.inner_corners[i*7 + last_index]['x'] + x_mean[i],
                    'y': self.inner_corners[i*7 + last_index]['y']
                })
                self.outer_corners.append({
                    'x': self.inner_corners[i + last_index*7]['x'],
                    'y': self.inner_corners[i + last_index*7]['y'] + y_mean[i]
                })

            self.sort_chessboard_corners(self.outer_corners, 'outer_corners')
            for corner in self.outer_corners:
                corner['x'] = round(corner['x'], 4)
                corner['y'] = round(corner['y'], 4)

            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.find_chessboard_inner_corners.__name__)
            return False

    def find_chessboard_all_corners(self):
        """
        This method takes the inner corners and outer corners found previously and appends them into the same list

        :return: Boolean (True or False)
        """
        try:
            # append first row
            for i in range(9):
                self.all_corners.append(self.outer_corners[i])

            # append every row except the last one
            for i in range(7):
                self.all_corners.append(self.outer_corners[9 + 2*i])

                for j in range(7):
                    self.all_corners.append(self.inner_corners[i*7 + j])

                self.all_corners.append(self.outer_corners[9 + 2*i + 1])

            for i in range(9):
                self.all_corners.append(self.outer_corners[i + 23])

            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.find_chessboard_all_corners.__name__)
            return False

    def sort_chessboard_corners(self, corners, list_label=None):
        """
        This function sorts the chessboard inner corners from the top-left corner to the bottom-right corner

        :param corners: (List) The list of corners that needs to be ordered accordingly
        :param list_label: (String) The list of corners which was sorted ('inner_corners' or 'outer_corners')
        :return: Boolean (True or False)
        """
        try:
            # sort by rows
            k = False
            while k is False:
                k = True
                for index in range(0, len(corners) - 1):
                    if corners[index]['y'] > corners[index + 1]['y']:
                        (corners[index], corners[index + 1]) = \
                            (corners[index + 1], corners[index])
                        k = False

            # sort by columns
            k = False
            while k is False:
                k = True
                for index in range(0, len(corners) - 1):
                    if abs(corners[index]['y'] - corners[index + 1]['y']) <= self.sort_tolerance and \
                            corners[index]['x'] > corners[index + 1]['x']:
                        (corners[index], corners[index + 1]) = \
                            (corners[index + 1], corners[index])
                        k = False

            if list_label is None or list_label == 'inner_corners':
                self.inner_corners = corners
            elif list_label == 'outer_corners':
                self.outer_corners = corners
            else:
                console.log('Unrecognized list_label %s. It should be either \'inner_corners\' or \'outer_corners\'' %
                            str(list_label),
                            console.LOG_WARNING,
                            self.sort_chessboard_corners.__name__)
                return False

            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.sort_chessboard_corners.__name__)
            return False

    def get_chessboard_positions_location(self):
        """
        This method used the all corners parameter in order to get the location of every square from the chessboard

        :return: Boolean (True or False)
        """
        try:
            for i in range(8):
                current_row = []
                for j in range(8):
                    current_row.append({
                        'upper_left': self.all_corners[i*9 + j],
                        'upper_right': self.all_corners[i*9 + j + 1],
                        'lower_left': self.all_corners[(i + 1)*9 + j],
                        'lower_right': self.all_corners[(i + 1)*9 + j + 1]
                    })

                self.chessboard_positions.append(current_row)

            return True
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.get_chessboard_positions_location.__name__)
            return False

    def highlight_position(self, row, col):
        """
        This method highlights a position on the chessboard

        :param row: (Integer) The x chessboard position (Values: 0 - 7)
        :param col: (Integer) The y chessboard position(Values: 0 - 7)
        :return: Boolean (True or False)
        """
        try:
            if row not in range(8):
                console.log('Invalid %s value for \'row\'. It should be between [0 - 7].' % row,
                            console.LOG_WARNING,
                            self.highlight_position.__name__)
                return False

            if col not in range(8):
                console.log('Invalid %s value for \'col\'. It should be between [0 - 7].' % col,
                            console.LOG_WARNING,
                            self.highlight_position.__name__)
                return False

            high_pos = self.chessboard_positions[row][col]
            cv2.rectangle(self.image,
                          (int(high_pos['lower_left']['x']), int(high_pos['lower_left']['y'])),
                          (int(high_pos['upper_right']['x']), int(high_pos['upper_right']['y'])),
                          (255, 0, 0),
                          3)
        except Exception as error_message:
            console.log(error_message, console.LOG_ERROR, self.highlight_position.__name__)
            return False


openCV_handler = OpenCVHandler()
# endregion OpenCVHandler


# region local functions
def get_mouse_position(event, x, y, flags, param):
    """
    This function prints the current mouse position on the image

    :param event: (Object) The current event that was performed using the mouse
    :param x: (Integer) The current X position on the image
    :param y: (Integer) The current Y position on the image
    :param flags: -
    :param param: -
    :returns: Boolean (True or False)
    """
    try:
        if event == cv2.EVENT_LBUTTONDOWN:
            console.log('Mouse position: (%d, %d)' % (x, y), console.LOG_INFO, get_mouse_position.__name__)

        return True
    except Exception as error_message:
        console.log(error_message, console.LOG_ERROR, get_mouse_position.__name__)
        return False
# endregion local functions
