import unittest

import cv2
import numpy as np

from skimage.metrics import structural_similarity as ssim

class TestMaskListAssertions(unittest.TestCase):
    def assertImagesAsEqual(self, list1, list2, msg=None):
        self.assertEqual(len(list1), len(list2), f"{msg}\n List lengths are different: {len(list1)} != {len(list2)}")

        for i, (img1, img2) in enumerate(zip(list1, list2)):
            self.assertEqual(img1.shape, img2.shape, f"{msg}\n Mask shapes are different: {img1.shape} != {img2.shape} at index {i}")

            if not self.__frames_are_similar(img1, img2, 0.99):
                diff_mask = img1 != img2
                num_diffs = np.count_nonzero(diff_mask)
                self.fail(
                    f"{msg}\n "
                    f"Arrays at index {i} are not equal. "
                    f"Number of different pixels: {num_diffs}, "
                    f"Values of the first pixels: {img1[0,0]},{img2[0,0]}"
                )

    def __frames_are_similar(self, frame1, frame2, threshhold=0.99):
        score = ssim(frame1, frame2)

        return score>=threshhold