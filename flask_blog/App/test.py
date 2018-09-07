class Test():
    def __new__(cls, *args, **kwargs):
        obj=super(Test,cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:

            return obj.filter_by(1,2) if not obj._with_deleted else obj
        return obj
    def with_deleted(self):
        return self.__class__(_with_deleted=True)
    def filter_by(self,x,y):
        print(x+y)
a=Test()