table_config = [
    {
        'p': None,
        'title': '选择',
        'display': True,
        'text': {
            'tpl': '<input type="checkbox">',
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
        }
    },
    {
        'p': 'hostname',
        'title': '主机名',
        'display': True,
        'text': {
            'tpl': 'dy.{n1}',
            'kwargs': {
                'n1': '@hostname'
            }
        },
        'attrs': {
            'edit-enable': True,
            'origin':'@hostname',
            'name':'hostname',
        }
    },
    {
        'p': 'asset__cabinet_num',
        'title': '机柜号',
        'display': True,
        'text': {
            'tpl': 'BJ-{n1}',
            'kwargs': {
                'n1': '@asset__cabinet_num'
            }
        },
        'attrs': {
            'edit-enable': True,
        }
    },
    {
        'p': 'asset__business_unit__name',
        'title': '业务线',
        'display': True,
        'text': {
            'tpl': '{n1}',
            'kwargs': {
                'n1': '@asset__business_unit__name'
            }
        },
        'attrs': {
            'edit-enable': True,
            'edit-type':'select',
            'origin':'@asset__business_unit__id',
            'global-key':'business_unit_choice',
        }
    },
    {
        'p': 'create_at',
        'title': '创建时间',
        'display': True,
        'text': {
            'tpl': '{n1}',
            'kwargs': {
                'n1': '@create_at'
            }
        }
    },
    # 页面显示：标题为操作 内容为编辑和删除
    {
        'p': None,
        'title': '操作',
        'display': True,
        'text': {
            'tpl': '<a href="/backstage/curd.html?id={id}">编辑</a>&nbsp;|&nbsp;<a href="#">删除</a>',
            'kwargs': {
                'id': '@id'
            }
        }
    },
]
search_config = [
    {
        'name': 'hostname__contains',
        'title': '主机名',
        'enter_type': 'input',
    },
    {
        'name': 'asset__cabinet_num__contains',
        'title': '机柜号',
        'enter_type': 'input',
    },
    {
        'name': 'asset__business_unit__name',
        'title': '业务线',
        'enter_type': 'select',
        'global_name': 'business_unit_choice',
    },
]