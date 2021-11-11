import mediapipe as mp
import numpy as np
import cv2


class Segmentation:
    def __init__(self):
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.mask = None
        self.bg_color = (0, 0, 0)
        self.fg_color = (255, 255, 255)

    def get_mask(self, frame):
        """
        Get segmentation mask from the frame
        :param frame: Frame obtained from the video stream
        :return: Segmentation mask
        """
        try:
            with self.mp_selfie_segmentation.SelfieSegmentation(
                    model_selection=1) as selfie_segmentation:

                frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                frame.flags.writeable = False
                results = selfie_segmentation.process(frame)
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                condition = np.stack((results.segmentation_mask,), axis=-1) > 0
                self.mask = np.where(condition, self.fg_color, self.bg_color)

            return self.mask, frame
        except Exception as e:
            raise e
