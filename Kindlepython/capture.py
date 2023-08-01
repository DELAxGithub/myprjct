import os
import time
import cv2
from mss import mss
from PIL import Image
import pytesseract
from constant import OUTPUT_IMG_FOLDER
from os import path
import pyautogui

class Capture:
    def window_manager(self):
        print("10秒以内に撮影したい範囲の左上にカーソルを合わせてください")
        time.sleep(10)
        upper_left_x, upper_left_y = pyautogui.position()
        print(f'左上の座標: {upper_left_x}, {upper_left_y}')

        print("10秒以内に撮影したい範囲の右下にカーソルを合わせてください")
        time.sleep(10)
        bottom_right_x, bottom_right_y = pyautogui.position()
        print(f'右上の座標: {bottom_right_x}, {bottom_right_y}')

        print('座標取得完了')

        return upper_left_x, upper_left_y, bottom_right_x, bottom_right_y

    def window_capture(self, x_1, y_1, x_2, y_2):
        print('保存するテキストファイル名を入力してください：')
        file_name = input()

        max_page = 3000
        span = 0.1
        time.sleep(10)

        img_file_path = path.join(OUTPUT_IMG_FOLDER, file_name)
        os.mkdir(img_file_path)

        os.chdir(img_file_path)
        print(f'{img_file_path}に画像を保存していきます')

        sct = mss()
        screenshot = sct.grab({"left": x_1, "top": y_1, "width": x_2 - x_1, "height": y_2 - y_1})
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img.save('picture_0.png')

        pyautogui.keyDown('down')
        pyautogui.keyUp('down')
        time.sleep(span)

        for page in range(1, max_page):
            screenshot = sct.grab({"left": x_1, "top": y_1, "width": x_2 - x_1, "height": y_2 - y_1})
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            img.save(f'picture_{page}.png')

            pyautogui.keyDown('down')
            pyautogui.keyUp('down')

            img_prev = cv2.imread(f'picture_{page-1}.png')
            img_current = cv2.imread(f'picture_{page}.png')
            time.sleep(span)

            mask = cv2.absdiff(img_prev, img_current)
            mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            if page == max_page or not cv2.countNonZero(mask_gray):
                break

        print('画像の保存が終了しました')

        return page, file_name, img_file_path
