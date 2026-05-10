import os
import unittest

import src.video_processing.input_reader.Reader as Reader
from src.utils.file_functions.config_readers.ReaderConfig import ReaderConfig

from tests.test_utils.ImageListAssertions import TestImageListAssertions

class reader_test(TestImageListAssertions):

    def setUp(self):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
        self.path_to_video = os.path.join(ROOT_DIR, r"tests\reader_tests\input_data\video.mp4")
        self.config = ReaderConfig.from_yaml(os.path.join(ROOT_DIR, r"tests\reader_tests\input_data\test_config.yml"))


    def test_reading_all_cv2_decord(self):
        self.assertImagesAsEqual(Reader.cv2_read_all(self.path_to_video, self.config),
                                 Reader.decord_read_all(self.path_to_video, self.config),
                                 msg="simple reader and decord reader are nor equal!")

    def test_reading_all_cv2_rsv(self):
        self.assertImagesAsEqual(Reader.cv2_read_all(self.path_to_video, self.config),
                                 Reader.rsv_read_all(self.path_to_video, self.config),
                                 msg="simple reader and rsv reader are nor equal!")

    def test_reading_all_cv2_gear(self):
        self.assertImagesAsEqual(Reader.cv2_read_all(self.path_to_video, self.config),
                                 Reader.gear_read_all(self.path_to_video, self.config),
                                 msg="simple reader and camgear reader are nor equal!")

    def test_reading_all_cv2_mp(self):
        self.assertImagesAsEqual(Reader.cv2_read_all(self.path_to_video, self.config),
                                 Reader.mp_read_all(self.path_to_video, self.config),
                                 msg="simple reader and multiprocessing reader are nor equal!")

    def test_reading_all_cv2_mpsm(self):
        self.assertImagesAsEqual(Reader.cv2_read_all(self.path_to_video, self.config),
                                 Reader.mpsm_read_all(self.path_to_video, self.config),
                                 msg="simple reader and shared memory multiprocessing reader are nor equal!")

    def test_reading_all_cv2_pyav(self):
        self.assertImagesAsEqual(Reader.cv2_read_all(self.path_to_video, self.config),
                                 Reader.pyav_read_all(self.path_to_video, self.config),
                                 msg="simple reader and PyAV reader are nor equal!")


    def test_reading_with_gaps_cv2_decord(self):
        self.assertImagesAsEqual(Reader.cv2_read_with_gap(self.path_to_video, self.config),
                                 Reader.decord_read_with_gap(self.path_to_video, self.config),
                                 msg="simple reader and decord reader are nor equal!")

    def test_reading_with_gaps_cv2_rsv(self):
        self.assertImagesAsEqual(Reader.cv2_read_with_gap(self.path_to_video, self.config),
                                 Reader.rsv_read_with_gap(self.path_to_video, self.config),
                                 msg="simple reader and rsv reader are nor equal!")

    def test_reading_with_gaps_cv2_gear(self):
        self.assertImagesAsEqual(Reader.cv2_read_with_gap(self.path_to_video, self.config),
                                 Reader.gear_read_with_gap(self.path_to_video, self.config),
                                 msg="simple reader and camgear reader are nor equal!")

    def test_reading_with_gaps_cv2_mp(self):
        self.assertImagesAsEqual(Reader.cv2_read_with_gap(self.path_to_video, self.config),
                                 Reader.mp_read_with_gap(self.path_to_video, self.config),
                                 msg="simple reader and multiprocessing reader are nor equal!")

    def test_reading_with_gaps_cv2_mpsm(self):
        self.assertImagesAsEqual(Reader.cv2_read_with_gap(self.path_to_video, self.config),
                                 Reader.mpsm_read_with_gap(self.path_to_video, self.config),
                                 msg="simple reader and multiprocessing reader are nor equal!")

    def test_reading_with_gaps_cv2_pyav(self):
        self.assertImagesAsEqual(Reader.cv2_read_with_gap(self.path_to_video, self.config),
                                 Reader.pyav_read_with_gap(self.path_to_video, self.config),
                                 msg="simple reader and PyAV reader are nor equal!")


if __name__ == '__main__':
    unittest.main()
