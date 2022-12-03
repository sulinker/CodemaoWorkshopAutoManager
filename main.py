import requests,random
import datetime,time
from allapi import *

'''
使用须知：
1、json文件无法用海龟编辑器打开，建议用sublime修改积分文件
  修改后记得保存sublime保存：ctrl+s，
  如果json改了后报错，sublime可以用ctrl+z撤销上一步操作
2、未经许可禁止将程序发给其他人
3、请不要删除“（自动管理程序来自水翎稞）”
'''

'''
自动招人说明：
如果有人申请了，将会读取他的赞数。如果他的赞>=AUDITLIKE而且没有在黑名单内，就会自动通过（否则就拒绝），并记录在log.json内。
为了防止有人恶意退出重进进行骚扰，每个人每小时只会通过一次。
'''
COOKIE = "cookie"
EM = ["ヾ(≧▽≦*)o",'(～￣▽￣)～','<(￣︶￣)↗','O(∩_∩)O','(*^▽^*)','(≧∇≦)','o(*￣︶￣*)o']
OWNER_ID = [] #将用户id填入，中间以“,”（英文逗号）分隔，这些用户可以使用“删除室员投稿”命令
LIMIT = 10 #每次执行时处理LIMIT（5<=LIMIT<=20）个新消息
AUDITLIKE = 1 #修改后面的数值可以设置几赞及以上可以自动通过
description = "工作室简介"
WHITE_ID = [10042242] #非工作室的也能签到的白名单
TOP_NUM = 1; #工作室评论区置顶的消息数（如果签到失效检查一下这个）
URID = 114514 #工作室编号
name = "" #工作室名
head = "" #工作室头像url（可抓包获取头像的url）

def find(n, l):
    for i in l:
        if i == n:
            return True
    return False


def findin(n, l, a):
    for i in l:
        if i[a] == n:
            return True
    return False


def canJoin(n, l, a, name):
    for i in l:
        if i[a] == n:
            if i[0] == name:
                return False
    return True


header = {
    "cookie": COOKIE
}

us = User(header)
ws = WorkShop(header)

WSID = ws.getwsid(URID)



i = 0

#记录的是黑名单id（如果有人捣乱可以把它的id加入（用sublime））
with open("blackId.json", "r", encoding="utf-8") as f:
    blackId = json.load(f)

# with open("words.json", "r", encoding="utf-8") as f:
#     words = json.load(f)

print(blackId)


while True:
    d = datetime.datetime.now()
    aaa = None
    
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(i, ws.updateDetail(WSID, description, name, head))
    text = ws.getWillJoin(WSID)[1]
    print(i, text)


