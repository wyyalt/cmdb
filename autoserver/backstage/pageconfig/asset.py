table_config = [
    {
        'p': None,
        'title': '选择',
        'display': True,
        'text': {
            'tpl': '<input type="checkbox" value="{n1}">',
            'kwargs': {
                'n1': '@id'
            }
        }
    },
    {
        'p': 'id',
        'title': 'ID',
        'display': False,
        'text': {
            'tpl': '{n1}',
            'kwargs': {
                'n1': '@id'
            }
        },
    },
    {
        'p': 'device_type_id',
        'title': '资产类型',
        'display': True,
        'text': {
            'tpl': '{n1}',
            'kwargs': {
                'n1': '@@device_type_choices'
            }
        },
        'attrs': {
            'k1': 'v1',
            'edit-enable': True,
            'edit-type': 'select',
            'origin': '@device_type_id',
            'global-key': 'device_type_choices',
            'name': 'device_type_id',
        }
    },
    {
        'p': 'device_status_id',
        'title': '状态',
        'display': True,
        'text': {
            'tpl': '{n1}',
            'kwargs': {
                'n1': '@@device_status_choices'
            }
        },
        'attrs': {
            'k1': 'v1',
            'edit-type': 'select',
            'edit-enable': True,
            'origin': '@device_status_id',
            'global-key': 'device_status_choices',
            'name': 'device_status_id',
        }
    },
    {
        'p': 'cabinet_num',
        'title': '机柜号',
        'display': True,
        'text': {
            'tpl': '{n1}',
            'kwargs': {
                'n1': '@cabinet_num'
            }
        },
        'attrs': {
            'k1': 'v1',
            'edit-enable': True,
            'origin': '@cabinet_num',
            'name': 'cabinet_num',
        }
    },
    {
        'p': 'idc__id',
        'title': '机房',
        'display': False,
        'text': {
            'tpl': '{n1}',
            'kwargs': {
                'n1': '@idc__id'
            }
        },
    },
    {
        'p': 'idc__name',
        'title': '机房',
        'display': True,
        'text': {
            'tpl': '{n1}',
            'kwargs': {
                'n1': '@idc__name'
            }
        },
        'attrs': {
            'k1': 'v1',
            'k2': 'v2',
            'edit-enable': True,
            'edit-type': 'select',
            'origin': '@idc__id',
            'global-key': 'idc_list',
            'name': 'idc_id',
        }
    },
    {
        'p': 'latest_date',
        'title': '时间',
        'display': True,
        'text': {
            'tpl': '{n1}',
            'kwargs': {
                'n1': '@latest_date'
            }
        },
        'attrs': {
            'k1': 'v1',
            'edit-enable': True,
            'origin': '@latest_date',
            'name': 'latest_date'
        }
    },
    # 页面显示：标题为操作 内容为编辑和删除
    {
        'p': None,
        'title': '操作',
        'display': True,
        'text': {
            'tpl': '<a href="/backstage/asset.html?id={id}">编辑</a>&nbsp;|&nbsp;<a href="#">删除</a>',
            'kwargs': {
                'id': '@id'
            }
        }
    },
]

search_config = [
    {
        'name': 'cabinet_num__contains',
        'title': '机柜号',
        'enter_type': 'input',
    },
    {
        'name': 'device_type_id',
        'title': '资产类型',
        'enter_type': 'select',
        'global_name': 'device_type_choices',
    },


]