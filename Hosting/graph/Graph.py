from utils.Callback import Callback
from graph.Node import Node


# def is_cond(conditions: dict, callback) -> bool:
#     for stage, option in conditions.items():
#         if callback[get_number(stage)] != option:
#             return False
#     return True


# def create_condition(conditions, nodes):
#     func = None
#     to = conditions['to']
#     if "if" not in conditions:
#         return lambda c : nodes[to]
#     condition = conditions['if']["cond"][0]
#     ifto = conditions['if']["to"]
#     func = lambda c : c.is_true(condition["stage"], condition["equals"])
#     for i in range(1, len(conditions["if"]["cond"]) // 2 - 1):
#         op = conditions["if"]["cond"][i]
#         condition = conditions["if"]["cond"][i + 1]
#         if op == "and":
#             func = lambda c : func(c) and c.is_true(condition["stage"], condition["equals"])
#         elif op == "or":
#             func = lambda c : func(c) or c.is_true(condition["stage"], condition["equals"])
#     return lambda c : nodes[ifto] if func(c) else nodes[to]




def create_condition(condition, nodes):
    to = condition['to']
    if "if" not in condition:
        return lambda c : nodes[to]
    else:

        ifto = condition['if']["to"]
        # print(to, ifto)
        # return lambda c : nodes[ifto]
        stage = condition['if']["stage"]
        equals = condition['if']["equals"]
        # print(condition)
        # func = lambda c : c.is_true(condition['if']["stage"], condition['if']["equals"])
        return lambda c : nodes[ifto] if c.is_true(stage, equals) else nodes[to]

class Graph:
    def __init__(self, data: dict):
        self.data = data
        self.all_nodes = dict()
        self.start: Node = Node("0", self.get_cond(data["0"]), self.data["0"])

        # print("ALL NODES", [str(i) for i in self.all_nodes.values()])


    def get_cond(self, options) -> dict:
        cond_old = {}
        for option, to in options["keyboard"]["buttons"].items():
            stage = to["to"]
            if stage not in self.all_nodes:
                node = Node(stage, self.get_cond(self.data[stage]), self.data[stage])
                self.all_nodes[stage] = node
                # print(stage, node)

            if "if" in to:
                if to["if"]["to"] not in self.all_nodes:
                    node = Node(to["if"]["to"], self.get_cond(self.data[to["if"]["to"]]), self.data[to["if"]["to"]])
                    self.all_nodes[to["if"]["to"]] = node
            cond_old[option] = create_condition(to, self.all_nodes)
        return cond_old

    def get_stage(self, callback:Callback) -> Node:
        node = self.start
        current_stage = callback.current_stage
        while current_stage != node.stage:
            next_node = node.get_next_node(callback)
            if callback.is_back(next_node.stage):
                callback.set_to_zero(next_node.stage)
                return node
            node = next_node
        n = node.get_next_node(callback)
        # print("STAGER", n.stager.text)
        return n

