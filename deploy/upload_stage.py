from fabric import Connection
import invoke
import os
import sys
import shutil

project_name = 'Backendplus'
server_path = '/home/pypro/Backendplus'

server = Connection('root@192.168.40.145')
local = invoke.Context()

base_dir = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )

def upload():
    print('git 打包当前分支')
    with local.cd('..'):
        local.run('git archive -o media/%(project_name)s.tar.gz HEAD'%{'project_name':project_name})
    print('上传打包文件')
    server.put(os.path.join(base_dir,'media/%(project_name)s.tar.gz'%{'project_name':project_name}) ,
               '%(path)s/media/%(name)s.tar.gz'%{'path':server_path,'name':project_name})
    print('解压文件')
    server.run("tar xvf %(path)s/media/%(name)s.tar.gz -C %(path)s"%{'path':server_path,'name':project_name})
    
    
if __name__=='__main__':
    upload()