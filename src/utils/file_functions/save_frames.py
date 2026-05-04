import os.path

import cv2


def save_frames(path, frame_list):
    """
    Сохраняет все кадры в указанной директории
    :param path: адрес директории из корня проекта
    """
    img_num = 0
    if os.path.exists(path) is False:
        os.mkdir(path)

    for frame in frame_list:
        outfile = f'{path}/{img_num}.png'
        img_num += 1
        cv2.imwrite(outfile, frame)
    print("Frames saved succesfully!")
