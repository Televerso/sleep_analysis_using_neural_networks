import VibeExtractor as ve
import numpy as np

from src.utils.config_readers.ViBEConfig import ViBEConfig

def process_frames_single_channel(frames : list, config : ViBEConfig):
    N = config.N
    R = config.R
    _min = config.min
    phi = config.phi

    motion_masks = np.zeros_like(frames)
    ViBE = ve.VibeAlgorithm(frames[0,:,:].copy(),N,R,_min,phi)
    for i, frame in enumerate(frames):
        motion_masks[i] = ViBE.vibe_detection(frame.copy())

    return motion_masks


def process_frames_three_channels(frames: list, config: ViBEConfig):
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


