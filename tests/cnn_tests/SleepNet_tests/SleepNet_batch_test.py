import os
import unittest

import cv2
import numpy as np

from src.cnn.SleepNet import predictor
from src.utils.config_readers.ReaderConfig import ReaderConfig
from src.utils.config_readers.ViBEConfig import ViBEConfig
import src.video_processing.vibe_extractor.vibe_extractor as vibe_extractor
from src.video_processing.input_reader import reader
from tests.test_utils.MaskListAssertions import TestMaskListAssertions


class SleepNet_batch_test(unittest.TestCase):
    def setUp(self):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
        weights_path = os.path.join(ROOT_DIR, r"tests\cnn_tests\SleepNet_tests\input_data\weights.pth")

        n = len(os.listdir(os.path.join(ROOT_DIR, r"tests/cnn_tests/SleepNet_tests/input_data/batch/")))
        self.images = np.empty(shape=(n,64,64), dtype=np.uint8)
        for i in range(n):
            self.images[i] = cv2.imread(os.path.join(ROOT_DIR, r'tests\cnn_tests\SleepNet_tests\input_data\batch', f"{str(i)}.png"))[..., 0]

        self.predictor = predictor.SleepNetPredictor(weights_path)

    def test_batch(self):
        results = self.predictor.predict_batch(self.images)
        for i, res in enumerate(results):
            self.assertEqual(i%3,res, msg=f"Mask with index {i} does not match for batch processing for cnn SleepNet")




if __name__ == '__main__':
    unittest.main()
