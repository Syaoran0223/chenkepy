部署
===========

### 后端

1. 安装python3及相关库

    `yum install python34`

    `yum install python34-devel`

    `curl https://bootstrap.pypa.io/get-pip.py | python3.4`

    `pip install virtualenv`

2. 安装项目依赖(在information项目目录下操作)
    virtualenv venv
    source ./venv/bin/active
    pip3 install -r requirement.txt  -i  https://pypi.douban.com/simple

3. 初始化数据

    `export BLOG_CONFIG=production`

    `python3 ./manage.py db upgrade`

    `python3 ./manage.py init_data`
    
    > 学校、地区数据

    > `mysql`中 使用`source`命令 导入sql文件 ./data/*.sql

4. 配置文件
    ./config.py

    class ProductionConfig(Config):
      #mysql数据库IP地址
      MYSQL_ADDR = "127.0.0.1"
      DB_NAME = 'pdb'
      USER_NAME = 'information'
      PASSWORD = 'information@i3ke.com'

      CACHE_TYPE ='simple'
      CACHE_REDIS_HOST = '127.0.0.1'
      CACHE_REDIS_PASSWORD = ''
      CACHE_REDIS_DB = 0

      SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{mysql_addr}/{db_name}'.\
          format(username=USER_NAME, password=PASSWORD, mysql_addr=MYSQL_ADDR, db_name=DB_NAME)

      SITE_URL = 'http://192.168.2.131:5000' # host


5.启动项目
    python3 ./run.py

### 前端

1. nodejs安装
    yum install gcc-c++ make
    curl --silent --location https://rpm.nodesource.com/setup_6.x | bash -
    yum -y install nodejs
    # 安装cnpm
    npm install -g cnpm --registry=https://registry.npm.taobao.org
2.安装依赖(在information-static目录下执行)
    cnpm install
3.生成前端代码
    npm run build