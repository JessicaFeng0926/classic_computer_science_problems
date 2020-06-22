from __future__ import annotations
from dataclasses import dataclass

# 用了这个装饰器，我们就不需要写__init__了，
# 它会自动创建好
# 前提是初始化的属性要有类型注解
@dataclass
class Edge:
    # 起点
    u: int
    # 指向的点
    v: int

    def reversed(self) -> Edge:
        return Edge(self.v,self.u)

    def __str__(self) -> str:
        return f'{self.u} -> {self.v}'
