
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input, decode_predictions
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.preprocessing.image import ImageDataGenerator
# from keras import backend as K

from config import CONFIG
from utils import *
from mlogging import mlogging

from datetime import datetime
import os
import json

# K.logging.set_verbosity(K.logging.WARNING)


class PornographyClassifier(object):

    def __init__(self, img_size=CONFIG.IMG_SIZE, batch_size=CONFIG.BATCH_SIZE, to_log_file=False):

        self._model_id = 'porn_class' + datetime.today().strftime('%Y%m%d%H%M%S')

        log_name = None if to_log_file==False else 'porn_class/%s.log'%self._model_id
        self._logger = mlogging.get_logger(log_name=log_name, prefix='porn_class')
        self._logger.info('model: %s'%self._model_id)

        self._img_size = img_size
        self._batch_size = batch_size


    def train(self, train_data_dir=CONFIG.TRAIN_DATA_DIR, epochs=CONFIG.EPOCHS, save_gen_imgs=False):

        base_model = InceptionV3(weights='imagenet', include_top=False)

        x = base_model.output
        x = GlobalAveragePooling2D()(x)

        x = Dense(1024, activation='relu')(x)

        predictions = Dense(CONFIG.CLASS_NUM, activation='softmax')(x)

        self._model = Model(inputs=base_model.input, outputs=predictions)

        for layer in base_model.layers:
            layer.trainable = False

        self._model.compile(optimizer='rmsprop', loss='categorical_crossentropy')

        # 其他參數可參考：https://zhuanlan.zhihu.com/p/30197320
        train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, horizontal_flip=True)

        if save_gen_imgs:
            generated_save_path = relpath('generated/%s'%self._model_id, CONFIG.DATA_DIR)
            os.mkdir(generated_save_path)
        else:
            generated_save_path = None

        train_generator = train_datagen.flow_from_directory(
            train_data_dir,
            target_size=self._img_size,
            batch_size=self._batch_size,
            # color_mode='grayscale',
            save_to_dir=generated_save_path)

        self._logger.info(json.dumps(train_generator.class_indices))

        self._model.fit_generator(train_generator, samples_per_epoch=train_generator.samples, verbose=1, workers=4, use_multiprocessing=False)


    def classify(self, imgs_dir):

        datagen = ImageDataGenerator(rescale=1. / 255)
        generator = datagen.flow_from_directory(
            imgs_dir,
            class_mode=None,
            target_size=self._img_size,
            batch_size=self._batch_size)

        self._logger.info(json.dumps(generator.class_indices))

        return self._model.predict_generator(generator, generator.samples/self._batch_size, workers=4, use_multiprocessing=False, verbose=1)

        

if __name__ == '__main__':

    mlogging.glogger.info('start')

    pclassifier = PornographyClassifier()

    pclassifier.train(save_gen_imgs=True)

    print(pclassifier.classify(relpath('test', CONFIG.DATA_DIR)))