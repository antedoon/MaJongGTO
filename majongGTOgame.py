from collections import Counter
import random


# ==========================================================
# 函式名稱：create_wall
# 功能說明：建立一整副麻將牌山（136張）
# 參數：
#   無
# 回傳值：
#   list[str] -> 完整牌山
# ==========================================================
def create_wall():
    wall = []

    suits = ['w', 's', 'p']
    for suit in suits:
        for num in range(1, 10):
            wall.extend([f"{num}{suit}"] * 4)

    honors = ['東', '南', '西', '北', '中', '發', '白']
    for tile in honors:
        wall.extend([tile] * 4)

    return wall


# ==========================================================
# 函式名稱：tile_sort_key
# 功能說明：定義牌的排序規則
# 參數：
#   tile: str -> 一張牌
# 回傳值：
#   tuple -> 排序用 key
# ==========================================================
def tile_sort_key(tile):
    honor_order = {
        '東': 28,
        '南': 29,
        '西': 30,
        '北': 31,
        '中': 32,
        '發': 33,
        '白': 34
    }

    if tile in honor_order:
        return (4, honor_order[tile])

    num = int(tile[0])
    suit = tile[1]
    suit_order = {'w': 1, 's': 2, 'p': 3}
    return (suit_order[suit], num)


# ==========================================================
# 函式名稱：sort_hand
# 功能說明：排序手牌
# 參數：
#   hand: list[str] -> 手牌
# 回傳值：
#   list[str] -> 排序後手牌
# ==========================================================
def sort_hand(hand):
    return sorted(hand, key=tile_sort_key)


# ==========================================================
# 函式名稱：display_hand
# 功能說明：顯示手牌與索引
# 參數：
#   hand: list[str] -> 手牌
# 回傳值：
#   無
# ==========================================================
def display_hand(hand):
    hand = sort_hand(hand)
    print("\n你的手牌：")
    for i, tile in enumerate(hand):
        print(f"[{i:2}] {tile}", end="   ")
        if (i + 1) % 6 == 0:
            print()
    print("\n")
    return hand


# ==========================================================
# 函式名稱：is_suited_tile
# 功能說明：判斷是否為數牌
# 參數：
#   tile: str -> 一張牌
# 回傳值：
#   bool
# ==========================================================
def is_suited_tile(tile):
    return len(tile) == 2 and tile[1] in ['w', 's', 'p']


# ==========================================================
# 函式名稱：next_two_in_sequence
# 功能說明：取得順子的後兩張牌
# 參數：
#   tile: str -> 起始牌
# 回傳值：
#   tuple[str, str] 或 None
# ==========================================================
def next_two_in_sequence(tile):
    if not is_suited_tile(tile):
        return None

    num = int(tile[0])
    suit = tile[1]

    if num > 7:
        return None

    return f"{num + 1}{suit}", f"{num + 2}{suit}"


# ==========================================================
# 函式名稱：can_form_melds
# 功能說明：遞迴檢查是否能拆成指定數量的面子
# 參數：
#   counts: Counter -> 牌張統計
#   meld_target: int -> 需要拆出的面子數
# 回傳值：
#   bool
# ==========================================================
def can_form_melds(counts, meld_target):
    total_tiles = sum(counts.values())

    if total_tiles == 0:
        return meld_target == 0

    if total_tiles != meld_target * 3:
        return False

    current_tile = min(counts.keys(), key=tile_sort_key)

    # 先試刻子
    if counts[current_tile] >= 3:
        counts[current_tile] -= 3
        if counts[current_tile] == 0:
            del counts[current_tile]

        if can_form_melds(counts, meld_target - 1):
            return True

        counts[current_tile] = counts.get(current_tile, 0) + 3

    # 再試順子
    seq = next_two_in_sequence(current_tile)
    if seq:
        t2, t3 = seq
        if counts.get(t2, 0) >= 1 and counts.get(t3, 0) >= 1:
            counts[current_tile] -= 1
            counts[t2] -= 1
            counts[t3] -= 1

            removed = []
            for t in [current_tile, t2, t3]:
                if counts[t] == 0:
                    removed.append(t)
            for t in removed:
                del counts[t]

            if can_form_melds(counts, meld_target - 1):
                return True

            counts[current_tile] = counts.get(current_tile, 0) + 1
            counts[t2] = counts.get(t2, 0) + 1
            counts[t3] = counts.get(t3, 0) + 1

    return False


# ==========================================================
# 函式名稱：is_win
# 功能說明：判斷 17 張手牌是否胡牌（5面子1雀頭）
# 參數：
#   hand: list[str] -> 17張手牌
# 回傳值：
#   bool
# ==========================================================
def is_win(hand):
    if len(hand) != 17:
        return False

    counts = Counter(hand)

    for tile in list(counts.keys()):
        if counts[tile] >= 2:
            temp_counts = counts.copy()
            temp_counts[tile] -= 2
            if temp_counts[tile] == 0:
                del temp_counts[tile]

            if can_form_melds(temp_counts, 5):
                return True

    return False


# ==========================================================
# 函式名稱：check_tenpai_tiles
# 功能說明：找出目前 16 張聽哪些牌
# 參數：
#   hand: list[str] -> 16張手牌
# 回傳值：
#   list[str] -> 聽牌列表
# ==========================================================
def check_tenpai_tiles(hand):
    if len(hand) != 16:
        return []

    all_tiles = []
    suits = ['w', 's', 'p']
    for suit in suits:
        for num in range(1, 10):
            all_tiles.append(f"{num}{suit}")
    all_tiles.extend(['東', '南', '西', '北', '中', '發', '白'])

    winning_tiles = []
    counts = Counter(hand)

    for tile in all_tiles:
        if counts[tile] < 4:
            test_hand = hand + [tile]
            if is_win(test_hand):
                winning_tiles.append(tile)

    return winning_tiles


# ==========================================================
# 函式名稱：game_loop
# 功能說明：17張麻將單人遊戲主迴圈
# 參數：
#   無
# 回傳值：
#   無
# ==========================================================
def game_loop():
    wall = create_wall()
    random.shuffle(wall)

    hand = [wall.pop() for _ in range(16)]

    print("輸入 q 可離開遊戲")
    print("====================================")

    turn = 1

    while True:
        if len(wall) == 0:
            print("\n牌山已空，流局！")
            break

        print(f"\n========== 第 {turn} 回合 ==========")
        hand = sort_hand(hand)
        display_hand(hand)

        tenpai_tiles = check_tenpai_tiles(hand)
        if tenpai_tiles:
            print("你目前聽牌：", " ".join(sort_hand(tenpai_tiles)))
        else:
            print("你目前尚未聽牌")

        draw_tile = wall.pop()
        hand.append(draw_tile)
        hand = sort_hand(hand)

        print(f"\n你摸到：{draw_tile}")
        display_hand(hand)

        if is_win(hand):
            print("恭喜，你自摸胡牌了！")
            print("胡牌手牌：")
            display_hand(hand)
            break

        while True:
            discard_input = input("請輸入要打掉的牌索引：").strip()

            if discard_input.lower() == 'q':
                print("遊戲結束。")
                return

            if not discard_input.isdigit():
                print("請輸入有效數字。")
                continue

            discard_index = int(discard_input)

            if 0 <= discard_index < len(hand):
                discarded = hand.pop(discard_index)
                print(f"你打出了：{discarded}")
                break
            else:
                print("索引超出範圍，請重新輸入。")

        turn += 1


# ==========================================================
# 主程式入口
# ==========================================================
if __name__ == "__main__":
    game_loop()