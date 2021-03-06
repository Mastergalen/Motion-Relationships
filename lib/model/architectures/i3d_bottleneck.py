"""
Transfer learning of Kinetics-i3d model

You need to run scripts/kinetics/save_i3d_bottleneck.py first to cache bottleneck features
on disk first
"""
import argparse
import keras.backend as K
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from keras import callbacks, losses
from keras.models import Sequential
from keras.layers import Conv3D, AveragePooling3D, Dropout, Lambda, Reshape, Activation

from lib.model.loaders.kinetics_bottleneck import KineticsBottleneckLoader
from lib.model import evaluation

_BATCH_SIZE = 8
_NB_EPOCHS = 50

parser = argparse.ArgumentParser()
parser.add_argument('--training', action='store_true')
parser.add_argument('--lr_flip', action='store_true',
                    help='Flag for enabling horizontal flipping data augmentation')
parser.add_argument('--binary_class', action='store_true',
                    help='Whether to reduce the classification problem to a binary problem')
args = parser.parse_args()


if args.binary_class:
    _NB_CLASSES = 2
else:
    _NB_CLASSES = 4


def build_model():
    model = Sequential()
    model.add(AveragePooling3D(pool_size=(2, 7, 7), strides=(1, 1, 1), padding='valid', input_shape=(19, 7, 7, 1024)))
    model.add(Dropout(0.2))

    # Unit 3D
    model.add(Conv3D(_NB_CLASSES, kernel_size=(1, 1, 1), use_bias=True))

    model.add(Reshape((-1, _NB_CLASSES)))
    model.add(Lambda(lambda x: K.mean(x, axis=1)))
    model.add(Activation('softmax'))

    return model


def get_class_weights(y):
    """
    Determine class weights based on frequency distribution of labels
    :param y:
    :return:
    """
    counter = Counter(np.argmax(y, axis=1))
    majority = max(counter.values())
    return {cls: float(majority/count) for cls, count in counter.items()}


def main():
    model = build_model()

    model.compile(optimizer='adam', loss=losses.categorical_crossentropy,
                  metrics=['accuracy'])

    test_loader = KineticsBottleneckLoader(_NB_CLASSES, 'test', args.lr_flip)
    test_x, test_y = test_loader.load_all()

    if args.training:
        train_loader = KineticsBottleneckLoader(_NB_CLASSES, 'training', args.lr_flip)
        x, y = train_loader.load_all()

        class_weights = get_class_weights(y)

        checkpointer = callbacks.ModelCheckpoint(filepath="data/weights/i3d_bottleneck_weights.hdf5", verbose=1, save_best_only=True)
        early_stopping = callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=2)

        model.fit(x, y, batch_size=_BATCH_SIZE, epochs=_NB_EPOCHS,
                  validation_data=(test_x, test_y),
                  callbacks=[
                      checkpointer,
                      early_stopping,
                  ],
                  shuffle=True,
                  class_weight=class_weights)

    # Load best model
    model.load_weights('data/weights/i3d_bottleneck_weights.hdf5')

    print('Test results:')
    evaluation.evaluate(model, test_x, test_y, _NB_CLASSES)
    print('Data augmentation: {}'.format(args.lr_flip))
    plt.show()


if __name__ == '__main__':
    main()
