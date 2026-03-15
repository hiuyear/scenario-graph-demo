"""
A minimal dependency graph engine.

Nodes hold a value and know how to recompute themselves
from their upstream dependencies. When an input changes,
only the affected downstream nodes are recomputed.

"""


class Node:
    def __init__(self, name, inputs=None, fn=None):
        self.name = name
        self.inputs = inputs or []
        self.fn = fn
        self.value = None

    def set(self, value):
        self.value = value

    def compute(self):
        if self.fn is not None:
            input_values = [node.value for node in self.inputs]
            self.value = self.fn(*input_values)


class DependencyGraph:
    def __init__(self):
        self.nodes = {}
        self.order = []

    def add(self, node):
        self.nodes[node.name] = node
        self.order.append(node)
        return node

    def compute_all(self):
        for node in self.order:
            node.compute()

    def update(self, node_name, value):
        self.nodes[node_name].set(value)
        self.compute_all()

    def fork(self):
        return {name: node.value for name, node in self.nodes.items()}

    def snapshot(self, title="Snapshot"):
        print(f"\n  {title}")
        for name, node in self.nodes.items():
            print(f"    {name}: {node.value}")