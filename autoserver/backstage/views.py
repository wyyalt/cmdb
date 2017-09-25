from django.shortcuts import render, HttpResponse
import json
from repostiroy import models
from datetime import datetime
from datetime import date

# 序列化
from django.core import serializers

from backstage.pageconfig import server
from backstage.pageconfig import asset as Asset

def get_server_list(request,table_config,module_cls):
    condition = json.loads(request.GET.get('condition'))

    from django.db.models import Q

    con = Q()
    for key, value in condition.items():
        sub_con = Q()
        sub_con.connector = "OR"
        for item in value:
            sub_con.children.append((key, item))

        con.add(sub_con, 'AND')

    params_list = []
    for col in table_config:
        if not col['p']:
            continue
        params_list.append(col['p'])

    server_list = module_cls.objects.filter(con).values(*params_list)
    return server_list

# 扩展json
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, value)

def curd(request):
    return render(request, 'curd.html')

def curd_json(request):
    if request.method == "DELETE":
        #行到删除ID列表
        id_list = json.loads(str(request.body,encoding='utf-8'))
        print(id_list)

        #数据库删除操作
        # models.Server.objects.filter(idc__in=id_list).delete()

        return HttpResponse("删除成功！")
    if request.method == "PUT":
        all_list = json.loads(str(request.body,encoding='utf-8'))
        print(all_list)

        #更新数据
        # for row in all_list:
        #     row_id = row.pop('id')
        #     models.Server.objects.filter(id=row_id).update(**row)
        return  HttpResponse("更新成功！")
    if request.method == "POST":
        pass
    if request.method == "GET":
        server_list = get_server_list(request,server.table_config,models.Server)
        # serializers序列化
        # server_set = models.Server.objects.all()
        # data = serializers.serialize('json',server_set)
        # print(data)
        result = {
            'table_config': server.table_config,
            'server_list': list(server_list),
            'global_dict':{
                'business_unit_choice':list(models.BusinessUnit.objects.values_list('id','name'))
            },
            'search_config':server.search_config,
        }

        return HttpResponse(json.dumps(result, cls=CustomJSONEncoder))

def asset(request):
    return render(request, 'asset.html')

def asset_json(request):
    if request.method == "DELETE":
        #行到删除ID列表
        id_list = json.loads(str(request.body,encoding='utf-8'))
        print(id_list)

        #数据库删除操作
        # models.Asset.objects.filter(idc__in=id_list).delete()

        return HttpResponse("删除成功！")
    if request.method == "PUT":
        all_list = json.loads(str(request.body,encoding='utf-8'))
        print(all_list)

        #更新数据
        # for row in all_list:
        #     row_id = row.pop('id')
        #     models.Asset.objects.filter(id=row_id).update(**row)
        return  HttpResponse("更新成功！")
    if request.method == "POST":
        pass
    if request.method == "GET":

        server_list = get_server_list(request,Asset.table_config,models.Asset)

        result = {
            'table_config': Asset.table_config,
            'server_list': list(server_list),
            'global_dict': {
                'device_type_choices': models.Asset.device_type_choices,
                'device_status_choices': models.Asset.device_status_choices,
                'idc_list':list(models.IDC.objects.values_list('id','name')),
            },
            'search_config': Asset.search_config
        }

        return HttpResponse(json.dumps(result, cls=CustomJSONEncoder))
