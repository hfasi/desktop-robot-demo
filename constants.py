# -*- coding: utf-8 -*-
import os

# main directory
APP_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

print(APP_PATH)


LIB_PATH = os.path.join(APP_PATH, "robot")
DATA_PATH = os.path.join(APP_PATH, "static")
TEMP_PATH = os.path.join(APP_PATH, "temp")


SERIAL_PORT_XU_FEI = "/dev/ttyUSB0"
BAUD_RATE_XU_FEI = 115200
NO_NEED_TO_HANDLE = "NO_NEED_TO_HANDLE"


def getData(*fname):
    """
    获取资源目录下指定文件的路径

    :param *fname: 指定文件名。如果传多个，则自动拼接
    :returns: 配置文件的存储路径
    """
    return os.path.join(DATA_PATH, *fname)


