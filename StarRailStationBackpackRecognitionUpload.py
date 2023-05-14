from __future__ import print_function
import os
import cv2
import time
import win32com.client
import win32ui
import win32gui
import win32con
import subprocess
import pytesseract
from PIL import Image
import ctypes.wintypes
import configparser
from numpy.compat import unicode
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pyautogui as ui
import ctypes, sys

pytesseract.pytesseract.tesseract_cmd = r'./Resources/Tesseract-OCR/tesseract'

ui.FAILSAFE = False

map = {}
material = []
file_list = []
chrome = 'chrome'
userDataDir = 'userDataDir'
host = 'host'
port = 'port'
automotive = False


# 获得文件
def getconfig(section, option):
    conf = configparser.ConfigParser()
    conf.read('./common/config')
    config = conf.get(section, option)
    return config


# 窗体框选
def get_window_rect(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
          ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          ctypes.byref(rect),
          ctypes.sizeof(rect)
          )
        return rect.left, rect.top, rect.right, rect.bottom


# 截取背包
def shot():
    # print(automode)
    i = int(getconfig('backpack', 'count'))
    if automotive == False:
        print('请输入背包截取的张数:\t')
        i = int(input())
    print('正在寻找游戏窗口......')
    hwnd = win32gui.FindWindow('UnityWndClass', '崩坏：星穹铁道')  # 根据窗口名称获取窗口对象
    left, top, right, bot = get_window_rect(hwnd)
    # 解决error: (0, 'SetForegroundWindow', 'No error message is available')错误
    del_file_list(f'./Resources/backpack')
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    # ui.PAUSE = 0.03
    wc = left + (right - left) / 2
    hc = top + (bot - top) / 2
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1.0)
    for k in range(3):
        ui.moveTo(wc, hc, duration=0.1)
        ui.dragRel(0, 400, duration=1)
    for idx in range(i):
        print('正在截取背包......')
        time.sleep(0.5)
        screenshot(hwnd, f'./Resources/backpack/backpack_{idx}.jpg')
        if idx != (i - 1):
            ui.moveTo(wc, hc, duration=0.1)
            ui.dragRel(0, -400, duration=1)


# 清空背包截图
def del_file_list(path):
    print('正在清空历史用户背包截图......')
    for file_name in os.listdir(path):
        if file_name == '.gitignore':
            continue
        os.remove(path + "\\" + file_name)


# 背包截图
def screenshot(hwnd, path):
    left, top, right, bot = get_window_rect(hwnd)
    w = right - left
    h = bot - top

    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)

    result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)
    if result == None:
        # PrintWindow Succeeded
        im.save(path)
    else:
        print("游戏背包截图失败")


# 截取素材
def getmaterial(mete):
    # hwnd = win32gui.FindWindow('UnityWndClass', '崩坏：星穹铁道')  # 根据窗口名称获取窗口对象
    # del_file_list(f'./Resources/backpack')
    # win32gui.SetForegroundWindow(hwnd)
    # time.sleep(1)
    # screenshot(hwnd, f'./Resources/backpack/backpack_1.jpg')
    img = cv2.imread('./Resources/backpack/backpack_0.jpg')
    print(img.shape)
    # s=map[mete]
    # s=s.replace('[','')
    # s = s.replace(']', '')
    # s = s.replace(',', ':')
    # # mete.replace[',',':']
    # arr=s.split(':')
    # print(s)
    cropped_img = img[440:523, 366:441]

    print(cropped_img.shape)

    cv2.imwrite(f'./Resources/material/qunxingyuezhang.jpg', cropped_img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])


# 匹配素材
def comparison(backpack, meter):
    img = cv2.imread(f'./Resources/backpack/{backpack}')
    # print(img.shape)
    material = cv2.imread(f"./Resources/material/{map[meter]}{'.png' if map[meter] == 'xinyongdian' else '.jpg'}")
    # print(material.shape)
    h, w, i = material.shape
    res = cv2.matchTemplate(img, material, cv2.TM_SQDIFF_NORMED)
    # print(cv2.minMaxLoc(res))
    if (cv2.minMaxLoc(res)[0] >= 0.2):
        print(f'匹配{meter}失败')
        return None
    else:
        upper_left = cv2.minMaxLoc(res)[2]
        lower_right = (upper_left[0] + w, upper_left[1] + h)
        # print(upper_left)
        # print(lower_right)
        print(f'匹配{meter}成功')
        return upper_left, lower_right


