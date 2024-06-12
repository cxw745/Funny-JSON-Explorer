---
title: Funny-JSON-Explorer
date: 2024-06-10T19:44:57Z
lastmod: 2024-06-12T11:26:46Z
---

# Funny JSON Explorer设计文档

# 任务介绍

> ​![image](https://cdn.jsdelivr.net/gh/cxw745/ImgBed/image-20240612112017-2ecxb23.png)​
>
> ​![image](https://cdn.jsdelivr.net/gh/cxw745/ImgBed/image-20240612112242-sjgq73y.png)​

# 设计文档

## 类图与说明

使用[PlantUML Web Server](https://www.plantuml.com/plantuml/uml/SyfFKj2rKt3CoKnELR1Io4ZDoSa70000) 绘制uml类图，绘制代码位于`class_pic.puml`​。

* ​`fje.py`​：包含命令行参数解析和 JSON 文件加载功能。
* ​`visualizer.py`​：包含所有可视化相关的类。
* ​`factory.py`​：包含可视化工厂相关的类。
* ​`builder.py`​：包含建造者模式相关的类。
* ​`node.py`​：包含节点相关的类。
* ​`example.json`​：测试可视化结果的代码。
* ​`icons.json`​：图标族的配置文件。

​![image](https://cdn.jsdelivr.net/gh/cxw745/ImgBed/20240612104909.png)​

* **组合模式**：在 `CompositeNode`​ 和 `LeafNode`​ 之间使用。`CompositeNode`​ 可以包含多个 `Node`​ 对象（即可以是 `CompositeNode`​ 或 `LeafNode`​）。
* **建造者模式**：通过 `NodeBuilder`​ 和其子类 `CompositeNodeBuilder`​ 构建复杂的树结构，并由 `TreeDirector`​ 指导构建过程。
* **抽象工厂模式**：通过 `VisualizerFactory`​ 和其子类 `ConcreteVisualizerFactory`​ 创建不同类型的 `Visualizer`​ 对象。
* **工厂模式**：`FjeExplorer`​ 使用 `ConcreteVisualizerFactory`​ 来获取特定样式的 `Visualizer`​ 实例。

### 组合模式

**定义**：组合模式将对象组合成树形结构以表示“部分-整体”的层次结构。组合模式使得用户对单个对象和组合对象的使用具有一致性。

**说明**：

* ​`Node`​ 是抽象基类，定义了节点的基本接口。
* ​`CompositeNode`​ 是组合节点，可以包含子节点（既可以是 `CompositeNode`​ 也可以是 `LeafNode`​）。
* ​`LeafNode`​ 是叶子节点，没有子节点。

**实现**：

```python
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
```

### 建造者模式

**定义**：建造者模式将一个复杂对象的构建过程与其表示分离，使得同样的构建过程可以创建不同的表示。

**说明**：

* ​`NodeBuilder`​ 是抽象建造者，定义了构建方法。
* ​`CompositeNodeBuilder`​ 是具体建造者，实现了具体的构建方法，将数据构建成一个树形结构。

**实现**：

```python
class NodeBuilder(ABC):
    @abstractmethod
    def build(self, data, name="root"):
        pass

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
```

### 抽象工厂模式 

**定义**：抽象工厂模式提供一个创建一系列相关或相互依赖对象的接口，而无需指定它们具体的类。

**说明**：

* ​`VisualizerFactory`​ 是抽象工厂，定义了获取 `Visualizer`​ 的接口。
* ​`ConcreteVisualizerFactory`​ 是具体工厂，实现了获取具体 `Visualizer`​ 对象的方法。

**实现**：

```python
class VisualizerFactory(ABC):
    @abstractmethod
    def get_visualizer(self, style, icons):
        pass

class ConcreteVisualizerFactory(VisualizerFactory):
    def get_visualizer(self, style, icons):
        if style == "tree":
            return TreeVisualizer(icons)
        elif style == "rectangle":
            return RectangleVisualizer(icons)
        elif style == "new":
            return NewVisualizer(icons)
        else:
            raise ValueError(f"Unknown style: {style}")
```

### 工厂方法模式

**定义**：工厂方法模式定义一个用于创建对象的接口，让子类决定实例化哪一个类。工厂方法使一个类的实例化延迟到其子类。

**说明**：

* ​`ConcreteVisualizerFactory`​ 实现了 `get_visualizer`​ 方法，这个方法就是工厂方法，根据传入的样式和图标创建具体的 `Visualizer`​ 对象。

**实现**：

```python
class ConcreteVisualizerFactory(VisualizerFactory):
    def get_visualizer(self, style, icons):
        if style == "tree":
            return TreeVisualizer(icons)
        elif style == "rectangle":
            return RectangleVisualizer(icons)
        elif style == "new":
            return NewVisualizer(icons)
        else:
            raise ValueError(f"Unknown style: {style}")
```

### FJE实现

**说明**：

1. **组合模式** 用于定义树形结构的节点（`CompositeNode`​ 和 `LeafNode`​）。
2. **建造者模式** 用于构建 JSON 数据的树形结构（`CompositeNodeBuilder`​ 和 `TreeDirector`​）。
3. **抽象工厂模式** 和 **工厂方法模式** 用于创建不同风格的可视化器（`VisualizerFactory`​ 和 `ConcreteVisualizerFactory`​）。

```python
# 解析命令行参数
args = FjeExplorer.parse_arguments()

# 加载 JSON 数据和图标
json_data = FjeExplorer.load_json(args.file)
icons = FjeExplorer.load_icons("icons.json")[args.icons]

# 使用建造者模式构建树
builder = CompositeNodeBuilder()
director = TreeDirector(builder)
json_tree = director.build_tree(json_data)

# 使用抽象工厂模式获取具体的可视化器
factory = ConcreteVisualizerFactory()
visualizer = factory.get_visualizer(args.style, icons)

# 可视化输出
output = visualizer.visualize(json_tree)
print(output)
```

# 结果展示

## 实现要求

1. 不改变现有代码，只需添加新的抽象工厂，即可添加新的风格。

    在`visualizer.py`​中，通过继承类**Visualizer**并重写**visualize**方法即可添加新的风格。

    示例如下，创建一个新的风格NewVisulizer，并在具体可视化工厂中添加创建实际的工厂选项，在执行脚本时，参数`-s`​后跟新添加的可视化风格名称即可使用新的可视化风格。

    ```python
    # visualizer.py
    # 新的可视化风格
    class NewVisualizer(Visualizer):
        def visualize(self, node, level=0):
            result = "This is new style!"
            indent = " " * level * 2  # 更紧凑的缩进
            if node.is_leaf():
                result += f"{indent}{self.icons['leaf']}{node.name}: {node.value}\n"
            else:
                result += f"{indent}{self.icons['composite']}{node.name}\n"
                for child in node.children:
                    result += self.visualize(child, level + 1)
            return result

    # factory.py
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
    ```

    ​![image](https://cdn.jsdelivr.net/gh/cxw745/ImgBed/20240612110822.png)​
2. 通过配置文件，可添加新的图标族。

    在`icons.json`​中添加新的图标，在执行脚本时，参数`-i`​后跟新添加的图标组名称即可使用新的图标。

    示例如下，添加了math图标组并使用。

    ```json
    {
      "poker": {
        "composite": "♢",
        "leaf": "♤"
      },
      "star": {
        "composite": "✪",
        "leaf": "★"
      },
      "math": {
        "composite": "@",
        "leaf": "#"
      }
    }
    ```

    ​![image](https://cdn.jsdelivr.net/gh/cxw745/ImgBed/20240612110937.png)​

## 运行截图

* Tree

  * poker

    ​![image](https://cdn.jsdelivr.net/gh/cxw745/ImgBed/20240612112603.png)​
  * star

    ​![image](https://cdn.jsdelivr.net/gh/cxw745/ImgBed/image-20240612103138-crp5wcq.png)​
* Rectangle

  * poker

    ​![image](https://cdn.jsdelivr.net/gh/cxw745/ImgBed/image-20240612103148-fredwyf.png)​
  * star

    ​![image](https://cdn.jsdelivr.net/gh/cxw745/ImgBed/image-20240612103153-57yh77x.png)​

‍
