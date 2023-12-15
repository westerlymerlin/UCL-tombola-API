import cv2
from logmanager import logger
from settings import settings

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(settings['cameraID'])
        if not self.video.isOpened():
            logger.error('VideoCameraClass: No video camera found')
        else:
            logger.info('VideoCameraClass: Starting video camera')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
