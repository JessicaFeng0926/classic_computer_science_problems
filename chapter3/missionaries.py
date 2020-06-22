from generic_search import Node,bfs,node_to_path

MAX_NUM = 3

class MCState:
    def __init__(self,missionaries:int,cannibals:int,boat:bool):
        # 西岸的传教士和食人族的数量
        self.wm = missionaries
        self.wc = cannibals
        # 东岸的数量
        self.em = MAX_NUM - self.wm
        self.ec = MAX_NUM - self.wc
        # True表示船在西岸，否则在东岸
        self.boat = boat
    
    @property
    def is_legal(self):
        if self.wm < self.wc and self.wm > 0:
            return False
        if self.em < self.ec and self.em > 0:
            return False
        return True

        
    def goal_test(self):
        '''检查是否实现了目标'''
        return self.is_legal and self.em == MAX_NUM and self.ec == MAX_NUM
    
    def successors(self):
        sucs = []
        # 如果船在西岸
        if self.boat:
            if self.wm > 1:
                sucs.append(MCState(self.wm-2,self.wc,not self.boat))
            if self.wm > 0:
                sucs.append(MCState(self.wm-1,self.wc,not self.boat))
            if self.wc > 1:
                sucs.append(MCState(self.wm,self.wc-2,not self.boat))
            if self.wc > 0:
                sucs.append(MCState(self.wm,self.wc-1,not self.boat))
            if self.wm > 0 and self.wc > 0:
                sucs.append(MCState(self.wm-1,self.wc-1,not self.boat))
        # 如果船在东岸
        else:
            if self.em > 1:
                sucs.append(MCState(self.wm+2,self.wc,not self.boat))
            if self.em > 0:
                sucs.append(MCState(self.wm+1,self.wc,not self.boat))
            if self.ec > 1:
                sucs.append(MCState(self.wm,self.wc+2,not self.boat))
            if self.ec > 0:
                sucs.append(MCState(self.wm,self.wc+1,not self.boat))
            if self.em > 0 and self.ec > 0:
                sucs.append(MCState(self.wm+1,self.wc+1,not self.boat))
        return [x for x in sucs if x.is_legal]



    def __str__(self):
        return ("On the west bank there are {} missionaries and {} cannibals\n"
                "On the east bank there are {} missionaries and {} cannibals\n"
                "The The boat is on the {} bank.").format(self.wm,self.wc,
                self.em,self.ec,
                'west' if self.boat else 'east')


def display_solution(path):
    '''这是用于打印解决方案给人看的函数'''
    if len(path) == 0:
        return 
    old_state = path[0]
    print(old_state)
    for current_state in path[1:]:
        # 如果当前船在西岸，说明是从东岸过来的
        if current_state.boat:
            print("{} missionaries and {} cannibals moved from the east bank to the west bank.\n".format(old_state.em-current_state.em,
                old_state.ec-current_state.ec))
        else:
            print("{} missionaries and {} cannibals moved from the west bank to the east bank.\n".format(old_state.wm-current_state.wm,
                old_state.wc-current_state.wc))
        print(current_state)
        old_state = current_state

if __name__ == '__main__':
    start = MCState(MAX_NUM,MAX_NUM,True)
    solution = bfs(start,MCState.goal_test,MCState.successors)
    if solution is None:
        print('No solution')
    else:
        path = node_to_path(solution)
        display_solution(path)