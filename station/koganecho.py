from requests_html import HTMLSession
import datetime

url = "https://norikae.keikyu.co.jp/transit/norikae/T5?uid=29520&dir=53&path=20201027233153548&USR=PC&dw=0&slCode=250-25&d=2&rsf=%89%A1%95%6C"
#京急線黄金町駅下り普通列車のURL

# セッション開始
session = HTMLSession()
r = session.get(url)

# ブラウザエンジンでHTMLを生成させる
r.html.render()

#運行情報を取得

#改行単位でsplit
#参考URL：https://karupoimou.hatenablog.com/entry/2019/07/08/112734
page = r.text.split("\n")
for i in range(len(page)):
    p = page[i]
    if "運行情報" in p:
        info = page[i+1]#「運行情報」文字列の次の行に内容が書いてある．

#時刻表（時間）を取得
hour = r.html.find(".side01")
hour_list = []
for h in hour:
    hour_list.append(int(h.text))
train = hour_list[0]#始発時間を取得

#時刻表（分）を取得
minute = r.html.find(".min1001")
minute_list = []
for m in minute:
    minute_list.append(int(m.text))
del minute_list[0]#最初と最後の要素は時刻ではないので削除
del minute_list[-1]#同上

#時刻表を格納するための２次元配列の初期化
num = len(minute_list)
dep = [[0 for i in range(2)] for j in range(num)]

#時刻表の構築作業
for i in range(num):
    if  i>0 and minute_list[i-1] > minute_list[i]:
        train+=1
    dep[i] = (train, minute_list[i])
#print(dep)#時刻表の確認

#現在時刻を取得
#参考URL：https://note.nkmk.me/python-datetime-now-today/
now_time = datetime.datetime.now()
now_hour = now_time.hour
now_minute = now_time.minute
#print(now_hour, now_minute)#現在時刻の確認


#現在時刻から最も近い発車時刻を取得
next=0
now_i=0
for i in range(num):#始発電車から１つずつ探していく．
    if dep[i][0]==now_hour:#現在時刻（時間）と比較
        now_i = i
        if dep[i][1]>now_minute:#現在時刻（分）と比較
            next = i
            break
if next==0:#分がHitしなかった場合の処理
    next=now_i+1

#結果出力
print("今日もおつかれさまでした．")
print("京急線は"+ info)
print("次の発車は")
for i in range(3):
    if next+i>=num:
        next = -1
        print("〜終電〜")
    print(str(dep[next+i][0]).zfill(2)+":"+str(dep[next+i][1]).zfill(2))#発車時刻を表示
