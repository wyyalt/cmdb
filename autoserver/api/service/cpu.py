from repostiroy import models

def Cpu(server_info,server_obj,hostname):
    if not server_info['cpu']['data']:
        models.ErrorLog.objects.create(asset_obj=server_obj.asset, title="[%s]CPU信息采集失败" % hostname,
                                       content=server_info['cpu']['data'])
    else:

        record_list = []
        record_dict = {
            'cpu_count':'CPU个数',
            'cpu_physical_count':'物理CPU个数',
            'cpu_model':'CPU型号',
        }

        new_cpu_data = server_info['cpu']['data']
        for k,v in new_cpu_data.items():
            value = getattr(server_obj,k)
            if value != v:
                setattr(server_obj,k,v)
                record_list.append("[%s] 项目[%s] 由[%s]更新为[%s]" % (hostname, record_dict[k], value, v))
        else:
            if record_list:
                server_obj.save()
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=';'.join(record_list))
