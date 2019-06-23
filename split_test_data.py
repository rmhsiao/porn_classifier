
import numpy as np

from config import CONFIG
from utils import *
from mlogging import mlogging

import os


data_path = CONFIG.TRAIN_DATA_DIR
test_data_path = relpath('test/', CONFIG.DATA_DIR)
test_data_ratio = CONFIG.TEST_DATA_RATIO

seed = CONFIG.SEED if CONFIG.SEED else np.random.randint(0, 20000)

for class_dirname in os.listdir(data_path):

    # mlogging.glogger.info('processing class "%s"'%class_dirname)

    img_fname_list = os.listdir(relpath(class_dirname, data_path))

    seed += 1
    np.random.seed(seed)
    test_img_indexes = np.random.choice(len(img_fname_list), int(len(img_fname_list)*test_data_ratio), replace=False)

    mlogging.glogger.info('split class "%s" with %s images to %s trainings & %s tests '%
                          (class_dirname, len(img_fname_list), len(img_fname_list)-len(test_img_indexes), len(test_img_indexes)))

    class_path = relpath(class_dirname, data_path)
    class_test_path = relpath(class_dirname, test_data_path)
    os.makedirs(class_test_path, exist_ok=True)

    for i in test_img_indexes:
        test_img_fname = img_fname_list[i]
        origin_path = relpath(test_img_fname, class_path)
        new_path = relpath(test_img_fname, class_test_path)
        os.rename(origin_path, new_path)
