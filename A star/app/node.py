import json

from app.block import Block
from app.move import Move


class Node:
    """
    A* Node object, lưu thông tin Block object và giá trị các hàm cost f(n), g(n), h(n) tại node đó.
    Đồng thời giữ reference tới parent node
    """
    def __init__(self, block: Block, move: Move, parent, f=0, g=0, h=0, ):
        self.f = f
        self.g = g
        self.h = h
        self.block = block
        self.move = move
        self.parent = parent

    def __str__(self):
        json.dumps([str(self.block), str(self.move), str(self.parent), str(self.f), str(self.g), str(self.h)])
