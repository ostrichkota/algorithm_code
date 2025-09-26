#!/usr/bin/env python3
"""
AIのテストスクリプト
ランダムな盤面でAIの動作をテストする
"""

import random
import time
from typing import List, Tuple
from main import MyAI
from local_driver import Board

def create_random_board(seed: int = None) -> Board:
    """ランダムな盤面を作成"""
    if seed is not None:
        random.seed(seed)
    
    board = [[[0 for x in range(4)] for y in range(4)] for z in range(4)]
    
    # ランダムに石を配置（0-20個程度）
    num_stones = random.randint(0, 20)
    
    for _ in range(num_stones):
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        
        # その列の最上段を探す
        for z in range(4):
            if board[z][y][x] == 0:
                player = random.randint(1, 2)  # プレイヤー1 or 2
                board[z][y][x] = player
                break
    
    return board

def create_test_board_1() -> Board:
    """テスト用盤面1: 中央に石が集中"""
    board = [[[0 for x in range(4)] for y in range(4)] for z in range(4)]
    
    # 中央付近に石を配置
    positions = [
        (1, 1, 0, 1), (1, 1, 1, 2), (1, 2, 0, 1), (2, 1, 0, 2),
        (2, 2, 0, 1), (2, 2, 1, 2), (1, 0, 0, 1), (0, 1, 0, 2)
    ]
    
    for x, y, z, player in positions:
        board[z][y][x] = player
    
    return board

def create_test_board_2() -> Board:
    """テスト用盤面2: 角に石が集中"""
    board = [[[0 for x in range(4)] for y in range(4)] for z in range(4)]
    
    # 角に石を配置
    positions = [
        (0, 0, 0, 1), (0, 0, 1, 2), (0, 3, 0, 1), (3, 0, 0, 2),
        (3, 3, 0, 1), (3, 3, 1, 2), (0, 0, 2, 1), (3, 3, 2, 2)
    ]
    
    for x, y, z, player in positions:
        board[z][y][x] = player
    
    return board

def create_test_board_3() -> Board:
    """テスト用盤面3: ほぼ満杯"""
    board = [[[0 for x in range(4)] for y in range(4)] for z in range(4)]
    
    # ほぼ満杯にする（各列に3個ずつ）
    for x in range(4):
        for y in range(4):
            for z in range(3):  # 最上段は空ける
                player = random.randint(1, 2)
                board[z][y][x] = player
    
    return board

def count_stones(board: Board) -> Tuple[int, int]:
    """盤面上の石の数をカウント"""
    count1 = count2 = 0
    for z in range(4):
        for y in range(4):
            for x in range(4):
                if board[z][y][x] == 1:
                    count1 += 1
                elif board[z][y][x] == 2:
                    count2 += 1
    return count1, count2

def test_ai_on_board(board: Board, player: int, test_name: str) -> bool:
    """指定された盤面でAIをテスト"""
    print(f"\n{'='*60}")
    print(f"テスト: {test_name}")
    print(f"プレイヤー: {player} ({'先手(黒)' if player == 1 else '後手(白)'})")
    
    count1, count2 = count_stones(board)
    print(f"盤面の石数: プレイヤー1={count1}個, プレイヤー2={count2}個")
    
    ai = MyAI()
    
    try:
        start_time = time.time()
        move = ai.get_move(board, player, (0, 0, 0))
        end_time = time.time()
        
        print(f"✅ 正常終了")
        print(f"選択された手: {move}")
        print(f"実行時間: {end_time - start_time:.3f}秒")
        
        return True
        
    except Exception as e:
        end_time = time.time()
        print(f"❌ エラー発生: {e}")
        print(f"実行時間: {end_time - start_time:.3f}秒")
        return False

def main():
    """メイン関数"""
    print("AIテストスクリプト開始")
    print("="*60)
    
    ai = MyAI()
    test_results = []
    
    # テスト1: 空の盤面
    empty_board = [[[0 for x in range(4)] for y in range(4)] for z in range(4)]
    result1 = test_ai_on_board(empty_board, 1, "空の盤面")
    test_results.append(("空の盤面", result1))
    
    # テスト2: ランダム盤面（複数回）
    for i in range(3):
        random_board = create_random_board(seed=i)
        result = test_ai_on_board(random_board, 1, f"ランダム盤面{i+1}")
        test_results.append((f"ランダム盤面{i+1}", result))
    
    # テスト3: 中央集中盤面
    center_board = create_test_board_1()
    result3 = test_ai_on_board(center_board, 1, "中央集中盤面")
    test_results.append(("中央集中盤面", result3))
    
    # テスト4: 角集中盤面
    corner_board = create_test_board_2()
    result4 = test_ai_on_board(corner_board, 2, "角集中盤面")
    test_results.append(("角集中盤面", result4))
    
    # テスト5: ほぼ満杯盤面
    full_board = create_test_board_3()
    result5 = test_ai_on_board(full_board, 1, "ほぼ満杯盤面")
    test_results.append(("ほぼ満杯盤面", result5))
    
    # テスト6: プレイヤー2でのテスト
    random_board2 = create_random_board(seed=100)
    result6 = test_ai_on_board(random_board2, 2, "プレイヤー2テスト")
    test_results.append(("プレイヤー2テスト", result6))
    
    # 結果サマリー
    print(f"\n{'='*60}")
    print("テスト結果サマリー")
    print("="*60)
    
    success_count = 0
    for test_name, result in test_results:
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"{test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n成功率: {success_count}/{len(test_results)} ({success_count/len(test_results)*100:.1f}%)")
    
    if success_count == len(test_results):
        print("🎉 すべてのテストが成功しました！")
    else:
        print("⚠️  一部のテストが失敗しました。")

if __name__ == "__main__":
    main()
