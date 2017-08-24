/**
 * Created by Administrator on 2017/6/8 0008.
 */
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
    province_id=''
    city_id=''
    county_id=''


    var date = new Date();
    var mon = date.getMonth() + 1;
    var day = date.getDate();
    var nowDay = date.getFullYear() + "-" + (mon<10?"0"+mon:mon) + "-" +(day<10?"0"+day:day);
    $("#date").val(nowDay);
    $("#date").prev().html(nowDay)
    var year=date.getFullYear();
    if(mon<9){
        year=year-1;
    }
    selectop(year,$("#year")[0]);
    $("#year").prev().html( $("#year").find("option").not(function(){ return !this.selected }).text());
    var xueqi;
    if((9<=mon && mon<=12) ||  (1<=mon && mon<=3) ){
        xueqi='FIRST_HALF';
    }else{
        xueqi='SECOND_HALF';
    }
    selectop(xueqi,$("#Semester")[0]);
    $("#Semester").prev().html( $("#Semester").find("option").not(function(){ return !this.selected }).text());
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
            cioption=11
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
    $("#year").change(function () {
        $(this).prev().html( $("#year").find("option:checked").text());
        // $(this).prev().html( $(this).val());
    })
    $("#Semester").change(function () {
        $(this).prev().html( $("#Semester").find("option:checked").text());
        // $(this).prev().html( $(this).val());
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
                console.log(data)
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
            alert("请先选择城市")
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
                    alert("暂无该区域学校信息")
                    $("#school").blur()
                }
            },
            error: function(err) {
                console.log(err)
            }

        })
    })
    $("#school").focus(function () {
        if(typeof(cioption)=="undefined")
        {
            alert("请先选择区域")
            $("#school").blur()
        }
         if(Schoolnum==0)
        {
            alert("暂无该区域学校信息")
            $("#school").blur()
        }
    }).change(function () {
        $(this).prev().html( $(this).val())
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
    }
    grade11=''
    console.log(subjects[0].children[0])
    $('#grade').change(function () {
        grade11=1;
        for(var i=1; i< $("#subject")[0].options.length; ){
            $("#subject")[0].removeChild( $("#subject")[0].options[i]);
        }
        $("#subject").prev().html('请选择');
        $("#subject").val('');
            if(parseInt($(this).val())<7){
                $.each(subjects[0].children,function (index,elem) {
                    $("#subject").append("<option  value='"+elem.id+"' >"+elem.label+"</option>");
                });
            }else  if(parseInt($(this).val())<10){
                $.each(subjects[1].children,function (index,elem) {
                    $("#subject").append("<option  value='"+elem.id+"' >"+elem.label+"</option>");
                });
            }else{
                $.each(subjects[2].children,function (index,elem) {
                    $("#subject").append("<option  value='"+elem.id+"' >"+elem.label+"</option>");
                });
            }

    })
    $("#schoolclass").change(function () {
        $(this).prev().html( $(this).val());
    })
    $("#grade").change(function () {
        
        $(this).prev().html( $("#grade").find("option:checked").text());
        // $(this).prev().html( $(this).val());
    })
    $("#subject").focus(function () {
        if(typeof(grade11)=="undefined" || grade11=='')
        {
            alert("请先选择年级")
            $("#subject").blur()
        }
    });
    $("#subject").change(function () {
        $(this).prev().html( $("#subject").find("option:checked").text());
    })
    $("#stage").change(function () {
        $(this).prev().html( $("#stage").find("option:checked").text());
        // $(this).prev().html( $(this).val());
    })
    // $("#date").datetimePicker({title:"选择日期",m:1});
    // $("#date").click(function () {
    //    alert($("#date").val())
    //     console.log($("#date").val())
    // });
    // laydate({
    //     elem: '#date',
    //     choose: function(dates){ //选择好日期的回调
    //         $("#date").prev().html( $("#date").val());
    //     }
    // })

    $("#date").datetimePicker({title:"选择日期",m:1}).change(function () {
        $(this).prev().html($("#date").val() );
        // $(this).prev().html( $(this).val());
    });

})