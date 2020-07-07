from typing import NamedTuple, List

class Item(NamedTuple):
    '''这是一个物品'''
    name: str
    weight: int
    value: float

def knapsack(items: List[Item], max_capacity: int) -> List[Item]:
    # 建立一个用于存放动态规划结果的列表
    table: List[List[float]] = [[0.0 for _ in range(max_capacity+1)] \
        for _ in range(len(items)+1)]

    for i, item in enumerate(items):
        for capacity in range(1,max_capacity+1):
            previous_items_value: float = table[i][capacity]
            if capacity >= item.weight:
                value_freeing_weight_for_item: float = \
                    table[i][capacity-item.weight]
                # 我们要在两种方案里面选，留下较大的值
                # 一种方案是把这个新东西偷了，剩下的容量用上一次的值，把这两个值加到一起
                # 一种方案就是维持上一次这个容量要偷的物品价值
                table[i+1][capacity] = max(value_freeing_weight_for_item+item.value,
                                           previous_items_value)
            else:
                # 放不下这个新的物品
                table[i+1][capacity] = previous_items_value
    # 从表格中把偷的物品抽出来
    solution: List[Item] = []
    capacity = max_capacity
    for i in range(len(items),0,-1):
        # 这个物品偷了吗？
        if table[i-1][capacity] != table[i][capacity]:
            solution.append(items[i-1])
            # 如果这个物品偷了，就减掉它的重量
            capacity -= items[i-1].weight
    return solution

if __name__ == '__main__':
    items: List[Item] = [Item('television',50,500),
                         Item('candlesticks',2,300),
                         Item('stereo',35,400),
                         Item('laptop',3,1000),
                         Item('food',15,50),
                         Item('clothing',20,800),
                         Item('jewelry',1,4000),
                         Item('books',100,300),
                         Item('printer',18,30),
                         Item('refrigerator',200,700),
                         Item('painting',10,1000)]
    print(knapsack(items,75))
