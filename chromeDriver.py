import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from getConfig import *


# 连接浏览器
def linkChrome():
    print('正在启动浏览器......')
    # chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\Files\PycharmProjects\StarRailStationBackpackRecognitionUpload\AutomationProfile"
    subprocess.Popen(
        f'chrome.exe --remote-debugging-port={getconfig("chrome", "port")} --user-data-dir="{getconfig("chrome", "userDataDir")}')

    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option("debuggerAddress", f"{getconfig('chrome', 'host')}:{getconfig('chrome', 'port')}")
    options.page_load_strategy = 'eager'

    print('正在连接浏览器......')
    browser = webdriver.Chrome(options=options)
    return browser
