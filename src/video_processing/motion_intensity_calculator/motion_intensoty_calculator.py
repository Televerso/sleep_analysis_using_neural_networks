import numpy as np


def detect_motion(motion_masks, n=5) -> list:

    pixel_count = int(255 * motion_masks.shape[1] * motion_masks.shape[2])

    motion_detection_list = list()

    for i in range(motion_masks.shape[0]):
        n_iter = n
        if i - n_iter < 0:
            n_iter = i
        mask = np.zeros_like(motion_masks[0])
        for j in range(1, n_iter):
            mask |= motion_masks[i] ^ motion_masks[i - j]
        motion_detection_list.append(np.sum(mask) / pixel_count)
    return motion_detection_list