"""
This file deals with all the image processing part of the project
"""

# region imports
# noinspection PyUnresolvedReferences
import picamera
import datetime

from enum import Enum
from globals import *
# endregion imports


# region PiCameraHandler
class PiCameraHandler(object):

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

    def set_entity_name(self, format):
        try:
            current_time = str(datetime.datetime.now().strftime('%Y%m%d_%H%M'))

            if format == self.file_format.IMAGE:
                self.entity_name = ('./images/pic_%s.jpg' % current_time)
            elif format == self.file_format.VIDEO:
                self.entity_name = ('./videos/vid_%s.h264' % current_time)
            else:
                console_log('Unknown file format %s' % str(format), LOG_WARNING, self.set_entity_name.__name__)
                return False

            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.set_entity_name.__name__)
            return False

    def capture_image(self):
        try:
            self.set_entity_name(self.file_format.IMAGE)
            self.camera_handler.capture(self.entity_name)
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.capture_image.__name__)
            return False

    def start_recording(self):
        try:
            self.set_entity_name(self.file_format.VIDEO)
            self.camera_handler.start_recording(self.entity_name)
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.start_recording.__name__)
            return False

    def stop_recording(self):
        try:
            self.camera_handler.stop_recording()
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.stop_recording.__name__)
            return False

    def set_recording_time_frame(self, seconds):
        try:
            self.camera_handler.wait_recording(seconds)
            return True
        except Exception as error_message:
            console_log(error_message, LOG_ERROR, self.set_recording_time_frame.__name__)
            return False


pi_camera_handler = PiCameraHandler()
# endregion PiCameraHandler

