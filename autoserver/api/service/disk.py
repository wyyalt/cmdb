from repostiroy import models

def Disk(server_info,server_obj,hostname):
    if not server_info['disk']['status']:
        models.ErrorLog.objects.create(asset_obj=server_obj.asset, title="[%s]磁盘信息采集失败" % hostname,
                                       content=server_info['disk']['data'])
    else:

        new_disk_data = server_info['disk']['data']
        old_disk_data = models.Disk.objects.filter(server_obj=server_obj)

        # 磁盘槽位列表
        new_slot_list = list(new_disk_data.keys())
        old_slot_list = []
        for item in old_disk_data:
            old_slot_list.append(item.slot)

        # 交集：更新
        update_list = set(new_slot_list).intersection(old_slot_list)

        record_list = []
        record_dict = {'pd_type': '类型', 'capacity': '容量', 'model': '型号'}
        for slot in update_list:
            new_disk_row = new_disk_data[slot]
            old_disk_row = models.Disk.objects.filter(server_obj=server_obj, slot=slot).first()

            for k, v in new_disk_row.items():
                value = getattr(old_disk_row, k)
                if value != v:
                    record = "槽位[%s] [%s]：由[%s]更新为[%s]" % (slot, record_dict[k], value, v)
                    record_list.append(record)
                    setattr(old_disk_row, k, v)
            else:
                old_disk_row.save()
        else:
            if record_list:
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=';'.join(record_list))

        # 差集：new-old :创建
        create_list = set(new_slot_list).difference(old_slot_list)

        record_list = []
        for slot in create_list:
            disk_data = server_info['disk']['data'][slot]
            disk_data['server_obj'] = server_obj
            models.Disk.objects.create(**disk_data)
            record = "新增硬盘：槽位{slot},容量{capacity},型号{model},类型{pd_type}".format(**disk_data)
            record_list.append(record)

        if record_list:
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=';'.join(record_list))

        # 差集：old-new :删除
        del_list = set(old_slot_list).difference(new_slot_list)
        if del_list:
            models.Disk.objects.filter(server_obj=server_obj, slot__in=del_list).delete()
            # 记录变更日志
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content="移除磁盘%s" % ("-".join(del_list)))