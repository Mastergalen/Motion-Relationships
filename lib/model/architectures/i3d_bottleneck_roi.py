"""
Transfer learning of Kinetics-i3d model with ROI input

You need to run scripts/kinetics/save_i3d_bottleneck.py first to cache bottleneck features
on disk first
"""
import argparse
import matplotlib.pyplot as plt
import numpy as np
import keras
from collections import Counter
from keras import callbacks, losses
from keras.models import Model
from keras.layers import Conv3D, AveragePooling3D, Dropout,\
    Dense, Flatten, LSTM, Input

from lib.model.loaders.kinetics_bottleneck_roi import KineticsBottleneckRoiLoader
from lib.model import evaluation

_NB_CLASSES = 2
_BATCH_SIZE = 8
_NB_EPOCHS = 50
_NB_FRAMES = 150

parser = argparse.ArgumentParser()
parser.add_argument('--training', action='store_true')
args = parser.parse_args()


def roi_rnn():
    roi_input = Input((_NB_FRAMES, 8), name='roi_input')
    x = LSTM(64, return_sequences=True)(roi_input)
    x = LSTM(64)(x)

    return roi_input, x


def bottleneck_classifier(roi_rnn_output):
    bottleneck_input = Input((19, 7, 7, 1024), name='bottleneck_input')

    x = AveragePooling3D(pool_size=(2, 7, 7), strides=(1, 1, 1), padding='valid')(bottleneck_input)
    x = Dropout(0.2)(x)

    # Unit 3D
    x = Conv3D(_NB_CLASSES, kernel_size=(1, 1, 1), use_bias=True)(x)

    x = Flatten()(x)
    x = keras.layers.concatenate([x, roi_rnn_output])
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = Dense(_NB_CLASSES, activation='softmax')(x)

    return bottleneck_input, x


def build_model():
    roi_input, lstm_output = roi_rnn()
    bottleneck_input, main_out = bottleneck_classifier(lstm_output)

    model = Model(inputs=[bottleneck_input, roi_input], outputs=[main_out])

    print(model.summary())

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

    test_loader = KineticsBottleneckRoiLoader(_NB_CLASSES, 'test')
    test_bottleneck_x, test_roi_x, test_y = test_loader.load_all()

    if args.training:
        train_loader = KineticsBottleneckRoiLoader(_NB_CLASSES, 'training')
        bottleneck_x, roi_x, y = train_loader.load_all()

        class_weights = get_class_weights(y)

        checkpointer = callbacks.ModelCheckpoint(filepath="data/weights/i3d_bottleneck_weights_roi.hdf5",
                                                 verbose=1,
                                                 save_best_only=True)
        early_stopping = callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=2)

        model.fit([bottleneck_x, roi_x], y, batch_size=_BATCH_SIZE, epochs=_NB_EPOCHS,
                  validation_data=([test_bottleneck_x, test_roi_x], test_y),
                  callbacks=[
                      checkpointer,
                      early_stopping,
                  ],
                  shuffle=True,
                  class_weight=class_weights)

    # Load best model
    model.load_weights('data/weights/i3d_bottleneck_weights_roi.hdf5')

    print('Test results:')
    evaluation.evaluate(model, [test_bottleneck_x, test_roi_x], test_y, nb_classes=_NB_CLASSES)

    plt.show()


if __name__ == '__main__':
    main()
