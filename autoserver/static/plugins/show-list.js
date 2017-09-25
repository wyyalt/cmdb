(function (jquery) {

    var GLOBAL_DICT = {};
    var LOAD_SEARCH_FLAG = true;

    //字符串格式化
    String.prototype.Format = function (args) {
        var new_Str = this.replace(/\{(\w+)\}/g, function (k, kk) {
            return args[kk]
        });
        return new_Str;
    };

    function initial(url) {
        $.ajax({
            url:url,
            type:'GET',
            dataType:'JSON',
            data:{
                'condition':JSON.stringify(getSearchCondition())
            },
            success:function (data) {
                $.each(data.global_dict,function (k,v) {
                   GLOBAL_DICT[k] = v
                });

                loadHeader(data.table_config);
                loadBody(data);
                loadSearch(data.search_config);
            }
        })
    }

    function createEnterElement(enter_type,global_name,name,parentEle) {
        if (enter_type === 'select'){
            var $select = $("<select></select>");
            $select.attr({
               'name':name,
               'class':'form-control no-radius enter-element'
            });
            $.each(GLOBAL_DICT[global_name],function (k,v) {
                var $option = $('<option></option>');
                $option.val(v[0]);
                $option.text(v[1]);
                $select.append($option);
            });
            $(parentEle).append($select);
        }else{
            var $input = $("<input>");
            $input.attr({
               'name':name,
               'type':'text',
               'class':'form-control no-radius enter-element'
            });
            $(parentEle).append($input);
        }
    }

    function loadSearch(searchConfig){
        if (LOAD_SEARCH_FLAG){
            $.each(searchConfig,function (k,v) {
                var $li = $("<li></li>");
                $li.attr('name',v.name);
                $li.attr('enter-type',v.enter_type);
                if (v.enter_type === 'select'){
                    $li.attr('global-name',v.global_name)
                }
                var $a = $("<a style='cursor: pointer'></a>");
                $a.text(v.title);
                $li.append($a);
                $(".down-list").append($li);
            });
            //设置默认值
            $(".active-item").text(searchConfig[0].title);
            createEnterElement(searchConfig[0].enter_type,searchConfig[0].global_name,searchConfig[0].name,$(".input-group")[0]);
            //标记search选项不再创建
            LOAD_SEARCH_FLAG = false;
        }

    }

    function loadHeader(tableConfig) {
        $("#thead").empty();
        var $tr = $("<tr></tr>");
        $.each(tableConfig,function (k,v) {
            if (v.display){
                $td = $("<th></th>");
                $td.text(v.title);
                $tr.append($td);
            }
        });
        $("#thead").append($tr);
    }

    function loadBody(data) {
        $("#tbody").empty();
        $.each(data.server_list,function (index,server_value) {
            var $tr = $("<tr></tr>");
            $tr.attr('row-id',server_value.id);
            $.each(data.table_config,function (index,title_value) {
                if (title_value.display){
                    var $td = $("<td></td>");
                    /*
                    if (title_value.p){
                        $td.text(server_value[title_value.p]);
                    }else{
                        $td.html('<a>删除</a>')
                    }
                    $td.text(server_value[title_value.p]);

                    if(title_value.p){
                        $td.text(server_value[title_value.p])
                    }else{
                        $td.html(title_value.text);
                    }*/
                    //生成td内容
                    var newKwargs = {};
                    $.each(title_value.text.kwargs,function (kk,vv) {
                        var colName = vv;
                        if(vv.substring(0,2) === '@@'){
                            choice = vv.substring(2,vv.length);
                            choiceIndex = server_value[title_value.p];
                            $.each(GLOBAL_DICT[choice],function (ck,cv) {
                                // console.log(ck,cv);
                                if (cv[0] === choiceIndex){
                                    colName = cv[1];
                                }
                            });
                        }else if(vv[0] === '@'){
                            colName = server_value[vv.substring(1,vv.length)];
                        }
                        newKwargs[kk] = colName;
                    });
                    var newStr = title_value.text.tpl.Format(newKwargs);
                    $td.html(newStr);

                    //设置td属性
                    $.each(title_value.attrs,function (aKey,aValue) {
                        if(aValue[0] == '@'){
                            $td.attr(aKey,server_value[aValue.substring(1,aValue.length)])
                        }else{
                            $td.attr(aKey,aValue)
                        }
                    });
                    $tr.append($td);
                }
            });
            $("#tbody").append($tr)
        })
    }

    function intoEdit($tr) {
        $tr.find('td[edit-enable="true"]').each(function () {
            if ($(this).attr('edit-type') === 'select'){
                //生成select
                var $select = $("<select></select>");
                var $origin = $(this).attr('origin');
                //获取选项
                var $choices = GLOBAL_DICT[$(this).attr('global-key')];

                $.each($choices,function (k,v) {
                    var $option = $("<option></option>");
                    $option.text(v[1]);
                    $option.val(v[0]);
                    if (Number($origin) === v[0]){
                        $option.prop('selected',true)
                    }
                    $select.append($option)
                });
                $(this).html($select)
            }else{
                var $input = $("<input type='text'>");
                $input.val($(this).text());
                $(this).html($input)
            }
        })
    }

    function exitEdit($tr) {
        $tr.find('td[edit-enable="true"]').each(function () {
            if ($(this).attr('edit-type') === 'select'){
                var option = $(this).find('select')[0].selectedOptions;
                var $text = $(option).text();
                $(this).attr('new-origin',$(option).val());
                $(this).html($text);
            }else{
                var $val = $(this).find("input").val();
                $(this).html($val);
            }
        })
    }

    function getSearchCondition() {
        var condition = {};
        $.each($('.search-list').find('input[type="text"],select'),function (k,v) {
            var $name = $(this).attr('name');
            var $value = $(this).val();

            if (condition[$name]){
                condition[$name].push($value);
            }else{
                condition[$name] = [$value];
            }

        });
        return condition
    }

    jquery.extend({
        showList:function (url) {
            initial(url);
            $('#tbody').on('click',':checkbox', function () {
                if($("#editModel").hasClass('btn-warning')) {
                    var $tr = $(this).parent().parent();
                    if ($(this).prop('checked')) {
                        intoEdit($tr);
                    } else {
                        exitEdit($tr);
                    }
                }
            });

            $("#select").click(function () {
                if($("#editModel").hasClass('btn-warning')){
                     $('#tbody').find(':checkbox').each(function () {
                         if (!$(this).prop('checked')){
                             var $tr = $(this).parent().parent();
                             intoEdit($tr);
                             $(this).prop('checked',true);
                         }
                     })
                }else{
                     $('#tbody').find(':checkbox').prop('checked',true);
                }
            });

            $("#reverse").click(function () {
                if($("#editModel").hasClass('btn-warning')){
                    $('#tbody').find(':checkbox').each(function () {
                        var $tr = $(this).parent().parent();
                        if($(this).prop('checked')){
                            $(this).prop('checked',false);
                            exitEdit($tr);
                        }else{
                            $(this).prop('checked',true);
                            intoEdit($tr);
                        }
                    })
                }else{
                    $('#tbody').find(':checkbox').each(function () {
                        $(this).prop('checked',!$(this).prop('checked'))
                    })
                }
            });

            $("#cancel").click(function () {
                if($("#editModel").hasClass('btn-warning')) {
                    $('#tbody').find(':checkbox').each(function () {
                        if($(this).prop('checked')){
                            var $tr = $(this).parent().parent();
                            $(this).prop('checked',false);
                            exitEdit($tr);
                        }
                    })
                }else{
                    $('#tbody').find(':checkbox').prop('checked', false);
                }
            });

            $("#editModel").click(function () {
                if($(this).hasClass('btn-warning')){
                    $(this).removeClass('btn-warning').text('进入编辑模式');
                    $('#tbody').find(':checkbox').each(function () {
                         var $tr = $(this).parent().parent();
                         if ($(this).prop('checked')){
                             exitEdit($tr);
                         }
                     })
                }else{
                    $(this).addClass('btn-warning').text('退出编辑模式');
                    $('#tbody').find(':checkbox').each(function () {
                        if($(this).prop('checked')){
                            var $tr = $(this).parent().parent();
                            intoEdit($tr);
                        }
                    })
                }
            });

            $("#del").click(function () {
                idList = [];
                $("#tbody").find(":checked").each(function () {
                    $val = $(this).val();
                    idList.push($val);
                    console.log($val);
                });

                $.ajax({
                    url:url,
                    type:'delete',
                    data:JSON.stringify(idList),

                    success:function (data) {
                        console.log(data)
                    }
                })

            });

            $("#refresh").click(function () {
                initial(url);
            });

            $("#save").click(function () {
                //退出编辑模式

                if($("#editModel").hasClass('btn-warning')) {
                    $('#tbody').find(':checkbox').each(function () {
                        var $tr = $(this).parent().parent();
                        if ($(this).prop('checked')) {
                            exitEdit($tr);
                        }
                    });
                    $("#editModel").removeClass('btn-warning').text('进入编辑模式');
                }
                //获取数据，通过ajax发送到后台

                var allList = [];
                $("#tbody").children().each(function () {
                    var $id = $(this).attr('row-id');

                    var rowDict = {};
                    var flag = false;
                    $(this).children().each(function () {
                        if($(this).attr('edit-enable')){
                            //下接框数据获取
                            if($(this).attr('edit-type') === 'select'){
                                var $newData = $(this).attr('new-origin');
                                var $oldData = $(this).attr('origin');
                                if($newData){
                                    if ($newData !== $oldData){
                                        var $name = $(this).attr('name');
                                        rowDict[$name] = $newData;
                                        flag = true;
                                    }
                                }
                            }else{
                                //非下拉框数据获取
                                var $newData = $(this).text();
                                var $oldData = $(this).attr('origin');
                                if ($newData !== $oldData){
                                    var $name = $(this).attr('name');
                                    rowDict[$name] = $newData;
                                    flag = true;
                                }
                            }
                        }
                    });
                    if (flag){
                        rowDict['id'] = $id;
                        allList.push(rowDict);
                    }
                });

                $.ajax({
                    url:url,
                    type:'PUT',
                    data:JSON.stringify(allList),

                    success:function (data) {
                        console.log(data)
                    }
                })
            });

            $(".search-list").on('click','li',function () {
                $(this).parent().prev().find(".active-item").text($(this).text());
                $enterType = $(this).attr('enter-type');
                $(this).parent().parent().next().remove();
                createEnterElement($enterType,$(this).attr('global-name'),$(this).attr('name'),$(this).parent().parent().parent());
            });

            $(".search-list").on('click','.add-item',function () {
                var $newItem = $(this).parent().clone();
                $newItem.find('.add-item').addClass('del-item').removeClass('add-item');
                $newItem.find(".glyphicon").removeClass('glyphicon-plus').addClass('glyphicon-minus');
                $(".search-list").append($newItem);
                console.log($newItem[0])
            });

            $(".search-list").on('click','.del-item',function () {
                $(this).parent().remove();
            });

            $(".search-btn").click(function () {
                initial(url);
            });
        }
    });

})(jQuery);