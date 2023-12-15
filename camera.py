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
            self.video.set(cv2.CAP_PROP_FPS, settings['cameraFPS'])
            self.video.set(cv2.CAP_PROP_FRAME_WIDTH, settings['cameraWidth'])
            self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, settings['cameraHeight'])
            self.video.set(cv2.CAP_PROP_EXPOSURE, settings['cameraExposure'])
            logger.info('Video FPS %s' % self.video.get(cv2.CAP_PROP_FPS))
            logger.info('Video Width %s' % self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
            logger.info('Video Height %s' % self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            logger.info('Video Exposure %s' % self.video.get(cv2.CAP_PROP_EXPOSURE))


    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
