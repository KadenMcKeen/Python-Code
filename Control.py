import pyautogui
import time


def locate(template, click):

    #Returns x, y, w, h
    location = pyautogui.locateOnScreen('Templates/{0}.png'.format(template))

    if location != None:
        if click:
            center_x, center_y = pyautogui.center(location)
            pyautogui.click(center_x, center_y)
        return True
    else:
        return False

def gym():    
    location = locate('gym', True)
    if location == True:
        time.sleep(5)
        pyautogui.click(760,506)
        time.sleep(3)
        pyautogui.click(1025,506)
        time.sleep(3)
        pyautogui.click(760,645)
        time.sleep(3)
        pyautogui.click(1025,645)
    else:
        location = locate('gym_full', True)
        if location == True:
            time.sleep(5)
            pyautogui.click(760,506)
            time.sleep(3)
            pyautogui.click(1025,506)
            time.sleep(3)
            pyautogui.click(760,645)
            time.sleep(3)
            pyautogui.click(1025,645)


def crimes():
    location = locate('crimes', True)
    if location == True:
        time.sleep(5)
        for i in range(10):
            location = locate('virus', True)
            time.sleep(3)
    else:
        location = locate('crimes_full', True)
        if location == True:
            time.sleep(5)
            for i in range(10):
                location = locate('virus', True)
                time.sleep(3)


def captcha():
    location = pyautogui.locateOnScreen('Templates/{0}.png'.format('validate'))

    if location != None:
        center_x, center_y = pyautogui.center(location)
        pyautogui.moveTo((center_x+50, center_y+200))
        pyautogui.click(button='right')

        pyautogui.moveRel(10,40)
        pyautogui.click()

        time.sleep(1)
        pyautogui.typewrite('guess_image', interval=0.1)
        
        locate('folder', True)
        pyautogui.typewrite('C:/Users/Kaden McKeen/Desktop/Programming/Python/Machine Learning/Captcha Neural Network', interval=0.01)

        pyautogui.press('enter')
        locate('change_folder', True)
        time.sleep(1)
        
        locate('save', True)
        time.sleep(1)

        locate('yes_replace', True)
        time.sleep(10)


def click_captcha(result):
    if 1 in result:
        try_number = result.index(1)+1
        locate(str(try_number), True)


def flying():
    location = locate('flight', False)
    if location == True:
        print("Flying")


