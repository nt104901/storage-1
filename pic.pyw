import ctypes
import os
import random
import time

# Папка с изображениями
folder = r"C:\Users\maybe\Documents\images\dark"

# Функция смены обоев
def set_wallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

# Основной цикл
while True:
    images = [os.path.join(folder, f) for f in os.listdir(folder)
              if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    if images:
        chosen = random.choice(images)
        set_wallpaper(chosen)
    time.sleep(60)  # пауза 60 секунд
