import pyautogui
import numpy as np
from PIL import Image
import webbrowser
import keyboard

import tkinter as tk

root = tk.Tk()

import cv2
import pytesseract

monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()
print('화면크기 : ', monitor_width,' x ',monitor_height)


pytesseract.pytesseract.tesseract_cmd = '.\\Tesseract-OCR\\tesseract.exe'

def adjust_contrast(input_image, alpha2):
    """
    input_image (str): 입력 이미지.
    contrast (float): 명암비 조절 값 (1.0-3.0은 명암비를 적당히 증가시킵니다).
    brightness (int): 밝기 조절 값 (0-100은 밝기를 적당히 증가시킵니다).
    input_image = cv2.imread(image_path)
    """

    # 명암비와 밝기 조절
    adjusted_image = np.clip((1+alpha2) * input_image - 128 * alpha2, 0, 255).astype(np.uint8)

    return adjusted_image


#pil -> cv2 변환
def opencv2PIL(pilimage):
    return cv2.cvtColor(np.array(pilimage),cv2.COLOR_RGB2BGR)

#CV -> PIL 변환
def openPIL2cv(cv2image):
    return Image.fromarray(cv2image)

# 화면의 특정 영역을 캡처하는 함수
def capture_screen(x1, y1, x2, y2, filename):
    screen = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

    new_width = screen.width * 3
    new_height = screen.height * 3
    screen = screen.resize((new_width, new_height))

    screen = opencv2PIL(screen)

    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    gray = cv2.subtract(gray, 67)
    gray = adjust_contrast(gray, 7.5)
    _,gray = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)


    text = pytesseract.image_to_string(gray, lang='chi_sim+chi_tra+eng+jpn+kor+eng')
    
    #openPIL2cv(screen).save(filename)
    #openPIL2cv(gray).save('gray' + filename)

    return text


#변수선언
captured_screen_1 = ""
captured_screen_2 = ""

# 메인 함수
def main():
    global captured_screen_1
    global captured_screen_2
    global monitor_height
    global monitor_width
    # 첫 번째 영역의 좌표
    x1_1, y1_1, x2_1, y2_1 = int(1365/1920*monitor_width), int(925/1080*monitor_height), int(1500/1920*monitor_width), int(955/1080*monitor_height)       
    # 두 번째 영역의 좌표
    x1_2, y1_2, x2_2, y2_2 = int(1647/1920*monitor_width), int(925/1080*monitor_height), int(1785/1920*monitor_width), int(955/1080*monitor_height)

    # 첫 번째 영역 캡처
    captured_screen_1 = capture_screen(x1_1, y1_1, x2_1, y2_1, '1.jpg')
    # 두 번째 영역 캡처
    captured_screen_2 = capture_screen(x1_2, y1_2, x2_2, y2_2, '2.jpg')

    # 추출된 텍스트 출력
    captured_screen_1=captured_screen_1.replace(" ", "")
    captured_screen_2=captured_screen_2.replace(" ", "")
    webbrowser.open_new('https://dak.gg/er/multi?q=' + captured_screen_1 + '%20'+ captured_screen_2)

if __name__ == "__main__":
    first = True
    while True:
        if first:
            print('픽창에서 CTRL + ALT + M 키를 눌러보세요')
            first = False

        if keyboard.is_pressed('ctrl+alt+m'):  # 단축키 설정 (Ctrl + Alt + M)
            main()
            print('전적검색을 완료했습니다' + '아군1 : '+ captured_screen_1 + ' / ' + '아군2 : ' + captured_screen_2)
            print('재검색을 하려면 픽창에서 CTRL + ALT + M 키를 눌러보세요')
        else:
            keyboard.wait('ctrl+alt+m')  # Ctrl + Alt + M 키가 눌릴 때까지 대기