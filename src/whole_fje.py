import argparse
import json
from abc import ABC, abstractmethod


class FjeExplorer:
    # JSON file loading
    @staticmethod
    def load_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # Loading icon set
    @staticmethod
    def load_icons(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # Command-line argument parsing
    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Funny JSON Explorer (FJE)")
        parser.add_argument("-f", "--file", required=True, help="Path to the JSON file")
        parser.add_argument("-s", "--style", required=True, help="Visualization style")
        parser.add_argument("-i", "--icons", required=True, help="Icon family")
        return parser.parse_args()


# Abstract Product
class Visualizer(ABC):
    @abstractmethod
    def visualize(self, node, level=0):
        pass


# Concrete Products
class TreeVisualizer(Visualizer):
    def visualize(self, node):
        result = self.draw(node)
        return self.beautify(result)

    def draw(self, node, level=0, is_last_child=False):
        result = ""
        prefix = "└─" if is_last_child else "├─"
        indent = "  " * (level - 1) if level > 0 else ""
        if node.is_leaf():
            if node.value == None:
                result += f"{indent}{prefix}{icons['leaf']}{node.name}\n"
            else:
                result += f"{indent}{prefix}{icons['leaf']}{node.name}: {node.value}\n"
        else:
            if node.name != "root":
                result += f"{indent}{prefix}{icons['composite']}{node.name}\n"
            if node.children:
                for i, child in enumerate(node.children[:-1]):
                    result += self.draw(child, level + 1, False)
                result += self.draw(node.children[-1], level + 1, True)
        return result

    def beautify(self, result):
        lines = result.split('\n')
        last_root_index = 0
        for i in range(len(lines) - 1):
            last_non_whitespace_index = len(lines[i]) - len(lines[i].lstrip())
            if last_non_whitespace_index > 0:
                lines[i] = '│' + lines[i][1:]
            if lines[i][0] == '└':
                last_root_index = i
        for i in range(last_root_index + 1, len(lines) - 1):
            lines[i] = ' ' + lines[i][1:]
        modified_result = '\n'.join(lines)
        return modified_result


class RectangleVisualizer(Visualizer):
    def visualize(self, node):
        result = self.draw(node)
        return self.beautify(result)

    def draw(self, node, level=0, is_last_child=False):
        result = ""
        prefix = "├─"
        indent = "│ " * (level - 1) if level > 0 else ""
        if node.is_leaf():
            if node.value == None:
                result += f"{indent}{prefix}{icons['leaf']}{node.name}\n"
            else:
                result += f"{indent}{prefix}{icons['leaf']}{node.name}: {node.value}\n"
        else:
            if node.name != "root":
                result += f"{indent}{prefix}{icons['composite']}{node.name}\n"
            if node.children:
                for i, child in enumerate(node.children[:-1]):
                    result += self.draw(child, level + 1, False)
                result += self.draw(node.children[-1], level + 1, True)
        return result

    def beautify(self, result):
        lines = result.split('\n')
        max_length = max(len(line) for line in lines)  # 获取最长的一行的长度
        for i in range(len(lines)):
            lines[i] = lines[i].ljust(max_length + 7, '─')  # 使用横线填充每行
        for i in range(len(lines)):
            lines[i] = '│' + lines[i][1:-1] + '┤'
        lines[0] = '┌' + lines[0][1:-1] + '┐'
        lines[-2] = '└' + lines[-2][1:-1] + '┘'
        lines[-2] = lines[-2].replace("├", "─", 1)
        lines[-1] = ''
        return '\n'.join(lines)


class NewVisualizer(Visualizer):
    def visualize(self, node, level=0):
        result = "This is new style!"
        indent = " " * level * 2  # More compact indent
        if node.is_leaf():
            result += f"{indent}{icons['leaf']}{node.name}: {node.value}\n"
        else:
            result += f"{indent}{icons['composite']}{node.name}\n"
            for child in node.children:
                result += self.visualize(child, level + 1)
        return result


# Abstract Factory
class VisualizerFactory(ABC):
    @abstractmethod
    def get_visualizer(self, style):
        pass


# Concrete Factory
class ConcreteVisualizerFactory(VisualizerFactory):
    def get_visualizer(self, style):
        if style == "tree":
            return TreeVisualizer()
        elif style == "rectangle":
            return RectangleVisualizer()
        elif style == "new":  # New style
            return NewVisualizer()
        else:
            raise ValueError(f"Unknown style: {style}")


# Builder Pattern
class NodeBuilder(ABC):
    @abstractmethod
    def build(self, data, name="root"):
        pass


# Concrete Builder
class CompositeNodeBuilder(NodeBuilder):
    def build(self, data, name="root"):
        if isinstance(data, dict):
            node = CompositeNode(name)
            for key, value in data.items():
                child = self.build(value, key)
                node.add(child)
            return node
        else:
            return LeafNode(name, data)


# Product of Builder
class Node(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def is_leaf(self):
        pass


class CompositeNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def add(self, node):
        self.children.append(node)

    def is_leaf(self):
        return False


class LeafNode(Node):
    def __init__(self, name, value):
        super().__init__(name)
        self.value = value

    def is_leaf(self):
        return True


# Building tree
class TreeDirector:
    def __init__(self, builder):
        self._builder = builder

    def build_tree(self, data, name='root'):
        return self._builder.build(data, name)


args = FjeExplorer.parse_arguments()
json_data = FjeExplorer.load_json(args.file)
icons = FjeExplorer.load_icons("icons.json")[args.icons]

builder = CompositeNodeBuilder()
director = TreeDirector(builder)
json_tree = director.build_tree(json_data)

# Creating concrete factory
factory = ConcreteVisualizerFactory()
visualizer = factory.get_visualizer(args.style)

# Visualization output
output = visualizer.visualize(json_tree)
print(output)