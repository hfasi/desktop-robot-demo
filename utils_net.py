import socket

def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    通过尝试连接到指定的主机和端口来判断网络是否连接。
    默认情况下，连接到Google的DNS服务器8.8.8.8的53端口。
    
    :param host: 目标主机，默认是8.8.8.8
    :param port: 目标端口，默认是53
    :param timeout: 连接超时时间，默认是3秒
    :return: 如果连接成功返回True，否则返回False
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        print('is connected 网络连接正常')
        return True
    except socket.error as ex:
        print(f"网络连接失败: {ex}")
        return False

if __name__ == "__main__":
    host = "oa.api2d.net"
    port = 443
    if is_connected(host, port):
        print("网络连接正常")
    else:
        print("网络连接失败")
