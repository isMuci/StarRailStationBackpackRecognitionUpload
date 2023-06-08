import json
import cv2
import pytesseract
from fileSystem import *
from colorama import init

init(autoreset=True)

material_map = {}


# 匹配素材
def comparison(backpack, meter):
    img = cv2.imread(f'./Resources/backpack/{backpack}', 0)
    # print(img.shape)
    material = cv2.imread(f"./Resources/material/{material_map[meter]}.png", 0)
    # print(material.shape)
    h, w = material.shape
    res = cv2.matchTemplate(img, material, cv2.TM_SQDIFF_NORMED)
    # print(cv2.minMaxLoc(res))
    if cv2.minMaxLoc(res)[0] >= 0.10:
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

    # cv2.imshow('img', new_img[lower_right[1]-100:lower_right[1] + 20, upper_left[0] - 10:lower_right[0] + 10])
    # cv2.waitKey()

    if material_map[meter] == 'xinyongdian':
        new_img = new_img[upper_left[1]:lower_right[1], lower_right[0]:lower_right[0] + 100]
    else:
        new_img = new_img[lower_right[1]:lower_right[1] + 21, upper_left[0] - 5:lower_right[0] + 5]

    # cv2.imshow('img', new_img)
    # cv2.waitKey()

    # 设置阈值
    height, width = new_img.shape[0:2]
    points = (width * 10, height * 10)
    new_img = cv2.resize(new_img, points, cv2.INTER_LINEAR)
    height, width = new_img.shape[0:2]

    # new_img = cv2.blur(new_img, (3, 3))

    thresh = 160
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

    string = pytesseract.image_to_string(new_img, lang='eng',
                                         config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789').strip()

    # print(string)
    # cv2.imshow('img', new_img)
    # cv2.waitKey()
    cv2.imwrite(f'./out/{material_map[meter]}.png',new_img)

    if string == '':
        print(f'计算素材\033[32m{meter}\033[0m失败！！！！！！！')
        return -1
    else:
        print(f"素材 \033[32m{meter}\033[0m 的个数为 \033[31m{string}\033[0m")
        try:
            return int(string)
        except:
            print(f'计算素材\033[32m{meter}\033[0m失败！！！！！！！')
            return -1


# 开始计算背包内素材
def count_backpack():
    idmap = {}
    material = []
    idx = 0
    file_list = get_file_list('./Resources/backpack')
    with open('Resources/materiallist.json', 'r', encoding='utf-8') as f:
        materialist = json.load(f)
    for key in materialist:
        material.append([key, 0])
        idmap[key] = idx
        idx += 1
        material_map[key] = materialist[key]
    # print(map)
    idx = 0
    for meter in material_map:
        for backpack in file_list:
            box = comparison(backpack, meter)
            if box is not None:
                print(f'开始计算素材 {meter} {backpack}')
                cnt = count(box, backpack, meter)
                if cnt > 0:
                    material[idmap[meter]][1] = cnt
                    # print(f'{material[idmap[meter]][0]} {material[idmap[meter]][1]}!!!!!!')
                    idx += 1
                    break
    open('Resources/backpack-count', 'w').close()
    f = open('Resources/backpack-count', 'w', encoding='utf-8')
    for i in range(0, len(material)):
        f.write(f'{material[i][0]} {material[i][1]}\n')
        # f.write(f'{material[i][0]} 0\n')
    return material
