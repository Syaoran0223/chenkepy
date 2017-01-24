部署
===========

后端
===========
1. 安装python3及相关库
  yum install python34
  yum install python34-devel
  curl https://bootstrap.pypa.io/get-pip.py | python3.4
  pip install virtualenv

2.安装项目依赖(在information项目目录下操作)
  virtualenv venv
  source ./venv/bin/active
  pip3 install -r requirement.txt  -i  https://pypi.douban.com/simple

3.启动项目
  python3 ./run.py

前端
==========
1. nodejs安装
  yum install gcc-c++ make
  curl --silent --location https://rpm.nodesource.com/setup_6.x | bash -
  yum -y install nodejs
  # 安装cnpm
  npm install -g cnpm --registry=https://registry.npm.taobao.org
2.安装依赖(在information-static目录下执行)
  cnpm install
3.生成前端代码
  npm run dev