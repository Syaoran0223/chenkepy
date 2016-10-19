### 编程规范

#### 缩进
1. 使用4个空格

2. 和括号的开始部分对齐


        foo = func_name(var_one, var_two,
                        var_three, var_four)

 3. 闭合括号
 
        mylist = [
            'a', 'b', 'c',
            'e', 'f', 'g',
            ]
               
4. 每行最大字符数 79（估计一下就可以了）
               


#### import使用

1. 分行包含



        import os
        import sys

2. 分行顺序（中间最好加一个空行）

        标准库
        第三方库
        本地应用或者库

#### 表达式和语句中的空格

1. 括号里

        spam(ham[1], {eggs: 2})
        
2. 逗号， 冒号， 分号之后：

        if x == 4: print x, y; x, y = y, x
        
3. 当＝用于给参数赋值时，不加空格
               

#### 命名

1. 模块名短一点，都小写，用下划线。因为模块会映射到文件的名字，所以避免和系统限制冲突（大小写不区分，长度限制等）

        user_model.py

2. 类名：首字母大写，内部类加入前导下划线

        UserModel

3. 异常名：加入后缀Error

        validationError

4. 函数名：小写+下划线

        get_user()

5. 函数和方法的参数：实例使用self 开始，类使用cls 开始。如果和系统参数名重复，在其后加_

        form.username(class_=‘form-control')

6. 方法名和实例变量：小写+下划线 

        user_name = ‘ck'