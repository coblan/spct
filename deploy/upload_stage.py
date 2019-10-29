from fabric import Connection
import invoke
import os
import sys
import shutil

project_name = 'Backendplus'
server_path = '/home/pypro/Backendplus'

server = Connection('root@enjoyst.com')
local = invoke.Context()

base_dir = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )

def upload():
    with local.cd('..'):
        local.run('git archive -o media/%(project_name)s.tar.gz HEAD'%{'project_name':project_name})
    
    server.put(os.path.join(base_dir,'media/%(project_name)s.tar.gz'%{'project_name':project_name}) ,
               '%(path)%s/media/%(name)s.tar.gz'%{'path':server_path,'name':project_name})
    
    server.run("tar xf %s/media/%s.tar.gz"%(server_path,project_name))

if __name__=='__main__':
    upload()