import numpy as np
import src.video_processing.ViBE_extractor_native_py.vibe as vibe
from src.utils.file_functions.config_readers.ViBEConfig import ViBEConfig

def process_frames_single_channel(frames : list, config : ViBEConfig):
    N = config.N
    R = config.R
    _min = config.min
    phi = config.phi

    motion_masks = np.zeros_like(frames)
    samples = vibe.initial_background(frames[0,:,:], N)
    for i, frame in enumerate(frames):
        motion_masks[i], samples = vibe.vibe_detection(frame, samples, _min, N, R)

    return motion_masks


def process_frames_three_channels(frames: list, config: ViBEConfig):
    N = config.N
    R = config.R
    _min = config.min
    phi = config.phi

    motion_masks = np.zeros_like(frames[:,:,:,0])
    samples_ch0 = vibe.initial_background(frames[0, :, :, 0], N)
    samples_ch1 = vibe.initial_background(frames[0, :, :, 1], N)
    samples_ch2 = vibe.initial_background(frames[0, :, :, 2], N)

    for i, frame in enumerate(frames):
        segmap_ch0, samples_ch0 = vibe.vibe_detection(frame[:, :, 0], samples_ch0, _min, N, R)
        segmap_ch1, samples_ch1 = vibe.vibe_detection(frame[:, :, 1], samples_ch1, _min, N, R)
        segmap_ch2, samples_ch2 = vibe.vibe_detection(frame[:, :, 2], samples_ch2, _min, N, R)
        motion_masks[i] = segmap_ch0 | segmap_ch1 | segmap_ch2


    return motion_masks


