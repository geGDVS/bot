#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 远方的开发者，您好！这是一个XChat的测试机器人，使用Python编写。这里面提供了一些实例，供您参考！
import XChat  # 引入模块
import time, random  # 引入模块

lockFlag = 0


def read_file(file):
    f = open(file, 'r')
    nList = f.readlines()
    f.close()
    for i in range(len(nList)):
        nList[i] = nList[i].strip('\n')
    for s in nList:
        if s == '':
            nList.remove(s)
    return nList


def write_file(file, List):
    for i in range(len(List)):
        List[i] += '\n'
    f = open(file, "w")
    f.writelines(List)


def words(txt):
    wList = []
    word = ''
    for c in txt:
        if 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_' or '0' <= c <= '9' or c in '+/':
            word += c
        elif word != '':
            wList.append(word)
            word = ''
    if word != '':
        wList.append(word)
    return wList


# 信息接收处理函数，当有人在公屏上发送信息时，会调用这个。
# 两个参数分别代表：信息内容和发送者。
def message_got(message, sender, trip):
    global lockFlag
    print('收到 [{trip}]{who} 在公屏上发送的信息：{msg}'.format(who=sender, msg=message, trip=trip))
    wList = words(message)
    modTrip = read_file('mod')
    trustTrip = read_file('trust')
    protectList = read_file('protect')
    if message[0:4] == '.bb ':
        if wList[1] == 'help':
            xc.send_to(sender, """下列指令可以使用：
            -----User-----
            1、.bb help：获取帮助
            2、.bb shoot <name>: 向<name>射击
            3、.bb hug <name>: 抱抱<name>
            4、.bb cookie <name>: 给<name>曲奇饼干
            5、.bb roll: 生成1～1000的随机数
            ----Trust ----
            1、.bb protect <name>: 派出BBI保护<name>免受枪击
            2、.bb cancel <name>: 取消BBI对<name>的保护
            3、.bb protectlist: 查看BBI的保护列表
            4、.bb lockflag: 查看锁房状态
            -----Mod -----
            1、.bb lock: 锁房
            2、.bb unlock: 解除锁房
            3、.bb kick <name>: 踢出<name>
            4、.bb add <trip>: 添加机器人额外功能使用权
            5、.bb del <trip>: 移除机器人额外功能使用权
            6、.bb list: 查看机器人额外功能使用权拥有者
            7、.bb trust <trip>: 添加本机器人的信任用户
            8、.bb deltrust <trip>: 移除本机器人的信任用户
            9、.bb getrust: 查看本机器人的信任用户
            ----Admin ----
            1、.bb nick <name>: 更换名称为<name>
            2、.bb move <room>: 将机器人移至<room>
            3、/w BBot send <text>: 让机器人发送<text>""")
        if wList[1] == 'shoot' and '&#8238;' not in message:
            shoot = message[10:]
            shootList = ['打断了Ta的膝盖', '打穿了Ta的胸膛', '打爆了Ta的头盖骨', '但是没打中', '但是被BBI拦截了']
            if shoot not in protectList:
                if shoot == 'BBot':
                    shoot = 'Ta自己'
                xc.send_message("{user}向{shoot}开了一枪，{how}".format(user=sender, shoot=shoot, how=shootList[random.randint(0, 3)]))
            else:
                xc.send_message("{user}向{shoot}开了一枪，{how}".format(user=sender, shoot=shoot, how=shootList[4]))
        if wList[1] == 'hug':
            hug = message[8:]
            xc.send_message('{user}给了{hug}一个抱抱'.format(user=sender, hug=hug))
        if wList[1] == 'cookie':
            cookie = message[11:]
            xc.send_message('{user}给了{cookie}一个曲奇饼干'.format(user=sender, cookie=cookie))
        if wList[1] == 'roll':
            xc.send_message('{user} roll出了{roll}'.format(user=sender, roll=random.randint(1, 1000)))
        if trip in trustTrip or trip in modTrip:
            if wList[1] == 'protect':
                protect = wList[2]
                if protect not in protectList:
                    protectList.append(protect)
                    write_file('protect', protectList)
                    xc.send_message('已派出BBI保护{name}'.format(name=protect))
                else:
                    xc.send_message('{name}已在BBI的保护名单里。'.format(name=protect))
            if wList[1] == 'cancel':
                protect = wList[2]
                if protect in protectList:
                    protectList.remove(protect)
                    write_file('protect', protectList)
                    xc.send_message('已取消对{name}的保护。'.format(name=protect))
                else:
                    xc.send_message('{name}不在BBI的保护名单里。'.format(name=protect))
            if wList[1] == 'protectlist':
                send = 'BBI的保护名单是：'
                for s in protectList:
                    send += s + ' '
                xc.send_to(sender, send)
            if wList[1] == 'lockflag':
                if lockFlag:
                    xc.send_message('锁房状态为：开启锁房')
                else:
                    xc.send_message('锁房状态为：关闭锁房')
        if trip in modTrip:
            if wList[1] == 'lock':
                lockFlag = 1
                xc.send_message('已锁房')
                # xc.send_to('ZhangHelper', '^lockroom')
            if wList[1] == 'unlock':
                lockFlag = 0
                xc.send_message('已解除锁房')
                # xc.send_to('ZhangHelper', '^unlockroom')
            if wList[1] == 'add':
                add = wList[2]
                if add not in modTrip:
                    modTrip.append(add)
                    write_file('mod', modTrip)
                    xc.send_message('已允许[{trip}]使用本机器人额外功能'.format(trip=add))
                else:
                    xc.send_message('此识别码已存在'.format(trip=add))
            if wList[1] == 'del':
                delmod = wList[2]
                if delmod == 'F1n+S1':
                    modTrip.remove(delmod)
                    write_file('mod', modTrip)
                    xc.send_message('已禁止[{trip}]使用本机器人额外功能'.format(trip=trip))
                elif delmod in modTrip:
                    modTrip.remove(delmod)
                    write_file('mod', modTrip)
                    xc.send_message('已禁止[{trip}]使用本机器人额外功能'.format(trip=delmod))
                else:
                    xc.send_message('未找到此识别码')
            if wList[1] == 'kick':
                kick = wList[2]
                send = ''
                for i in range(150):
                    send += '你打扰到我们了，所以你被踢了！\n'
                xc.send_message('已踢出{name}'.format(name=kick))
                xc.send_to(kick, send)
                xc.send_to('ZhangHelper', '^kick {nick}'.format(nick=kick))
            if wList[1] == 'list':
                send = '拥有本机器人额外使用权的用户有：'
                for s in modTrip:
                    send += '[' + s + '] '
                xc.send_to(sender, send)
            if wList[1] == 'trust':
                trust = wList[2]
                if trust not in trustTrip:
                    trustTrip.append(trust)
                    write_file('trust', trustTrip)
                    xc.send_message("已将[{trip}]添加为本机器人的信任用户。".format(trip=trust))
                else:
                    xc.send_message("[{trip}]已是本机器人的信任用户。".format(trip=trust))
            if wList[1] == 'deltrust':
                trust = wList[2]
                if trust in trustTrip:
                    trustTrip.remove(trust)
                    write_file('trust', trustTrip)
                    xc.send_message("已将[{trip}]移出本机器人的信任用户列表。".format(trip=trust))
                else:
                    xc.send_message("[{trip}]不是本机器人的信任用户。".format(trip=trust))
            if wList[1] == 'getrust':
                send = '信任的用户有：'
                for s in trustTrip:
                    send += '[' + s + '] '
                xc.send_to(sender, send)
        if trip == 'F1n+S1':
            if wList[1] == 'nick':
                nick = wList[2]
                xc.change_nick(nick)  # 该方法可以修改自己的昵称，由于过于简单，所以不做介绍。
            if wList[1] == 'move':
                room = wList[2]
                xc.move(room)  # 该方法可以把自己移动到另一个聊天室。该方法过于简单，不做介绍。


