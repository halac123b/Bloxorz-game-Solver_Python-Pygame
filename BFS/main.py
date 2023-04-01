import numpy as np
import copy

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Block():
    def __init__(self, p1: Point, p2: Point):
        self.path = "";
        self.head = p1;
        self.tail = p2;
    def is_standing(self) -> bool:
        return self.head.x == self.tail.x and self.head.y == self.tail.y

    def MoveLeft(self):
        if self.is_standing(): #tru nam dung
            self.head.y -= 2
            self.tail.y -= 1
        elif self.head.y == self.tail.y: #tru nam ngang tru Ox (nam doc)
            self.head.y -= 1
            self.tail.y -= 1
        #tru nam ngang tru Oy (nam ngang)
        elif self.head.y > self.tail.y:
            self.head.y -= 2
            self.tail.y -= 1
        elif self.head.y < self.tail.y:
            self.head.y -= 1
            self.tail.y -= 2            
            
    def MoveRight(self):
        if self.is_standing(): #tru nam dung
            self.head.y += 2
            self.tail.y += 1
        elif self.head.y == self.tail.y: #tru nam ngang tru Ox (nam doc)
            self.head.y += 1
            self.tail.y += 1
        #tru nam ngang tru Oy (nam ngang)
        elif self.head.y < self.tail.y:
            self.head.y += 2
            self.tail.y += 1
        elif self.head.y > self.tail.y:
            self.head.y += 1
            self.tail.y += 2
    
    def MoveUp(self):
        if self.is_standing(): #tru nam dung
            self.head.x -= 2
            self.tail.x -= 1
        elif self.head.x == self.tail.x: #tru nam ngang tru Oy (nam ngang)
            self.head.x -= 1
            self.tail.x -= 1
        #tru nam ngang tru Ox (nam doc)
        elif self.head.x < self.tail.x:
            self.head.x -= 1
            self.tail.x -= 2
        elif self.head.x > self.tail.x:
            self.head.x -= 2
            self.tail.x -= 1        
        
    def MoveDown(self):
        if self.is_standing(): #tru nam dung
            self.head.x += 2
            self.tail.x += 1
        elif self.head.x == self.tail.x: #tru nam ngang tru Oy (nam ngang)
            self.head.x += 1
            self.tail.x += 1
        #tru nam ngang tru Ox (nam doc)
        elif self.head.x < self.tail.x:
            self.head.x += 2
            self.tail.x += 1
        elif self.head.x > self.tail.x:
            self.head.x += 1
            self.tail.x += 2    


def play_block(a, head_x, head_y, tail_x, tail_y):
    a[head_x][head_y] = 1
    a[tail_x][tail_y] = 1
    return a

def play_goal(a, goal_x, goal_y):
    a[goal_x][goal_y] = 3
    return a

def print_map(map_game):
    for line in map_game:
        print ('  '.join(map(str, line)))
        
class Breath_Frist_Search():
    def __init__(self, map, block: Block):
        self.map = map
        self.block = block
        self.MoveSequence = ""
        self.queue = []
        self.visited = []
    
    def check_legit(self, map, block: Block) -> bool:
        if (block.head.x < 0 or block.head.y < 0 or block.tail.x < 0 or block.tail.y  < 0): 
            return False
        try:
            map[block.head.x][block.head.y]
        except IndexError:
            return False
        try:
            map[block.tail.x][block.tail.y]
        except IndexError:            
            return False  
          
        if map[block.head.x][block.head.y] == 0 or map[block.tail.x][block.tail.y] == 0:
            return False        
        return True
    
    def not_in_visit_list(self, block: Block, visit) -> bool:
        if visit == []: return True
        for element in visit:
            if block.head.x == element.head.x and block.head.y == element.head.y and block.tail.x == element.tail.x and block.tail.y == element.tail.y:
                return False
        return True
            
    
    def run(self):
        #print(self.block.head.x, self.block.head.y)
        self.queue.append(self.block)
        self.visited.append(self.block)
        while self.queue != []:
            considered_node = self.queue[0]
            #print(considered_node.head.x, considered_node.head.y)
            #print(considered_node.tail.x, considered_node.tail.y)
            self.queue.pop(0)
            if self.map[considered_node.head.x][considered_node.head.y] == 4 and self.map[considered_node.tail.x][considered_node.tail.y] == 4:
                return considered_node.path
            
            block_move_L = copy.deepcopy(considered_node)
            block_move_L.MoveLeft()
            block_move_R = copy.deepcopy(considered_node)
            block_move_R.MoveRight()
            block_move_U = copy.deepcopy(considered_node)
            block_move_U.MoveUp()
            block_move_D = copy.deepcopy(considered_node)
            block_move_D.MoveDown()

            if self.check_legit(self.map, block_move_U) and self.not_in_visit_list(block_move_U, self.visited):
                block_move_U.path = considered_node.path + " U"
                self.MoveSequence = block_move_U.path
                self.queue.append(block_move_U)

            if self.check_legit(self.map, block_move_D) and self.not_in_visit_list(block_move_D, self.visited):
                block_move_D.path = considered_node.path + " D"
                self.MoveSequence = block_move_D.path
                self.queue.append(block_move_D)

            if self.check_legit(self.map, block_move_L) and self.not_in_visit_list(block_move_L, self.visited):
                block_move_L.path = considered_node.path + " L"
                self.MoveSequence = block_move_L.path
                self.queue.append(block_move_L)

            if self.check_legit(self.map, block_move_R) and self.not_in_visit_list(block_move_R, self.visited):
                block_move_R.path = considered_node.path + " R"
                self.MoveSequence = block_move_R.path
                self.queue.append(block_move_R)
            
            self.visited.append(considered_node)
                
        return [] 

