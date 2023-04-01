from app.position import Position
import json


class Block:
    """
    Block object biểu diễn Bloxorz block chứa 2 brick.
    Khi dựng đứng 2 brick cùng tọa độ
    Khi đặt nằm mỗi brick có tọa độ riêng
    """

    def __init__(self, p1: Position, p2: Position):
        # Assert đảm bảo tọa độ brick hợp lệ
        assert (p1.x <= p2.x and p1.y <= p2.y), "Position of blok is not valid: p1=" + p1 + ", p2=" + p2
        self.p1 = p1
        self.p2 = p2

    def is_standing(self) -> bool:
        """
        Check xem block có đang ở trạng thái đứng hay không
        """
        return self.p1.x == self.p2.x and self.p1.y == self.p2.y

    def left(self):
        """
        Block move left
        """
        if self.is_standing():
            return self.dy(-2, -1)
        elif self.p1.x == self.p2.x:
            return self.dy(-1, -2)
        else:
            return self.dy(-1, -1)

    def right(self):
        """
        Block move right
        """
        if self.is_standing():
            return self.dy(1, 2)
        elif self.p1.x == self.p2.x:
            return self.dy(2, 1)
        else:
            return self.dy(1, 1)

    def up(self):
        """
        Block move up
        """
        if self.is_standing():
            return self.dx(-2, -1)
        elif self.p1.x == self.p2.x:
            return self.dx(-1, -1)
        else:
            return self.dx(-1, -2)

    def down(self):
        """
        Block move down
        """
        if self.is_standing():
            return self.dx(1, 2)
        elif self.p1.x == self.p2.x:
            return self.dx(1, 1)
        else:
            return self.dx(2, 1)

    # Return block với tọa độ x mới được update
    def dx(self, d1, d2):
        return Block(self.p1.dx(d1), self.p2.dx(d2))

    # Return block với tọa độ y mới được update
    def dy(self, d1, d2):
        return Block(self.p1.dy(d1), self.p2.dy(d2))

    def __str__(self):
        return json.dumps([str(self.p1), str(self.p2)])
