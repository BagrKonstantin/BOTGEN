from Callback import Callback
from graph.Node import Node
from graph.encrypter import get_number


def is_cond(conditions: dict, callback) -> bool:
    for stage, option in conditions.items():
        if callback[get_number(stage)] != option:
            return False
    return True


def create_condition(conditions, nodes):
    func = None
    to = conditions['to']
    if "if" not in conditions:
        return lambda c : nodes[to]
    condition = conditions['if']["cond"][0]
    ifto = conditions['if']["to"]
    func = lambda c : c.is_true(condition["stage"], condition["equals"])
    for i in range(1, len(conditions["if"]["cond"]) // 2 - 1):
        op = conditions["if"]["cond"][i]
        condition = conditions["if"]["cond"][i + 1]
        if op == "and":
            func = lambda c : func(c) and c.is_true(condition["stage"], condition["equals"])
        elif op == "or":
            func = lambda c : func(c) or c.is_true(condition["stage"], condition["equals"])
    return lambda c : nodes[ifto] if func(c) else nodes[to]



class Graph:
    def __init__(self, data: dict):
        self.data = data
        self.all_nodes = dict()
        self.start: Node = Node("0", self.get_cond(data["0"]), self.data["0"])

    def get_cond(self, options) -> dict:
        cond_old = {}
        for option, to in options["keyboard"]["buttons"].items():
            stage = to["to"]
            if stage not in self.all_nodes:
                node = Node(stage, self.get_cond(self.data[stage]), self.data[stage])
                self.all_nodes[stage] = node

            if "if" in to:
                if to["if"]["to"] not in self.all_nodes:
                    node = Node(to["if"]["to"], self.get_cond(self.data[stage]), self.data[stage])
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
        return node.get_next_node(callback)


# if __name__ == '__main__':
#     import json
#     with open("condition.json", "r", encoding="utf-8") as file:
#         data_raw = json.load(file)
#
#         f = create_condition(data_raw["first"])
#         callback = Callback(1, 1, "1ad")
#         ans = f(callback)
#         print(ans)
#
#         f = create_condition(data_raw["second"])
#         callback = Callback(1, 1, "0b")
#         ans = f(callback)
#         print(ans)
#
#         f = create_condition(data_raw["third"])
#         callback = Callback(1, 1, "0b")
#         ans = f(callback)
#         print(ans)
#
#     with open("nodetest.json", "r", encoding="utf-8") as file:
#         data_raw = json.load(file)
#         print(data_raw)
#
#     graph = Graph(data_raw["stages"])
#     print("before")
#     print(graph.all_nodes)
#     print(graph.get_stage(2, "dcda").stage)