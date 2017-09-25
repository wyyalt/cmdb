
from src.plugins import PluginsManage
import json
from lib.conf.config import settings
from concurrent.futures import ThreadPoolExecutor
import requests
from lib.utils import auth,encrypt

class Base(object):
    #发送资产信息到API
    def post_asset(self,server_info):
        #加密
        data = encrypt(json.dumps(server_info))

        result = requests.post(
            url=settings.API,
            headers={"OpenKey":auth(),"Content-Type":"application/json"},
            data=data,
        )
        return result

class Agent(Base):
    def execute(self):
        server_info = PluginsManage().run_plugins()
        cert_file = settings.CERT_FILE
        hostname = open(cert_file, 'r').read().strip()
        if not hostname:
            with open(cert_file,'w') as f:
                f.write(server_info['basic']['data']['hostname'])
        else:
            server_info['basic']['data']['hostname'] = hostname

        result = self.post_asset(server_info)
        print(result.text)

class SSHSALT(Base):

    def get_host(self):
        respones = requests.get(settings.API)
        result = json.loads(respones.text)
        if not result['status']:
            return
        return result['data']

    def run(self,host):
        server_info = PluginsManage(host).run_plugins()
        self.post_asset(server_info)

    def execute(self):
        pool = ThreadPoolExecutor(10)
        host_list = self.get_host()
        for host in host_list:
            pool.submit(self.run,host)



