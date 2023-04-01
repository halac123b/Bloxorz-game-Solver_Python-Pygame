import json


class Position:
    """
    Class lưu các tọa độ trên map
    """
    def __init__(self, x, y):
        """
        Initialize position based on column (x) row(y)
        """
        self.x = x
        self.y = y

    def dx(self, d):
        """
        Dịch chuyển tọa độ x 1 khoảng d
        """
        return Position(self.x + d, self.y)

    def dy(self, d):
        """
           Dịch chuyển tọa độ y 1 khoảng d
        """
        return Position(self.x, self.y + d)

    def __str__(self):
        return json.dumps([self.x, self.y])