# 计算素材
def count(box, backpack, meter):
    img_orig = cv2.imread(f'./Resources/backpack/{backpack}')
    new_img = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)
    upper_left = box[0]
    lower_right = box[1]
    if (map[meter] == 'xinyongdian'):
        new_img = new_img[upper_left[1]:lower_right[1], lower_right[0]:lower_right[0] + 100]
    else:
        new_img = new_img[lower_right[1]:lower_right[1] + 20, upper_left[0] - 10:lower_right[0] + 10]

    # thresh, new_img = cv2.threshold(new_img, 150, 255, cv2.THRESH_BINARY)
    # 设置阈值
    height, width = new_img.shape[0:2]
    points = (width * 3, height * 3)
    new_img = cv2.resize(new_img, points, cv2.INTER_LINEAR)
    height, width = new_img.shape[0:2]
    thresh = 150
    for row in range(height):
        for col in range(width):
            # 获取到灰度值
            gray = new_img[row, col]
            # 如果灰度值高于阈值 就等于255最大值
            if gray > thresh:
                new_img[row, col] = 0
            # 如果小于阈值，就直接改为0
            elif gray < thresh:
                new_img[row, col] = 255
    #
    cv2.imwrite(f"./Resources/count/{map[meter]}.jpg", new_img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    #
    string = pytesseract.image_to_string(new_img, lang='eng',
                                         config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789').strip()
    # print(string)
    # cv2.imshow('img', new_img)
    # cv2.waitKey()
    if (string == ''):
        print(f'计算素材{meter}失败！！！！！！！')
        return -1
    else:
        print(f'素材 {meter} 的个数为 {string}')
        try:
            return int(string)
        except:
            print(f'计算素材{meter}失败！！！！！！！')
            return -1


# 获取背包截图列表
def get_file_list(path):
    print('正在获取用户背包截图......')
    for file_name in os.listdir(path):
        if file_name == '.gitignore':
            continue
        file_list.append(file_name)
    return file_list


# 开始计算背包内素材
def countback():
    idmap = {}
    id = 0
    get_file_list('./Resources/backpack')
    with open('Resources/locate', 'r', encoding='utf-8') as f:
        for line in f:
            met = line.strip().split(' ')

            material.append([met[0], 0])
            idmap[met[0]] = id
            id += 1

            if (len(met) > 2):
                map[met[0]] = met[1]
    # print(map)
    id = 0
    for meter in map:
        for backpack in file_list:
            box = comparison(backpack, meter)
            if (box != None):
                print(f'开始计算素材 {meter} {backpack}')
                cnt = count(box, backpack, meter)
                if (cnt > 0):
                    material[idmap[meter]][1] = cnt
                    # print(f'{material[idmap[meter]][0]} {material[idmap[meter]][1]}!!!!!!')
                    id += 1
                    break
    open('Resources/backpack-count', 'w').close()
    f = open('Resources/backpack-count', 'w', encoding='utf-8')
    for i in range(0, len(material)):
        f.write(f'{material[i][0]} {material[i][1]}\n')
        # f.write(f'{material[i][0]} 0\n')


# 连接浏览器
def linkChrome():
    print('正在启动浏览器......')
    # chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\Files\PycharmProjects\StarRailStationBackpackRecognitionUpload\AutomationProfile"
    subprocess.Popen(
        f'chrome.exe --remote-debugging-port={getconfig(chrome, port)} --user-data-dir="{getconfig(chrome, userDataDir)}')

    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option("debuggerAddress", f"{getconfig(chrome, host)}:{getconfig(chrome, port)}")
    options.page_load_strategy = 'eager'

    print('正在连接浏览器......')
    browser = webdriver.Chrome(options=options)

    # start = time.time()

    try:
        print('正在打开铁道站养成计算页面...')
        browser.get("https://starrailstation.com/cn/planner")
    except:  # 捕获timeout异常
        print('打开失败，停止加载页面....')
        browser.execute_script('window.stop()')  # 执行Javascript来停止页面加载 window.stop()
    # end = time.time()
    # 页面加载所需时间
    # print(end - start)

    print(f'已经打开 {browser.title} ......')
    print('开始更新背包材料.......')
    update(browser)


# 更新背包
def update(browser):
    try:
        print("正在寻找背包按钮......")
        # //*[@id="page"]/div[2]/div[2]/div[2]/div/div/button[3]
        browser.find_element(By.XPATH, '//*[@id="page"]/div[2]/div[2]/div[2]/div/div/button[3]').click()

        print("正在获取背包内容表......")
        # //*[@id="page"]/div[2]/div[3]/div/div/div[2]/div/div
        list = browser.find_elements(By.XPATH, '//*[@id="page"]/div[2]/div[3]/div/div/div[2]/div/div/div')

        global material
        if len(material) == 0:
            materialHistory = []
            with open('Resources/backpack-count', 'r', encoding='utf-8') as f:
                for line in f:
                    met = line.strip().split(' ')
                    materialHistory.append([met[0], met[1]])
            material = materialHistory

        print("正在向背包内填入材料......")
        cnt = 0
        for item in list:
            # print(item.tag_name)
            x = item.find_element(By.TAG_NAME, 'input')
            x.send_keys(Keys.CONTROL, 'a')
            x.send_keys(material[cnt][1])
            print(f'填入材料 {material[cnt][0]} 完成！ 数量 {material[cnt][1]}')
            cnt += 1
        # print("4")
        # //*[@id="page"]/div[2]/div[3]/div/div/div[1]/div[2]/button[1]
        browser.find_element(By.XPATH, '//*[@id="page"]/div[2]/div[3]/div/div/div[1]/div[2]/button[1]').click()
    except Exception as e:
        print(type(e))
        update(browser)


# 自动模式
def automation():
    shot()
    countback()
    linkChrome()


# 开始提取素材
def showmenu():
    print('=========menu=========')
    print('===1 getbackpack======')
    print('===2 countbackpack====')
    print('===3 updatebackpack===')
    print('===4 automation=======')
    print('===5 exitscript=======')


# 退出
def exit():
    return True


# 获取脚本管理员权限
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


opts = {
    0: True,
    1: shot,
    2: countback,
    3: linkChrome,
    4: automation,
    5: exit
}


# 启动脚本
def start():
    if is_admin():
        # 将要运行的代码加到这里
        try:
            print('在使用脚本前，请先打开星穹铁道，并进入背包材料界面......')
            while (True):
                showmenu()
                opt = int(input())
                global automotive
                automotive = True if opt == 4 else False
                # print(automotive)
                if opts[opt]():
                    print('退出脚本......')
                    break
        except Exception as e:
            out = open('./common/error.txt', 'w')
            print(e, file=out)
    else:
        print('正在获取管理员权限......')
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        else:  # in python2.x
            ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)


if __name__ == '__main__':
    # getmaterial('asdad')
    start()
