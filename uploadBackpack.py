from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from chromeDriver import *
from edgeDriver import *
from getConfig import *


# 更新背包
def update(browser, material):
    try:
        print("正在寻找背包按钮......")
        # //*[@id="page"]/div[2]/div[2]/div[2]/div/div/button[3]
        # //*[@id="page"]/div[2]/div[2]/div[1]/div/div/button[3]
        browser.find_element(By.XPATH, '//*[@id="page"]/div[2]/div[2]/div[1]/div/div/button[3]').click()

        print("正在获取背包内容表......")
        # //*[@id="page"]/div[2]/div[3]/div/div/div[2]/div/div
        material_list = browser.find_elements(By.XPATH, '//*[@id="page"]/div[2]/div[3]/div/div/div[2]/div/div/div')

        if len(material) == 0:
            materialHistory = []
            with open('Resources/backpack-count', 'r', encoding='utf-8') as f:
                for line in f:
                    met = line.strip().split(' ')
                    materialHistory.append([met[0], met[1]])
            material = materialHistory

        print("正在向背包内填入材料......")
        cnt = 0
        for item in material_list:
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
        update(browser, material)


# 连接浏览器
def linkWeb(material):
    driver = getconfig('browser', 'browser')
    if driver == 'chrome':
        browser = linkChrome()
    elif driver == "edge":
        browser = linkEdge()
    try:
        print('正在打开铁道站养成计算页面...')
        browser.get("https://starrailstation.com/cn/planner")
    except:  # 捕获timeout异常
        print('打开失败，停止加载页面....')
        browser.execute_script('window.stop()')  # 执行Javascript来停止页面加载 window.stop()

    print(f'已经打开 {browser.title} ......')
    print('开始更新背包材料.......')
    update(browser, material)
