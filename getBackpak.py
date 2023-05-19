import time
import win32com.client
import win32gui
import win32con
import win32ui
from PIL import Image
import ctypes.wintypes
import pyautogui as ui
import ctypes
from getConfig import *
from fileSystem import *


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
    if result is None:
        # PrintWindow Succeeded
        im.save(path)
    else:
        print("游戏背包截图失败")


# 截取背包
def shot(automotive):
    i = int(getconfig('backpack', 'count'))
    if not automotive:
        print('请输入背包截取的张数:\t')
        i = int(input())
    print('正在寻找游戏窗口......')
    hwnd = win32gui.FindWindow('UnityWndClass', '崩坏：星穹铁道')  # 根据窗口名称获取窗口对象
    left, top, right, bot = get_window_rect(hwnd)
    # 解决error: (0, 'SetForegroundWindow', 'No error message is available')错误
    del_file_list(f'./Resources/backpack')
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')

    wc = left + (right - left) / 2
    hc = top + (bot - top) / 2
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1.0)
    for k in range(i+1):
        ui.moveTo(wc, hc, duration=0.1)
        ui.dragRel(0, 400, duration=1)
    for idx in range(i):
        print(f'正在截取第 {i+1} 张背包......')
        time.sleep(0.5)
        screenshot(hwnd, f'./Resources/backpack/backpack_{idx}.png')
        if idx != (i - 1):
            ui.moveTo(wc, hc, duration=0.1)
            ui.dragRel(0, -400, duration=1)
