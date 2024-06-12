import argparse
import json
from builder import CompositeNodeBuilder, TreeDirector
from factory import ConcreteVisualizerFactory


class FjeExplorer:
    # JSON 文件加载
    @staticmethod
    def load_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # 加载图标集
    @staticmethod
    def load_icons(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # 命令行参数解析
    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Funny JSON Explorer (FJE)")
        parser.add_argument("-f", "--file", required=True, help="Path to the JSON file")
        parser.add_argument("-s", "--style", required=True, help="Visualization style")
        parser.add_argument("-i", "--icons", required=True, help="Icon family")
        return parser.parse_args()


if __name__ == "__main__":
    args = FjeExplorer.parse_arguments()
    json_data = FjeExplorer.load_json(args.file)
    icons = FjeExplorer.load_icons("icons.json")[args.icons]

    builder = CompositeNodeBuilder()
    director = TreeDirector(builder)
    json_tree = director.build_tree(json_data)

    factory = ConcreteVisualizerFactory()
    visualizer = factory.get_visualizer(args.style, icons)  # 传递图标

    output = visualizer.visualize(json_tree)
    print(output)
