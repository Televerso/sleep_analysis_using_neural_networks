import os
import random

import cv2
import numpy as np
from matplotlib import pyplot as plt

from src.utils.basic_functions import BasicFunctions as bf

ROOT_DIR = os.path.split(os.environ['VIRTUAL_ENV'])[0]
path_out = os.path.join(ROOT_DIR, 'data', 'datasets', 'SleepNet', 'Dataset')

path_test = os.path.join(r"D:\datasets\Sleep_with_IR", 'Dataset_RGB', "Test")
path_train = os.path.join(r"D:\datasets\Sleep_with_IR", 'Dataset_RGB', "Train")


path_leftlog = "left_log"
path_rightlog= "right_log"
path_leftprone = "prone_left"
path_rightprone = "prone_right"
path_supine = "supine"

# path_pose = [path_supine, path_leftlog, path_rightlog, path_leftprone, path_rightprone]
path_pose = [path_supine, path_leftlog, path_rightlog]

def show_image(image):
    plt.plot()
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()

def process_image(path, angle, scale, thresh, inv):
    image = cv2.imread(path) # Считывает изображение

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Приводит изображение к отенкам серого
    image = bf.resize(image, 180*2, 135*2) # Подгоняет изображения к общему разрешению

    coef = 70/(np.sum(image)/(image.shape[0]*image.shape[1]))
    image = (image*coef).astype('uint8') # Нормализуем среднюю яркость к 70

    image[-25:-1,0:60] = 0 # Удаляет водяной знак на изображениях датасета
    image = bf.rotate(image,angle,scale) # Вращает и изменяет масштаб изображения в соответствии с переданными значениями
    image = bf.threshold(image, thresh) # Приводит изображение к бинарному в соответствии с переданным значением
    image = bf.blur(image, 7, 2) # Применяет медианный фильтр 3х3 К изображению
    image = bf.get_64pix_mask(image) # Приводит изображение к размеру 64х64, используемому при обучении сети

    if inv:
        image = image[::,::-1]

    return image


# show_image(process_image(os.path.join(os.path.join(path_test,path_supine),os.listdir(os.path.join(path_test,path_supine))[0]), 0, 1, 120, 0))

for pose in path_pose:
    path = os.path.join(path_train, pose)

    i = 0
    for item in os.listdir(path):
        th_low = 95
        th_high = 145
        for var in range(0,10):
            path_item = os.path.join(path, item)
            angle = np.random.randint(0,30)-15 # От - 15 до 15
            scale = 1.05 - np.random.random()/10 # От 0.95 до 1.05
            th = np.random.randint(th_low,th_high) # от 95 до 145
            inv = np.random.randint(0,1) # Шанс 50% отразить изображенеи по вертикали

            image = process_image(path_item,angle,scale, th, inv)
            if np.sum(image) < 0.35*1*256*(image.shape[0]*image.shape[1]) and np.sum(image) > 0.1*1*256*(image.shape[0]*image.shape[1]):
                if pose == path_leftlog and inv:
                    cv2.imwrite(os.path.join(path_out, f"Train/{path_rightlog}/_{i}.png"), image)
                elif pose == path_rightlog and inv:
                    cv2.imwrite(os.path.join(path_out, f"Train/{path_leftlog}/_{i}.png"), image)
                else:
                    cv2.imwrite(os.path.join(path_out, f"Train/{pose}/{i}.png"), image)
                i+=1

    print(i)
    print(pose)

for pose in path_pose:
    path = os.path.join(path_test, pose)

    i = 0
    for item in os.listdir(path):

        for var in range(0,10):
            path_item = os.path.join(path, item)
            angle = np.random.randint(0, 30) - 15  # От - 15 до 15
            th = np.random.randint(90, 130)  # от 95 до 145
            inv = np.random.randint(0, 1)  # Шанс 50% отразить изображенеи по вертикали

            image = process_image(path_item,angle,1,th, inv)

            if np.sum(image) < 0.35*1*256*(image.shape[0]*image.shape[1]) and np.sum(image) > 0.1*1*256*(image.shape[0]*image.shape[1]):
                if pose == path_leftlog and inv:
                    cv2.imwrite(os.path.join(path_out, f"Test/{path_rightlog}/_{i}.png"), image)
                elif pose == path_rightlog and inv:
                    cv2.imwrite(os.path.join(path_out, f"Test/{path_leftlog}/_{i}.png"), image)
                else:
                    cv2.imwrite(os.path.join(path_out, f"Test/{pose}/{i}.png"), image)
                i += 1
    print(pose)