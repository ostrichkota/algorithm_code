from typing import List, Tuple
from local_driver import Alg3D, Board # ローカル検証用
# from framework import Alg3D, Board # 本番用

class MyAI(Alg3D):
    def get_move(
        self,
        board: Board, # 盤面情報
        player: int, # 先手(黒):1 後手(白):2
        last_move: Tuple[int, int, int] # 直前に置かれた場所(x, y, z)
    ) -> Tuple[int, int]:
        # 可視化: 現在の盤面と置けるマスを表示
        self.visualize_board(board)
        self.print_legal_moves(board)
        
        # 可視化: 各マスのアクセス可能ライン数を表示
        self.print_line_accessibility(board, player)
        
        # 基本的なAIアルゴリズムを実装
        move = self.find_best_move(board, player)
        
        # 可視化: AIの選択理由を表示
        self.print_move_reason(board, player, move)
        
        return move

    def get_legal_moves(self, board: Board) -> List[Tuple[int, int, int]]:
        """現在置けるすべての手を (x, y, z) で返す。満杯列は除外。"""
        moves: List[Tuple[int, int, int]] = []
        for y in range(4):
            for x in range(4):
                z = self.get_height(board, x, y)
                if z < 4:
                    moves.append((x, y, z))
        return moves

    def print_legal_moves(self, board: Board) -> None:
        """置けるマスを4x4の表で表示。各セルには石が落ちる z を表示（満杯は .）。"""
        grid = [['.' for _ in range(4)] for _ in range(4)]
        moves = self.get_legal_moves(board)
        for x, y, z in moves:
            grid[y][x] = str(z)

        # y=3 を上にして見やすく表示
        print("  x→   0 1 2 3    （値＝落ちる z / .＝満杯）")
        for y in range(3, -1, -1):
            print(f"y={y} |", ' '.join(grid[y]))
        print("合法手一覧:", sorted(moves))
    
    def count_accessible_lines(self, board: Board, x: int, y: int, z: int, player: int) -> int:
        """指定位置に石を置いた時にアクセスできる勝利ライン数をカウント"""
        # 仮想的に石を置く
        temp_board = [[[board[z][y][x] for x in range(4)] for y in range(4)] for z in range(4)]
        temp_board[z][y][x] = player
        
        accessible_lines = 0
        
        # 13方向の直線をチェック
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
            while 0 <= nx < 4 and 0 <= ny < 4 and 0 <= nz < 4 and temp_board[nz][ny][nx] == player:
                count += 1
                nx, ny, nz = nx + dx, ny + dy, nz + dz
            
            # 負方向にカウント
            nx, ny, nz = x - dx, y - dy, z - dz
            while 0 <= nx < 4 and 0 <= ny < 4 and 0 <= nz < 4 and temp_board[nz][ny][nx] == player:
                count += 1
                nx, ny, nz = nx - dx, ny - dy, nz - dz
            
            # 4つ以上並ぶ可能性があるラインをカウント
            if count >= 2:  # 2つ以上並んでいるライン
                accessible_lines += 1
        
        return accessible_lines
    
    def count_potential_lines(self, board: Board, x: int, y: int, z: int, player: int) -> int:
        """指定位置に石を置いた時に、4つ並ぶ可能性があるライン数をカウント"""
        potential_lines = 0
        
        # 13方向の直線をチェック
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
            # この方向に4つ並ぶ可能性があるかチェック
            can_form_line = True
            
            # 正方向の最大距離と障害物チェック
            max_pos = 0
            for i in range(1, 4):
                nx, ny, nz = x + i*dx, y + i*dy, z + i*dz
                if 0 <= nx < 4 and 0 <= ny < 4 and 0 <= nz < 4:
                    # 他のプレイヤーの石がある場合はラインを断ち切る
                    if board[nz][ny][nx] != 0 and board[nz][ny][nx] != player:
                        break
                    max_pos = i
                else:
                    break
            
            # 負方向の最大距離と障害物チェック
            max_neg = 0
            for i in range(1, 4):
                nx, ny, nz = x - i*dx, y - i*dy, z - i*dz
                if 0 <= nx < 4 and 0 <= ny < 4 and 0 <= nz < 4:
                    # 他のプレイヤーの石がある場合はラインを断ち切る
                    if board[nz][ny][nx] != 0 and board[nz][ny][nx] != player:
                        break
                    max_neg = i
                else:
                    break
            
            # 合計で4つ以上並べるかチェック
            if max_pos + max_neg + 1 >= 4:
                potential_lines += 1
        
        return potential_lines
    
    def print_line_accessibility(self, board: Board, player: int) -> None:
        """各マスに置いた時のアクセス可能ライン数を表示"""
        print(f"\n📊 プレイヤー{player}の各マスアクセス可能ライン数:")
        print("  x→   0 1 2 3    （値＝4つ並ぶ可能性があるライン数）")
        
        for y in range(3, -1, -1):
            print(f"y={y} |", end=" ")
            for x in range(4):
                if self.can_place_stone(board, x, y):
                    z = self.get_height(board, x, y)
                    # 常に潜在的なライン数を表示
                    lines = self.count_potential_lines(board, x, y, z, player)
                    print(f"{lines:2d}", end=" ")
                else:
                    print(" .", end=" ")
            print()
    
    def visualize_board(self, board: Board) -> None:
        """3D盤面を可視化"""
        print("\n" + "=" * 50)
        print("立体四目並べ盤面 (Z軸: 下から上へ 0→3)")
        print("=" * 50)
        
        for z in range(3, -1, -1):  # 上から下へ表示
            print(f"\nZ = {z} (高さ {z}):")
            print("  0 1 2 3")
            for y in range(4):
                print(f"{y} ", end="")
                for x in range(4):
                    if board[z][y][x] == 0:
                        print("・", end=" ")
                    elif board[z][y][x] == 1:
                        print("●", end=" ")  # 先手（黒）
                    elif board[z][y][x] == 2:
                        print("○", end=" ")  # 後手（白）
                print()
    
    def print_move_reason(self, board: Board, player: int, move: Tuple[int, int]) -> None:
        """AIの選択理由を表示"""
        print(f"\n🎮 AI選択: {move}")
        print(f"プレイヤー: {player} ({'先手(黒)' if player == 1 else '後手(白)'})")
        
        # 選択理由を分析
        win_move = self.find_winning_move(board, player)
        if win_move and win_move == move:
            print("🏆 理由: 勝利手")
            return
        
        opponent = 3 - player
        block_move = self.find_winning_move(board, opponent)
        if block_move and block_move == move:
            print("🛡️ 理由: 防御手")
            return
        
        best_line_move = self.find_highest_line_access_move(board, player)
        if best_line_move and best_line_move == move:
            lines = self.count_potential_lines(board, move[0], move[1], self.get_height(board, move[0], move[1]), player)
            print(f"📊 理由: 最高ラインアクセス ({lines}本)")
            return
        
        print("📍 理由: フォールバック")
    
    def find_best_move(self, board: Board, player: int):
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
        
        # 3. 最もアクセス可能なライン数が多い位置を探す
        best_move = self.find_highest_line_access_move(board, player)
        if best_move:
            return best_move
        
        # 4. 空いている最初の位置に置く
        return self.find_first_available_move(board)
    
    def find_highest_line_access_move(self, board: Board, player: int):
        """最もアクセス可能なライン数が多い位置を探す"""
        best_move = None
        max_lines = -1
        
        for x in range(4):
            for y in range(4):
                if self.can_place_stone(board, x, y):
                    z = self.get_height(board, x, y)
                    lines = self.count_potential_lines(board, x, y, z, player)
                    
                    if lines > max_lines:
                        max_lines = lines
                        best_move = (x, y)
        
        return best_move
    
    def find_winning_move(self, board: Board, player: int):
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
    
    def find_center_move(self, board: Board):
        """中央付近の空いている位置を探す"""
        center_positions = [(1, 1), (1, 2), (2, 1), (2, 2), (0, 1), (1, 0), (2, 3), (3, 2)]
        
        for x, y in center_positions:
            if self.can_place_stone(board, x, y):
                return (x, y)
        return None
    
    def find_first_available_move(self, board: Board):
        """最初に見つかった空いている位置に置く"""
        for x in range(4):
            for y in range(4):
                if self.can_place_stone(board, x, y):
                    return (x, y)
        return (0, 0)  # フォールバック
    
    def can_place_stone(self, board: Board, x: int, y: int):
        """指定位置に石を置けるかチェック"""
        return board[3][y][x] == 0  # 最上段が空いているか
    
    def get_height(self, board: Board, x: int, y: int):
        """指定位置の現在の高さを取得"""
        for z in range(4):
            if board[z][y][x] == 0:
                return z
        return 4  # 満杯
    
    def check_win(self, board: Board, x: int, y: int, z: int, player: int):
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