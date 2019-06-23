
import numpy as np

from config import CONFIG
from utils import *

from collections import defaultdict
from shutil import copyfile, move


ground_truth_file_path = relpath('imagenet/caffe_ilsvrc12/val.txt', CONFIG.DATA_DIR)
target_dir_path = relpath('imagenet_val_0.06/', CONFIG.TRAIN_DATA_DIR)
# target_dir_path = relpath('imagenet_val_sensity/', CONFIG.TRAIN_DATA_DIR)
select_num_per_class = 3
class_ids_to_skip = set([434, 446, 460, 843, 639, 640])
# n02807133、n02837789、n02892767、n04371430、n03710637、n03710721
seed = CONFIG.SEED if CONFIG.SEED else np.random.randint(0, 20000)

class_img_map = defaultdict(lambda:[])

with open(ground_truth_file_path) as f:

    for line in f:
        img_fname, class_id = line.split()
        class_id = int(class_id) + 1
        if class_id not in class_ids_to_skip:
            class_img_map[class_id].append(img_fname)


# copy normal imagenet images

for class_imgs in class_img_map.values():

    seed += 1
    np.random.seed(seed)
    selected_indexes = np.random.choice(len(class_imgs), select_num_per_class, replace=False)

    for i in selected_indexes:
        img_fname = class_imgs[i]
        origin_path = relpath('imagenet/ILSVRC2012_img_val/%s'%img_fname, CONFIG.DATA_DIR)
        new_path = relpath(img_fname, target_dir_path)
        copyfile(origin_path, new_path)


# copy sensity imagenet images

# for class_imgs in class_img_map.values():

#     for img_fname in class_imgs:
#         origin_path = relpath('imagenet/ILSVRC2012_img_val/%s'%img_fname, CONFIG.DATA_DIR)
#         new_path = relpath(img_fname, target_dir_path)
#         copyfile(origin_path, new_path)

