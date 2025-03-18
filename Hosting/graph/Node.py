from graph.Stages import AbstractStage
from graph.encrypter import get_number



class Node:
    def __init__(self, stage: str, cond: dict, data):
        self.stage: int = get_number(stage)
        self.cond_next: dict = cond
        self.stager = AbstractStage.get_stage(self.stage, data)


    def get_next_node(self, callback):
        return self.cond_next[callback.get_option(self.stage)](callback)
