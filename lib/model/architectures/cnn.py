import os
import numpy as np
from comet_ml import Experiment
from keras import applications
from keras.preprocessing.image import ImageDataGenerator
from keras import losses, callbacks, optimizers
from keras.utils import to_categorical
from keras.models import Sequential, Model
from keras.layers import Dropout, Flatten, Dense
from dotenv import load_dotenv

import lib.model.utils as utils
from lib.model.config import CONFIG
from lib.model import evaluation

load_dotenv('.env')

# experiment = Experiment(api_key=os.environ.get('COMET_ML_KEY')

batch_size = 16
epochs = 50
img_height, img_width = 228, 228
train_data_dir = 'data/cnn_input'

# FIXME: Temporarily set validation set to training
validation_data_dir = 'data/cnn_input'
top_model_weights_path = 'data/weights/bottleneck_fc_model.h5'


def save_bottleneck_features():
    # FIXME: Is preprocessing (subtracting by mean pixel) needed?
    datagen = ImageDataGenerator(rescale=1. / 255)

    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False)
    bottleneck_features_train = model.predict_generator(
        generator)
    np.save('tmp/bottleneck_features_train_y.npy', generator.classes)
    np.save('tmp/bottleneck_features_train.npy',
            bottleneck_features_train)

    generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False)
    bottleneck_features_validation = model.predict_generator(
        generator)
    np.save('tmp/bottleneck_features_validation_y.npy', generator.classes)
    np.save('tmp/bottleneck_features_validation.npy',
            bottleneck_features_validation)


def build_top_model(input_shape):
    model = Sequential()
    model.add(Flatten(input_shape=input_shape))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(CONFIG['num_relationships'], activation='softmax'))

    return model


def train_top_model():
    print('Training top model')
    train_data = np.load('tmp/bottleneck_features_train.npy')
    train_labels = to_categorical(np.load('tmp/bottleneck_features_train_y.npy'),
                                  num_classes=CONFIG['num_relationships'])

    validation_data = np.load('tmp/bottleneck_features_validation.npy')
    validation_labels = to_categorical(np.load('tmp/bottleneck_features_validation_y.npy'),
                                       num_classes=CONFIG['num_relationships'])

    model = build_top_model(train_data.shape[1:])
    model.compile(optimizer='rmsprop',
                  loss=losses.categorical_crossentropy, metrics=['accuracy'])

    checkpointer = callbacks.ModelCheckpoint(filepath=top_model_weights_path, verbose=1, save_best_only=True)
    early_stopping = callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=2)

    class_weight = utils.get_class_weights(train_labels)

    model.fit(train_data, train_labels,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(validation_data, validation_labels),
              class_weight=class_weight,
              callbacks=[
                  checkpointer,
                  early_stopping,
              ])

    model.load_weights(top_model_weights_path)

    evaluation.evaluate(model, validation_data, validation_labels)


def fine_tuning():
    print('Fine tuning')
    # TODO: Change to InceptionResNet
    base_model = applications.VGG16(weights='imagenet', include_top=False, input_shape=(img_height, img_width, 3))
    print('Base model loaded')

    # build a classifier model to put on top of the convolutional model
    top_model = build_top_model(base_model.output_shape[1:])

    # note that it is necessary to start with a fully-trained
    # classifier, including the top classifier,
    # in order to successfully do fine-tuning
    top_model.load_weights(top_model_weights_path)

    # add the model on top of the convolutional base
    model = Model(input=base_model.input, output=top_model(base_model.output))

    # set the first 25 layers (up to the last conv block)
    # to non-trainable (weights will not be updated)
    for layer in model.layers[:15]:
        layer.trainable = False

    # compile the model with a SGD/momentum optimizer
    # and a very slow learning rate.
    model.compile(loss=losses.categorical_crossentropy,
                  optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
                  metrics=['accuracy'])

    # prepare data augmentation configuration
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical')

    validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical')

    checkpointer = callbacks.ModelCheckpoint(filepath="data/weights/top_weights_fine_tune.hdf5", verbose=1, save_best_only=True)
    early_stopping = callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=2)

    class_weight = utils.get_class_weights(train_generator.classes)

    # fine-tune the model
    model.fit_generator(
        train_generator,
        epochs=epochs,
        validation_data=validation_generator,
        class_weight=class_weight,
        callbacks=[
            checkpointer,
            early_stopping,
        ],
    )

    model.load_weights('data/weights/top_weights_fine_tune.hdf5')

    evaluation.evaluate_generator(model, validation_generator)


if __name__ == '__main__':
    save_bottleneck_features()
    train_top_model()
    # fine_tuning()
