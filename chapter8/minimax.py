from __future__ import annotations

from board import Piece, Board, Move

def minimax(board: Board, maximizing: bool, 
            original_player: Piece, max_depth: int = 8) -> float:
    # 基线条件：最终位置或者是达到了最大深度
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)
    
    # 递归调用：把你的利益最大化，把对手的利益最小化
    if maximizing:
        best_eval: float = float('-inf')
        for move in board.legal_moves:
            # 这里下棋的是X
            result: float = minimax(board.move(move),False,original_player,max_depth-1)
            best_eval = max(result, best_eval)
        return best_eval
    else:
        worst_eval: float = float('inf')
        for move in board.legal_moves:
            # 这里下棋的是O
            result: float = minimax(board.move(move), True, original_player,max_depth-1)
            worst_eval = min(result, worst_eval)
        return worst_eval

def find_best_move(board: Board, max_depth: int = 8) -> Move:
    best_eval: float = float('-inf')
    best_move: Move = Move(-1)
    for move in board.legal_moves:
        # result: float = minimax(board.move(move),False,board.turn,max_depth)
        # 我把上面的minimax换成了它的升级版alphabeta，性能得到了优化
        result: float = alphabeta(board.move(move),False,board.turn,max_depth)
        if result>best_eval:
            best_eval = result
            best_move = move
    return best_move

# 优化版的minimax算法，剪枝
def alphabeta(board: Board, maximizing: bool, 
              original_player: Piece,
              max_depth: int = 8,
              alpha: float = float('-inf'),
              beta: float = float('inf')) -> float:
    # 基线条件
    if board.is_win or board.is_draw or max_depth == 0:
        return board.evaluate(original_player)
    
    # 递归
    if maximizing:
        for move in board.legal_moves:
            result: float = alphabeta(board.move(move), 
                                      False, 
                                      original_player, 
                                      max_depth-1, 
                                      alpha, 
                                      beta)
            alpha = max(result,alpha)
            if beta <= alpha:
                break
        return alpha
    else:
        for move in board.legal_moves:
            result: float = alphabeta(board.move(move),
                                      True,
                                      original_player,
                                      max_depth-1,
                                      alpha,
                                      beta)
            beta = min(result, beta)
            if beta<=alpha:
                break
        return beta
    


