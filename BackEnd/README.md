## 服务包装的调用模块

#### 相关技术和框架

- nginx
- docker
- flask
- mongodb
- gunicorn
- selenium headless-chrome browsermobproxy

#### 部署方式

`upload-server.sh`

#### 文件意义

-- ./app 文件夹下为核心业务

-- ./docker 文件夹下为docker compose 配置和nginx配置

-- Dockerfile 为 selenium镜像的配置

-- requirements.txt 为selenium镜像为flask所需要下载的库

-- run.py 为main函数，运行代码

-- upload-server.sh 为上传脚本