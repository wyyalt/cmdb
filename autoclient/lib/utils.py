import time
import hashlib
from lib.conf.config import settings
from Crypto.Cipher import AES

def auth():
    client_time = time.time()
    temp = "%s|%s" % (settings.API_KEY, client_time)
    md5 = hashlib.md5()
    md5.update(temp.encode("utf-8"))
    md5_key = md5.hexdigest()

    result = "%s|%s" % (md5_key, client_time)
    return result

def encrypt(msg):
    cipher = AES.new(settings.DATA_KEY,AES.MODE_CBC,settings.DATA_KEY)
    bytes_msg = bytearray(msg,encoding='utf-8')

    #数据长度处理
    v1 = len(bytes_msg)
    v2 = v1 % 16
    if v2 == 0:
        v3 = 16
    else:
        v3 = 16 - v2

    for i in range(v3):
        bytes_msg.append(v3)
    final_data = bytes_msg.decode("utf-8")

    msg = cipher.encrypt(final_data)
    return msg

def decrypt(msg):
    cipher = AES.new(settings.DATA_KEY, AES.MODE_CBC, settings.DATA_KEY)
    data = cipher.decrypt(msg)
    result = data[0:-data[-1]]
    return result.decode('utf8')


