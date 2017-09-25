from django.conf import settings
from django.shortcuts import HttpResponse
import time,hashlib

auth_record_dict={}

def AUTH_API(func):
    def wrapper(*args,**kwargs):
        client_md5_key_time = args[0].META.get('HTTP_OPENKEY')
        client_md5_key, client_time_str = client_md5_key_time.split("|")
        client_time = float(client_time_str)
        server_time = time.time()

        # 第一层 时间超时
        if server_time - client_time > 10:
            return HttpResponse("验证失败：TimeOut")

        # 第二层 MD5比对
        server_key = settings.AUTH_KEY
        auth_str = "%s|%s" % (server_key, client_time)
        md5 = hashlib.md5()
        md5.update(auth_str.encode("utf-8"))
        server_md5_key = md5.hexdigest()

        if server_md5_key != client_md5_key:
            return HttpResponse("验证失败：KeyError")

        for key in list(auth_record_dict.keys()):
            value = auth_record_dict[key]
            if server_time > value:
                del auth_record_dict[key]

        # 第三层 key唯一性
        if client_md5_key_time in auth_record_dict:
            return HttpResponse("验证失败：ManayRequest")
        else:
            auth_record_dict[client_md5_key_time] = client_time + 10


        result = func(*args,**kwargs)
        return result
    return wrapper