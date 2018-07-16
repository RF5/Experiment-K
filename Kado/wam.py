import tensorflow as tf
import numpy as np

tf.enable_eager_execution()
Sequential = tf.keras.models.Sequential
Layers = tf.keras.layers

class Wam(object):

    def __init__(self, name):
        self.name = name
        self.model = Sequential()
        self.model.add(Layers.Dense(32, input_shape=(4,), activation='relu'))
        self.model.add(Layers.Dense(32, activation='relu'))
        self.model.add(Layers.Dense(2, activation='softmax'))

        self.score = 0

    def predict(self, observation):
        ob_in = np.reshape(observation, (1, 4))
        action = self.model.predict(ob_in)
        action = action[0]
        if action[0] > 0.5 and action[1] < 0.5:
            act = 1
        else:
            act = 0
        return act

    def cross_power_score(self, rollout):
        base_val = 0



    def __str__(self):
        return 'Wam {} | score {}'.format(self.name, self.score)