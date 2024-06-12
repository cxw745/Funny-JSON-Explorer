from abc import ABC, abstractmethod

# 抽象基类，表示节点
class Node(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def is_leaf(self):
        pass


# 复合节点类，表示可以包含子节点的节点（组合模式中的“组合”）
class CompositeNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

    # 添加子节点
    def add(self, node):
        self.children.append(node)

    def is_leaf(self):
        return False


# 叶子节点类，表示没有子节点的节点（组合模式中的“叶子”）
class LeafNode(Node):
    def __init__(self, name, value):
        super().__init__(name)
        self.value = value

    def is_leaf(self):
        return True