def main():
    LEVEL1_ARRAY = [
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 1, 4, 1, 1],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 0]
    ]
    
    block_1 = Block(Point(1,1),Point(1,1))
    result = Breath_Frist_Search(LEVEL1_ARRAY, block_1).run()

    print("Possible move to sovle this puzzle:")
    for x in range(len(result)):
        print(result[x], end = " ")
    print("\n")
    
    LEVEL2_ARRAY = [
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 4, 1],
    [1, 1, -2, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    ]
    
    block_2 = Block(Point(3,1),Point(3,1))
    result = Breath_Frist_Search(LEVEL2_ARRAY, block_2).run()
    
    print("Possible move to sovle this puzzle:")
    for x in range(len(result)):
        print(result[x], end = " ")
    print("\n")   
    
    # map_game = np.array([
    #     [0,0,0,2,2,2,2,2,2,2],
    #     [0,0,0,0,0,0,2,2,2,2],
    #     [0,0,0,0,0,0,0,0,0,0],
    #     [2,0,0,0,0,0,0,0,0,0],
    #     [2,2,2,2,2,0,0,0,0,0],
    #     [2,2,2,2,2,2,0,0,0,2],
    #     ])
    
    # map_game_3 = np.array([
    #     [2,2,2,2,2,2,0,0,0,0,0,0,0,2,2],
    #     [0,0,0,0,2,2,0,0,0,2,2,0,0,2,2],
    #     [0,0,0,0,0,0,0,0,0,2,2,0,0,0,0],
    #     [0,0,0,0,2,2,2,2,2,2,2,0,0,0,0],
    #     [0,0,0,0,2,2,2,2,2,2,2,0,0,0,0],
    #     [2,2,2,2,2,2,2,2,2,2,2,2,0,0,0],
    #     ])
    
    # map_game_6 = np.array([
    #     [2,2,2,2,2,0,0,0,0,0,0,2,2,2,2],
    #     [2,2,2,2,2,0,2,2,0,0,0,2,2,2,2],
    #     [2,2,2,2,2,0,2,2,0,0,0,0,0,2,2],
    #     [0,0,0,0,0,0,2,2,2,2,2,0,0,0,0],
    #     [2,2,2,2,0,0,0,2,2,2,2,0,0,0,0],
    #     [2,2,2,2,0,0,0,2,2,2,2,2,0,0,0],
    #     [2,2,2,2,2,2,0,2,2,0,0,2,2,2,2],
    #     [2,2,2,2,2,2,0,0,0,0,0,2,2,2,2],
    #     [2,2,2,2,2,2,0,0,0,0,0,2,2,2,2],
    #     [2,2,2,2,2,2,2,0,0,0,2,2,2,2,2],
    #     ])
    
    
    # block_6 = Block(Point(3,0),Point(3,0))
    # goal_6 = Point(4,13)
    # result = Breath_Frist_Search(map_game_6, block_6, goal_6).run()
    # head = Point(3,1)
    # tail = Point(3,1)
    # block_o = Block(head, tail)
    # goal = Point(3,13)
    # result = Breath_Frist_Search(map_game_3, block_o, goal).run()

if __name__ == "__main__":
    main()