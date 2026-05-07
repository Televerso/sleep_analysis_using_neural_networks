import os
import unittest

import src.video_processing.input_reader.Reader as Reader

from tests.test_utils.ImageListAssertions import TestImageListAssertions

class ReaderTest(TestImageListAssertions):

    def setUp(self):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
        self.path_to_video = os.path.join(ROOT_DIR, r"tests\reader_tests\input_data\video.mp4")
        self.gap = 5


    def test_reading_all_cv2_decord(self):
        self.assertImagesAsEqual(Reader.cv2_read_all(self.path_to_video),
                                 Reader.decord_read_all(self.path_to_video),
                                 msg="simple reader and decord reader are nor equal!")

    def test_reading_all_cv2_rsv(self):
        self.assertImagesAsEqual(Reader.cv2_read_all(self.path_to_video),
                                 Reader.rsv_read_all(self.path_to_video),
                                 msg="simple reader and rsv reader are nor equal!")

    def test_reading_all_cv2_gear(self):
        self.assertImagesAsEqual(Reader.cv2_read_all(self.path_to_video),
                                 Reader.gear_read_all(self.path_to_video),
                                 msg="simple reader and camgear reader are nor equal!")

    def test_reading_all_cv2_mp(self):
        self.assertImagesAsEqual(Reader.cv2_read_all(self.path_to_video),
                                 Reader.mp_read_all(self.path_to_video),
                                 msg="simple reader and multiprocessing reader are nor equal!")

    def test_reading_all_cv2_mpsm(self):
        self.assertImagesAsEqual(Reader.cv2_read_all(self.path_to_video),
                                 Reader.mpsm_read_all(self.path_to_video),
                                 msg="simple reader and shared memory multiprocessing reader are nor equal!")


    def test_reading_with_gaps_cv2_decord(self):
        self.assertImagesAsEqual(Reader.cv2_read_with_gap(self.path_to_video),
                                 Reader.decord_read_with_gap(self.path_to_video),
                                 msg="simple reader and decord reader are nor equal!")

    def test_reading_with_gaps_cv2_rsv(self):
        self.assertImagesAsEqual(Reader.cv2_read_with_gap(self.path_to_video),
                                 Reader.rsv_read_with_gap(self.path_to_video),
                                 msg="simple reader and rsv reader are nor equal!")

    def test_reading_with_gaps_cv2_gear(self):
        self.assertImagesAsEqual(Reader.cv2_read_with_gap(self.path_to_video),
                                 Reader.gear_read_with_gap(self.path_to_video),
                                 msg="simple reader and camgear reader are nor equal!")

    def test_reading_with_gaps_cv2_mp(self):
        self.assertImagesAsEqual(Reader.cv2_read_with_gap(self.path_to_video),
                                 Reader.mp_read_with_gap(self.path_to_video),
                                 msg="simple reader and multiprocessing reader are nor equal!")

    def test_reading_with_gaps_cv2_mpsm(self):
        self.assertImagesAsEqual(Reader.cv2_read_with_gap(self.path_to_video),
                                 Reader.mpsm_read_with_gap(self.path_to_video),
                                 msg="simple reader and multiprocessing reader are nor equal!")


if __name__ == '__main__':
    unittest.main()
