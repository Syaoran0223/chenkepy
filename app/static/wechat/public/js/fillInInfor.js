/**
 * Created by Administrator on 2017/6/8 0008.
 */
function GetQueryString(name)
{
    var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if(r!=null)return  unescape(r[2]); return null;
}
//选择option
function selectop(op,se) {
    var nextYear = op;
    for(var i=0; i<se.options.length; i++){
        if(se.options[i].value == nextYear){
            se.options[i].selected = true;
            break;
        }
    }
}
$(function () {
    $('#telnNumber').val(GetQueryString('teln'));

    province_id='';
    city_id='';
    county_id='';


    var date = new Date();
    var mon = date.getMonth() + 1;
    var day = date.getDate();
    var nowDay = date.getFullYear() + "-" + (mon<10?"0"+mon:mon) + "-" +(day<10?"0"+day:day);
    $("#date").val(nowDay);
    $("#date").prev().html(nowDay)
    var year=date.getFullYear();


    $.ajax({
        // url: "http://127.0.0.1:5000/api/province",
        url: "/api/province",
        crossDomain: true,
        type: "get",
        // data: JSON.stringify({user_name: "test1", password: "123456"}),
        contentType: "application/json",
        dataType: "json",
        beforeSend:function () {


        },
        success: function(data) {
            $('#loadingToast').hide();
            $.each(data.data,function (index,elem) {
                $("#province").append("<option id='"+elem.id+"' value='"+data.data[index].name+"' >"+data.data[index].name+"</option>");
                // alert(elem.title)
            });
            selectop('福建省',$("#province")[0]);
            $("#province").prev().html( '福建省');
            proption=11
            province_id =1257

        },
        error: function(err) {
            console.log(err)
        }
    });
    $.ajax({
        // url: "http://127.0.0.1:5000/api/city",
        url: "/api/city",
        crossDomain: true,
        type: "get",
        data: {"pro_id":1257 },
        contentType: "application/json",
        dataType: "json",
        beforeSend:function () {
        },
        success: function(data) {
            $('#loadingToast').hide();
            $.each(data.data,function (index,elem) {
                $("#city").append("<option id='"+elem.id+"' value='"+data.data[index].name+"' >"+data.data[index].name+"</option>");
                // alert(elem.title)
            });
            selectop('福州市',$("#city")[0]);
            $("#city").prev().html( '福州市');
            cioption=11;
            city_id=1258

        },
        error: function(err) {
            console.log(err)
        }
    });
    $.ajax({
        // url: "http://127.0.0.1:5000/api/area",
        url: "/api/area",
        crossDomain: true,
        type: "get",
        data: {"city_id":1258 },
        contentType: "application/json",
        dataType: "json",
        beforeSend:function () {
        },
        success: function(data) {
            $('#loadingToast').hide();
            console.log(data)
            $.each(data.data,function (index,elem) {
                $("#county").append("<option id='"+elem.id+"' value='"+data.data[index].name+"' >"+data.data[index].name+"</option>");
                // alert(elem.title)
            });
            selectop('鼓楼区',$("#county")[0]);
            $("#county").prev().html( '鼓楼区');
            option=11
            county_id=1260
        },
        error: function(err) {
            console.log(err)
        }
    });
    $.ajax({
        async:false,
        // url: "http://127.0.0.1:5000/api/school",
        url: "/api/school",
        crossDomain: true,
        type: "get",
        data: {"ctid":1260 },
        contentType: "application/json",
        dataType: "json",
        beforeSend:function () {
            $('#loadingToast').show();
        },
        success: function(data) {
            $('#loadingToast').hide();
            Schoolnum=data.data.length;
            if(data.data.length!=0){
                $.each(data.data,function (index,elem) {
                    $("#school").append("<option id='"+elem.id+"' value='"+data.data[index].name+"' >"+data.data[index].name+"</option>");
                    // alert(elem.title)
                });
            }
            else{
                alert("暂无该区域学校信息")
                $("#school").blur()
            }
        },
        error: function(err) {
            console.log(err)
        }

    })


    $("#province").change(function () {
        $(this).prev().html( $(this).val());
        $("#city").val('').prev().html( '请选择');
        $("#county").val('').prev().html( '请选择');
        $("#school").val('').prev().html( '请选择');
        for(var i=1; i< $("#city")[0].options.length; ){
            $("#city")[0].removeChild(   $("#city")[0].options[i]);
        }
        proption = $("#province")[0].options[$("#province")[0].selectedIndex];
        province_id=proption.id
       // alert($("#province").find("option:checked").attr("id"))
        $.ajax({
            // url: "http://127.0.0.1:5000/api/city",
            url: "/api/city",
            crossDomain: true,
            type: "get",
            data: {"pro_id":proption.id },
            contentType: "application/json",
            dataType: "json",
            beforeSend:function () {
                $("#loadingToast").removeAttr("style")
            },
            success: function(data) {
                $('#loadingToast').hide();
                $.each(data.data,function (index,elem) {
                    $("#city").append("<option id='"+elem.id+"' value='"+data.data[index].name+"' >"+data.data[index].name+"</option>");
                    // alert(elem.title)
                });

            },
            error: function(err) {
                console.log(err)
            }
        })
    });

    $("#city").focus(function () {
        if(typeof(proption)=="undefined")
        {
            alert("请先选择省份")
            $("#city").blur()
        }
    }).change(function () {
        $(this).prev().html( $(this).val());
        $("#county").val('').prev().html( '请选择');
        $("#school").val('').prev().html( '请选择');
        for(var i=1; i< $("#county")[0].options.length; ){
            $("#county")[0].removeChild( $("#county")[0].options[i]);
        }
        cioption = $("#city")[0].options[$("#city")[0].selectedIndex];
        city_id=cioption.id
        $.ajax({
            // url: "http://127.0.0.1:5000/api/area",
            url: "/api/area",
            crossDomain: true,
            type: "get",
            data: {"city_id":cioption.id },
            contentType: "application/json",
            dataType: "json",
            beforeSend:function () {
                $("#loadingToast").removeAttr("style")
            },
            success: function(data) {
                $('#loadingToast').hide();
                console.log(data);
                $.each(data.data,function (index,elem) {
                    $("#county").append("<option id='"+elem.id+"' value='"+data.data[index].name+"' >"+data.data[index].name+"</option>");
                    // alert(elem.title)
                });
            },
            error: function(err) {
                console.log(err)
            }
        })
    });

    $("#county").focus(function () {
        if(typeof(cioption)=="undefined")
        {
            alert("请先选择城市");
            $("#county").blur()
        }

    }).change(function () {
        $(this).prev().html( $(this).val());
        $("#school").val('').prev().html( '请选择');
        option = $("#county")[0].options[$("#county")[0].selectedIndex];
        for(var i=1; i< $("#school")[0].options.length; ){
            $("#school")[0].removeChild( $("#school")[0].options[i]);
        }
        county_id=option.id
        $.ajax({
            async:false,
            // url: "http://127.0.0.1:5000/api/school",
            url: "/api/school",
            crossDomain: true,
            type: "get",
            data: {"ctid":option.id },
            contentType: "application/json",
            dataType: "json",
            beforeSend:function () {
                $('#loadingToast').show();
            },
            success: function(data) {
                $('#loadingToast').hide();
                Schoolnum=data.data.length;
                if(data.data.length!=0){
                    $.each(data.data,function (index,elem) {
                        $("#school").append("<option id='"+elem.id+"' value='"+data.data[index].name+"' >"+data.data[index].name+"</option>");
                        // alert(elem.title)
                    });
                }
                else{
                    alert("暂无该区域学校信息");
                    $("#school").blur()
                }
            },
            error: function(err) {
                console.log(err)
            }

        })
    });
    $("#school").focus(function () {
        if(typeof(cioption)=="undefined")
        {
            alert("请先选择区域");
            $("#school").blur()
        }
         if(Schoolnum==0)
        {
            alert("暂无该区域学校信息");
            $("#school").blur()
        }
    }).change(function () {
        $(this).prev().html( $(this).val());
        schoolid = $("#school")[0].options[$("#school")[0].selectedIndex];
    });
    GRADE = {
        '1': '一年级',
        '2': '二年级',
        '3': '三年级',
        '4': '四年级',
        '5': '五年级',
        '6': '六年级',
        '7': '初一',
        '8': '初二',
        '9': '初三',
        '10': '高一',
        '11': '高二',
        '12': '高三'
    };
    grade11='';
    console.log(subjects[0].children[0]);
    $('#grade').change(function () {
        grade11=1;


    });
    $("#schoolclass").change(function () {
        $(this).prev().html( $(this).val());
    });
    $("#grade").change(function () {
        
        $(this).prev().html( $("#grade").find("option:checked").text());
    });

    $("#stage").change(function () {
        $(this).prev().html( $("#stage").find("option:checked").text());
    });
    //返回
    $("#return").click(function () {
        $("#return_dialog").fadeIn(1)
    });
    $("#cancel_return").click(function () {
        $("#return_dialog").fadeOut(1)
    });
    $("#Confirm_return").click(function () {
        $("#return_dialog").fadeOut(1);
        window.history.back()
    });
    $("#submit").click(function () {
        if($('#userName').val()=='')
        { alert('用户名不能为空') }
        else if($('#passwrod').val()=='')
        { alert('密码不能为空') }
        else if($('#e-mail').val()=='')
        { alert('邮箱地址不能为空') }
        else if($('#province').val()=='请选择')
        { alert('请选择所在省份') }
        else if($('#city').val()=='请选择')
        { alert('请选择所在城市') }
        else if($('#county').val()=='请选择')
        { alert('请选择所在区县') }
        else if($('#school').val()=='请选择')
        { alert('请选择所在学校') }
        else if($('#grade').val()=='请选择')
        { alert('请选择所在年级') }
        else{
            $.ajax({
                url:'/api/register/info/',
                type:'post',
                data:JSON.stringify({
                    "phone": $('#telnNumber').val(),
                    "email": $('#e-mail').val(),
                    "password": $('#passwrod').val(),
                    "repassword": $('#surepass').val(),
                    "user_name": $('#userName').val(),
                    "school_id": schoolid.id,
                    "city_id":city_id,
                    "grade_id": $('#grade').val(),
                    "province_id": province_id,
                    "area_id": county_id
                }),
                dataType: "json",
                contentType: "application/json",
                traditional:true,
                beforeSend:function () {
                    $("#loadingToast2").removeAttr("style")
                    $("#submit").attr({"disabled":"disabled"});
                },
                success:function (data){
                    $("#loadingToast2").hide();
                    if(data.code==0){
                        alert('注册成功');
                        window.location.href="/wechat/login";
                        $("#submit").removeAttr("disabled");
                    }else {
                        $("#submit").removeAttr("disabled");
                        alert(data.msg);
                    }
                },
                error:function () {
                    alert("ajax错误");
                }
            });
        }


    })


})