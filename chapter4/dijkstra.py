from __future__ import annotations
from typing import TypeVar, List, Optional, Tuple, Dict
from dataclasses import dataclass

from mst import WeightedPath, print_weighted_path
from weighted_graph import WeightedGraph
from weighted_edge import WeightedEdge
from priority_queue import PriorityQueue

V = TypeVar('V')

@dataclass
class DijkstraNode:
    # 顶点的索引
    vertex: int
    # 起点到该顶点的距离
    distance: float

    def __lt__(self, other: DijkstraNode) -> bool:
        return self.distance < other.distance

    def __eq__(self, other: DijkstraNode) -> bool:
        return self.distance == other.distance


def dijkstra(wg: WeightedGraph[V], root:V) -> Tuple[List[Optional[float]],\
    Dict[int: WeightedEdge]]:
    # 找到起点的索引
    first: int = wg.index_of(root)
    # 这个列表用来存储从起点到图中每个点的最小距离
    distances: List[Optional[float]] = [None]*wg.vertex_count
    # 起点到自己的距离是0
    distances[first] = 0
    # 这个字典用于存放我们是如何到达各个顶点的
    path_dict:Dict[int, WeightedEdge] = {}
    # 堆
    pq: PriorityQueue[DijkstraNode] = PriorityQueue()
    # 把起始顶点包裹成的节点压进堆
    pq.push(DijkstraNode(first,0))

    while not pq.empty:
        # 弹出堆顶元素，获取它的索引
        # 由于堆里面的元素都是节点类型，
        # 而节点类型是按照起点到该顶点的距离比较大小的
        # 所以堆顶元素一定是目前距离起点最近的元素
        u: int = pq.pop().vertex
        # 取出起点到该顶点的距离,所有堆里的顶点到起点的最小距离都是已知的
        dist_u: float = distances[u]
        # 查看当前顶点的所有边
        for we in wg.edges_for_index(u):
            # 取出原来保存的起点到这条边的另一端v的距离
            dist_v:float = distances[we.v]
            # 如果这个v是第一次见到或者发现从u走到v比原来的保存路径更短
            if dist_v is None or dist_v>we.weight + dist_u:
                # 更新从起点到v的最短距离
                distances[we.v] = we.weight + dist_u
                # 更新到v这个顶点的最短路径
                path_dict[we.v] = we

                # 把这个点压进堆
                pq.push(DijkstraNode(we.v,we.weight+dist_u))
    return distances,path_dict

def distance_array_to_vertex_dict(wg: WeightedGraph[V], 
                                 distances: List[Optional[float]]) -> Dict[V,Optional[float]]:
    '''这个辅助方法能把距离列表变成距离字典'''
    distance_dict: Dict[V, Optional[float]] = {}
    for i in range(len(distances)):
        distance_dict[wg.vertex_at(i)] = distances[i]

    return distance_dict

def path_dict_to_path(start: int, end: int, 
                      path_dict: Dict[int,WeightedEdge]) -> WeightedPath:
    '''返回从某个起点到某个终点的路径'''
    if len(path_dict) == 0:
        return []
    edge_path: WeightedPath = []
    e: WeightedEdge = path_dict[end]
    edge_path.append(e)
    while e.u != start:
        e = path_dict[e.u]
        edge_path.append(e)
    return list(reversed(edge_path))



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

    distances,path_dict = dijkstra(city_graph2,'Los Angeles')
    name_distance: Dict[str,Optional[int]] = distance_array_to_vertex_dict(city_graph2,
                                                                           distances)
    print('Distances from Los Angeles:')
    for key,value in name_distance.items():
        print(f'{key}: {value}')
    print('')
    print('Shortest path from Los Angeles to Boston:')
    path: WeightedPath = path_dict_to_path(city_graph2.index_of('Los Angeles'),
                                           city_graph2.index_of('Boston'),
                                           path_dict)
    print_weighted_path(city_graph2,path)
