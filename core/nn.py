# Author: borgwang <borgwang@126.com>
# Date: 2018-05-05
#
# Filename: nn.py
# Description: Feedforwad Neural Network class.


import numpy as np

from core.layers import Dropout


class NeuralNet(object):

    def __init__(self, layers):
        self.layers = layers
        self._phase = 'TRAIN'

    def forward(self, inputs):
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs

    def backward(self, grad):
        all_grads = []
        for layer in reversed(self.layers):
            grad = layer.backward(grad)
            all_grads.append(layer.grads)
        return all_grads[::-1]

    def initialize(self):
        for layer in self.layers:
            layer.initialize()

    def get_params_and_grads(self):
        for layer in self.layers:
            for name, param in layer.params.items():
                grad = layer.grads[name]
                yield param, grad

    def get_parameters(self):
        return [layer.params for layer in self.layers]

    def set_parameters(self, params):
        for i, layer in enumerate(self.layers):
            assert layer.params.keys() == params[i].keys()
            for key in layer.params.keys():
                assert layer.params[key].shape == params[i][key].shape
                layer.params[key] = params[i][key]

    def get_phase(self):
        return self._phase

    def set_phase(self, phase):
        for layer in self.layers:
            layer.set_phase(phase)
        self._phase = phase
