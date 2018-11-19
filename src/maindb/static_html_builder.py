import requests
import re
from urllib.parse import urljoin, urlparse
import os

class StaticHtmlBuilder(object):
    def __init__(self, url, root_path): 
        rt = requests.get(url)
        self.root_url = url
        o = urlparse(url)
        self.file_name = re.search(r'[^/]+$', o.path).group()
        self.root_path = root_path
        self.content = rt.content.decode('utf-8')
    
    def run(self): 
        self.proc_static()
        fl_path = os.path.join(self.root_path, self.file_name)
        with open(fl_path, 'wb') as f:
            f.write(self.content.encode('utf-8'))
    
    def proc_static(self): 
        ls = []
        for static_mt in re.finditer('"(/static/.+?)"|\'(/static/.+?)\'', self.content):
            ls.append(static_mt.group(1))
        for static_rsc in set(ls):
            rsc_url = urljoin(self.root_url, static_rsc)
            rt = requests.get(rsc_url)
            rsc_path = os.path.join(self.root_path, static_rsc[1:] )  # 移除决定路径 /
            rsc_dir = os.path.dirname(rsc_path)
            os.makedirs(rsc_dir,  exist_ok = True)
            with open(rsc_path, 'bw') as f:
                f.write(rt.content)
        self.content = self.content.replace('"/static', '"static')
        self.content = self.content.replace("'/static", "'static")
    
    def proc_media(self): 
        ls = []
        for static_mt in re.finditer('"(/media/.+?)"|\'(/media/.+?)\'', self.content):
            ls.append(static_mt.group(1))
        for static_rsc in set(ls):
            rsc_url = urljoin(self.root_url, static_rsc)
            rt = requests.get(rsc_url)
            rsc_path = os.path.join(self.root_path, static_rsc[1:] )  # 移除决定路径 /
            rsc_dir = os.path.dirname(rsc_path)
            os.makedirs(rsc_dir,  exist_ok = True)
            with open(rsc_path, 'bw') as f:
                f.write(rt.content)
        self.content = self.content.replace('"/media', '"media')
        self.content = self.content.replace("'/media", "'media")    
        
        
    
    
    