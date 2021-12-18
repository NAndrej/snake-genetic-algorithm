import keras
from keras.models import Sequential
from keras.layers import Dense, Input
from keras.optimizers import SGD, Adam
from keras.constraints import maxnorm
import numpy as np, os

os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '3'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class Brain:

    def __init__(self, input_size, output_size, hidden_layer_size, single_model = None):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_layer_size = hidden_layer_size
        self.build_model(single_model)

    def build_model(self, single_model):
        """Builds the model for generating directions
        """
        if single_model:
            self.model = keras.models.load_model(f"models/{single_model}")
            return
        
        self.model = Sequential([
            Dense(self.input_size, activation = "sigmoid", input_shape=(self.input_size,)),
            Dense(self.output_size, activation = "sigmoid")
        ])
    
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss="mse", optimizer=sgd, metrics=["accuracy"])

        # self.model.compile(optimizer=opt, loss = "mse", metrics = ["accuracy"])
        # self.model.build()

    def set_weights(self, weights):
        """Sets the model weights to the given ones

        Args:
            weights ([array]): [Weights that will replace the ones in this model]
        """
        if len(self.model.layers) != len(weights):
            print("ERROR: Weight mismatch")
            return

        for w, l in zip(weights, self.model.layers):
            w = np.array(w, dtype=np.float32).reshape(l.get_weights()[0].shape)
            bias = np.zeros(l.get_weights()[0].shape[1])
            weight = w, bias

            l.set_weights(weight)

    def get_movement(self, X):
        """Gets a prediction from the model.

        Args:
            X ([array]): [State of the snake]

        Returns:
            [int]: [Predicted direction of the snake]
        """

        # TODO: Please define which integer output maps to which string direction

        X = np.asarray(X)
        X = np.atleast_2d(X)
        prediction = np.argmax(self.model(X), axis=-1)[0]

        return prediction

    def get_weights(self):
        """Gets the weights from the model

        Returns:
            [dict]: [Weights for each model layer]
        """
        dict_ = {}
        for i, layer in enumerate(self.model.layers):
            dict_[i] = layer.get_weights()[0]

        return dict_