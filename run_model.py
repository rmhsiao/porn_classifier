
from config import CONFIG
from utils import *
from mlogging import mlogging
from model import PornographyClassifier



mlogging.glogger.info('start')

TO_TRAIN = True
# TO_TRAIN = False

if TO_TRAIN:

    pclassifier = PornographyClassifier(to_log_file=False)
    pclassifier.train(save_gen_imgs=True, use_tensorboard=True)

else:

    pclassifier = PornographyClassifier(model_id='porn_class.20190613133041.03-0.7911', to_log_file=False)
    print([pclassifier.classify(relpath('test', CONFIG.DATA_DIR))])