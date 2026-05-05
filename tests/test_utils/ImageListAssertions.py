import unittest

import cv2
import numpy as np

from skimage.metrics import structural_similarity as ssim

class TestImageListAssertions(unittest.TestCase):
    def assertImagesAsEqual(self, list1, list2, msg=None):
        self.assertEqual(len(list1), len(list2), f"{msg}\n List lengths are different: {len(list1)} != {len(list2)}")

        for i, (img1, img2) in enumerate(zip(list1, list2)):
            self.assertEqual(img1.shape, img2.shape, f"{msg}\n Image shapes are different: {img1.shape} != {img2.shape} at index {i}")

            if not self.__frames_are_similar(img1, img2, 0.98):
                diff_mask = img1 != img2
                num_diffs = np.count_nonzero(diff_mask)
                max_diff = np.max(np.abs(img1.astype(float) - img2.astype(float)))
                self.fail(
                    f"{msg}\n "
                    f"Arrays at index {i} are not equal. "
                    f"Number of different pixels: {num_diffs}, "
                    f"Maximum difference: {max_diff}, "
                    f"Values of the first pixels: {img1[0,0]},{img2[0,0]}"
                )

    def __frames_are_similar(self, frame1, frame2, threshhold=0.99):
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        score = ssim(gray1, gray2)

        return score>=threshhold