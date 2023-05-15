import os


# 清空背包截图
def del_file_list(path):
    print('正在清空历史用户背包截图......')
    for file_name in os.listdir(path):
        if file_name == '.gitignore':
            continue
        os.remove(path + "\\" + file_name)


# 获取背包截图列表
def get_file_list(path):
    file_list = []
    print('正在获取用户背包截图......')
    for file_name in os.listdir(path):
        if file_name == '.gitignore':
            continue
        file_list.append(file_name)
    return file_list
