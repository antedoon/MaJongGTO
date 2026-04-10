"""
全部胡牌可能
=全不重疊*眼 + 一張重疊*眼 + 兩張重疊*眼 + 三張重疊*眼 +...+十五張重疊
=

一張重疊
=一二組重疊 + 二三組重疊 +...+ 四五組重疊
=

全部胡牌可能
=全順 + 1刻4順 +...+ 全刻
=全順 + 第1組刻 2345順 + 第1組順 2刻 345順 +...+ 全刻
=

0409
目前版本:優化get_pair(), countallcomb(), 以get_cant_be_pair(), loop()取代 
get_cant_be_pair(), loop()已可包含所有胡牌可能 帶入參數改為使用list
4010
嘗試將參數自動化輸入，目前發現可能規律，用xapart跟xxchange窮舉即可，bnx跟xxend可以用xapart去反推
新增all_xapart_xxchange()函式

嘗試後發現規律不對且複雜 改試 全順 + 1刻4順 +...+ 全刻
新增函式illegal_comb()，將不合法組合都去除
    
todo: 
    1.把全部胡牌可能的參數一個一個帶入 or 寫一個函式盡量可涵蓋全部胡牌可能 直接帶入loop即可
    2.製作胡牌種期望值
"""
import time
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
mlist = ['null', 
        '1w', '2w', '3w', '4w', '5w', '6w', '7w', '8w', '9w', '1s', 
        '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '1p', '2p', 
        '3p', '4p', '5p', '6p', '7p', '8p', '9p', '東', '南', '西', 
        '北', '中', '發', '白']
def check(x, bn):
    '''
    順子不可能出現那些起始數字
    輸入: 不可出現的整數 0 <= x <= 9
    輸出: 跳過不可出現數的數(進位)
    
    若是刻子輸入0
    '''
    banned_number=[]
    if bn == 0: return x
    for i in range(bn, 10): banned_number.append(i)
    for i in range(bn+9, 10+9): banned_number.append(i)
    while x in banned_number: x+=1
    return x

def illegal_comb(xx, who_is_trip):
    '''
    跳過不合法組合
    輸入: 目前組合, 誰是刻子
    輸出: 合不合法
    '''
    hand=[]
    
    for i in range(5):
        if i+1 not in who_is_trip:
            for seq in range(3): hand.append(xx[i]+seq)
        else:
            for l in range(3): hand.append(xx[i])
    hand_set = list(set(hand))
    for i in hand_set:
        if hand.count(i) >= 5: return True
    return False

def get_cant_be_pair(who_is_trip, xx, bnx, count, showtile):
    '''
    那些牌不能當眼
    
    輸入: 刻子的位置
    輸出: 更新後的 count
    '''
    if illegal_comb(xx, who_is_trip): return count
    cant_be_pair = []
    for i in range(5): #111
        if bnx[i] == 0:  cant_be_pair.append(xx[i])
  
    for i in range(3):
        if (xx[i]+2) == (xx[i+1]+1) == xx[i+2]: cant_be_pair.append(xx[i+2]) #123, 234, 345
        if xx[i] == xx[i+1] == xx[i+2]: #123, 123, 123
            cant_be_pair.append(xx[i])
            cant_be_pair.append(xx[i]+1)
            cant_be_pair.append(xx[i]+2)
        if xx[i]+1 == xx[i+1]+1 == xx[i+2] or xx[i]+1 == xx[i+1] == xx[i+2]: #123, 123, 234 OR 123, 234, 234
            cant_be_pair.append(xx[i]+1)
            cant_be_pair.append(xx[i]+2)
        if xx[i]+2 == xx[i+1]+2 == xx[i+2] or xx[i]+2 == xx[i+1] == xx[i+2]: #123, 123, 345 OR 123, 345, 345
            cant_be_pair.append(xx[i+2])
        
    cant_be_pair = list(set(cant_be_pair))
    cant_be_pair.sort()
    if cant_be_pair == []: cant_be_pair.append(0)
    pair = 1
    while pair <= 34:
        if pair not in cant_be_pair:
            if showtile:
                for i in range(5):
                    print(mlist[xx[i]], end=' ')
                print(mlist[pair] + mlist[pair])
                time.sleep(1)
            count += 1
        pair += 1

    return count

