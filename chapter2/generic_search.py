from __future__ import annotations
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Set,\
Deque, Dict, Any, Optional,Protocol
from heapq import heappush, heappop

# 它表示任何类型都可以
T = TypeVar('T')

def linear_contains(iterable: Iterable[T], key: T) -> bool:
    '''线性查找'''
    for item in iterable:
        if item == key:
            return True
    return False

C = TypeVar("C", bound="Comparable")

class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...
    def __lt__(self: C, other: C) -> bool:
        ...
    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other
    def __le__(self: C, other: C) -> bool:
        return self < other or self == other
    def __ge__(self: C, other: C) -> bool:
        return not self < other

def binary_contains(sequence: Sequence[C], key: C) -> bool:
    '''二分查找'''
    low: int = 0
    high: int = len(sequence) - 1
    while low <= high: # while there is still a search space
        mid: int = (low + high) // 2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False


class Stack:
    '''用列表实现的栈'''
    def __init__(self):
        self._container = []

    @property
    def empty(self):
        return not self._container

    def push(self,item):
        '''压栈'''
        self._container.append(item)

    def pop(self):
        '''弹栈'''
        return self._container.pop()

    def __repr__(self):
        return repr(self._container)

class Node(Generic[T]):
    # Optional的意思是说这个参数可能是None
    def __init__(self,state:T,parent:Optional[Node],cost:float=0.0,
                 heuristic:float=0.0)->None:
        self.state:T = state
        # 保存一个指向前方的指针
        self.parent:Optional[Node] = parent
        self.cost:float = cost
        self.heuristic:float = heuristic
    
    def __lt__(self,other:Node)->bool:
        '''为了使用小顶堆，必须实现小于的比较'''
        return (self.cost + self.heuristic)<(other.cost + self.heuristic)


def dfs(initial:T,goal_test:Callable[[T],bool],successors:Callable[[T],List[T]])->Optional[Node[T]]:
    # 我们还没有搜索的
    frontier:Stack[Node[T]] = Stack()
    frontier.push(Node(initial,None))
    # 已经搜索过的
    explored:Set[T] = {initial} 

    # 只要还有未搜索的，就一直搜索
    while not frontier.empty:
        current_node:Node[T] = frontier.pop()
        current_state:T = current_node.state
        # 检测刚弹出的栈顶元素是否就是我们的目的地
        if goal_test(current_state):
            return current_node
        # 检查下一步还能往哪里走
        for child in successors(current_state):
            # 如果这个可以走的位置已经探索过了
            # 过
            if child in explored:
                continue
            # 如果这个可以走的位置还没有探索过
            # 添加到已经探索过的集合里面
            explored.add(child)
            # 把这个位置压栈
            frontier.push(Node(child,current_node))
    # 没有找到目标
    return None
        
def node_to_path(node:Node[T])->List[T]:
    path:List[T] = [node.state]
    # 从后往前遍历
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    # 因为是倒着的，所以还要转过来
    path.reverse()
    return path

class Queue:
    def __init__(self):
        self._container = Deque()
    @property
    def empty(self):
        return not self._container
    def push(self,item):
        self._container.append(item)
    def pop(self):
        return self._container.popleft()
    def __repr__(self):
        return repr(self._container)

def bfs(initial,goal_test,successors):
    # 我们还没有搜索的
    frontier:Stack[Node[T]] = Queue()
    frontier.push(Node(initial,None))
    # 已经搜索过的
    explored:Set[T] = {initial} 
    
    # 只要还有未搜索的，就一直搜索
    while not frontier.empty:
        current_node:Node[T] = frontier.pop()
        current_state:T = current_node.state
     
        # 检测刚弹出的栈顶元素是否就是我们的目的地
        if goal_test(current_state):
            return current_node
        # 检查下一步还能往哪里走
        for child in successors(current_state):
            # 如果这个可以走的位置已经探索过了
            # 过
            if child in explored:
                continue
            # 如果这个可以走的位置还没有探索过
            # 添加到已经探索过的集合里面
            explored.add(child)
            # 把这个位置压栈
            frontier.push(Node(child,current_node))
    # 没有找到目标
    return None


class PriorityQueue:
    '''这是借助于小顶堆的队列'''
    def __init__(self):
        self._container = []
    @property
    def empty(self):
        return not self._container
    def push(self,item):
        heappush(self._container,item)
    def pop(self):
        return heappop(self._container)
    def __repr__(self):
        return repr(self._container)


def astar(initial,goal_test,successors,heuristic):
    # 待检查的节点
    frontier = PriorityQueue()
    # 把起点装进去
    frontier.push(Node(initial,None,0.0,heuristic(initial)))
    explored = {initial:0.0}
    count = 0
    while not frontier.empty:
        current_node = frontier.pop()
        current_state = current_node.state
        count += 1
        if goal_test(current_state):
            return current_node,count
        for child in successors(current_state):
            new_cost = current_node.cost + 1
            if child not in explored or explored[child]>new_cost:
                explored[child] = new_cost
                frontier.push(Node(child,current_node,new_cost,heuristic(child)))
    return None
