from __future__ import annotations
from typing import List, Callable, TypeVar, Tuple
from functools import reduce

from layer import Layer
from util import sigmoid, derivative_sigmoid

# 神经网络输出的类型
T = TypeVar('T')

class Network:
    def __init__(self, layer_structure: List[int], learning_rate: float,
                 activation_function: Callable[[float], float] = sigmoid,
                 derivative_activation_function: Callable[[float],float] = derivative_sigmoid) -> None:
        if len(layer_structure) < 3:
            raise ValueError('Error: Should be at least 3 layers (1 input, 1 hidden, 1 output)')
        self.layers: List[Layer] = []
        # 输入层
        input_layer: Layer = Layer(None, layer_structure[0], learning_rate,
                                   activation_function,derivative_activation_function)
        self.layers.append(input_layer)
        # 隐藏层和输出层
        for previous, num_neurons in enumerate(layer_structure[1:]):
            next_layer = Layer(self.layers[previous],num_neurons,learning_rate,
                               activation_function,derivative_activation_function)
            self.layers.append(next_layer)

    def outputs(self, input: List[float]) -> List[float]:
        '''层层传递之后得到的最终输出'''
        return reduce(lambda inputs, layer: layer.outputs(inputs), self.layers, input)

    def backpropagate(self, expected: List[float]) -> None:
        '''计算每一层的每个神经元的delta值'''
        # 计算输出层神经元的delta值
        last_layer: int = len(self.layers) - 1
        self.layers[last_layer].calculate_deltas_for_output_layer(expected)
        # 倒着计算隐藏层的delta值
        for l in range(last_layer-1, 0 ,-1):
            self.layers[l].calculate_deltas_for_hidden_layer(self.layers[l+1])


    def update_weights(self) -> None:
        '''根据向后冒泡算出来的那些delta值来更新权重'''
        # 跳过输入层
        for layer in self.layers[1:]:
            for neuron in layer.neurons:
                for w in range(len(neuron.weights)):
                    neuron.weights[w] = neuron.weights[w]+\
                        (neuron.learning_rate*\
                            (layer.previous_layer.output_cache[w])*\
                                neuron.delta)


    def train(self, inputs: List[List[float]], expecteds: List[List[float]]) -> None:
        '''用向后冒泡和更新权重来训练网络'''
        for location,xs in enumerate(inputs):
            ys: List[float] = expecteds[location]
            outs: List[float] = self.outputs(xs)
            self.backpropagate(ys)
            self.update_weights()

    def valildate(self, inputs: List[List[float]], expecteds: List[T], 
                  interpret_output: Callable[[List[float]],T]) -> Tuple[int, int, float]:
        '''这是用来测试训练好的网络的，返回正确个数、总测试数量、正确率'''
        correct: int = 0
        for input, expected in zip(inputs, expecteds):
            result: T = interpret_output(self.outputs(input))
            if result == expected:
                correct += 1
        percentage: float = correct / len(inputs)
        return correct, len(inputs), percentage