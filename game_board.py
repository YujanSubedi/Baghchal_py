class move_class:
    def __init__(self, fp=None, ip=None, cp=None) -> None:
        self.final_pos= fp
        self.initial_pos= ip
        self.capture_pos= cp

class board_class:
    def __init__(self) -> None:
        self.turn= -1 # -1 for Goat and 1 for Tiger
        self.goat_remaining = 20
        self.goat_killed = 0
        self.board_details= [[1,0,0,0,1],
                             [0,0,0,0,0],
                             [0,0,0,0,0],
                             [0,0,0,0,0],
                             [1,0,0,0,1]]  
        self.move_list = []

    def update_board(self, move:move_class) -> None:
        self.move_list.append(move)
        if move.initial_pos : self.board_details[move.initial_pos[0]][move.initial_pos[1]] = 0 
        else: self.goat_remaining -=1
        if move.capture_pos : 
            self.board_details[move.capture_pos[0]][move.capture_pos[1]] = 0 
            self.goat_killed +=1
        self.board_details[move.final_pos[0]][move.final_pos[1]]  = self.turn
        self.turn *= -1 # change turn

    def undo_last_move(self) -> None:
        if not self.move_list : return
        move:move_class = self.move_list[-1]
        if move.initial_pos : self.board_details[move.initial_pos[0]][move.initial_pos[1]] = -self.turn
        else: self.goat_remaining +=1
        if move.capture_pos : 
            self.board_details[move.capture_pos[0]][move.capture_pos[1]] = -1 
            self.goat_killed -=1
        self.board_details[move.final_pos[0]][move.final_pos[1]]  = 0
        self.turn *= -1 # change turn
        self.move_list.pop()

    def get_possible_moves(self) -> dict:
        possible_moves={'P':[] , 'M' : [], 'C' : []} # 'P' = placement , 'M' = movement , 'C' = capture
        if self.turn==-1 and self.goat_remaining :
            for i in range(5) :
                for j in range(5) :
                    if not self.board_details[i][j] : possible_moves['P'].append(move_class((i,j)))
            return possible_moves
        for i in range(5) :
            for j in range(5) :
                if self.turn == self.board_details[i][j] :
                    temp_list = [(i, j+1),(i, j-1),(i+1, j),(i-1, j)]
                    if i%2==j%2: temp_list += [(i+1, j+1),(i-1, j-1)]
                    if not (i+j)%2 : temp_list  += [(i-1,j+1),(i+1,j-1)]
                    possible_moves['M'] += [move_class(mv, (i,j)) for mv in temp_list  if ((mv[0]>=0 and mv[0]<=4) and (mv[1]>=0 and mv[1]<=4) and self.board_details[mv[0]][mv[-1]]==0)]
                    if self.turn==1:
                        temp_list  = [(i,j+2),(i,j-2),(i+2,j),(i-2,j)]
                        if i%2==j%2: temp_list += [(i+2,j+2),(i-2,j-2)]
                        if not (i+j)%2 : temp_list += [(i-2,j+2),(i+2,j-2)]
                        possible_moves['C'] += [move_class(mv, (i,j), (int((mv[0]+i)/2),int((mv[-1]+j)/2))) for mv in temp_list if (mv[0]>=0 and mv[0]<=4) and (mv[1]>=0 and mv[1]<=4) 
                            and self.board_details[mv[0]][mv[-1]]==0 and self.board_details[int((mv[0]+i)/2)][int((mv[-1]+j)/2)] == -1 ]
        return possible_moves

    def check_winner(self) -> str:
        if self.goat_killed>4 : return 'T'
        if self.turn==-1 : return None
        available_moves = self.get_possible_moves()
        if available_moves['M'] or available_moves['C'] : return None
        return 'G'
