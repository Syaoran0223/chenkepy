/**
 * Created by Administrator on 2017/6/22 0022.
 */
$(function () {

    PAPER_TYPE = {
        'PAPER_UNIT': '单元考',
        'PAPER_MONTH': '月考',
        'PAPER_MIDLE_TERM': '半期考',
        'PAPER_LAST': '期末考',
        'PAPER_TEST': '小测',
        'PAPER_LX': '练习',
        'PAPER_HK': '会考',
        'PAPER_QULITY': '质检',
        'PAPER_MODEL': '模拟考',
        'PAPER_MIDLE': '中考',
        'PAPER_HIGH': '高考',
        'PAPER_ZZZS': '自主招生考试'
    }

    SCHOOL_YEAR = {
        '2010': '2010-2011学年',
        '2011': '2011-2012学年',
        '2012': '2012-2013学年',
        '2013': '2013-2014学年',
        '2014': '2014-2015学年',
        '2015': '2015-2016学年',
        '2016': '2016-2017学年',
        '2017': '2017-2018学年',
        '2018': '2018-2019学年',
        '2019': '2019-2020学年',
        '2020': '2020-2021学年',
        '2021': '2021-2022学年',
        '2022': '2022-2023学年',
        '2023': '2023-2024学年',
        '2024': '2024-2025学年',
        '2025': '2025-2026学年'
    }

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

    SECTION = {
        'FIRST_HALF': "上学期",
        'SECOND_HALF': "下学期"
    }

    SUBJECT = {
        'GS001': '语文',
        'GS002': '数学',
        'GS003': '英语',
        'GS004': '科学',
        'GS005': '体育',
        'GS006': '音乐',
        'GS007': '美术',
        'GS008': '校本课',
        'GS017': '思品',
        'GS009': '品德与生活',
        'GS010': '品德与社会',
        'GS011': '综合实践',
        'GS012': '写字',
        'GS013': '信息',
        'GS014': '少先队活动课',
        'GS015': '心理',
        'GS016': '其他'
    }

    // alert(SUBJECT.GS001)
    $.ajax({
        // url: "http://127.0.0.1:5000/api/paper/upload?pageIndex=0",
        url: "/api/paper/upload?pageIndex=0",
        crossDomain: true,
        type: "get",
//                data: JSON.stringify({user_name: "test1", password: "123456"}),
        contentType: "application/json",
        dataType: "json",
        async:false,
        beforeSend:function () {
            $("#loadingToast").removeAttr("style")
        },
        success: function(data) {
            $('#loadingToast').css("display","none")
            if(data.msg!="请登录后再访问"){
            $.each(data.data.items,function (index,elme) {
                var date=elme.updated_at.substring(0,10);var shenhe="";
                if (elme.state==0){
                   shenhe="未审核"
                }
                else{
                    shenhe="已审核"
                }
                $("#continue").append("<div class='weui-cells page__category-content row' id='"+elme.id+"'> <a class='weui-cell weui-cell_access js_item'  href='javascript:;'> <div class='weui-cell__bd'><p style='float: left'>"+elme.name+"</p> &nbsp;<sub style='color: #9b9b9b'>("+date+")</sub><span style='float: right'>"+shenhe+" &nbsp;</span> </div> <div class='weui-cell__ft'></div> </a> </div>")
            })
            }else{
                alert("请登入后访问")
                window.location.href="/wechat/login";
            }
            // $(".logout").show();

            // $("#updated_at").find("span").html(data.data.updated_at)
            // alert(1111)
            // console.log(data)
        },
        error: function(err) {
            console.log(err)
        }
    })

    function selectop(op,se) {
        var nextYear = op;
        for(var i=0; i<se.options.length; i++){
            if(se.options[i].value == nextYear){
                se.options[i].selected = true;
                break;
            }
        }
    }

    // $(".row").click(function () {
    //     alert( $(this).attr("id"))

    // })
    // document.getElementById("continue").onclick()
    // onClick=alert(1111)
// $("#body").click(function () {
//     alert(11)
//     $('#loadingToast').css("display","block")
// })
//     $(".weui-mask_transparent").click(function () {
//         $('#loadingToast').css("display","none");
//     })
  $(".row").click(function () {
      $("#loadingToast").removeAttr("style")

      var arr = new Array(),sum=0
      uploadid=  $(this).attr("id")
      var winH = $(window).height();
      var categorySpace = 10;
      //刷新页面
      // $("#tiaozhuan").click(function () {
      //     location.reload([true])
      // });
      // $('.js_item').on('click', function(){
      //     var id = $(this).data('id');
      //     window.pageManager.go(id);
      // });

      //改变tabbar样式
      $('.weui-tabbar__item').on('click', function () {
          $(this).addClass('weui-bar__item_on').siblings('.weui-bar__item_on').removeClass('weui-bar__item_on');
      });
      //添加图图片显示
      var asd;


      $gallery = $("#gallery"), $galleryImg = $("#galleryImg"),
          $uploaderInput = $("#uploaderInput"),
          $uploaderFiles = $("#uploaderFiles");

      $uploaderInput.on("change", function(e){
          // test++;
          var t_files = this.files;
          var src, url = window.URL || window.webkitURL || window.mozURL, files = e.target.files;
          for (var i = 0, len = files.length; i < len; ++i) {
              var file = files[i];
              if (url) {
                  src = url.createObjectURL(file);

              } else {
                  src = e.target.result;
              }
              // $uploaderFiles.append($(tmpl.replace('#asd', src)));
//                $uploaderFiles.html($(tmpl.replace('#asd', src)));
//                $("#shangchuang").hide();
              var formData = new FormData($("#uploadForm")[0]);
              // alert( $uploaderInput[0].files[0].name)

              $.ajax({
                  // url:'http://127.0.0.1:5000/api/uploads',
                  url:'/api/uploads',
                  type:'post',
                  // data:{'photo': $uploaderInput[0].files[0].name},
                  // async: false,
                  // data: {"id":"WU_FILE_0"},
                  // data: {user_name: "test1", password: "123456"},
                  data: formData,

                  cache: false,
                  contentType: false,
                  processData: false,
                  beforeSend:function () {
                      $('#loadingToast1').css("display","block")
                  },
                  success:function (date){
                      $('#loadingToast1').css("display","none")
                      arr.push({
                          "url":String(date.data),
                          "can_preview":true,  //如果是图片填true，word填false
                          "name":$uploaderInput[0].files[0].name,
                          "serverCode":0, // 填0
                          "status":"success", // 填 success
                          "percentage":"100%", // 填100%
                          "id":"upfile_"+sum, // 唯一id upfile_开头
                          "error_msg":""
                      });
                      console.log(arr)
                      console.log(sum)

                      var tmpl = '<li class="weui-uploader__file" id="upfile_'+sum+'" style="background-image:url(#asd)"></li>';
                      $uploaderFiles.append($(tmpl.replace('#asd', src)));
                      sum++;
                      console.log(sum)
                      $uploaderInput.val("");
                  },
                  error:function () {
                      alert("ajax错误");
                  }
              });
          }
          console.log(sum)
      });
      //点击删除图片


      function removeByValue(arr, val) {
          for(var i=0; i<arr.length; i++) {
              if(arr[i].id == val) {
                  arr.splice(i, 1);
                  break;
              }
          }
      }
//        var somearray = ["mon", "tue", "wed", "thur"]

      $uploaderFiles.on("click", "li", function(){
          $("#form").removeAttr("style").css("margin-bottom","50px");
          that=this,jqthat=$(this);
          $galleryImg.attr("style", this.getAttribute("style"));
          $gallery.fadeIn(100);
          $("#tabbar").hide();
          console.log(arr);

      });
      $gallery.find("a div").click(function () {
          that.remove();
          var divID = jqthat.attr("id");
          console.log(divID);
          console.log(arr);
          removeByValue(arr,divID);
          console.log(arr);
          // test--;
          sum--;
          console.log(sum)
          $("#uploaderInput").val("");
          $("#shangchuang").show();
      })
      $gallery.on("click", function(){
          $gallery.fadeOut(100);
          $("#tabbar").show();
      });
          $.ajax({
              url: "/api/paper/upload/"+$(this).attr("id"),
              // url: "http://127.0.0.1:5000/api/paper/upload/"+$(this).attr("id"),
              // url: "http://127.0.0.1:5000/api/paper/upload/47",
              crossDomain: true,
              type: "get",
//                data: JSON.stringify({user_name: "test1", password: "123456"}),
              contentType: "application/json",
              dataType: "json",
              // async:false,
              success: function(data) {
                  if (data.data.state==0){
                      $("#state").find("span").html("待审核")
                  }
                  else{
                      $("#state").find("span").html("已审核")
                  }
                  $("#updated_at").find("span").html(data.data.updated_at)
                  $("#year").prev().html(SCHOOL_YEAR[data.data.year]);
                  selectop(data.data.year,$("#year")[0]);
                  $("#Semester").prev().html(SECTION[data.data.section]);
                  selectop(data.data.section, $("#Semester")[0]);
                  var date=data.data.exam_date.substring(0,10);
                  $("#date").val(date).prev().html(date);
                  positionid=data.data.province_id;
                  cioptionid=data.data.city_id;
                  optionid=data.data.area_id;
                  schoolid1=data.data.school_id;
                  Schoolnum=1;
                  $("#province").prev().html(data.data.province_name).prev().val(data.data.province_name);
                  $("#city").prev().html(data.data.city_name).prev().val(data.data.city_name);
                  $("#county").prev().html(data.data.area_name).prev().val(data.data.area_name);
                  $("#school").prev().html(data.data.school_name).prev().val(data.data.school_name);
                  $("#grade").prev().html(GRADE[data.data.grade]);
                  selectop(data.data.grade, $("#grade")[0]);
                  $("#subject").prev().html(SUBJECT[data.data.subject]);
                  selectop(data.data.subject, $("#subject")[0]);
                  $("#stage").prev().html(PAPER_TYPE[data.data.paper_types]);
                  selectop(data.data.paper_types, $("#stage")[0]);
                  $("#papuser").val(data.data.name);
                  $.each(data.data.attachments,function (index,elme) {
                      arr.push(elme);
                      var tmpl = '<li class="weui-uploader__file" id="'+elme.id+'" style="background-image:url(#asd)"></li>';
                      $uploaderFiles.append($(tmpl.replace('#asd', elme.url)));
                      sum=elme.id.replace("upfile_","");
                      console.log(sum)
                      sum++
                      console.log(sum)
                      console.log(elme.id)
                      // test=sum;
                  })
                  diqu(positionid,cioptionid,optionid);
                  $("#continue").hide()
                  // $(".logout").hide();
                  $("#form").show()

              },
              error: function(err) {
                  console.log(err)
              }
          })

// //
        //先载入地点学校
      function diqu(positionid,cioptionid,optionid){
          $.ajax({
              url: "/api/province",
              // url: "http://127.0.0.1:5000/api/province",
              crossDomain: true,
              type: "get",
              // data: JSON.stringify({user_name: "test1", password: "123456"}),
              contentType: "application/json",
              dataType: "json",
              beforeSend:function () {

                  // $('#loadingToast').show();


              },
              success: function(data) {
                  // $('#loadingToast').hide();
                  $.each(data.data,function (index,elem) {
                      $("#province").append("<option id='"+elem.id+"' value='"+data.data[index].name+"' >"+data.data[index].name+"</option>");
                      // alert(elem.title)
                  });

              },
              error: function(err) {
                  console.log(err)
              }
          })

          $.ajax({
              url: "/api/city",
              // url: "http://127.0.0.1:5000/api/city",
              crossDomain: true,
              type: "get",
              data: {"pro_id":positionid },
              contentType: "application/json",
              dataType: "json",
              beforeSend:function () {
                  // $('#loadingToast').show();
              },
              success: function(data) {
                  // $('#loadingToast').hide();
                  $.each(data.data,function (index,elem) {
                      $("#city").append("<option id='"+elem.id+"' value='"+data.data[index].name+"' >"+data.data[index].name+"</option>");
                      // alert(elem.title)
                  });


              },
              error: function(err) {
                  console.log(err)
              }
          })
          $.ajax({
              url: "/api/area",
              // url: "http://127.0.0.1:5000/api/area",
              crossDomain: true,
              type: "get",
              data: {"city_id":cioptionid },
              contentType: "application/json",
              dataType: "json",
              beforeSend:function () {
                  // $('#loadingToast').show();
              },
              success: function(data) {
                  // $('#loadingToast').hide();
                  // console.log(data)
                  $.each(data.data,function (index,elem) {
                      $("#county").append("<option id='"+elem.id+"' value='"+data.data[index].name+"' >"+data.data[index].name+"</option>");
                      // alert(elem.title)
                  });
              },
              error: function(err) {
                  console.log(err)
              }
          })
          $.ajax({
              async:false,
              url: "/api/school",
              // url: "http://127.0.0.1:5000/api/school",
              crossDomain: true,
              type: "get",
              data: {"ctid":optionid },
              contentType: "application/json",
              dataType: "json",
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
                      alert("暂无该区域学校信息1")
                      $("#school").blur()
                  }
              },
              error: function(err) {
                  console.log(err)
              }

          })
      }


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
        $(this).prev().prev().val($(this).val());
        $("#city").val('').prev().html( '请选择').prev().val('请选择');
        $("#county").val('').prev().html( '请选择').prev().val('请选择');
        $("#school").val('').prev().html( '请选择').prev().val('请选择');
        for(var i=1; i< $("#city")[0].options.length; ){
            $("#city")[0].removeChild(   $("#city")[0].options[i]);
        }
        proption = $("#province")[0].options[$("#province")[0].selectedIndex];
        // alert($("#province").find("option:checked").attr("id"))
        positionid=proption.id
        $.ajax({
            url: "/api/city",
            // url: "http://127.0.0.1:5000/api/city",
            crossDomain: true,
            type: "get",
            data: {"pro_id":positionid },
            contentType: "application/json",
            dataType: "json",
            beforeSend:function () {
                $('#loadingToast').show();
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
        if(typeof(positionid)=="undefined")
        {
            alert("请先选择省份")
            $("#city").blur()
        }
    }).change(function () {

        $(this).prev().html( $(this).val());
        $(this).prev().prev().val($(this).val());
        $("#county").val('').prev().html( '请选择').prev().val('请选择');
        $("#school").val('').prev().html( '请选择').prev().val('请选择');
        for(var i=1; i< $("#county")[0].options.length; ){
            $("#county")[0].removeChild( $("#county")[0].options[i]);
        }
        cioption = $("#city")[0].options[$("#city")[0].selectedIndex];
        cioptionid=cioption.id
        $.ajax({
            url: "/api/area",
            // url: "http://127.0.0.1:5000/api/area",
            crossDomain: true,
            type: "get",
            data: {"city_id":cioptionid },
            contentType: "application/json",
            dataType: "json",
            beforeSend:function () {
                $('#loadingToast').show();
            },
            success: function(data) {
                $('#loadingToast').hide();
                // console.log(data)
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
        if(typeof(cioptionid)=="undefined")
        {
            alert("请先选择城市")
            $("#county").blur()
        }

    }).change(function () {
        $(this).prev().html( $(this).val());
        $(this).prev().prev().val($(this).val());
        $("#school").val('').prev().html( '请选择').prev().val('请选择');
        option = $("#county")[0].options[$("#county")[0].selectedIndex];
        optionid=option.id
        for(var i=1; i< $("#school")[0].options.length; ){
            $("#school")[0].removeChild( $("#school")[0].options[i]);
        }

        $.ajax({
            async:false,
            url: "/api/school",
            // url: "http://127.0.0.1:5000/api/school",
            crossDomain: true,
            type: "get",
            data: {"ctid":optionid },
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
        if(typeof(cioptionid)=="undefined")
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
        $(this).prev().prev().val($(this).val());
        schoolid = $("#school")[0].options[$("#school")[0].selectedIndex];
        schoolid1= schoolid.id
    });

    $("#schoolclass").change(function () {
        $(this).prev().html( $(this).val());
    })
    $("#grade").change(function () {

        $(this).prev().html( $("#grade").find("option:checked").text());
        // $(this).prev().html( $(this).val());
    })
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


    $("#submit").click(function () {
        if($('#year').val()=='请选择')
        { alert('请选择年度') }
        else if($('#Semester').val()=='请选择')
        { alert('请选择学期') }
        else if($('#date').val()=='')
        { alert('请选择考试时间') }
        else if($('#province').prev().prev().val()=='请选择')
        { alert('请选择所在省份') }
        else if($('#city').prev().prev().val()=='请选择')
        { alert('请选择所在城市') }
        else if($('#county').prev().prev().val()=='请选择')
        { alert('请选择所在区县') }
        else if($('#schoolclass').val()=='请选择')
        { alert('请选择学校类别') }
        else if($('#school').prev().prev().val()=='请选择')
        { alert('请选择所在学校') }
        else if($('#grade').val()=='请选择')
        { alert('请选择所在年级') }
        else if($('#subject').val()=='请选择')
        { alert('请选择所属科目') }
        else if($('#stage').val()=='请选择')
        { alert('请选择试卷阶段') }
        else  if($('#papuser').val()=='')
        { alert('请输入试卷名称')}
        else  if(arr=='')
        { alert('请选择图片')}
        else {
            $("#loadingToast2").removeAttr("style")
            $.ajax({
                url:'/api/paper/upload/'+uploadid,
                // url:'http://127.0.0.1:5000/api/paper/upload/'+uploadid,
                type:'put',
                data:JSON.stringify({
                    "year":$("#year").val(),
                    "section":$("#Semester").val(), // FIRST_HALF 上学期 SECOND_HALF 下学期
                    "province_id":positionid,
                    "city_id":cioptionid ,
                    "area_id":optionid,
                    "school_id":schoolid1,
                    "grade":$("#grade").val(),
                    "paper_types":$("#stage").val(),
                    "subject":$("#subject").val(),
                    "name":$("#papuser").val(),
                    "exam_date":$("#date").val(),
                    "attachments":arr
                }),
                async: false,
//                data: formData,
//                cache: false,
                // contentType: false,
                // processData: false,
                dataType: "json",
                contentType: "application/json",
                traditional:true,
                beforeSend:function () {
                    $("#submit").attr({"disabled":"disabled"});

                },

                success:function (date){
                    $('#loadingToast2').hide();
                    alert('上传成功')
                    // window.location.href="http://127.0.0.1:5000/wechat/upload";
                    window.location.href="/wechat/upload";
                },
                error:function () {
                    alert("ajax错误");
                }
            });
        }
    })
      // console.log(arr);
//点击返回
      $("#return").click(function () {
            $("#return_dialog").fadeIn(1)
      })
      $("#cancel_return").click(function () {
          $("#return_dialog").fadeOut(1)
      })
      $("#Confirm_return").click(function () {
          $("#return_dialog").fadeOut(1)
          $("#continue").show()
          // $(".logout").show()
              $("#form").hide()

              $("#uploaderInput").val("");
              $('li').remove();
          // test=0;
              sum=0;
              arr=[];
      })

    // $("#return").click(function () {
    //
    //     $("#continue").show()
    //     $("#form").hide()
    //     $("#uploaderInput").val("");
    //     $('li').remove();
    //     arr=[];
    // })
      pushHistory();
      window.addEventListener("popstate", function(e) {

          $("#return").click() ;//根据自己的需求实现自己的功能
      }, false);
      function pushHistory() {
          var state = {
              title: "title",
              url: "#"
          };
          window.history.pushState(state, "title", "#");
      }
    //点击删除
    $("#delete").click(function () {
        $("#delete_dialog").fadeIn(1)
    })
    $("#cancel_delete").click(function () {
        $("#delete_dialog").fadeOut(1)
    })
    $("#Confirm_delete").click(function () {
        $("#delete_dialog").fadeOut(1)
        $.ajax({
            // url:'http://127.0.0.1:5000/api/paper/upload/'+uploadid,
            url:'/api/paper/upload/'+uploadid ,
            type:'delete',
            dataType: "json",
            contentType: "application/json",
            beforeSend:function () {
                $("#loadingToast3").removeAttr("style")
            },
            success:function (date){
                $('#loadingToast3').hide();
                alert('删除成功')
                // window.location.href="http://127.0.0.1:5000/wechat/upload";
                window.location.href="/wechat/upload";
            },
            error:function () {
                alert("ajax错误");
            }
        });
    })
      $("#form").css("margin-bottom","50px");

  })
//     $("#logout").click(function () {
//         $.ajax({
// //                url: "http://127.0.0.1:5000/api/login/",
//             url: "/api/logout/",
//             crossDomain: true,
//             type: "get",
//             // data: JSON.stringify({user_name:$("#user").val(), password: $("#pass").val()}),
//             contentType: "application/json",
//             dataType: "json",
//             success: function(data) {
//                 // if(data.code!=400){
//                     alert("退出成功")
//                     window.location.href="/wechat/login";
//                 // }
// //                    window.location.href="/wechat/upload";
// //                    window.location.href="http://127.0.0.1:5000/wechat/upload";
//             },
//             error: function(err) {
//                 console.log(err)
//             }
//         })
//     })
})
