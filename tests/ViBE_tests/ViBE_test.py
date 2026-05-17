import os
import unittest

from src.utils.config_readers.ReaderConfig import ReaderConfig
from src.utils.config_readers.ViBEConfig import ViBEConfig
import src.video_processing.vibe_extractor.vibe_extractor as vibe_extractor
from src.video_processing.input_reader import reader
from tests.test_utils.MaskListAssertions import TestMaskListAssertions


class ViBE_test(TestMaskListAssertions):
    def setUp(self):
        ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
        self.path_to_video = os.path.join(ROOT_DIR, r"tests\reader_tests\input_data\video.mp4")
        config = ReaderConfig.from_yaml(os.path.join(ROOT_DIR, r"tests\reader_tests\input_data\test_config.yml"))
        self.frames = reader.rsv_read_all(self.path_to_video, config)

        self.config = ViBEConfig.from_yaml(os.path.join(ROOT_DIR, r"tests\reader_tests\input_data\test_config.yml"))

    def test_vibe_single_channel(self):
        masks_native = vibe_extractor.native_process_single_channel(self.frames[:, :, :, 1], self.config)
        masks_pybind = vibe_extractor.pybind_process_single_channel(self.frames[:, :, :, 1], self.config)
        self.assertImagesAsEqual(masks_native, masks_pybind, msg="Error in reading for single channel, native and pybind implementations are not equal!")

    def test_vibe_three_channels(self):
        masks_native = vibe_extractor.native_process_three_channels(self.frames, self.config)
        masks_pybind = vibe_extractor.pybind_process_three_channels(self.frames, self.config)
        self.assertImagesAsEqual(masks_native, masks_pybind, msg="Error in reading for single channel, native and pybind implementations are not equal!")


if __name__ == '__main__':
    unittest.main()
