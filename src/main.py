import os
#import time
import sys
# 實驗室自行實作之程式檔引用,請參考demo.py,視實際情況替換之
# import demo

# 這隻程式用於單元測試,確保在尚未輸入之前可以正常執行
# 輸入用的範例檔案請先預備在unittest_input資料夾內
# 輸出用的檔案會放在unittest_output資料夾內,注意這個範例會在執行之前強制刪除輸出資料夾的內容!
import cv2 as cv
import numpy as np 
import glob
from pathlib import Path
from A01_panicle_image_extract import *

# 相對路徑輸入輸出資料夾
DATA_PATH = './data'
PROCESSED_DIR = './predictions'


def main():
    # print(os.getcwd())
    # 如果 輸入檔路徑資料夾不存在,後面不處理了
    if (not os.path.isdir(DATA_PATH)):
        print(f'{DATA_PATH} not exist')
        print(f'error')
        return False
    # 輸出資料夾則是先刪除裡面的檔案
    # 如果資料夾存在
    if (os.path.isdir(PROCESSED_DIR)):
        # 先把檔案都刪了
        for f in os.listdir(PROCESSED_DIR):
            os.remove(os.path.join(PROCESSED_DIR, f))
    else:
        # 否則 建立 輸出檔路徑資料夾
        os.mkdir(PROCESSED_DIR)

    result = True
    try:
        # ========================================================================
        # 呼叫範例用的函數,這邊需勞煩實驗室自行實作之
        exec(DATA_PATH, PROCESSED_DIR)

        # result = demo.exec(DATA_PATH, PROCESSED_DIR)
        # ========================================================================
    except Exception as e:
        # 印出 Exception 資訊
        print(e)
        result = False
    # ========================================================================

    # 是否執行成功?
    if (result):
        # 輸出結束資訊
        print(f'finish')
        return True
    else:
        print(f'error')
        return False


# 如果是主程式
if __name__ == '__main__':
    main()
