class PluginMount(type):
    def __init__(cls,name,bases,attrs):
        if not hasattr(cls,'plugins'):
            cls.plugins = {} 
        else:
            cls.plugins[cls.title] =  cls

class ActionProvider:
    __metaclass__ = PluginMount

