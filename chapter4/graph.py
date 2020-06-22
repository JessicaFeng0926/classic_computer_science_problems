from typing import Generic, List, Optional, TypeVar

from edge import Edge

# 图中顶点的类型
V = TypeVar('V')


class Graph(Generic[V]):
    def __init__(self, vertices: Optional[List[V]] = None) -> None:
        # 为了保证不会出现一些奇怪的行为，默认值我尽量不适用空列表
        # 这里vertices的默认值使用了None，在方法体内做了判断
        self._vertices: List[V] = vertices or []
        self._edges: List[List[Edge]] = [[] for _ in self._vertices]

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)

    @property
    def edge_count(self) -> int:
        # _edges是一个二维列表，要计算所有元素的个数
        return sum(map(len,self._edges))
    
    def add_vertex(self, vertex: V) -> int:
        self._vertices.append(vertex)
        self._edges.append([])
        # 返回新添加的顶点的索引
        return self.vertex_count - 1
    
    # 这是一个无向图，所以要把两个方向的边都加上
    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)
        self._edges[edge.v].append(edge.reversed())
    
    # 这是上一个方法的变体，对用户比较友好
    def add_edge_by_indices(self,u: int, v:int) -> None:
        edge = Edge(u,v)
        self.add_edge(edge)
    
    # 这还会上上个方法的变体，对用户比较友好
    def add_edge_by_vertices(self,first: V, second: V) -> None:
        u: int = self._vertices.index(first)
        v: int = self._vertices.index(second)
        self.add_edge_by_indices(u,v)

    # 查找指定索引处的顶点
    def vertex_at(self, index: int) -> V:
        return self._vertices[index]

    # 查找指定顶点的索引
    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)
    
    # 根据给定的索引，查找这个顶点的邻居（也就是它指向的所有顶点）
    def neighbors_for_index(self, index: int) -> List[V]:
        # 根据这个索引找到它涉及的所有边
        # 因为这个索引就是u了，所以要找出它指向的所有v
        # 根据索引找出对应的顶点，放到一个列表里返回
        return list(map(self.vertex_at,[e.v for e in self._edges[index]]))
    
    # 只给出顶点，就找到它所有的邻居，这是上一个方法的变体
    def neighbors_for_vertex(self, vertex: V) -> List[V]:
        return self.neighbors_for_index(self.index_of(vertex))

    # 根据索引找出这个顶点的所有边
    def edges_for_index(self, index: int) -> List[Edge]:
        return self._edges[index]
    
    # 根据顶点找到它所有的边，上一个方法的变体
    def edges_for_vertex(self, vertex: V) -> List[Edge]:
        return self.edges_for_index(self.index_of(vertex))

    def __str__(self) -> str:
        desc: str = ''
        for i in range(self.vertex_count):
            desc += f'{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n'
        return desc


if __name__ == '__main__':
    import sys
    import os
    classic_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    
    sys.path.insert(0,classic_dir)
    
    from chapter2.generic_search import bfs,Node,node_to_path

    city_graph: Graph[str] = Graph(['Seattle','San Francisco','Los Angeles',
                                    'Riverside','Phoenix','Chicago','Boston',
                                    'New York','Atlanta','Miami','Dallas',
                                    'Houston','Detroit','Philadelphia','Washington'])
    city_graph.add_edge_by_vertices('Seattle','Chicago')
    city_graph.add_edge_by_vertices('Seattle','San Francisco')
    city_graph.add_edge_by_vertices('San Francisco','Riverside')
    city_graph.add_edge_by_vertices('San Francisco','Los Angeles')
    city_graph.add_edge_by_vertices('Los Angeles','Riverside')
    city_graph.add_edge_by_vertices('Los Angeles','Phoenix')
    city_graph.add_edge_by_vertices('Riverside','Phoenix')
    city_graph.add_edge_by_vertices('Riverside','Chicago')
    city_graph.add_edge_by_vertices('Phoenix','Dallas')
    city_graph.add_edge_by_vertices('Phoenix','Houston')
    city_graph.add_edge_by_vertices('Dallas','Chicago')
    city_graph.add_edge_by_vertices('Dallas','Atlanta')
    city_graph.add_edge_by_vertices('Dallas','Houston')
    city_graph.add_edge_by_vertices('Houston','Atlanta')
    city_graph.add_edge_by_vertices('Houston','Miami')
    city_graph.add_edge_by_vertices('Atlanta','Chicago')
    city_graph.add_edge_by_vertices('Atlanta','Washington')
    city_graph.add_edge_by_vertices('Atlanta','Miami')
    city_graph.add_edge_by_vertices('Miami','Washington')
    city_graph.add_edge_by_vertices('Chicago','Detroit')
    city_graph.add_edge_by_vertices('Detroit','Boston')
    city_graph.add_edge_by_vertices('Detroit','Washington')
    city_graph.add_edge_by_vertices('Detroit','New York')
    city_graph.add_edge_by_vertices('Boston','New York')
    city_graph.add_edge_by_vertices('New York','Philadelphia')
    city_graph.add_edge_by_vertices('Philadelphia','Washington')
    
    bfs_result: Optional[Node[V]] = bfs('Boston',
                                        lambda x:x=='Miami',
                                        city_graph.neighbors_for_vertex)

    if bfs_result is None:
        print('No path')
    else:
        path: List[V] = node_to_path(bfs_result)
        print('Path from Boston to Miami:')
        print(path)

    


        