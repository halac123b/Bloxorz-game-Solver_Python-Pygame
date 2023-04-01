from math import sqrt

from app.block import Block
from app.node import Node
from app.terrain import Terrain


class A_Star_Solver:
    """
    A* alogorithm implementation
    Sử dụng Chebyshev distance là giá trị mặc định trong hàm Heuristic
    """
    # Heuristic Function có thể dùng cả 'Eucledian' hoặc 'Chebyshev' distance.
    heuristic_functions = ["Eucledian", "Chebyshev"]

    def __init__(self, h_func="Chebyshev"):
        """
        Constructor dùng Chebyshev distance mặc định cho Heuristic function
        :param h_func: The Heuristic function được dùng
        """
        self.h_func = h_func
        assert self.h_func in self.heuristic_functions, "Heuristic Function can be either 'Eucledian' or 'Chebyshev' "

    def solve(self, terrain: Terrain) -> list:
        """
        Implementation
        :param terrain: mapdata
        :return: list of moves
        """
        open_list = []  # Initialize open list
        closed_list = []  # Initialize closed list

        start_pos = terrain.start
        start_block = Block(start_pos, start_pos)
        start_node = Node(start_block, move=None, parent=None, f=0, g=0, h=0) #Initialize a start Node object

        goal_pos = terrain.goal
        goal_block = Block(goal_pos, goal_pos)

        open_list.append(start_node)  #add start Node to the open list

        while len(open_list) > 0:
            print(len(open_list))
            # Get the current node
            # for index in range(len(open_list)):
            #     print("Node index:", index)
            #     print(f"f: {open_list[index].f} | g: {open_list[index].g} | h: {open_list[index].h}")
            #     print(f"Coordinate of bricks: [{open_list[index].block.p1.x}, {open_list[index].block.p1.y}], [{open_list[index].block.p2.x}, {open_list[index].block.p2.y}]")
            # print("---------------------------------------------------------------------------")
            current_node = open_list[0]
            current_index = 0

            for index, item in enumerate(open_list):
                # Check xem node đó có priority f(n) tốt hơn không, nếu có thì đổi node
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Lấy node tốt nhất ra khỏi open_list và thêm vào closed_list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # print("Selected node:")
            # print(f"f: {current_node.f} | g: {current_node.g} | h: {current_node.h}")
            # print(f"Coordinate of bricks: [{current_node.block.p1.x}, {current_node.block.p1.y}], [{current_node.block.p2.x}, {current_node.block.p2.y}]")
            # print("---------------------------------------------------------------------------")

            # Check xem win chưa
            if terrain.done(current_node.block):
                path = []
                current = current_node
                # BackTrack Moves
                while current is not None:
                    path.append(current.move)
                    current = current.parent
                return path[::-1]  # Return string các bước di chuyển

            # Nếu chưa win tiếp tục tìm các node con của node đó
            children = self.get_children(current_node, terrain)

            for child in children:
                # Nếu child đã từng đi qua rồi thì bỏ qua (tránh đi lùi)
                if child in closed_list:
                    continue

                # Tìm các giá trị hàm f(n), g(n), h(n)

                # g(n): path cost từ vị trí ban đầu đến được node đó
                child.g = current_node.g + 1

                # Tìm h(n) bằng heuristic function
                # Dùng Eucledian distance cho heuristic function
                if self.h_func == "Eucledian":
                    child.h = sqrt(((child.block.p2.x - goal_block.p2.x) ** 2) + ((child.block.p2.y - goal_block.p2.y) ** 2))

                # Dùng Chebyshev distance cho heuristic function
                if self.h_func == "Chebyshev":
                    hn1 = max(abs(child.block.p1.x - goal_block.p1.x), abs(child.block.p1.y - goal_block.p1.y))
                    hn2 = max(abs(child.block.p2.x - goal_block.p2.x), abs(child.block.p2.y - goal_block.p2.y))
                    child.h = max(hn1, hn2)

                child.f = child.g + child.h

                # Child có sẵn trong open_List và có độ ưu tiên thấp hơn thì bỏ qua
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

    def get_children(self, current_node: Node, terrain: Terrain):
        """
        Gets Children của currentNode bằng cách query các legal neighbour của node đó.
        """
        legal_neighbours = terrain.legal_neighbors(current_node.block)
        children = []
        for (legal_neighbour, legal_move) in legal_neighbours:
            child = Node(block=legal_neighbour, move=legal_move, parent=current_node)
            children.append(child)
        return children
