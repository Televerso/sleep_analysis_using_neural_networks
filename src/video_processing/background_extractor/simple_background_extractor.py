import numpy as np
import src.utils.basic_functions.BasicFunctions as bf
from src.utils.config_readers.BGSubstractorConfig import BGSubstractorConfig


class SimpleBackgroundExtractor:
    def __init__(self, image, config : BGSubstractorConfig):
        self.background_image = np.asarray(image)
        self.background_image[:,:,0] = bf.blur(np.asarray(image[:,:,0]), 5, 1)
        self.background_image[:,:,1] = bf.blur(np.asarray(image[:,:,1]), 5, 1)
        self.background_image[:,:,2] = bf.blur(np.asarray(image[:,:,2]), 5, 1)

        self.threshold = config.threshold

    def detect(self, image):
        curr_image = np.asarray(image)

        curr_image[:,:,0] = bf.blur(image[:,:,0], 5, 1)
        curr_image[:,:,1] = bf.blur(image[:,:,1], 5, 1)
        curr_image[:,:,2] = bf.blur(image[:,:,2], 5, 1)

        image_diff = np.abs(curr_image.astype(int) - self.background_image.astype(int))

        image_diff[image_diff < self.threshold] = 0
        image_diff[image_diff >= self.threshold] = 255

        image_diff = image_diff[:,:,0] | image_diff[:,:,1] | image_diff[:,:,2]

        return image_diff.astype('uint8')