from typing import List, Tuple
# from local_driver import Alg3D, Board # ローカル検証用
from framework import Alg3D, Board # 本番用

class MyAI(Alg3D):
    def get_move(
        self,
        board: Board, # 盤面情報
        player: int, # 先手(黒):1 後手(白):2
        last_move: Tuple[int, int, int] # 直前に置かれた場所(x, y, z)
    ) -> Tuple[int, int]:
        # 基本的なAIアルゴリズムを実装
        return self.find_best_move(board, player)
    
    def find_best_move(self, board: Board, player: int) -> Tuple[int, int]:
        """最適な手を見つける"""
        # 1. 勝利できる手があるかチェック
        win_move = self.find_winning_move(board, player)
        if win_move:
            return win_move
        
        # 2. 相手の勝利を阻止する手があるかチェック
        opponent = 3 - player  # 相手のプレイヤー番号
        block_move = self.find_winning_move(board, opponent)
        if block_move:
            return block_move
        
        # 3. 中央付近に置く（基本的な戦略）
        center_move = self.find_center_move(board)
        if center_move:
            return center_move
        
        # 4. 空いている最初の位置に置く
        return self.find_first_available_move(board)
    
    def find_winning_move(self, board: Board, player: int) -> Tuple[int, int]:
        """勝利できる手を探す"""
        for x in range(4):
            for y in range(4):
                if self.can_place_stone(board, x, y):
                    # 仮想的に石を置いてみる
                    temp_board = [[[board[z][y][x] for x in range(4)] for y in range(4)] for z in range(4)]
                    z = self.get_height(board, x, y)
                    temp_board[z][y][x] = player
                    
                    if self.check_win(temp_board, x, y, z, player):
                        return (x, y)
        return None
    
    def find_center_move(self, board: Board) -> Tuple[int, int]:
        """中央付近の空いている位置を探す"""
        center_positions = [(1, 1), (1, 2), (2, 1), (2, 2), (0, 1), (1, 0), (2, 3), (3, 2)]
        
        for x, y in center_positions:
            if self.can_place_stone(board, x, y):
                return (x, y)
        return None
    
    def find_first_available_move(self, board: Board) -> Tuple[int, int]:
        """最初に見つかった空いている位置に置く"""
        for x in range(4):
            for y in range(4):
                if self.can_place_stone(board, x, y):
                    return (x, y)
        return (0, 0)  # フォールバック
    
    def can_place_stone(self, board: Board, x: int, y: int) -> bool:
        """指定位置に石を置けるかチェック"""
        return board[3][y][x] == 0  # 最上段が空いているか
    
    def get_height(self, board: Board, x: int, y: int) -> int:
        """指定位置の現在の高さを取得"""
        for z in range(4):
            if board[z][y][x] == 0:
                return z
        return 4  # 満杯
    
    def check_win(self, board: Board, x: int, y: int, z: int, player: int) -> bool:
        """指定位置で勝利条件を満たしているかチェック"""
        # 6方向の直線をチェック
        directions = [
            (1, 0, 0),   # x軸方向
            (0, 1, 0),   # y軸方向
            (0, 0, 1),   # z軸方向
            (1, 1, 0),   # xy対角線
            (1, 0, 1),   # xz対角線
            (0, 1, 1),   # yz対角線
            (1, 1, 1),   # xyz対角線
            (1, -1, 0),  # xy逆対角線
            (1, 0, -1),  # xz逆対角線
            (0, 1, -1),  # yz逆対角線
            (1, -1, -1), # xyz逆対角線
            (1, 1, -1),  # xy正、z負対角線
            (1, -1, 1),  # xy負、z正対角線
        ]
        
        for dx, dy, dz in directions:
            count = 1  # 現在の石を含む
            
            # 正方向にカウント
            nx, ny, nz = x + dx, y + dy, z + dz
            while 0 <= nx < 4 and 0 <= ny < 4 and 0 <= nz < 4 and board[nz][ny][nx] == player:
                count += 1
                nx, ny, nz = nx + dx, ny + dy, nz + dz
            
            # 負方向にカウント
            nx, ny, nz = x - dx, y - dy, z - dz
            while 0 <= nx < 4 and 0 <= ny < 4 and 0 <= nz < 4 and board[nz][ny][nx] == player:
                count += 1
                nx, ny, nz = nx - dx, ny - dy, nz - dz
            
            if count >= 4:
                return True
        
        return False