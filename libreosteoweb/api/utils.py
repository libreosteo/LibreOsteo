def enum(enumName, *listValueNames):
    listValueNumbers = range(len(listValueNames))
    dictAttrib = dict( zip(listValueNames, listValueNumbers) )
    dictReverse = dict( zip(listValueNumbers, listValueNames) )
    dictAttrib["dictReverse"] = dictReverse
    mainType = type(enumName, (), dictAttrib)
    return mainType

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