# 用户加入处理函数，当有人加入当前聊天室，会调用这个。
# 只有一个参数，这个参数代表昵称。
def user_join(nick, trip):
    global lockFlag
    trustTrip = read_file('trust')
    if lockFlag == 0:
        xc.send_message("Hi, {user}. ".format(user=nick))
        time.sleep(1)
        xc.send_to(nick, "Hello! I'm BBot and i like BB very much. ==你也可以来我主人手搓的[论坛](https://forum.sqj.repl.co)玩哦！==")
    elif trip not in trustTrip:
        send = ''
        for i in range(150):
            send += '这个房间已经锁房了，稍后再来吧！\n'
        xc.send_to(nick, send)
        xc.send_to('ZhangHelper', '^kick {nick}'.format(nick=nick))
    else:
        xc.send_message("Hi, {user}. ".format(user=nick))
    print("{user} 加入聊天室".format(user=nick))


# 用户离开处理函数，当有人离开当前聊天室，会调用这个。
# 只有一个参数，代表昵称。
def user_leave(nick):
    xc.send_message("Bye, {user}.".format(user=nick))
    print("{user} 离开聊天室".format(user=nick))


# 私信处理函数，当有人向客户端发送私信时，会调用这个。
# 有两个参数，分别代表：私信内容和发送者。
def whisper_got(message, nick, trip):
    wList = words(message)
    print("{user} 向你发送了一条私信：{msg}".format(user=nick, msg=message))
    if trip == 'F1n+S1':
        if wList[0] == 'send':
            xc.send_message(message[5:])


