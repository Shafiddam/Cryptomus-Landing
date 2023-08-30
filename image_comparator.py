import cv2
import numpy as np


def compare_images(img1_path, img2_path):
    # Загрузка изображений
    img1 = cv2.imread(img1_path, cv2.IMREAD_COLOR)
    img2 = cv2.imread(img2_path, cv2.IMREAD_COLOR)
    # Проверка размеров изображений
    if img1.shape != img2.shape:
        print("Изображения разного размера!")
        return
    # Вычисление абсолютного различия между изображениями
    difference = cv2.absdiff(img1, img2)
    # Преобразование различия в черно-белое изображение
    grayscale_diff = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    # Пороговая обработка для выявления заметных различий
    _, threshold_diff = cv2.threshold(grayscale_diff, 30, 255, cv2.THRESH_BINARY)
    # Вычисление процента различия
    diff_percentage = (np.sum(threshold_diff) / 255.0) / (threshold_diff.shape[0] * threshold_diff.shape[1]) * 100
    return diff_percentage