#自动同意申请：
    if text["items"] != []:
        id = text["items"][0]["user_id"]
        nickname = text["items"][0]["nickname"]
        r = us.getDetail(id)
        like = r[1]['liked_total']

        y = d.year
        m = d.month
        dy = d.day
        h = d.hour
        mi = d.minute
        s = d.second
        timeCode = f"{y},{m},{dy},{h}"

        findornot = find(id, blackId)

        if not findornot and like >= AUDITLIKE:
            text = f"欢迎 {nickname} 加入工作室！"
            with open("log.json", "r", encoding="utf-8") as f:
                aaa = json.load(f)
                print(nickname, canJoin(timeCode, aaa, 2, nickname))
                if canJoin(timeCode, aaa, 2, nickname):
                    ws.sendReview(URID, text)
                    ws.audit(WSID, id, True)
                    aaa.append([nickname, {"id": id, "like": like}, timeCode, {
                               "year": y, "month": m, "day": dy, "hour": h, "minute": mi, "second": s}, text, True])
                    time.sleep(3)
                else:
                    aaa.append([nickname, {"id": id, "like": like}, timeCode, {
                               "year": y, "month": m, "day": dy, "hour": h, "minute": mi, "second": s}, "进入过于频繁", False])
                    ws.audit(WSID, id, False)

            with open("log.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(aaa, sort_keys=False,
                        indent=4, ensure_ascii=False))

        else:
            ws.audit(WSID, id, False)
            with open("log.json", "r", encoding="utf-8") as f:
                aaa = json.load(f)
                if findornot and like < AUDITLIKE:
                    aaa.append([nickname, {"id": id, "like": like}, timeCode, {
                               "year": y, "month": m, "day": dy, "hour": h, "minute": mi, "second": s}, f"点赞小于{AUDITLIKE}（{like}）且 ", False])
                elif like < AUDITLIKE:
                    aaa.append([nickname, {"id": id, "like": like}, "-1", {"year": y, "month": m, "day": dy,
                               "hour": h, "minute": mi, "second": s}, f"点赞小于{AUDITLIKE}（{like}）", False])
                elif findornot:
                    aaa.append([nickname, {"id": id, "like": like}, timeCode, {
                               "year": y, "month": m, "day": dy, "hour": h, "minute": mi, "second": s}, f"黑名单", False])

            with open("log.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(aaa, sort_keys=False,
                        indent=4, ensure_ascii=False))


    if i %1000 == 0:
        nu = LIMIT;
    else:
        nu = 1;
    for q in range(TOP_NUM,TOP_NUM+nu):
        if nu == 1:
            rev = ws.getReviews(URID,limit=5)[1]
        else:
            rev = ws.getReviews(URID,limit=TOP_NUM+nu)[1]

        # print(rev)
        # rev = rev[q]
        # print(q)
        islike = rev['items'][q]['is_liked']
        userid = rev['items'][q]['user']['id']
        intUserid = int(userid)
        wsnm = rev['items'][q]['user']["work_shop_name"]
        nkname = rev['items'][q]['user']['nickname']
        messageid = rev['items'][q]['id']
        text = rev['items'][q]['content']
        createat = rev['items'][q]["created_at"]
        # print(text,wsnm)
        y = d.year
        m = d.month
        dy = d.day
        h = d.hour
        mi = d.minute
        s = d.second
        tk = f"{y},{m},{dy}"
        adds = "（自动管理程序来自水翎稞）" #小广告（（（

        # print(text)

        can = True
        if i % 2 == 0 and islike == False:
            if text == '签到' and (wsnm == name or find(intUserid,WHITE_ID)):
                with open("mark.json", "r", encoding="utf-8") as f:
                    ts = json.load(f)
                    ks = ts.keys()
                    print(ks)
                    try:
                        ass = adds
                    except Exception as e:
                        break
                    ishave = find(userid, ks)
                    if ishave:
                        tc = ts[userid]["timeCode"]
                        mk = ts[userid]["mark"]
                        if tc == tk:
                            can = False
                            print(ws.replyReview(
                                f'你今天已经签到过了！当前积分：{mk}{adds}', URID, messageid))
                            print(ws.likeReview(messageid))
                        else:
                            ts[userid]["timeCode"] = tk
                            ts[userid]["mark"] += 10

                    else:
                        ts[userid] = {"timeCode": tk, "name": nkname, "mark": 10}
                with open("mark.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(ts, sort_keys=False,
                            indent=4, ensure_ascii=False))

                if can:
                    print(ws.replyReview(
                        f'签到成功！当前积分{ts[userid]["mark"]}{adds}', URID, messageid))
                    print(ws.likeReview(messageid))
            elif text[0:12] == "删除我的投稿，作品id：":
                try:
                    num = int(text[12:-1]+text[-1])
                    print(num)
                    r = ws.getAllWorks(URID);
                    for z in r:
                        if z["workId"] == num:
                            if z["creatorId"] == userid:
                                ws.removeWork(WSID,num)
                                print(ws.replyReview("已删除。",URID,messageid))
                                break;
                            else:
                                print(ws.replyReview("这不是你的作品",URID,messageid))
                                break;
                    else:
                        print(ws.replyReview("没找到诶",URID,messageid))
                    print(ws.likeReview(messageid));
                except:
                    print(ws.replyReview(f"删除作品格式错误",URID,messageid))
                    print(ws.likeReview(messageid));
                    print("error")
            elif text[0:12] == "删除室员投稿，室员id：" and find(intUserid,OWNER_ID):
                try:
                    num = int(text[12:-1]+text[-1])
                    print(num)
                    r = ws.getAllWorks(URID);
                    deleteId = []
                    for z in r:
                        if int(z["creatorId"]) == num:
                            print(ws.removeWork(WSID,z["workId"]))
                            # print(ws.replyReview("删除",URID,messageid))
                            print("删除作品："+str(z["workId"]))
                            deleteId.append(z["workId"])
                    if deleteId == []:
                        print(ws.replyReview("没找到诶",URID,messageid))
                    else:
                        print(ws.replyReview(f"删除作品：{str(deleteId)}",URID,messageid))
                    print(ws.likeReview(messageid));
                except Exception as e:
                    traceback.print_exc()
                    # print(e)
                    print(ws.replyReview(f"删除作品格式错误",URID,messageid))
                    print(ws.likeReview(messageid));
                    # print("exception")
            elif text[0:2] == "串门":
                print(ws.replyReview(f"欢迎！{random.choice(EM)}",URID,messageid))
                print(ws.likeReview(messageid));

    # except Exception as e:
    #     print(e)
    #     print("fail")
    #     print("出错了")

    #没必要太快，于是调成了3s一次
    #为了测试的效果，我调成了1s，如果我傻了忘记改为3s，记得改回去（下面的1改成3就好）
    #太快浪费资源，建议5s一次
    i += 1
    time.sleep(5)
