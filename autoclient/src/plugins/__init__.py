
import importlib
import traceback
from lib.conf.config import settings
class PluginsManage(object):

    def __init__(self,hostname=None):
        self.data = {}
        self.debug = settings.DEBUG
        self.mode = settings.MODE
        self.hostname = hostname
        self.plugins_dict = settings.PLUGINS_DICT
        if self.mode == "SSH":
            self.ssh_user = settings.SSH_USER
            self.ssh_pass = settings.SSH_PASS
            self.ssh_port = settings.SSH_PORT
            self.ssh_key = settings.SSH_KEY

    def run_plugins(self):
        for k,v in self.plugins_dict.items():
            ret = {'status': True, 'data': None}
            try:
                module_name,class_name = v.rsplit(".",1)
                m = importlib.import_module(module_name)

                if hasattr(m,class_name):
                    cls = getattr(m,class_name)
                    #预留勾子
                    if hasattr(cls,'initial'):
                        obj = cls().initial()
                    else:
                        obj = cls()

                    #获取plugins执行结果
                    ret['data'] = obj.process(self.exec_command,self.debug)

            except Exception as e:
                    ret['status'] = False
                    ret['data'] = "[%s][%s] 采集数据出现错误：%s" %(self.hostname if self.hostname else "AGENT",k,traceback.format_exc())

            self.data[k] = ret

        else:
            return self.data

    def exec_command(self,cmd):
        if self.mode == "AGENT":
            return self.__Agent(cmd)
        if self.mode == "SSH":
            return self.__Ssh(cmd)
        if self.mode == "SALT":
            return self.__Salt(cmd)
        #模式配置错误抛出异常
        raise Exception("Settings MODE Config Error!")

    def __Agent(self,cmd):
        import subprocess
        result = subprocess.getoutput(cmd)
        return result

    def __Ssh(self,cmd):
        import paramiko
        ssh_client = paramiko.SSHClient()
        ssh_client.connect(hostname=self.hostname, username=self.ssh_user, password=self.ssh_pass, port=self.ssh_port)
        result = ssh_client.exec_command(cmd)
        ssh_client.close()
        return result

    def __Salt(self,cmd):
        import subprocess
        result = subprocess.getoutput(cmd)
        return result