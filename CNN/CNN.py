from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import CNN_create_train_data as data
import time

X, Y = data.getTrainingData()

dense_layers = [1]
layer_sizes = [50]
conv_layers = [10]

for dense_layer in dense_layers:
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
            NAME = "{}-conv-{}-nodes-{}-dense{}".format(conv_layer, layer_size, dense_layer, int(time.time()))
            tensorboard = TensorBoard(log_dir='logs\{}'.format(NAME))
            model = Sequential()
            model.add(Conv2D(layer_size, (2, 2), input_shape=(3, 200, 200)))
            model.add(Activation("relu"))
            model.add(MaxPooling2D(pool_size=(2, 2)))

            for l in range(conv_layer - 1):
                model.add(Conv2D(layer_size, (2, 2), padding="same"))
                model.add(Activation("relu"))
                model.add(MaxPooling2D(pool_size=(2, 2), padding="same"))

            model.add(Flatten())
            model.add(Dropout(0.5))
            for l in range(dense_layer):
                model.add(Dense(layer_size))
                model.add(Activation("relu"))

            model.add(Dense(3))

            model.add(Activation('sigmoid'))

            model.compile(loss='sparse_categorical_crossentropy',
                          optimizer="adam",
                          metrics=['accuracy'])

            model.fit(X, Y, batch_size=32, epochs=45, validation_split=0.3, callbacks=[tensorboard])
            model.save(NAME)
