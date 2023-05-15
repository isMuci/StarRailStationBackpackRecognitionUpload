import configparser


# 获得配置文件
def getconfig(section, option):
    conf = configparser.ConfigParser()
    conf.read('./Resources/config.ini')
    config = conf.get(section, option)
    return config
