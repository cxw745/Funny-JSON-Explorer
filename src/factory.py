from abc import ABC, abstractmethod
from visualizer import TreeVisualizer, RectangleVisualizer, NewVisualizer

# 抽象工厂
class VisualizerFactory(ABC):
    @abstractmethod
    def get_visualizer(self, style):
        pass


# 具体工厂
class ConcreteVisualizerFactory(VisualizerFactory):
    def get_visualizer(self, style, icons):
        if style == "tree":
            return TreeVisualizer(icons)
        elif style == "rectangle":
            return RectangleVisualizer(icons)
        elif style == "new":  # 新样式
            return NewVisualizer(icons)
        else:
            raise ValueError(f"Unknown style: {style}")
