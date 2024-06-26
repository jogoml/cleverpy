from typing import List
from activation import Activation
from optimizer import Optimizer
from loss import Loss
from neuron import Neuron

class Layer:
    def activate(self, inputs: List[float]) -> List[float]:
        raise NotImplementedError

    def calculate_gradients(self, targets: List[float] = None, downstream_layer = None, loss: Loss = None):
        raise NotImplementedError

    def update_weights(self, inputs: List[float], learning_rate: float, optimizer: Optimizer, layer_index: int):
        raise NotImplementedError

class Dense(Layer):
    def __init__(self, num_neurons: int, activation: Activation):
        self.num_neurons = num_neurons
        self.activation = activation
        self.neurons = []

    def initialize(self, num_inputs_per_neuron: int):
        self.neurons = [Neuron(num_inputs_per_neuron, self.activation) for _ in range(self.num_neurons)]

    def activate(self, inputs: List[float]) -> List[float]:
        return [neuron.activate(inputs) for neuron in self.neurons]

    def calculate_gradients(self, targets: List[float] = None, downstream_layer = None, loss: Loss = None):
        for i, neuron in enumerate(self.neurons):
            if targets is not None:
                neuron.calculate_gradient(target=targets[i], loss=loss)
            else:
                downstream_gradients = [n.gradient for n in downstream_layer.neurons]
                downstream_weights = [[n.weights[i + 1] for n in downstream_layer.neurons] for _ in range(len(self.neurons))]
                neuron.calculate_gradient(downstream_gradients=downstream_gradients, downstream_weights=downstream_weights[i])

    def update_weights(self, inputs: List[float], learning_rate: float, optimizer: Optimizer, layer_index: int):
        for i, neuron in enumerate(self.neurons):
            neuron.update_weights(inputs, learning_rate, optimizer, layer_index, i)