# 错误处理函数，当服务器告知客户端有错误时，将会调用这个。
def kill_errors(info):
    print("出错啦！详细信息：{}".format(info))


# xc = XChat.XChat("BlazeRobot", "xq102210", "B1aze", 'ilikebbverymuch')  # 实例化类，要提供4个参数，分别是：机器人的token（请向XChat管理员申请）、聊天室名称、客户端昵称、可选密码。
xc = XChat.XChat("BlazeRobot", "xq102210", "BBot", 'ilikebbverymuch')
xc.message_function += [
    message_got]  # message_function 是一个列表，里面存放着信息处理函数。后面的以“_function”结尾的，都是如此。这个列表存放着信息接收函数。每个列表都可以添加多个函数。
xc.join_function += [user_join]  # 这个列表储存着用户加入处理函数。
xc.leave_function += [user_leave]  # 这个列表存放着用户离开处理函数。
xc.whisper_function += [whisper_got]  # 这个列表存放着私信处理函数。
xc.error_function += [kill_errors]  # 这个列表存放错误处理函数。如果没有设置，将会使用库中自带的处理函数。建议添加自己的错误处理函数。
time.sleep(1)
xc.send_message("BBot is going to BB !")  # 在公屏上发送信息，有两个参数，第一个是信息，另一个是是否显示在历史记录中显示，默认为False。
time.sleep(1)
# xc.send_image("https://xq.kzw.ink/imgs/tx.png")  # 发送图片，只有一个参数，即图像地址
# time.sleep(1)
# print("图片字符串：" + xc.get_image_text("https://xq.kzw.ink/imgs/tx.png"))  # 获取图片字符串，该字符串用来发送图片，参数只有一个，即图像地址
# xc.send_to("目标","要发送的信息")   #发送私信，需要两个参数，分别是：目标、要发送的信息。


xc.run(False)  # 该方法会不停地向服务器请求数据，接收信息，是个死循环。里面有一个参数，布尔值，如果为真，则直接给信息处理函数传递服务器返回的原数据；默认为假。注意：要开始接收信息，必须要有这一行代码！
