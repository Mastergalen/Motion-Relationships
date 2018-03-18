import keras
from keras.models import Input, Sequential
from keras.layers import Dense, Dropout
import lib.model.loader as loader
from lib.model.config import CONFIG


def build():
    model = Sequential()
    model.add(Dense(128, activation='relu', input_shape=(300,)))
    model.add(Dropout(CONFIG['dropout']))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(CONFIG['num_relationships'], activation='softmax'))

    # TODO: Early stop
    model.summary()
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer='adam',
                  metrics=['accuracy'])

    return model


def train():
    x_train, y_train, x_valid, y_valid = loader.load()

    model = build()

    history = model.fit(x_train, y_train,
                        batch_size=CONFIG['batch_size'],
                        epochs=CONFIG['epochs'],
                        verbose=1,
                        shuffle=True,
                        validation_data=(x_valid, y_valid))


train()