def loop(i, who_is_trip, xx, bnx, xxend, xapart, xxchange, count, showtile):
    '''
    主窮舉迴圈
    輸入:
        who_is_trip=誰是刻子
        bnx=順子不可出現的最小數字
        xxend=窮舉最後一組數字
        xapart=x2-x1
        xxchange=xx[i]每次迴圈動多少(分組)同組必有重疊, 從1到下個1之間都同組
        xx=第幾組
    輸出:
        int count
    '''
    while xx[i] <= xxend[i]:
        xx[i] = check(xx[i], bnx[i])
        if i == 4: count = get_cant_be_pair(who_is_trip, xx, bnx, count, showtile)
        else:
            xx[i + 1] = xx[i] + xapart[i]
            count = loop(i + 1, who_is_trip, xx, bnx, xxend, xapart, xxchange, count, showtile)
        xx[i] += xxchange[i]
        if xxchange[i] == 0: break
    return count

#全順 1762320
who_is_trip=[]
bnx=[w8, w8, w8, w8, w8]
xxend=[p4, p7, p7, p7, p7]
xapart=[0, 0, 0, 0]
xxchange=[1, 1, 1, 1, 1]
xx=[1, 0, 0, 0, 0]
count=0
#count = loop(0, who_is_trip, xx, bnx, xxend, xapart, xxchange, 0, showtile=1)
print(count)
#第一組是刻 1830316
who_is_trip=[1]
bnx=[0, w8, w8, w8, w8]
xxend=[p7, p7, p7, p7, p7]
xapart=[0, 0, 0, 0]
xxchange=[1, 1, 1, 1, 1]
xx=[1, 0, 0, 0, 0]
count=0
#count = loop(0, who_is_trip, xx, bnx, xxend, xapart, xxchange, 0, showtile=1)
print(count)
#第二組是刻
who_is_trip=[2]
bnx=[w8, 0, w8, w8, w8]
xxend=[p7, p7, p7, p7, p7]
xapart=[0, 0, 0, 0]
xxchange=[1, 1, 1, 1, 1]
xx=[1, 0, 0, 0, 0]
count=0
count = loop(0, who_is_trip, xx, bnx, xxend, xapart, xxchange, 0, showtile=1)
print(count)
'''
print("全部不重複")
count += countallcomb(w8, w8, w8, w8, w8, s4, s7, p1, p4, p7, 3, 3, 3, 3, 1, 1, 1, 1, 1, count, showtile=False)
print(count)

count = 0
print("1張重疊*眼")
print("一二組重疊")
count += countallcomb(w6, w8, w8, w8, w8, s5, s7, p1, p4, p7, 2, 3, 3, 3, 1, 0, 1, 1, 1, count, showtile=False)
print("二三組重疊")
count += countallcomb(w8, w6, w8, w8, w8, s2, s5, s7, p4, p7, 3, 2, 3, 3, 1, 1, 0, 1, 1, count, showtile=False)
print("三四組重疊")
count += countallcomb(w8, w8, w6, w8, w8, s4, s7, p2, p4, p7, 3, 3, 2, 3, 1, 1, 1, 0, 1, count, showtile=False)
print("四五組重疊")
count += countallcomb(w8, w8, w8, w6, w8, s4, s7, p2, p5, p7, 3, 3, 3, 2, 1, 1, 1, 1, 0, count, showtile=False)
print(count)

count = 0
print("2張重疊*眼")
#一二三組各疊一張
count += countallcomb(w4, w6, w8, w8, w8, s3, s5, s7, p4, p7, 2, 2, 3, 3, 1, 0, 0, 1, 1, count, showtile=False)
#二三四組各疊一張
count += countallcomb(w8, w4, w6, w8, w8, w7, s3, s5, s7, p7, 3, 2, 2, 3, 1, 1, 0, 0, 1, count, showtile=False)
#三四五組各疊一張
count += countallcomb(w8, w8, w4, w6, w8, s4, s7, p3, p5, p7, 3, 3, 2, 2, 1, 1, 1, 0, 0, count, showtile=False)
#一二組疊兩張
count += countallcomb(w7, w8, w8, w8, w8, s6, s7, p1, p4, p7, 1, 3, 3, 3, 1, 0, 1, 1, 1, count, showtile=False)
#二三組疊兩張
count += countallcomb(w8, w7, w8, w8, w8, s3, s6, s7, p4, p7, 3, 1, 3, 3, 1, 1, 0, 1, 1, count, showtile=False)
#三四組疊兩張
count += countallcomb(w8, w8, w7, w8, w8, s4, s7, p3, p4, p7, 3, 3, 1, 3, 1, 1, 1, 0, 1, count, showtile=False)
#四五組重疊兩張
count += countallcomb(w8, w8, w8, w7, w8, s4, s7, p3, p6, p7, 3, 3, 3, 1, 1, 1, 1, 1, 0, count, showtile=False)
print(count)

count=0
print("3張重疊*眼")
#一組是刻
count += countallcomb(0, w8, w8, w8, w8, s7, s7, p1, p4, p7, 0, 3, 3, 3, 1, 1, 1, 1, 1, count, showtile=False)
#二組是刻
count += countallcomb(w8, 0, w8, w8, w8, s7, p1, p1, p4, p7, 2, 3, 3, 3, 1, 1, 1, 1, 1, count, showtile=False)
#三組是刻
count += countallcomb(w8, w8, 0, w8, w8, s7, p1, p4, p4, p7, 3, 2, 3, 3, 1, 1, 1, 1, 1, count, showtile=False)
#四組是刻
count += countallcomb(w8, w8, w8, 0, w8, s7, p1, p4, p7, p7, 3, 3, 2, 3, 1, 1, 1, 1, 1, count, showtile=False)
#五組是刻
count += countallcomb(w8, w8, w8, w8, 0, s7, p1, p4, p7, 白, 3, 3, 3, 2, 1, 1, 1, 1, 1, count, showtile=False)
#一二組重疊三張
print(countallcomb(w8, w8, w8, w8, w8, s7, s7, p1, p4, p7, 0, 3, 3, 3, 1, 0, 1, 1, 1, count, showtile=False))
#一二組是刻
loop(0, 0, 8w, 8w, 8w, s9, p1, p1, p4, p7, 1, 0, 3, 3, 1, 0, 1, 1, 1)
'''
def get_all_xapart_xxchange():
    xapart=[0, 0, 0, 0]
    all_xapart=[]
    for x1apart in range(4):
        xapart[0] = x1apart
        for x2apart in range(4):
            xapart[1] = x2apart
            for x3apart in range(4):
                xapart[2] = x3apart
                for x4apart in range(4):
                    xapart[3] = x4apart
                    all_xapart.append(xapart)
    xxchange = [0, 0, 0, 0, 0]
    all_xxchange=[]
    count=0
    for x1change in range(2):
        xxchange[0] = x1change
        for x2change in range(2):
            xxchange[1] = x2change
            for x3change in range(2):
                xxchange[2] = x3change
                for x4change in range(2):
                    xxchange[3] = x4change
                    for x5change in range(2):
                        xxchange[4] = x5change
                        all_xxchange.append(xxchange)
                        count+=1
    return all_xapart, all_xxchange

def trans_xapart_to_bnx_xxend(get_all_xapart_xxchange, xxend):
    all_xapart = get_all_xapart_xxchange[0]
    all_xxchange = get_all_xapart_xxchange[1]
    for xapart in all_xapart:
        if xapart[3] == 0: xxend[4] = 白
        else: xxend[4] = p7
    
#print(get_all_xapart_xxchange())