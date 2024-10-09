import random
from game_board import board_class, move_class

no_of_itteration:int

def evaluate(board:board_class ) -> int:
    tiger_moves= board.get_possible_moves() 
    no_of_tiger_move= len(tiger_moves['M'])
    no_of_hanging_piece= len(tiger_moves['C'])
    return no_of_tiger_move + 7*(no_of_hanging_piece + board.goat_killed)


def min_max_eval(board:board_class, move:move_class, depth=1, alpha=0, beta=200) -> int :
    global no_of_itteration
    no_of_itteration+=1
    board.update_board(move)
    winner= board.check_winner()
    if winner :
        board.undo_last_move()
        return 0 if winner=='G' else 200
    if depth>2 and board.turn==-1:
        board.undo_last_move()
        return evaluate(board)
    available_moves = board.get_possible_moves()

    if available_moves['C'] :
        for mov in available_moves['C'] :
            eval= min_max_eval(board, mov ,depth+1, alpha, beta)
            if (eval>alpha) : alpha=eval
            if(alpha>=beta) : break
    elif available_moves['P']:
        for mov in available_moves['P'] :
            eval= min_max_eval(board, mov ,depth+1, alpha, beta)
            if (eval<beta) : beta= eval
            if(alpha>=beta) : break
    else :
        for mov in available_moves['M'] :
            eval= min_max_eval(board, mov ,depth+1, alpha, beta)
            if (eval>alpha and board.turn==-1) : alpha=eval
            elif (eval<beta and board.turn==1) : beta= eval
            if(alpha>=beta) : break

    board.undo_last_move()
    return alpha if board.turn==-1 else beta

def get_move_by_bot(board:board_class) -> move_class : 
    global no_of_itteration
    no_of_itteration= 0
    best_eval=0 if board.turn==1 else 100
    available_moves = board.get_possible_moves()
    if (len(available_moves['C']) + len(available_moves['M']))==1 : return available_moves['C'][0] if available_moves['C']  else available_moves['M'][0]
    if available_moves['C'] : 
        best_move= available_moves['C'][0]
        for mov in available_moves['C'] :
            eval= min_max_eval(board, mov) 
            if (eval>best_eval and board.turn==1) or (eval<best_eval and board.turn==-1) :
                best_eval= eval
                best_move= mov
    elif available_moves['P']:
        if board.goat_remaining==20 : return move_class(random.choice([(0,2),(2,0),(4,2),(2,4)]))
        best_move= available_moves['P'][0]
        for mov in available_moves['P'] :
            eval= min_max_eval(board, mov) 
            if (eval>best_eval and board.turn==1) or (eval<best_eval and board.turn==-1) :
                best_eval= eval
                best_move= mov
    else : 
        best_move= available_moves['M'][0]
        for mov in available_moves['M'] :
            eval= min_max_eval(board, mov) 
            if (eval>best_eval and board.turn==1) or (eval<best_eval and board.turn==-1) :
                best_eval= eval
                best_move= mov
    print("no of itteration=",no_of_itteration,"  Best evaluation=",best_eval)
    return best_move
