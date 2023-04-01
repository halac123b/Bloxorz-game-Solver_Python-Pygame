#  Copyright (c) 2020. Abhilshit Soni

from app.position import Position
from app.block import Block
from app.move import Move

class Terrain:
    """
    Class Terrain biểu diễn bản đồ của game. Bao gồm:
        1. map biểu diễn các ô có thể đến và không thể đến đc (các lỗ trống), bằng các giá trị True/False
        2. Vị trí bắt đầu của bloxorz block
        3. Đích đến cần đạt được để win game
        4. width, height: kích thước của map
    """
    map = None  # Map chứa thông tin các ô có thể và không thể di chuyển
    # Vị trí bắt đầu kết thúc
    start = None
    goal = None
    width = None  # Số cột của map
    height = None  # Số hàng của map

    def __init__(self, level_file="resources/level01.txt"):
        """
        Constructor nhận vào file chứa map data
        """
        self.parse_terrain(level_file)

    def can_hold(self, b: Block) -> bool:
        """
        Check xem block có đang ở vị trí hợp lệ bên trong map hay không
        """
        try:
            can_hold = self.map[b.p1.x][b.p1.y] and self.map[b.p2.x][b.p2.y]
        except IndexError:
            can_hold = False
            #print("Warning: "+ str(b.p1) + " or " + str(b.p2) + " is out of range !!")

        return can_hold

    def neighbours(self, b: Block) -> list:
        """
        Các node liền kề mà block có thể di chuyên đến, dựa theo các hướng đi được cho phép (up,down,left,right)
        :param b: Block object đang tìm các vị trí lân cận
        :return: list of (Block, Move) biểu diễn vị trí block có thể di chuyển đến và Move - bước đi cần thiết để đến vị trí đó
        """
        return [(b.up(), Move.Up), (b.down(), Move.Down), (b.left(), Move.Left), (b.right(), Move.Right)]

    def legal_neighbors(self, b: Block) -> list:
        """
        Từ các node neighbor tìm được ở trên, check xem chúng có nằm ở vị trí hợp lệ để di chuyển đến hay không
        :param b: Block object có các Neigbour đang được xét
        :return: list of (Block, Move) hợp lệ
        """
        return [(n, move) for (n, move) in self.neighbours(b) if self.can_hold(n)]

    def done(self, b: Block) -> bool:
        """
        Check xem vị trí block hiện tại đã đến đích hay chưa
        """
        return b.is_standing() and b.p1.x == self.goal.x and b.p1.y == self.goal.y

    def parse_terrain(self, level_file):
        """
        Đọc data map từ file
        """
        file = open(level_file, "r")
        self.map = []
        content = file.read().split()
        self.height = len(content)
        self.width = len(content[0])
        file.seek(0)
        for x, line in enumerate(file):
            row = []
            for y, char in enumerate(line):
                if char == 'S':
                    self.start = Position(x, y)
                    row.append(True)
                elif char == '4':
                    self.goal = Position(x, y)
                    row.append(True)
                elif char == '1':
                    row.append(True)
                elif char == '0':
                    row.append(False)
            self.map.append(row)
        file.close()
        print("Terrain map created")