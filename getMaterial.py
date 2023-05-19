import cv2


# 截取素材
def get_material(num,mete, top, bot, left, right):
    img = cv2.imread(f'./Resources/backpack/backpack_{num}.png')
    print(img.shape)

    cropped_img = img[top:bot, left:right]

    print(cropped_img.shape)

    cv2.imwrite(f'./Resources/material/{mete}.png', cropped_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
