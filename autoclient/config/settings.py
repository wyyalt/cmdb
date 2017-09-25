import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

HOST = '127.0.0.1'

HOSTNAME = 'yun@duyun.co'

MODE="AGENT"

DEBUG = True

PLUGINS_DICT = {
    'basic':'src.plugins.basic.Basic',
    'board':'src.plugins.board.Board',
    'cpu':'src.plugins.cpu.Cpu',
    'disk':'src.plugins.disk.Disk',
    'memory':'src.plugins.memory.Memory',
    'nic':'src.plugins.nic.Nic',
}

API = 'http://127.0.0.1:9006/api/asset.html'

CERT_FILE = os.path.join(BASEDIR,'config','cert')

API_KEY='daied325aa41bcwqlj87q3r4132fs2w'

DATA_KEY = 'kiu4wo2sl7d8hesk'