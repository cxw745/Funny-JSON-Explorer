from abc import ABC, abstractmethod
from node import CompositeNode, LeafNode

# 建造者模式的抽象基类
class NodeBuilder(ABC):
    @abstractmethod
    def build(self, data, name="root"):
        pass


# 具体建造者，建造 CompositeNode 和 LeafNode
class CompositeNodeBuilder(NodeBuilder):
    def build(self, data, name="root"):
        if isinstance(data, dict):
            node = CompositeNode(name)
            for key, value in data.items():
                child = self.build(value, key)  # 递归建造子节点
                node.add(child)  # 添加子节点到当前节点
            return node
        else:
            return LeafNode(name, data)  # 创建叶子节点


# 指导者类，用于建造树结构
class TreeDirector:
    def __init__(self, builder):
        self._builder = builder

    def build_tree(self, data, name='root'):
        return self._builder.build(data, name)
