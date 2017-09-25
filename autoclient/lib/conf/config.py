import os
import importlib
from .import default_settings

class LoadConfig(object):

    def __init__(self):
        #加载默认配置
        for name in dir(default_settings):
            if name.isupper():
                value = getattr(default_settings,name)
                setattr(self,name,value)

        #字符串方式导入用户配置模块
        module_name = importlib.import_module(os.environ['USER_SETTINGS'])

        # 加载用户配置
        for name in dir(module_name):
            if name.isupper():
                value = getattr(module_name,name)
                setattr(self,name,value)
#全局配置加载
settings = LoadConfig()
