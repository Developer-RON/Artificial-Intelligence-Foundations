import keras
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt


#load the datasets
(x_train, y_train), (x_test, y_test) =  keras.datasets.mnist.load_data()

#normalize the pixels
x_train = x_train / 255.0
x_test = x_test / 255.0

#create a model
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28), dtype=np.float32),

    #hidden layers
    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.2),

    #output layer -> 10 possible outputs
    keras.layers.Dense(10, activation='softmax')
])

#compile model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

#stop once accuracy stops improving
early_stop = keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)

#train model
model.fit(x_train,y_train, 
          epochs=10, 
          batch_size= 32, 
          callbacks=[early_stop])





if __name__ == "__main__":
    #evaluate model
    test_loss, test_accuracy = model.evaluate(x_test,y_test)
    # make predictions
    predictions = model.predict(x_test)

    # display first 5 test images with predictions
    for i in range(5):

        # predicted digit
        predicted_label = np.argmax(predictions[i])

        # actual digit
        actual_label = y_test[i]

        # show image
        plt.imshow(x_test[i], cmap='gray')

        # title
        plt.title(f"Predicted: {predicted_label} | Actual: {actual_label}")

        # remove axis
        plt.axis('off')

        # display image
        plt.show()