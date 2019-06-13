
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input, decode_predictions
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from keras.callbacks import ModelCheckpoint, TensorBoard
# from keras import backend as K

from config import CONFIG
from utils import *
from mlogging import mlogging

from datetime import datetime
import os
import json

# K.logging.set_verbosity(K.logging.WARNING)


class PornographyClassifier(object):

    def __init__(self, model_id=None, img_size=CONFIG.IMG_SIZE, batch_size=CONFIG.BATCH_SIZE, to_log_file=False):

        """
        色情圖片分類模型

        Args:
            model_id: optional，若有指定時會自動載入mode_id所對應的模型，model_id為hdf5檔的檔名
            img_size: 圖片在輸入模型時的長寬(pixel)
            batch_size: 訓練模型或圖片分類時的batch 大小
            to_log_file: 是否要將log匯出
        """

        if model_id==None:
            self._model_id = 'porn_class.' + datetime.today().strftime('%Y%m%d%H%M%S')
        else:
            self._model_id = '%s.contd.%s'%(model_id, datetime.today().strftime('%Y%m%d%H%M%S'))
            self._model = load_model(relpath('%s.hdf5'%model_id, CONFIG.MODELBASE_DIR))

        log_name = None if to_log_file==False else 'porn_class/%s.log'%self._model_id
        self._logger = mlogging.get_logger(log_name=log_name, prefix='porn_class')
        self._logger.info('model: %s'%self._model_id)

        self._img_size = img_size
        self._batch_size = batch_size


    def train(self, data_dir=CONFIG.TRAIN_DATA_DIR, epochs=CONFIG.EPOCHS, dense_infos=CONFIG.DENSE_INFOS, save_gen_imgs=False, use_tensorboard=True):

        """
        訓練色情圖片分類模型

        Args:
            data_dir: 存放訓練圖片的目錄
            epoch: 總共要訓練的回合數
            batch_size: 訓練模型或圖片分類時的batch 大小
            dense_infos: 建立模型時要在pretrained model上加的隱藏層的設定
            save_gen_imgs: 在訓練過程中匯入的圖片會經過預處理，是否要儲存預處理過的圖片
            use_tensorboard: 是否要將訓練的過程紀錄為tensorboard的event log
        """

        self._logger.debug('config: \n%s'%CONFIG)

        base_model = InceptionV3(weights='imagenet', include_top=False)

        x = base_model.output
        x = GlobalAveragePooling2D()(x)

        for info in dense_infos:
            x = Dense(info[0], activation=info[1])(x)

        predictions = Dense(CONFIG.CLASS_NUM, activation='softmax')(x)

        self._model = Model(inputs=base_model.input, outputs=predictions)

        for layer in base_model.layers:
            layer.trainable = False

        self._model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['acc'])

        self._logger.info('model compiled')

        # 其他參數可參考：https://zhuanlan.zhihu.com/p/30197320
        datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, horizontal_flip=True, 
                                      validation_split=CONFIG.VAL_RATIO)

        if save_gen_imgs:
            generated_save_path = relpath('generated/%s'%self._model_id, CONFIG.DATA_DIR)
            os.mkdir(generated_save_path)
        else:
            generated_save_path = None

        train_data_generator = datagen.flow_from_directory(
            data_dir,
            target_size=self._img_size,
            batch_size=self._batch_size,
            # color_mode='grayscale',
            save_to_dir=generated_save_path,
            subset='training',
            seed=CONFIG.SEED)

        val_data_generator = datagen.flow_from_directory(
            data_dir,
            target_size=self._img_size,
            batch_size=self._batch_size,
            # color_mode='grayscale',
            save_to_dir=generated_save_path,
            subset='validation',
            seed=CONFIG.SEED)

        callbacks = []

        checkpoint = ModelCheckpoint(relpath('%s.{epoch:02d}-{val_loss:.4f}.hdf5'%self._model_id, CONFIG.MODELBASE_DIR),
                                     verbose=1, save_best_only=True, mode='min')
        callbacks.append(checkpoint)

        if use_tensorboard:
            tensorboard = TensorBoard(relpath('tensorboard/%s'%self._model_id, CONFIG.LOG_DIR),
                                      batch_size=self._batch_size, histogram_freq=0, write_images=False, write_grads=False, update_freq='batch')
                                      # batch_size=self._batch_size, histogram_freq=1, write_images=True, write_grads=True, update_freq='batch')
            callbacks.append(tensorboard)

        self._logger.info('start training, class infos:\n'+self._get_imgclass_infos(train_data_generator.class_indices))

        history = self._model.fit_generator(train_data_generator, train_data_generator.samples/self._batch_size, 
                                  epochs=epochs, verbose=1, workers=4, use_multiprocessing=False, callbacks=callbacks,
                                  validation_data=val_data_generator, validation_steps=val_data_generator.samples/self._batch_size)

        # if to_log_file:
        #     with open(relpath('%s.trainginglog.json'%self._model_id, CONFIG.LOG_DIR), 'w') as f:
        #         json.dump(history.history, f)

        # self._model.save(relpath(self._model_id, CONFIG.MODELBASE_DIR))



    def classify(self, imgs_dir):

        if not hasattr(self, '_model'):
            raise Exception('No model available.')

        datagen = ImageDataGenerator(rescale=1. / 255)
        generator = datagen.flow_from_directory(
            imgs_dir,
            class_mode=None,
            target_size=self._img_size,
            batch_size=self._batch_size)

        self._logger.info('class info:\n'+self._get_imgclass_infos(generator.class_indices))

        return self._model.predict_generator(generator, generator.samples/self._batch_size, workers=4, use_multiprocessing=False, verbose=1)
        # return self._model.evaluate_generator(generator, generator.samples/self._batch_size, workers=4, use_multiprocessing=False, verbose=1)


    def _get_imgclass_infos(self, indice_map):
        return '\n'.join('- %s: %s'%(class_name, class_indice) for class_name, class_indice in indice_map.items())
 

# class LossHistory(keras.callbacks.Callback):

#    def __init__(self, logger):
#        super(LossHistory, self).__init__()
#        self._logger = logger

#    def on_train_begin(self, logs={}):
#        self.losses = []

#    def on_batch_end(self, batch, logs={}):
#        self.losses.append(logs.get('loss'))
