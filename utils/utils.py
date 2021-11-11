import cv2
import numpy as np


class Utils:
    def __init__(self):
        self.output_frame = None

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
            blurred_frame = cv2.GaussianBlur(frame, (55, 55), 0)
            self.output_frame = np.where(mask == 0, blurred_frame, frame)

            return self.output_frame
        except Exception as e:
            raise e

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
            self.output_frame = np.where(mask == 0, 0, frame)

            return self.output_frame
        except Exception as e:
            raise e

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
            image = cv2.imread(path)
            image = cv2.resize(image, (frame.shape[1], frame.shape[0]))
            self.output_frame = np.where(mask == 0, image, frame)

            return self.output_frame
        except Exception as e:
            raise e

