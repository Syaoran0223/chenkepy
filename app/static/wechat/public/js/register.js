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
                    if(data.code==404){
                        $.toptips('后台未查询到您的电话信息，如有疑问请联系思明前台','warning');

                    }else if(data.code==0){
                        $.toptips('短信发送成功','ok');
                        time(code_this);
                    }else if(data.code==400){
                        if(data.msg=='isv.MOBILE_NUMBER_ILLEGAL'){
                            $.toptips('电话号码格式不正确','warning');
                        }else{
                            $.toptips('获取验证码次数过多','warning');
                        }
                    }
                   console.log(data)
                },
                error: function (err) {
                    console.log(err)
                }
            });
        }
    });
    $('#login').on('click',function () {
        if($('#teln').val().length!=11 ){
            $.toptips('请输入11位手机号码','warning');
        }else if(isNaN($('#teln').val())){
            $.toptips('手机号必须为数字','warning');
        }else if($('#code').val()==''){
            $.toptips('请先填写验证码','warning');
        }else {
            window.location.href="/wechat/fillInInfor";
        // $.ajax({
        //     url: "/api/login/",
        //     crossDomain: true,
        //     type: "post",
        //     data: JSON.stringify({user_name:$("#user").val(), password: $("#pass").val()}),
        //     contentType: "application/json",
        //     dataType: "json",
        //     beforeSend: function () {
        //         $.showLoading('登入中');
        //     },
        //     success: function(data) {
        //         $.hideLoading();
        //         if(data.code!=400){
        //             $.toptips('登入成功','ok');
        //             window.location.href="/wechat/index";
        //         }
        //         else {
        //             $.toptips('用户名或密码错误','warning');
        //         }
        //     },
        //     error: function(err) {
        //         console.log(err)
        //     }
        // });
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
            obj.attr('disabled',true);
            obj.html("重新发送(" + wait + ")");
            wait--;
            setTimeout(function() {
                    time(obj)
                },
                1000)
        }
    }
});