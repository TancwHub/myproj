"""
    import方式：
        from common import network_helper
"""

import socket

class NetWork_helper:
    @staticmethod
    def GetLocalIPByPrefix(prefix):
        """
         多网卡情况下，根据前缀获取IP
        :param prefix: IP前缀
        :return:
        """
        localIP = ''
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if ip.startswith(prefix):
                localIP = ip
        return localIP




