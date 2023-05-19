import subprocess
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from getConfig import *


# 连接浏览器
def linkEdge():
    print('正在启动浏览器......')
    # msedge.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\zlh13\AppData\Local\Microsoft\Edge\User Data"
    subprocess.Popen(
        f'msedge.exe --remote-debugging-port={getconfig("edge", "port")} --user-data-dir="{getconfig("edge", "userDataDir")}')

    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option("debuggerAddress", f"{getconfig('edge', 'host')}:{getconfig('edge', 'port')}")
    options.page_load_strategy = 'eager'

    print('正在连接浏览器......')
    browser = webdriver.Edge(options=options)
    return browser
