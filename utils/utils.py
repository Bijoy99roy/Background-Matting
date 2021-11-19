import cv2
import numpy as np
from application_logging.logger import AppLogger


class Utils:
    def __init__(self):
        self.output_frame = None
        self.logger = AppLogger()
        self.logger.database.connect_db()
        self.collection_name = 'utils_handler'

    def blur_background(self, mask, frame):
        """
        Blur the background of the frame
        parameters
        ----------------------
        mask: Extracted binary mask from the frame
        frame: Input frame from the video stream
        :return: blurred background image
        """
        try:
            # self.logger.log(self.collection_name, "Blurring the background", "Info")
            blurred_frame = cv2.GaussianBlur(frame, (55, 55), 0)
            self.output_frame = np.where(mask == 0, blurred_frame, frame)

            return self.output_frame
        except Exception as e:
            self.logger.log(self.collection_name,
                            f"An exception has occured while blurring the background. Message: {str(e)}",
                            "Error")

    def remove_background(self, mask, frame):
        """
        Completely removing the background of the image.
        parameters
        ----------------------
        mask: Extracted binary mask from the frame
        frame: Input frame from the video stream
        :return:
        """
        try:
            # self.logger.log(self.collection_name, f"Removing the background.", "Info")
            self.output_frame = np.where(mask == 0, 0, frame)

            return self.output_frame
        except Exception as e:
            self.logger.log(self.collection_name,
                            f"An exception has occured while removing the background. Message: {str(e)}",
                            "Error")

    def change_background(self, mask, frame, path):
        """
        Change the background of the incoming frame
        parameters
        ----------------------
        mask: Extracted binary mask from the frame
        frame: Input frame from the video stream
        path: The image to replace background with
        :return:
        """
        try:
            # self.logger.log(self.collection_name, "Changing the background", "Info")
            image = cv2.imread(path)
            image = cv2.resize(image, (frame.shape[1], frame.shape[0]))
            self.output_frame = np.where(mask == 0, image, frame)

            return self.output_frame
        except Exception as e:
            self.logger.log(self.collection_name,
                            f"An exception has occured while changing background. Message: {str(e)}",
                            "Error")
