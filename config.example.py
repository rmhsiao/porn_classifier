
class Config():

    def __init__(self):

        pass

    def __repr__(self):

        repr_lines = []
        repr_strs = []
        for key, value in self.__dict__.items():
            repr_strs.append('\'%s\': %s'%(key,value))
            if len(repr_strs)>5:
                repr_lines.append(', '.join(repr_strs))
                repr_strs = []
        if len(repr_strs)>0:
            repr_lines.append(', '.join(repr_strs))

        return '\n'.join(repr_lines)



CONFIG = Config()

if __name__ == '__main__':
    
    print('config: \n%s'%CONFIG)