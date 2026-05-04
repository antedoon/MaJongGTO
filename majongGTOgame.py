'''
w = (1w, 2w, 3w, 4w, 5w, 6w, 7w, 8w, 9w) #萬
s = (1s, 2s, 3s, 4s, 5s, 6s, 7s, 8s, 9s) #索
p = (1p, 2p, 3p, 4p, 5p, 6p, 7p, 8p, 9p) #餅
z = (1z, 2z, 3z, 4z, 5z, 6z, 7z) #東南西北白發中
h = (1h, 2h, 3h, 4h, 5h, 6h, 7h, 8h) #春夏秋冬梅蘭竹菊
'''
mlist = ['1w', '2w', '3w', '4w', '5w', '6w', '7w', '8w', '9w', '1s', 
        '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '1p', '2p', 
        '3p', '4p', '5p', '6p', '7p', '8p', '9p', '東', '南', '西', 
        '北', '中', '發', '白']

MaJong = [i for i in range(136)]

    
def hand_sort(hand):
    '''
    整理手牌
    輸入:原本手牌list
    輸出:整理後手牌list
    '''
    HandIndex = [i for i in range(16)]
    for i in range(16): HandIndex[i] = MaJong.index(hand[i])
    HandIndex.sort()
    for i in range(16): hand[i] = MaJong[HandIndex[i]]
    return hand
def win(hand):
    '''
    https://www.thenewslens.com/article/100657
    定理1
    一副牌P，若把一個對子（俗稱眼睛）拿掉後，假設此時數字最小的牌是x，
    若x的張數是3張以上，則拿掉3張x（一刻）後，剩下牌為Q。
    否則拿掉x, x+1, x+2（一順）之後，剩下的牌為Q。（若無法拿，則P沒胡）
    則「P胡」若且唯若「Q胡」。

    定理2
    一副牌，依一四七、二五八、三六九分成三堆，
    每堆的張數除以三的餘數必有一個與另兩個不同，則眼睛就在不同的那堆裡。
    
    順序:
    除4確定是哪張牌 
    -> 判斷是不是字牌
        -> 若是, 分到字牌堆 
        -> 若不是, 除3判斷是147, 258, 369分堆
    -> 判斷字牌堆裡有沒有刻子
        ->若有, 直接拿掉
    -> 判斷字牌堆裡有沒有只有一對對子
        -> 若有, 跳到定理一
        -> 若沒有, 回傳沒胡
    -> 判斷每堆張數除三的餘數(找眼睛)(定理二)
    -> 眼睛拿掉後...(定理一)
    
    判斷胡牌
    輸入:手牌
    輸出:有無胡牌bool
    '''
    return False

def check_can_pon(hand, p, distile):
    '''
    確認可不可以碰
    輸入:手牌list, 第幾家打的, 棄牌
    輸出:哪一家能碰 沒有就輸出5
    '''
    for i in range(4):
        if i != p:
            for j in range(len(hand[i])): hand[i][j] = int(hand[i][j]/4)
            distile = int(distile/4)
            hand_set = list(set(hand[i]))
            for j in hand_set:
                if hand[i].count(j) >= 2 and j == distile: return True
    return False

def check_can_kan(hand, distile):
    for i in range(len(hand)): hand[i] = int(hand[i]/4)
    distile = int(distile/4)
    hand_set = list(set(hand))
    for i in hand_set:
        if hand.count(i) >= 3 and i == distile: return True
    return False

def check_can_chi(hand, p, distile):
    '''
    確認可不可以吃
    輸入:手牌List, 誰打的, 棄牌
    輸出:BOOL
    '''
    for i in range(len(hand[(p+1)%4])): hand[(p+1)%4][i] = int(hand[(p+1)%4][i]/4)
    distile = int(distile/4)
    hand_set = list(set(hand[p+1]))
    for j in hand_set:
        if hand[p+1].count(j) >= 2 and j == distile: return True
    return False
    
def game():
    #洗牌
    import random
    stack = MaJong.copy()
    random.shuffle(stack)
    #四家抓牌
    player_hand = [i for i in range(4)]
    for i in range(4): 
        player_hand[i] = []
        for j in range(16): player_hand[i].append(stack.pop())
        hand_sort(player_hand[i])
    dispool=[]
    p=0
    while True:
        #摸牌
        player_hand[p].append(stack.pop())
        #有無自摸
        if win(player_hand[p]): #自摸
            print(f"恭喜{mlist[p+27]}風玩家獲勝")
            return player_hand(p)
        
        while True:
            #棄牌
            print(player_hand[p])
            distile_index = int(input(f"輪到{p+27}風玩家，輸入要打掉的牌的索引值:"))
            distile = player_hand[p][distile_index-1]
            dispool.append(player_hand[p].pop(distile_index-1))
            
            #三家有無胡
            for i in range(4):
                if i != p and win(player_hand[i]): #放槍
                    print(f"恭喜{mlist[i+27]}風玩家獲勝")
                    player_hand[i].append(distile)
                    return player_hand(i)
            
            if check_can_pon(player_hand, p, distile) != 5: #確認其他家可不可以碰
                need_pon = int(input(f"請問{check_can_pon(player_hand, p, distile)+27}風玩家需要碰嗎，輸入 1 碰，輸入 0 不碰")) #要不要碰
                if need_pon == 1: #碰
                    p=check_can_pon(player_hand, p, distile)
                    print(f"{p+27}風玩家 碰，輪到{p+27}風玩家")
                    player_hand[p].append(distile)
                    hand_sort(player_hand[p])
                    continue
                elif need_pon == 0:  #不碰
                    if check_can_kan(player_hand, p, distile):  #確認可不可以槓
                        need_kan = int(input(f"請問{check_can_kan(player_hand, p, distile)+27}風玩家需要槓嗎，輸入 1 槓，輸入 0 不槓")) #要不要槓
                        if need_kan == 1: #要槓
                            p=check_can_kan(player_hand[check_can_pon(player_hand, p, distile)], distile)
                            print(f"{p+27}風玩家 槓，輪到{p+27}風玩家")
                            #摸牌
                            player_hand[p].append(stack.pop())
                            continue
                        elif need_kan == 0: continue #不槓
                        else: print("數字錯誤 放棄機會")
                else: print("數字錯誤 放棄機會")
            if check_can_chi(player_hand, p, distile): #確認下家可不可以吃
                need_chi = int(input(f"請問{p+27}風玩家需要吃嗎，輸入 1 吃，輸入 0 不吃")) #要不要吃
                if need_chi == 1: #要吃
                    print(f"{p+27}風玩家 吃，輪到{p+27}風玩家")
                    player_hand[p].append(distile)
                    hand_sort(player_hand[p])
                    continue
                elif need_chi == 0: break #不吃
            break
        if stack_is_empty():
            print("牌山為空 流局")
            return 0
#game()


