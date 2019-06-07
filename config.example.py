
class Config():

    def __init__(self):

        self.ROOT_DIR = '../' # 'D:/asus_final/'
        self.DATA_DIR = self.ROOT_DIR + 'data/'
        self.TRAIN_DATA_DIR = self.DATA_DIR + 'train/'
        self.LOG_DIR = self.ROOT_DIR + 'programs/logs/'

        self.EPOCHS = 50
        self.TRAIN_SAMPLES_PER_EPOCH = 2000
        self.VAL_SAMPLES_PER_EPOCH = 800
        self.BATCH_SIZE = 32

        self.IMG_SIZE = (299, 299)

        self.CLASS_NUM = 2

        import logging
        self.LOG_LEVEL = logging.INFO


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