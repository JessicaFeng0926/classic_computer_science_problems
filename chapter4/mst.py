from typing import TypeVar, List, Optional

from weighted_graph import WeightedGraph
from weighted_edge import WeightedEdge
from priority_queue import PriorityQueue

V = TypeVar('V')
WeightedPath = List[WeightedEdge]

def total_weight(wp: WeightedPath) -> float:
    # 原书sum里面的参数还用方括号括起来变成了列表
    # 其实没有必要，sum接受生成器参数
    return sum(e.weight for e in wp)

def mst(wg: WeightedGraph[V], start: int=0) -> Optional[WeightedPath]:
    '''规划出能够保证每个顶点都可达且总权重最小的路径'''
    if start > (wg.vertex_count-1) or start<0:
        return None
    # 保存最终的路径
    result: WeightedPath = []
    # 用于保存还没有规划的边
    pq: PriorityQueue[WeightedEdge] = PriorityQueue()
    # 用于记录哪些顶点已经规划过了
    visited: [bool] = [False]*wg.vertex_count

    def visit(index: int) -> None:
        # 把当前索引的顶点标记为已经规划过了
        visited[index] = True
        # 对于当前索引的顶点的所有边
        # 如果边的另一个顶点还没有规划
        # 就把这条边放进pq里
        for edge in wg.edges_for_index(index):
            if not visited[edge.v]:
                pq.push(edge)
    # 先从第一个顶点开始规划
    # 执行的操作包括把它标记为已规划
    # 以及把它的边都添加到pq里面
    visit(start)

    while not pq.empty:
        edge = pq.pop()
        # 避免重复添加
        if visited[edge.v]:
            continue
        # 添加新的边
        result.append(edge)
        # 规划这条边的另一个顶点
        visit(edge.v)
    return result

def print_weighted_path(wg: WeightedGraph, wp: WeightedPath) -> None:
    for edge in wp:
        print(f'{wg.vertex_at(edge.u)} {edge.weight}> {wg.vertex_at(edge.v)}')
    print(f'Total Weight: {total_weight(wp)}')

if __name__ == '__main__':
    city_graph2: WeightedGraph[str] = WeightedGraph(["Seattle", "San Francisco", 
                                                     "Los Angeles", "Riverside",
                                                    "Phoenix", "Chicago", 
                                                    "Boston","New York", 
                                                    "Atlanta", "Miami",
                                                    "Dallas", "Houston",
                                                    "Detroit","Philadelphia", 
                                                    "Washington"]) 
    city_graph2.add_edge_by_vertices("Seattle", "Chicago", 1737)
    city_graph2.add_edge_by_vertices("Seattle", "San Francisco", 678)
    city_graph2.add_edge_by_vertices("San Francisco", "Riverside", 386)
    city_graph2.add_edge_by_vertices("San Francisco", "Los Angeles", 348)
    city_graph2.add_edge_by_vertices("Los Angeles", "Riverside", 50)
    city_graph2.add_edge_by_vertices("Los Angeles", "Phoenix", 357)
    city_graph2.add_edge_by_vertices("Riverside", "Phoenix", 307)
    city_graph2.add_edge_by_vertices("Riverside", "Chicago", 1704)
    city_graph2.add_edge_by_vertices("Phoenix", "Dallas", 887)
    city_graph2.add_edge_by_vertices("Phoenix", "Houston", 1015)
    city_graph2.add_edge_by_vertices("Dallas", "Chicago", 805)
    city_graph2.add_edge_by_vertices("Dallas", "Atlanta", 721)
    city_graph2.add_edge_by_vertices("Dallas", "Houston", 225)
    city_graph2.add_edge_by_vertices("Houston", "Atlanta", 702)
    city_graph2.add_edge_by_vertices("Houston", "Miami", 968)
    city_graph2.add_edge_by_vertices("Atlanta", "Chicago", 588)
    city_graph2.add_edge_by_vertices("Atlanta", "Washington", 543)
    city_graph2.add_edge_by_vertices("Atlanta", "Miami", 604)
    city_graph2.add_edge_by_vertices("Miami", "Washington", 923)
    city_graph2.add_edge_by_vertices("Chicago", "Detroit", 238)
    city_graph2.add_edge_by_vertices("Detroit", "Boston", 613)
    city_graph2.add_edge_by_vertices("Detroit", "Washington", 396)
    city_graph2.add_edge_by_vertices("Detroit", "New York", 482)
    city_graph2.add_edge_by_vertices("Boston", "New York", 190)
    city_graph2.add_edge_by_vertices("New York", "Philadelphia", 81)
    city_graph2.add_edge_by_vertices("Philadelphia", "Washington", 123)
    
    result: Optional[WeightedPath] = mst(city_graph2)
    if result is None:
        print('No solution')
    else:
        print_weighted_path(city_graph2, result)


