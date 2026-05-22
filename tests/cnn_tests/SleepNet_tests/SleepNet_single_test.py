import os
import unittest

import cv2

from src.cnn.SleepNet import classifier
from src.utils.config_readers.ReaderConfig import ReaderConfig
from src.utils.config_readers.ViBEConfig import ViBEConfig
import src.video_processing.vibe_extractor.vibe_extractor as vibe_extractor
from src.video_processing.input_reader import reader
from tests.test_utils.MaskListAssertions import TestMaskListAssertions


class SleepNet_single_test(unittest.TestCase):
    def setUp(self):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
        self.image0 = cv2.imread(os.path.join(ROOT_DIR, r'tests\cnn_tests\SleepNet_tests\input_data\single\0.png'))[..., 0]
        self.image1 = cv2.imread(os.path.join(ROOT_DIR, r'tests\cnn_tests\SleepNet_tests\input_data\single\1.png'))[..., 0]
        self.image2 = cv2.imread(os.path.join(ROOT_DIR, r'tests\cnn_tests\SleepNet_tests\input_data\single\2.png'))[..., 0]
        weights_path = os.path.join(ROOT_DIR, r"tests\cnn_tests\SleepNet_tests\input_data\weights.pth")
        self.predictor = predictor.SleepNetClassifier(weights_path)

    def test_pose_0(self):
        self.assertEqual(0,self.predictor.predict_single(self.image0), msg="Pose left_log for SleepNet for single frame processing does not match")

    def test_pose_1(self):
        self.assertEqual(1,self.predictor.predict_single(self.image1), msg="Pose right_log for SleepNet for single frame processing does not match")

    def test_pose_2(self):
        self.assertEqual(2,self.predictor.predict_single(self.image2),  msg="Pose supine for SleepNet for single frame processing does not match")



if __name__ == '__main__':
    unittest.main()
