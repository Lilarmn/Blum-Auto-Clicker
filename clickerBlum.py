import cv2
import numpy as np
from PIL import ImageGrab
from time import sleep
import pyautogui
import keyboard

upper_rgb = np.array([157, 255, 90])
lower_rgb = np.array([0,255,100])

lower_hsv = cv2.cvtColor(np.uint8([[lower_rgb]]), cv2.COLOR_BGR2HSV)[0][0]
upper_hsv = cv2.cvtColor(np.uint8([[upper_rgb]]), cv2.COLOR_BGR2HSV)[0][0]

lower_hsv = np.array([lower_hsv[0] - 10, max(50, lower_hsv[1] - 50), max(50, lower_hsv[2] - 50)])
upper_hsv = np.array([upper_hsv[0] + 10, min(255, upper_hsv[1] + 50), min(255, upper_hsv[2] + 50)])

print("Lower green HSV:", lower_hsv)
print("Upper green HSV:", upper_hsv)

def detect_green_balls(screen):
    hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    return mask

def main():
    counter = 0 
    while counter < 5:
        screenshot = ImageGrab.grab()
        screen_np = np.array(screenshot)

        mask = detect_green_balls(screen_np)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        print(f"Detected {len(contours)} contours")

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cx, cy = x + w // 2, y + h // 2
            print(f"Contour position: x={x}, y={y}, w={w}, h={h}")
            print(f"Click position: cx={cx}, cy={cy}")
            if keyboard.is_pressed('q'):
                print("Stopping automation...")
                return 0
            pyautogui.click(cx, cy)
        
        counter += 1

if __name__ == "__main__":
    sleep(5)
    main()
