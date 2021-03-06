from repostiroy import models

def Board(server_info,server_obj,hostname):
    if not server_info['basic']['data']:
        models.ErrorLog.objects.create(asset_obj=server_obj.asset, title="[%s]基本信息采集失败" % hostname,
                                       content=server_info['board']['data'])
    else:

        record_list = []
        record_dict = {
            'manufacturer':'厂商',
            'model':'型号',
            'sn':'SN号',
        }

        new_basic_data = server_info['board']['data']
        for k,v in new_basic_data.items():
            value = getattr(server_obj,k)
            if value != v:
                setattr(server_obj,k,v)
                record_list.append("[%s] 项目[%s] 由[%s]更新为[%s]" % (hostname, record_dict[k], value, v))
        else:
            if record_list:
                server_obj.save()
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=';'.join(record_list))
