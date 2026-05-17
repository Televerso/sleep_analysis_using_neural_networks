import VibeExtractor as ve
import numpy as np

from src.utils.config_readers.ViBEConfig import ViBEConfig

def pybind_process_single_channel(frames : list, config : ViBEConfig):
    N = config.N
    R = config.R
    _min = config.min
    phi = config.phi

    motion_masks = np.zeros_like(frames)
    ViBE = ve.VibeAlgorithm(frames[0,:,:].copy(),N,R,_min,phi)
    for i, frame in enumerate(frames):
        motion_masks[i] = ViBE.vibe_detection(frame.copy())

    return motion_masks


def pybind_process_three_channels(frames: list, config: ViBEConfig):
    N = config.N
    R = config.R
    _min = config.min
    phi = config.phi

    motion_masks = np.zeros_like(frames[:,:,:,0])
    ViBE_ch0 = ve.VibeAlgorithm(frames[0, :, :, 0], N, R, _min, phi)
    ViBE_ch1 = ve.VibeAlgorithm(frames[0, :, :, 1], N, R, _min, phi)
    ViBE_ch2 = ve.VibeAlgorithm(frames[0, :, :, 2], N, R, _min, phi)

    for i, frame in enumerate(frames):
        motion_masks[i]  = ViBE_ch0.vibe_detection(frame[:,:,0])
        motion_masks[i] |= ViBE_ch1.vibe_detection(frame[:,:,1])
        motion_masks[i] |= ViBE_ch2.vibe_detection(frame[:,:,2])

    return motion_masks


import numpy as np
import src.video_processing.vibe_extractor.ViBE_extractor_native_py.vibe as vibe
from src.utils.config_readers.ViBEConfig import ViBEConfig

def native_process_single_channel(frames : list, config : ViBEConfig):
    N = config.N
    R = config.R
    _min = config.min
    phi = config.phi

    motion_masks = np.zeros_like(frames)
    samples = vibe.initial_background(frames[0, :, :], N)
    for i, frame in enumerate(frames):
        motion_masks[i], samples = vibe.vibe_detection(frame, samples, _min, N, R)

    return motion_masks


def native_process_three_channels(frames: list, config: ViBEConfig):
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

