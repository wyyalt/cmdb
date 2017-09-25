from django.shortcuts import render,HttpResponse
import json
from repostiroy import models
from django.conf import settings
import importlib
from api.utils.wrapper import AUTH_API
from Crypto.Cipher import AES
from django.http import JsonResponse

def decrypt(msg):
    DATA_KEY = 'kiu4wo2sl7d8hesk'
    cipher = AES.new(DATA_KEY, AES.MODE_CBC, DATA_KEY)
    data = cipher.decrypt(msg)
    result = data[0:-data[-1]]
    return result.decode('utf8')


@AUTH_API
def asset(request):
    if request.method == "POST":
        server_info = json.loads(decrypt(request.body))
        hostname = server_info['basic']['data']['hostname']
        server_obj = models.Server.objects.filter(hostname=hostname).first()

        if not server_obj:
            return HttpResponse("资产没有录入！")

        for k,v in server_info.items():
            print(k,v)

        #资产已录入处理数据

        for k,v in settings.SERVICE_DICT.items():
            module_name,func_name = v.rsplit(".",1)
            m = importlib.import_module(module_name)
            if hasattr(m,func_name):
                func = getattr(m,func_name)
                func(server_info,server_obj,hostname)


    return HttpResponse("OK")


#restful api
def servers(request):
    if request.method == "GET":
        v = models.Server.objects.values('id','hostname')
        server_list = list(v)
        return JsonResponse(server_list,safe=False)
    if request.method == "POST":
        #do something
        return JsonResponse({'status':201})

def server_detail(request,nid):
    if request.method == "GET":
        v = models.Server.objects.filter(id=nid).values('id','hostname')
        server_list = list(v)
        return JsonResponse(server_list, safe=False)

    if request.method == "POST":
        pass

    if request.method == "PUT":
        pass

    if request.method == "DELETE":
        pass




from rest_framework import serializers

class ServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Server
        #设置显示列
        fields = ('id', 'asset_id','hostname') # fields = '__all__'
        #除什么之外
        # exclude = ('ug',)
        #fk显示
        depth = 1  # 0<=depth<=10

from rest_framework import viewsets
class ServerViewSet(viewsets.ModelViewSet):
    queryset = models.Server.objects.all().order_by('-id')
    serializer_class = ServerSerializer



from rest_framework.views import APIView

class AssetView(APIView):
    def get(self,request,*args,**kwargs):
        from django.core import serializers
        data_list = models.Asset.objects.all()

        data = serializers.serialize('json',data_list)
        return HttpResponse(data)


    def post(self,request,*args,**kwargs):
        pass


class DetailView(APIView):
    def get(self,request,nid,*args,**kwargs):
        pass

    def post(self,request,nid,*args,**kwargs):
        pass