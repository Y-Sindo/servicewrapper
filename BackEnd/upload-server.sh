
set -e

sed -i "_old" 's/False/True/g' ./app/service/setting.py

host='fwwg@192.168.9.50'

echo "开始上传文件..."
dest=/home/fwwg/gf-srvicePacking-call
ssh ${host} "mkdir ${dest}/new"
ssh ${host} "rm -rf ${dest}/current.old"
scp -r * ${host}:${dest}/new

echo "文件上传成功，进行版本更迭..."
ssh ${host} "mv ${dest}/current ${dest}/current.old"
ssh ${host} "mv ${dest}/new ${dest}/current"

echo "docker-compose build ..."
ssh ${host} "cd ${dest}/current/docker && echo zju.edu.cn | sudo -S docker-compose build"

echo "docker-compose up -d ..."
ssh ${host} "cd ${dest}/current/docker && echo zju.edu.cn | sudo -S docker-compose up -d"
echo "Done!"