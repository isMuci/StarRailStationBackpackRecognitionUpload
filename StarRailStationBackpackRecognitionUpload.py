import pytesseract
import pyautogui as ui
from getBackpak import shot
from countBackpack import count_backpack
from uploadBackpack import linkWeb
from getMaterial import get_material

pytesseract.pytesseract.tesseract_cmd = r'./Resources/Tesseract-OCR/tesseract'

ui.FAILSAFE = False

material = []


# 自动模式
def automation(automotive):
    shot(automotive)
    count_backpack()
    linkWeb(material)


# 开始提取素材
def show_menu():
    print('=========menu=========')
    print('===1 getbackpack======')
    print('===2 countbackpack====')
    print('===3 updatebackpack===')
    print('===4 automation=======')
    print('===5 exitscript=======')


# 启动脚本
def start():
    try:
        print('在使用脚本前，请先打开星穹铁道，并进入背包材料界面......')
        while True:
            show_menu()
            opt = int(input())
            automotive = True if opt == 4 else False

            if opt == 1:
                shot(automotive)
            elif opt == 2:
                count_backpack()
            elif opt == 3:
                linkWeb(material)
            elif opt == 4:
                automation(automotive)
            elif opt == 5:
                print('退出脚本......')
                break
            else:
                print("未知指令！！！")
    except Exception as e:
        out = open('./Resources/error.txt', 'w')
        print(e, file=out)


if __name__ == '__main__':
    # get_material(0, 'lianxingzheleizhi', 152, 239, 962, 1043)
    start()
# 打包命令
# pyinstaller StarRailStationBackpackRecognitionUpload.spec
# 开发请注意将pycharm的兼容性设置中的以管理员身份运行打开
