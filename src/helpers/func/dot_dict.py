class DotObj(object):
    def __init__(self,dc):
        for k,v in dc.items():
            setattr(self,k,v)
    def __getattr__(self,name):
        try:
            return object.__getattr__(self,name)
        except AttributeError:
            return ''