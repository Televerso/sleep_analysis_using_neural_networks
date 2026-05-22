import numpy as np

from src.utils.config_readers.BGSubstractorConfig import BGSubstractorConfig
from src.video_processing.background_extractor.simple_background_extractor import SimpleBackgroundExtractor


def substract_background(frames, config : BGSubstractorConfig):
    starting_frame = None

    if config.use_first_or_last_frame_as_the_model == 'first': starting_frame = frames[0]
    elif config.use_first_or_last_frame_as_the_model == 'last': starting_frame = frames[-1]
    else: raise ValueError('Invalid value for use_first_or_last_frame_as_the_model')

    bg_substractor = SimpleBackgroundExtractor(starting_frame, config)
    masks = np.asarray(frames[:,:,:,0])

    for i, frame in enumerate(frames):
        masks[i] = bg_substractor.detect(frame)

    return masks

