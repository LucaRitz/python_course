from typing import Dict, List, Tuple, Union, Set

from scipy.io import arff
import threading
import math


class Attribute:

    def __init__(self, attribute: str, values: Set[str]) -> None:
        self.attribute = attribute
        self.values = values


class DataSet:

    class Row:

        def __init__(self, attribute_values, attribute_names):
            self.values: List[Tuple[str, str]] = DataSet.Row.__parse(attribute_values, attribute_names)
            self.expected: str = DataSet.Row.__expected(attribute_values)

        @staticmethod
        def __parse(attribute_values, attribute_names) -> List[Tuple[str, str]]:
            results: List[Tuple[str, str]] = []
            for value, name in zip(attribute_values[:-1], attribute_names[:-1]):
                results.append(tuple((name, DataSet.Row.__clean(value))))
            return results

        @staticmethod
        def __expected(attribute_values: List[str]) -> str:
            return DataSet.Row.__clean(attribute_values[-1])

        @staticmethod
        def __clean(value: str) -> str:
            return value.replace("b'", '').replace("'", '')

    def __init__(self, data: Tuple = None, rows: List[Row] = None, classes: Set[str] = None):
        if rows is not None:
            self.__rows = rows
            self.__classes = classes
        else:
            self.__rows: List[DataSet.Row] = self.__parse(data)
            self.__classes: Set[str] = self.__class_values()

    def reduce(self, attribute: str, value: str):
        rows: List[DataSet.Row] = list(filter(lambda row: (attribute, value) in row.values, self.__rows))
        return DataSet(rows=rows, classes=self.__classes)

    def count_results(self, attribute: str, value: str) -> Dict[str, int]:
        result: Dict[str, int] = {i: 0 for i in self.__classes}
        for row in filter(lambda row: (attribute, value) in row.values, self.__rows):
            result[row.expected] += 1
        return result

    def attributes(self) -> List[Attribute]:
        result: List[Attribute] = []

        for row in self.__rows:
            for attribute, value in row.values:
                found: bool = False
                for attr in result:
                    if attr.attribute == attribute:
                        attr.values.add(value)
                        found = True
                if not found:
                    result.append(Attribute(attribute, {value}))

        return result

    def __class_values(self) -> Set[str]:
        values: Set[str] = set()
        for row in self.__rows:
            values.add(row.expected)

        return values

    def __parse(self, data: Tuple) -> List[Row]:
        rows: List[DataSet.Row] = []
        for row in data[0]:
            row = list(map(lambda ro: ro.decode('utf-8'), row))
            rows.append(self.Row(row, data[1].names()))

        return rows


class RootNode:

    def __init__(self, data_set: DataSet):
        self.reduced_data_set = data_set
        self.non_performed_attributes = data_set.attributes()
        self.top_level_info = 0.940
        self.children: List[DecisionNode] = []


def build_decision_tree(arff_file: str) -> RootNode:
    data, meta = arff.loadarff(arff_file)
    data_set = DataSet(tuple((data, meta)))
    root_node = RootNode(data_set)
    __build(root_node).join()

    return root_node


def print_node(node: RootNode):
    print('- Root')
    for child in node.children:
        __print_rec(child, 1)


class DecisionNode:

    def __init__(self, parent_node, attribute: Attribute, value: str):
        self.__parent_node = parent_node
        self.attribute = attribute
        self.value = value

        self.non_performed_attributes = DecisionNode.__reduce_attr(parent_node.non_performed_attributes, attribute)
        self.reduced_data_set: DataSet = parent_node.reduced_data_set.reduce(attribute.attribute, value)

        self.top_level_info = parent_node.top_level_info
        self.children: List[DecisionNode] = []

    def result(self) -> str:
        if not self.non_performed_attributes:
            results: Dict[str, int] = self.reduced_data_set.count_results(self.attribute.attribute, self.value)
            for name, count in results.items():
                if count > 0:
                    return name
        return ''

    def activate(self):
        self.__parent_node.children.append(self)

    @staticmethod
    def __reduce_attr(non_performed_attributes: List[Attribute], attribute: Attribute) -> List[Attribute]:
        reduced: List[Attribute] = non_performed_attributes.copy()
        reduced.remove(attribute)
        return reduced

    def information(self) -> [int, float]:
        results: Dict[str, int] = self.reduced_data_set.count_results(self.attribute.attribute, self.value)
        summed, normalized = DecisionNode.__normalize(tuple(results.values()))

        result: float = 0.0
        for normed in normalized:
            result += -normed * math.log2(normed) if normed > 0 else 0

        return summed, result

    @staticmethod
    def __normalize(values: Tuple[int]) -> [int, Tuple[float]]:
        summed = sum(values)
        return summed, tuple(map(lambda val: float(val) / summed if summed > 0 else 0, values))


def __build(parent_node: Union[RootNode, DecisionNode]) -> threading.Thread:
    thread: threading.Thread = threading.Thread(target=__build_impl, args=[parent_node])
    thread.start()
    return thread


def __build_impl(parent_node: Union[RootNode, DecisionNode]):
    if parent_node.non_performed_attributes:
        attribute_values: List[AttributeValue] = []
        for non_performed_attr in parent_node.non_performed_attributes:
            attribute_values.append(AttributeValue(non_performed_attr, parent_node))

        gaines: Dict[AttributeValue, float] = {i: i.gain() for i in attribute_values}

        max_value = max(gaines.values())  # maximum value
        max_key = [k for k, v in gaines.items() if v == max_value][0]

        threads: List[threading.Thread] = []
        for node in max_key.nodes:
            node.activate()
            threads.append(__build(node))

        for thread in threads:
            thread.join()


def __print_rec(node: DecisionNode, level: int) -> None:
    indent: str = '  ' * level
    print(indent + '- ' + node.attribute.attribute + '.' + node.value + '.' + node.result())
    level += 1
    for child in node.children:
        __print_rec(child, level)


class AttributeValue:

    def __init__(self, attribute: Attribute, parent_node: Union[DecisionNode, RootNode]) -> None:
        self.__parent_node = parent_node
        self.attribute = attribute
        self.nodes = AttributeValue.__build_nodes(attribute, parent_node)

    def gain(self) -> float:
        infos: List[Tuple[int, float]] = []
        all_sum: int = 0
        for node in self.nodes:
            sum_val, info_val = node.information()
            all_sum += sum_val
            infos.append(tuple((sum_val, info_val)))

        info: float = 0.0
        for inf in infos:
            info += (inf[0]/all_sum) * inf[1] if all_sum > 0 else 0

        return self.__parent_node.top_level_info - info

    @staticmethod
    def __build_nodes(attribute: Attribute, parent_node: Union[DecisionNode, RootNode]) -> List[DecisionNode]:
        return list(map(lambda attr_val: DecisionNode(parent_node, attribute, attr_val), attribute.values))
