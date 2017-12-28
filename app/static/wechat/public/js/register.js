/**
 * Created by yifan on 2017/12/24.
 */
$(function () {
    var flag = false;//先定义一个变量，当改变窗口大小的时候用来做判断

    $("input").focus(function(){//获取焦点时，flag为true

        flag = true;

    });

    window.onresize = function(){

        if(flag){//如果flag为true，键盘弹起，改变底部按钮的position，同时将flag改为false

            $(".weui-footer").css({"position":"initial"});

            flag = false;

        }else {
            $(".weui-footer").css({"position":"fixed"});
            console.log(document.activeElement.tagName);
            if(document.activeElement.tagName == "INPUT"){//如果只是收起键盘，而不失去焦点，仍然将flag设为true，否则键盘弹起时仍会将底部按钮顶起
                flag = true;
            }

        }
    };

    $('#teln').blur(function () {
        if($('#teln').val().length!=11 ){
            $.toptips('请输入11位手机号码','warning');
        }
        if(isNaN($('#teln').val())){
            $.toptips('手机号必须为数字','warning');
        }
    });
    $('#hqCode').on('click',function () {
     var    code_this=$(this)
        if($('#teln').val().length!=11 ){
            $.toptips('请输入11位手机号码','warning');
        }else if(isNaN($('#teln').val())){
            $.toptips('手机号必须为数字','warning');
        }else {
            //提交手机号码发送短息
            $.ajax({
                url: "http://j.i3ke.com/api/sms",
                type: "get",
                data: {phone: $('#teln').val()},
                success: function (data) {
                    if(data.code==0){
                        $.toptips('短信发送成功','ok');
                        time(code_this);
                    }else {
                            $.toptips(data.msg,'warning');
                    }
                   console.log(data)
                },
                error: function (err) {
                    console.log(err)
                }
            });
        }
    });
    $('#register').on('click',function () {
        if($('#teln').val().length!=11 ){
            $.toptips('请输入11位手机号码','warning');
        }else if(isNaN($('#teln').val())){
            $.toptips('手机号必须为数字','warning');
        }else if($('#code').val()==''){
            $.toptips('请先填写验证码','warning');
        }else {

        $.ajax({
            url: "/api/register/",
            crossDomain: true,
            type: "post",
            data: JSON.stringify({phone:$("#teln").val(), valid_code: $("#code").val(),visit_code:$("#invitecode").val()}),
            contentType: "application/json",
            dataType: "json",
            beforeSend: function () {
                $.showLoading('验证中');
            },
            success: function(data) {
                $.hideLoading();
                if(data.code==0){
                    window.location.href="/wechat/fillInInfor?teln="+$("#teln").val();
                }
                else {
                    $.toptips(data.msg,'warning');
                }
            },
            error: function(err) {
                console.log(err)
            }
        });
        }
    });

    //获取验证码倒计时
    var wait=60;
    function time(obj) {
        if (wait == 0) {
            obj.attr('disabled',false);
            obj.html("获取验证码");
            wait = 60;
            return;
        } else {
            obj.removeAttr('disabled');
            obj.html("重新发送(" + wait + ")");
            wait--;
            setTimeout(function() {
                    time(obj)
                },
                1000)
        }
    }
});