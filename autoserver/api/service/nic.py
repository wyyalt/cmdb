
from repostiroy import models

def Nic(server_info,server_obj,hostname):
    if not server_info['nic']['status']:
        models.ErrorLog.objects.create(asset_obj = server_obj.asset,title="%s网卡信息采集失败"%hostname,content = server_obj['nic']['data'])
    else:
        new_nic_data =server_info['nic']['data']
        old_nic_data = models.NIC.objects.filter(server_obj=server_obj)

        new_eth_list = list(new_nic_data.keys())
        old_eth_list = []
        for eth in old_nic_data:
            old_eth_list.append(eth.name)

        #交集
        record_list = []
        record_dict = {
            'up':'状态',
            'hwaddr':'MAC地址',
            'ipaddrs':'IP地址',
            'netmask':'子网掩码',
        }
        update_list = set(new_eth_list).intersection(old_eth_list)
        for name in update_list:
            new_eth_data = new_nic_data[name]
            old_eth_data = models.NIC.objects.filter(server_obj=server_obj,name=name).first()
            for k,v in new_eth_data.items():
                value = getattr(old_eth_data,k)
                if value != v:
                    setattr(old_eth_data,k,v)
                    record_list.append("网卡：[%s] 项目：[%s] 由[%s]更新为[%s]".format(name,record_dict[k],value,v))
            else:
                old_eth_data.save()
        else:
            if record_list:
                models.AssetRecord.objects.create(asset_obj = server_obj.asset,content = ";".join(record_list))

        #差集 创建
        create_list = set(new_eth_list).difference(old_eth_list)
        record_list = []
        for name in create_list:
            eth_data = new_nic_data[name]
            eth_data['name'] = name
            eth_data['server_obj'] = server_obj
            models.NIC.objects.create(**eth_data)
            record_list.append("新增加网卡：名称:{name}状态:{up}MAC地址:{hwaddr}IP地址:{ipaddrs}子网掩码:{netmask}".format(**eth_data))
        else:
            if record_list:
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=";".join(record_list))

        #差集 删除
        del_list = set(old_eth_list).difference(new_eth_list)
        if del_list:
            models.NIC.objects.filter(name__in=del_list).delete()
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content="删除网卡：%s"%";".join(del_list))


