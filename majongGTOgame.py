'''
w = (1w, 2w, 3w, 4w, 5w, 6w, 7w, 8w, 9w) #萬
s = (1s, 2s, 3s, 4s, 5s, 6s, 7s, 8s, 9s) #索
p = (1p, 2p, 3p, 4p, 5p, 6p, 7p, 8p, 9p) #餅
z = (1z, 2z, 3z, 4z, 5z, 6z, 7z) #東南西北白發中
h = (1h, 2h, 3h, 4h, 5h, 6h, 7h, 8h) #春夏秋冬梅蘭竹菊
'''
w1=1
w2=2
w3=3
w4=4
w5=5
w6=6
w7=7
w8=8
w9=9
s1=10
s2=11
s3=12
s4=13
s5=14
s6=15
s7=16
s8=17
s9=18
p1=19
p2=20
p3=21
p4=22
p5=23
p6=24
p7=25
p8=26
p9=27
東=28
南=29
西=30
北=31
中=32
發=33
白=34
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

def game():
    #洗牌
    import random
    stack = MaJong.copy()
    random.shuffle(stack)
    #四家抓牌
    player_hand = [i for i in range(4)]
    for i in range(4): 
        player_hand[i] = [j for j in range(17)]
        for j in range(16): player_hand[i][j] = stack.pop()
        hand_sort(player_hand[i])
    #hand = ['6w', '7w', '7w', '8w', '8w', '9w', '4w', '1w', '1w', '1w', '2w', '2w', '3w', '3w', '3w', '4w', '4w']
    dispool=[]
    p=0
    while True:
        player_hand[p].append(stack.pop())
        if win(player_hand[p]): 
            print(f"恭喜{mlist[p+27]}風玩家獲勝")
            break
        #棄牌
        print(player_hand[p])
        distile = int(input("輸入要打掉的牌的索引值"))
        dispool.append(player_hand[p][distile-1].pop())
        print(dispool)
        print(player_hand[p])
        break
        p+=1
        if p>=4: p=0
game()


