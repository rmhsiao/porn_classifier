
from config import CONFIG
from utils import *
from mlogging import mlogging
from model import PornographyClassifier, ImageClassifier



mlogging.glogger.info('start')

# MODE = 'train'
# MODE = 'eval'
MODE = 'classify'

if MODE=='train':

    classes = ['diverse_normal_0.06', 'sensity']
    # classes = ['1-normal', 'sensity']
    # classes = ['2-bikini', 'all_naked']
    # classes = ['2-bikini', '4-naked', '6-sex']

    pclassifier = ImageClassifier(model_name='diversed_init_stage_porn_classifier', classes=classes, to_log_file=True)

    pclassifier.train(save_gen_imgs=False, use_tensorboard=True)

elif MODE=='eval':

    # classes = ['1-normal', 'sensity']
    classes = ['2-bikini', 'all_naked']
    # classes = ['2-bikini', '4-naked', '6-sex']

    # model_id = 'soft_porn_classifier.20190622035912.01-1.0523'  # (0.075, 0.9826)
    # model_id = 'soft_porn_classifier.20190622035912.02-0.5248'  # (0.1830, 0.9304)
    # model_id = 'soft_porn_classifier.20190622035912.04-0.4564'  # (0.2270, 0.9130)
    model_id = 'soft_porn_classifier.20190622035912.05-0.3722'  # (0.3144, 0.8696)
    # model_id = 'soft_porn_classifier.20190622035912.06-0.3613'  # (0.4999, 0.8348)

    pclassifier = ImageClassifier(model_id=model_id, classes=classes, to_log_file=False)

    pclassifier.evalutate()

else:

    # classes = ['1-normal', 'sensity']
    # model_id = 'init_stage_porn_classifier.20190622151509.val_loss.02-0.3213-0.8876'

    # classes = ['2-bikini', 'all_naked']
    # model_id = 'soft_porn_classifier.20190622035912.05-0.3722'

    # classes = ['2-bikini', '4-naked', '6-sex']

    pclassifier = PornographyClassifier()

    img_path = relpath('classify/ILSVRC2012_val_00018600.JPEG', CONFIG.DATA_DIR)

    print(pclassifier.classify(img_path))