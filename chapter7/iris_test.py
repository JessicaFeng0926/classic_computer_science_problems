import csv
from typing import List
from random import shuffle
import os

from util import normalize_by_feature_scaling
from network import Network

if __name__ == '__main__':
    # 如果像书上的代码那样直接打开，是找不到文件路径的
    # 我这里把chapter7这个目录保存为BASE_DIR
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    iris_parameters: List[List[float]] = []
    # 这里保存的是预期输出
    iris_classifications: List[List[float]] = []
    iris_species: List[str] = []
    # 因为iris.csv就正好在BASE_DIR里面，
    # 所以拼接起来就是绝对路径了
    with open(os.path.join(BASE_DIR,'iris.csv'),mode='r') as iris_file:
        # 文件后面可能有空行，为了消除这个影响，手动指定只要前150行
        irises: List = list(csv.reader(iris_file))[:150]
        # 原有数据集是按照种类排好序的，我们把它打乱
        shuffle(irises)
        for iris in irises:
            parameters: List[float] = [float(n) for n in iris[:4]]
            iris_parameters.append(parameters)
            species: str = iris[4]
            if species == 'Iris-setosa':
                iris_classifications.append([1.0,0.0,0.0])
            elif species == 'Iris-versicolor':
                iris_classifications.append([0.0,1.0,0.0])
            else:
                iris_classifications.append([0.0,0.0,1.0])
            iris_species.append(species) 
    # 把输入数据规范化
    normalize_by_feature_scaling(iris_parameters)

    iris_network: Network = Network([4,6,3],0.3)

    def iris_interpret_output(output: List[float]) -> str:
        if max(output) == output[0]:
            return "Iris-setosa"
        elif max(output) == output[1]:
            return "Iris-versicolor"
        else:
            return "Iris-virginica"
    
    # 用前140个鸢尾花的数据训练网络50次
    iris_trainers: List[List[float]] = iris_parameters[0:140]
    iris_trainers_corrects: List[List[float]] = iris_classifications[0:140]
    
    for _ in range(50):
        iris_network.train(iris_trainers, iris_trainers_corrects)
    
    # 用最后10朵鸢尾花来测试
    iris_testers: List[List[float]] = iris_parameters[140:150]
    iris_testers_corrects: List[str] = iris_species[140:150]
    iris_results = iris_network.validate(iris_testers, iris_testers_corrects, iris_interpret_output)
    print(f"{iris_results[0]} correct of {iris_results[1]} = {iris_results[2] * 100}%")
    
            
