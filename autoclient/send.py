import  requests,hashlib,time

key = 'daied325aa41bcwqlj87q3r4132fs2w'
client_time=time.time()
temp = "%s|%s"%(key,client_time)
md5 = hashlib.md5()
md5.update(temp.encode("utf-8"))

md5_key = md5.hexdigest()

requests.post('http://127.0.0.1:9005/api/asset.html',headers={"OpenKey":"%s|%s"%(md5_key,client_time)})