from repostiroy import models

def Memory(server_info,server_obj,hostname):
    if not server_info['memory']['status']:
        models.ErrorLog.objects.create(asset_obj=server_obj.asset, title="[%s]内存信息采集失败" % hostname,
                                       content=server_info['memory']['data'])
    else:

        new_memory_data = server_info['memory']['data']
        old_memory_data = models.Memory.objects.filter(server_obj=server_obj)

        # 磁盘槽位列表
        new_slot_list = list(new_memory_data.keys())
        old_slot_list = []
        for item in old_memory_data:
            old_slot_list.append(item.slot)

        # 交集：更新
        update_list = set(new_slot_list).intersection(old_slot_list)

        record_list = []
        record_dict = {'capacity': '容量', 'slot': '槽位', 'model': '型号','speed':'速度','manufacturer':'厂商','sn':'SN号'}
        for slot in update_list:
            new_memory_row = new_memory_data[slot]
            old_memory_row = models.Memory.objects.filter(server_obj=server_obj, slot=slot).first()

            for k, v in new_memory_row.items():
                value = getattr(old_memory_row, k)
                if value != v:
                    record = "槽位[%s] 项目[%s] 由[%s]更新为[%s]" % (slot, record_dict[k], value, v)
                    record_list.append(record)
                    setattr(old_memory_row, k, v)
            else:
                old_memory_row.save()
        else:
            if record_list:
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=';'.join(record_list))

        # 差集：new-old :创建
        create_list = set(new_slot_list).difference(old_slot_list)

        record_list = []
        for slot in create_list:
            memory_data = server_info['memory']['data'][slot]
            memory_data['server_obj'] = server_obj
            models.Memory.objects.create(**memory_data)
            record = "新增内存：槽位{slot},容量{capacity},型号{model},速度{speed},厂商{manufacturer},SN号{sn}".format(**memory_data)
            record_list.append(record)

        if record_list:
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=';'.join(record_list))

        # 差集：old-new :删除
        del_list = set(old_slot_list).difference(new_slot_list)
        if del_list:
            models.Memory.objects.filter(server_obj=server_obj, slot__in=del_list).delete()
            # 记录变更日志
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content="移除内存%s" % (";".join(del_list)))