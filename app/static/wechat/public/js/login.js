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

    $('#login').on('click',function () {

        $.ajax({
            url: "/api/login/",
            crossDomain: true,
            type: "post",
            data: JSON.stringify({user_name:$("#user").val(), password: $("#pass").val()}),
            contentType: "application/json",
            dataType: "json",
            beforeSend: function () {
                $.showLoading('登入中');
            },
            success: function(data) {
                $.hideLoading();
                if(data.code!=400){
                    $.toptips('登入成功','ok');
                    window.location.href="/wechat/index";
                }
                else {
                    $.toptips('用户名或密码错误','warning');
                }
            },
            error: function(err) {
                $.hideLoading();
                $.toptips('用户名或密码错误','warning');
                console.log(err)
            }
        });

    });

});