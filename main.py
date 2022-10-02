#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 远方的开发者，您好！这是一个XChat的测试机器人，使用Python编写。这里面提供了一些实例，供您参考！
import XChat  # 引入模块
import time, random  # 引入模块
import _thread as thread
import datetime
import os, sys
import traceback


def print_text():
    while True:
        time.sleep(1)
        # print(str(datetime.datetime.now()))
        if str(datetime.datetime.now())[17:19] == '00':
            signList = read_file('sign')
            for i in range(len(signList)):
                signList[i] = '0'
                # print(signList)
            write_file('sign', signList)
        if str(datetime.datetime.now())[14:19] == '00:00':
            nameList = read_file('name')
            moneyList = read_file('money')
            hour = int(str(datetime.datetime.now())[11:13])
            xc.send_message("""
            定点报时：现在是北京时间{hour}点整！
            
            欢迎前往我主人的论坛：https://forum.sqj.repl.co/
            也欢迎来我主人的mc服务器：https://mc.sqj.repl.co/
            
            此外，我还要随机抽取一位幸运观众奖励100个BB币，~~然后踢出。~~
            """.format(hour=hour))
            num = random.randint(0, len(nameList) - 1)
            kick = nameList[num]
            moneyList[num] = str(eval(moneyList[num]) + 100)
            write_file('money', moneyList)
            xc.send_message('这位幸运观众就是{name}!\n@{name} 100个BB币已经汇到你的账户上了'.format(name=kick))
            xc.send_message('^kick {name}'.format(name=kick))


thread.start_new_thread(print_text, ())

lockFlag = 0


def read_file(file):
    f = open(file, 'r')
    List = f.readlines()
    f.close()
    for i in range(len(List)):
        List[i] = List[i].strip('\n')
    for s in List:
        if s == '':
            List.remove(s)
    return List


def write_file(file, List):
    for i in range(len(List)):
        List[i] += '\n'
    f = open(file, "w")
    f.writelines(List)
    for i in range(len(List)):
        List[i] = List[i].strip('\n')


def words(txt):
    wList = []
    word = ''
    for c in txt:
        if (c == ' ') + (c == '@') == 0:
            word += c
        elif word != '':
            wList.append(word)
            word = ''
    if word != '':
        wList.append(word)
    return wList


# 信息接收处理函数，当有人在公屏上发送信息时，会调用这个。
# 两个参数分别代表：信息内容和发送者。
def message_got(message, sender, trip, online, w=False):
    for s in online:
        if s[-2:] == '挂机':
            online.remove(s)
    history = read_file('history')
    nameList = read_file('name')
    moneyList = read_file('money')
    levelList = read_file('level')
    signList = read_file('sign')
    if sender not in nameList:
        nameList.append(sender)
        moneyList.append('0')
        signList.append('0')
        levelList.append('0')
        write_file('name', nameList)
        write_file('money', moneyList)
        write_file('sign', signList)
        write_file('level', levelList)
    for a in range(len(moneyList) - 1):
        flag = 0
        for i in range(len(moneyList) - 1 - a):
            if eval(moneyList[i]) < eval(moneyList[i + 1]):
                moneyList[i], moneyList[i + 1] = moneyList[i + 1], moneyList[i]
                nameList[i], nameList[i + 1] = nameList[i + 1], nameList[i]
                signList[i], signList[i + 1] = signList[i + 1], signList[i]
                levelList[i], levelList[i + 1] = levelList[i + 1], levelList[i]
                flag = 1
        if flag == 0:
            break
    write_file('name', nameList)
    write_file('money', moneyList)
    write_file('sign', signList)
    write_file('level', levelList)
    global lockFlag
    if not w: print('收到 [{trip}]{who} 在公屏上发送的信息：{msg}'.format(who=sender, msg=message, trip=trip))
    if not w: history.append('收到 [{trip}]{who} 在公屏上发送的信息：{msg}'.format(who=sender, msg=message, trip=trip))
    write_file('history', history)
    wList = words(message)
    modTrip = read_file('mod')
    trustTrip = read_file('trust')
    protectList = read_file('protect')
    bbi = read_file('bbi')

    if message[0:4] == '.bb ':
        num = nameList.index(sender)
        if wList[1] == 'help':
            xc.send_to(sender, """下列指令可以使用：
            -----User-----
            1、.bb help：获取帮助
            2、.bb shoot <name>: 花5个BB币向<name>射击
            3、.bb hug <name>: 抱抱<name>
            4、.bb cookie <name>: 给<name>曲奇饼干
            5、.bb roll: 生成1～1000的随机数
            6、.bb join: 加入BBI警卫队
            7、.bb quit: 退出BBI警卫队
            8、.bb bbi: 查看BBI警卫队的成员
            9、/w BBot shoot <name>: 花1个BB币向<name>射箭
            10、.bb readme: 聊天室使用守则
            11、.bb online: 查看在线用户
            12、.bb rkick <name>: 有65%的可能自己被踢，30%的可能<name>被踢，5%的可能在线用户中的随机一人被踢
            13、.bb money: 查看自己的资产
            14、.bb sign: 每分钟签到领取10个BB币
            15、.bb send <name> <money>: 送给<name><money>个BB币
            16、.bb most：查看福布斯富豪榜
            17、.bb level: 查看自己的等级
            18、.bb update: 花费$2^{level}$个BB币升级
            ----Trust ----
            1、.bb protect <name>: 派出BBI保护<name>免受枪击
            2、.bb cancel <name>: 取消BBI对<name>的保护
            3、.bb protectlist: 查看BBI的保护列表
            4、.bb lockflag: 查看锁房状态
            5、.bb fire <name>: 将某人开除出BBI
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
            3、/w BBot send <text>: 让机器人发送<text>
            4、.bb give <name> <money>: 给予<name><money>个BB币""")
        if wList[1] == 'level':
            level = levelList[num]
            xc.send_to(sender, '你的等级为{level}级'.format(level=level))
        if wList[1] == 'update':
            level = int(levelList[num])
            if eval(moneyList[num]) >= 2 ** level:
                moneyList[num] = str(eval(moneyList[num]) - 2 ** level)
                levelList[num] = str(int(levelList[num]) + 1)
                write_file('money', moneyList)
                write_file('level', levelList)
                xc.send_message('@{name} 你的等级已经升级到了{level}级'.format(name=sender, level=levelList[num]))
            else:
                xc.send_message('余额不足')
        if wList[1] == 'most':
            send = '|名次|名字|BB币数量|等级|\n|----|-------------------------|-------------|-----|\n'
            for i in range(5):
                send += '|No.' + str(i + 1) + '|' + nameList[i] + '|' + moneyList[i] + '|' + levelList[i] + '|\n'
            if not w:
                xc.send_message(send)
            else:
                xc.send_to(sender, send)
        if wList[1] == 'send':
            name = wList[2]
            money = abs(eval(wList[3]))
            if name not in nameList:
                xc.send_message('未找到此用户')
            else:
                if eval(moneyList[num]) >= money:
                    moneyList[num] = str(eval(moneyList[num]) - money)
                    moneyList[nameList.index(name)] = str(eval(moneyList[nameList.index(name)]) + money)
                    if not w:
                        xc.send_message('{nick}赠送{money}个BB币给了{name}'.format(nick=sender, money=money, name=name))
                    else:
                        xc.send_to(sender,
                                   '{nick}赠送{money}个BB币给了{name}'.format(nick=sender, money=money, name=name))
                    write_file('money', moneyList)
                else:
                    if not w:
                        xc.send_message('余额不足')
                    else:
                        xc.send_to(sender, '余额不足')
        if wList[1] == 'sign':
            if signList[num] == '0':
                signList[num] = '1'
                money = 10 * int(levelList[num])
                moneyList[num] = str(eval(moneyList[num]) + money)
                write_file('money', moneyList)
                write_file('sign', signList)
                if not w:
                    xc.send_message('@{name} 签到成功，你获得了{money}个BB币。'.format(name=sender, money=money))
                else:
                    xc.send_to(sender, '@{name} 签到成功，你获得了{money}个BB币。'.format(name=sender, money=money))
            else:
                if not w:
                    xc.send_message('@{name} 你已经签到过了'.format(name=sender))
                else:
                    xc.send_to(sender, '@{name} 你已经签到过了'.format(name=sender))
        if wList[1] == 'money':
            # print(nameList, sender)
            money = moneyList[num]
            xc.send_to(sender, '您的现有资产为{money}个BB币。'.format(money=money))
        if wList[1] == 'readme':
            xc.send_to(sender, '''.
# XChat帮助文件（版本：2.21）
###### 更新日期：北京时间 2022-7-25 凌晨
## 前言  
XChat，是一款由Hack.Chat改变的聊天平台，由线圈团队编写。它有着艰辛的发展历程。为推动XChat发展，Mr_Zhang特意编写了本帮助文件，希望诸位用户能细细阅读。
###### 小提示：某些人只会胡乱贬低XChat，请不要相信他们。
## 基本教程
### 识别码
#### 介绍
识别码是一个六位的“乱码”，位于头像左侧，由你的密码生成，可以有效让其他用户识别是否是你本人。
#### 使用方法
1. 刷新网页；
2. 在昵称输入框中按照`昵称#密码`的格式填写，如`Test#123456`。
3. 点击确定或者按下回车，进入XChat。
4. 在这个例子中，`123456`就是密码，`QTCCbB`是其对应的识别码。
###### 小提示：一个密码只对应一个识别码。请确保你的密码足够特殊，让别人猜不到你的密码，不能冒充你。
###### 一般用户的识别码都是六位，站长的识别码一般是`Admin`。某些用户拥有特殊的识别码（例如笔者的识别码是`zhang`），那是站长替换的。
### 机器人（bot）
#### 介绍
机器人，简称bot，是由其他开发者开发的，可以服务于大家，也可以活跃聊天气氛。机器人开发者可以通过机器人后台控制机器人发送信息。
#### 机器人列表
截至北京时间 2022-7-25 凌晨，机器人有：`BBot`、`eebot`、`SuMx_bot`、`Zhang系列Bot`（昵称以`Zhang`开头）、`dotbot`、`zzBot`（常用昵称为`zzChumo`；有时是真人，有时是机器人）、`AfK_Bot`、`ModBot`、`ABot` 等等。
###### 小提示：开发机器人需要向XChat管理员申请token来让机器人跳过验证码。
### 发送图片
#### 介绍
给大家发送一张图片
#### 使用方法
1. 把要发送的图片上传到图片托管网站（图床）。
2. 复制图片托管网站提供的图片URL。
3. 回到XChat，按照`![](图片URL)`的格式发送信息。
### 设置头像
#### 介绍
头像可以让别人更快速地产生对你的第一印象，选择一个好看的头像可以在一定程度上改善别人对你的印象。
#### 使用方法
1. 把头像图片上传到图片托管网站（图床）。
2. 复制图片托管网站提供的图片URL。
3. 回到XChat，在侧边栏里点击`设置头像`按钮，在弹出来的输入框中粘贴图片URL，并点击确定或按下回车。
###### 小提示：请勿盗用他人头像。
### 设置背景
#### 介绍
设置背景图片，只有你自己看得到。
#### 使用方法
1. 把背景图片上传到图片托管网站（图床）。
2. 复制图片托管网站提供的图片URL。
3. 回到XChat，在侧边栏里点击`设置背景`按钮，在弹出来的输入框中粘贴图片URL，并点击确定或按下回车。
### 一起看视频
#### 介绍
一起看视频，顾名思义，即在聊天室内观看视频，而且可以保证所有人的进度和视频播放者进度相同。属于XChat的特色功能。
#### 使用方法
1. 在侧边栏里点击`一起看视频！`按钮，即可观看视频。
###### 小提示：视频可能会失效，所以不是任何时候都能看视频。如需设置视频，可以联系XChat管理员。
### 连接到HC服务器
#### 介绍
该功能可以让你同时加入HackChat聊天室。是XChat的特色功能。
#### 使用方法
1. 在侧边栏里勾选`连接HC服务器`。
2. 重新进入XChat。
3. 把信息发送到HackChat，只需要给你要发送的信息加上前缀`hc-`即可。
#### 备注
1. 如果你在XChat里的`?xq102210`，那么在HackChat的`?your-channel`里，会有一名叫做`XC_你的昵称`的用户。
2. 当HackChat用户发信息的时候，你会在XChat看到以`HC_`开头的用户，那是HackChat内部的用户。
###### 小提示：除了XChat内的`?xq102210`聊天室，其他聊天室都会镜像连接到HackChat。例如在XChat内的`?test`，相应的，你也会加入HackChat的`?test`聊天室。
### 发送语音
#### 介绍
该功能可以让你在聊天室内发送语音信息，属于XChat特色功能。
#### 使用方法
1. 点击聊天框左侧的`发送语音`按钮（可能会弹出权限申请界面，请同意权限申请）。
2. 要结束录音并发送，可以点击`结束录音`按钮。
###### 小提示：录音最长时间为60秒，超时后会自动结束录音并发送。XChat提供文字聊天室和语音聊天室，即只能发送文字的聊天室和只能发送语音的聊天室。以`TEXT_`开头的是文字聊天室，以`VOICE_`开头的是语音聊天室（区分大小写）。
### 挂机（afk）
#### 介绍
该功能可以在你离开聊天室后为你预留当前的昵称，可以有效防止被他人冒充
#### 使用方法
1. 在聊天室内发送 `afk`
2. 自己进入了挂机状态
### 房主制度
#### 介绍
第一个进入非公共聊天室的用户为房主，可以执行某些操作
#### 使用方法
- 设置视频：您可以发送 `/video 视频链接` 来设置一个一起看的视频
- 强制某人下线：您可以发送 `/offline 目标昵称` 来强制一个用户下线
- 聊天室内喊话：您可以发送 `/channelshout 文本` 来让一个信息显示在聊天室内所有用户的屏幕上
### 直播
#### 介绍
该功能可以将你的麦克风接收到的声音实时传输给收听直播的用户，属于XChat特色功能。
#### 使用方法
##### 收听直播
1. 点击侧边栏里面的“收听直播”按钮即可收听直播。
2. 若要停止收听，请刷新网页。
##### 发起直播
1. 请向管理员申请直播权限。
2. 点击侧边栏里面的“我来直播！”按钮即可发起直播。
3. 若要停止直播，请刷新网页。
### 创建个人聊天室
#### 介绍
创建一个新的个人聊天室
#### 使用方法
1. 把网址`https://xq.kzw.ink/?xq102210`中的半角问号后更改为你要创建的聊天室的名称，即可创建。例如`https://xq.kzw.ink/?test`
### 私聊
#### 介绍
偷偷地给某人发送信息，只有你和对方能看到。
#### 使用方法
1. 在聊天室按照`/w 对方的昵称 要发送的信息`的格式发送信息即可发送私聊。例如`/w 小明 你好！`就是把内容为`你好`的信息发送给用户`小明`。
###### 小提示: 当有人向你发送私聊时, 你只需要发送`/r 要发送的信息`即可快速回复。
## 高风险行为
### 禁止
1. 乱刷屏（包括发长信息之前没有提醒以及滥用LaTeX和MarkDown）
2. 随意辱骂某人
3. 轰炸某人
4. 发送大量无意义的信息
5. 非网络原因进进出出
6. 网络攻击XChat
7. 发送任何违反中华人民共和国相关法律的内容
8. 诋毁线圈团队以及XChat（不包括提出问题和建议）
9. 盗用他人昵称（包括机器人）（除非他人允许）
10. 使用令人反感或有特殊含义的昵称
11. 发送令人反感的内容
12. 过度使用机器人（如果要玩机器人，可以去 ?bot ，随后联系机器人开发者把机器人搬到 ?bot ）
13. 盗用他人头像（网图除外，鼓励使用个性化头像，但不要令人反感的）
14. 在违规的边界线上跳来跳去
15. 未经他人允许询问他人真实信息
16. 未经管理员允许放置机器人

### 不建议（在某些情况下，可能会被管理员当作违规处理）
1. 使用看上去像机器人的昵称（这可能会导致管理员误判断为非法机器人，从而导致不必要的损失）
2. 发送长信息之前没有提醒，或屡次在公共聊天室内发送过长的信息
3. 胡言乱语
4. 过度打广告（即：每小时打广告次数超过3次）

###### 小提示：人少不是违规的的理由！！！
==如果违反以上规定，可能会受到踢出聊天室/禁言/封禁处罚==

## 结束语
我们希望此帮助对您有帮助，如有疑问，请联系XChat用户Mr_Zhang。
感谢您的阅读，祝您聊天愉快！
---
感谢有你，陪伴着 XChat 走过风风雨雨；感谢有你，激励着 XChat 不断前进；感谢有你，信任我们。
发展路上，感谢有你。''')
        if wList[1] == 'online':
            send = '在线用户有：'
            for s in online:
                send += s + '，'
            xc.send_to(sender, send[:-1])
        if wList[1] == 'shoot' and '&#8238;' not in message:
            if eval(moneyList[num]) >= 5:
                shoot = message[10:]
                moneyList[num] = str(eval(moneyList[num]) - 5)
                write_file('money', moneyList)
                shootList = ['打断了Ta的膝盖', '打穿了Ta的胸膛', '打爆了Ta的头盖骨', '但是没打中']
                if shoot not in protectList:
                    if shoot == 'BBot':
                        shoot = 'Ta自己'
                    xc.send_message("{user}向{shoot}开了一枪，{how}".format(user=sender, shoot=shoot,
                                                                           how=shootList[random.randint(0, 3)]))
                else:
                    xc.send_message("{user}向{shoot}开了一枪，但是被BBI的{name}拦截了。".format(user=sender, shoot=shoot,
                                                                                              name=bbi[random.randint(0,
                                                                                                                      len(bbi) - 1)]))
            else:
                xc.send_message('余额不足')
        if wList[1] == 'hug':
            hug = message[8:]
            xc.send_message('{user}给了{hug}一个抱抱'.format(user=sender, hug=hug))
        if wList[1] == 'cookie':
            cookie = message[11:]
            xc.send_message('{user}给了{cookie}一个曲奇饼干'.format(user=sender, cookie=cookie))
        if wList[1] == 'roll':
            xc.send_message('{user} roll出了{roll}'.format(user=sender, roll=random.randint(1, 1000)))
        if wList[1] == 'join':
            if sender not in bbi:
                bbi.append(sender)
                write_file('bbi', bbi)
                xc.send_message("{name}加入了BBI警卫队".format(name=sender))
                xc.send_to(sender, "你收到了BBI警卫队发来的100个BB币")
                moneyList[num] = str(int(moneyList[num]) + 100)
                write_file('money', moneyList)
            else:
                xc.send_message("@{name} 你已是BBI警卫队的成员。".format(name=sender))
        if wList[1] == 'quit':
            if sender in bbi:
                bbi.remove(sender)
                write_file('bbi', bbi)
                xc.send_message("{name}退出了BBI警卫队".format(name=sender))
                xc.send_to(sender, "你被扣除100个BB币")
                moneyList[num] = str(int(moneyList[num]) - 100)
                write_file('money', moneyList)
            else:
                xc.send_message("@{name} 你不是BBI警卫队的成员。".format(name=sender))
        if wList[1] == 'bbi':
            send = 'BBI警卫队的成员有：'
            for s in bbi:
                send += s + '，'
            xc.send_to(sender, send[:-1])
        if wList[1] == 'rkick':
            name = message[10:]
            roll = random.randint(1, 100)
            if roll <= 65:
                xc.send_message('^kick {nick}'.format(nick=sender))
            elif roll <= 95:
                xc.send_message('^kick {nick}'.format(nick=name))
            else:
                xc.send_message('^kick {nick}'.format(nick=online[random.randint(0, len(online) - 1)]))
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
                    send += s + '，'
                xc.send_to(sender, send[:-1])
            if wList[1] == 'lockflag':
                if lockFlag:
                    if not w:
                        xc.send_message('锁房状态为：开启锁房')
                    else:
                        xc.send_to(sender, '锁房状态为：开启锁房')
                else:
                    if not w:
                        xc.send_message('锁房状态为：关闭锁房')
                    else:
                        xc.send_to(sender, '锁房状态为：关闭锁房')
            if wList[1] == 'fire':
                name = wList[2]
                if name not in bbi:
                    xc.send_message('未找到此BBI警卫员')
                else:
                    bbi.remove(name)
                    write_file('bbi', bbi)
                    xc.send_message("{name}被{mod}炒了".format(name=name, mod=sender))
                    xc.send_to(name, "你被扣除150个BB币")
                    moneyList[nameList.index(name)] = str(eval(moneyList[nameList.index(name)]) - 150)
                    write_file('money', moneyList)
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
                kick = message[9:]
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
            if wList[1] == 'give':
                name = wList[2]
                money = wList[3]
                # print(moneyList[nameList.index(name)], money, name)
                if name not in nameList:
                    xc.send_message('未找到此用户')
                else:
                    moneyList[nameList.index(name)] = str(eval(moneyList[nameList.index(name)]) + eval(money))
                    xc.send_message(
                        '@{name} 你收到了我主人发来的{money}个BB币。==输入`.bb money`查看现有资产=='.format(name=name,
                                                                                                           money=money))
                    write_file('money', moneyList)


# 用户加入处理函数，当有人加入当前聊天室，会调用这个。
# 只有一个参数，这个参数代表昵称。
def user_join(nick, trip):
    history = read_file('history')
    global lockFlag
    trustTrip = read_file('trust')
    if lockFlag == 0:
        xc.send_message("Hi, {user}. ".format(user=nick))
        time.sleep(1)
        xc.send_to(nick,
                   "Hello! I'm BBot and i like BB very much. 发送`.bb help`查看帮助。==你也可以来我主人手搓的[论坛](https://forum.sqj.repl.co)玩哦！==")
    elif trip not in trustTrip:
        send = ''
        for i in range(150):
            send += '这个房间已经锁房了，稍后再来吧！\n'
        xc.send_to(nick, send)
        xc.send_to('ZhangHelper', '^kick {nick}'.format(nick=nick))
    else:
        xc.send_message("Hi, {user}. ".format(user=nick))
    print("{user} 加入聊天室".format(user=nick))
    history.append("{user} 加入聊天室".format(user=nick))
    write_file('history', history)


# 用户离开处理函数，当有人离开当前聊天室，会调用这个。
# 只有一个参数，代表昵称。
def user_leave(nick):
    history = read_file('history')
    xc.send_message("Bye, {user}.".format(user=nick))
    print("{user} 离开聊天室".format(user=nick))
    history.append("{user} 离开聊天室".format(user=nick))
    write_file('history', history)


# 私信处理函数，当有人向客户端发送私信时，会调用这个。
# 有两个参数，分别代表：私信内容和发送者。
def whisper_got(message, nick, trip):
    history = read_file('history')
    wList = words(message)
    protectList = read_file('protect')
    bbi = read_file('bbi')
    moneyList = read_file('money')
    nameList = read_file('name')
    print("{user} 向你发送了一条私信：{msg}".format(user=nick, msg=message))
    history.append("{user} 向你发送了一条私信：{msg}".format(user=nick, msg=message))
    write_file('history', history)
    if trip == 'F1n+S1':
        if wList[0] == 'send':
            xc.send_message(message[5:])
    if wList[0] == 'shoot' and '&#8238;' not in message:
        shoot = message[6:]
        if nick in nameList:
            if int(moneyList[nameList.index(nick)]) >= 1:
                moneyList[nameList.index(nick)] = str(eval(moneyList[nameList.index(nick)]) - 1)
                write_file('money', moneyList)
                shootList = ['射中了Ta的膝盖', '射穿了Ta的胸膛', '射中了Ta的头盖骨', '但是没射中']
                if shoot not in protectList:
                    if shoot == 'BBot':
                        shoot = 'Ta自己'
                    xc.send_message(
                        "{user}向{shoot}射了一箭，{how}".format(user=nick, shoot=shoot,
                                                               how=shootList[random.randint(0, 3)]))
                else:
                    xc.send_message("{user}向{shoot}射了一箭，但是被BBI的{name}拦截了。".format(user=nick, shoot=shoot,
                                                                                              name=bbi[random.randint(0,
                                                                                                                      len(bbi) - 1)]))
            else:
                xc.send_message('余额不足')
    else:
        message_got(message, nick, trip, xc.online_users, True)


# 错误处理函数，当服务器告知客户端有错误时，将会调用这个。
def kill_errors(info):
    print("出错啦！详细信息：{}".format(info))


# xc = XChat.XChat("BlazeRobot", "xq102210", "B1aze", 'ilikebbverymuch')  # 实例化类，要提供4个参数，分别是：机器人的token（请向XChat管理员申请）、聊天室名称、客户端昵称、可选密码。
xc = XChat.XChat("BlazeRobot", "bot", "BBot", 'ilikebbverymuch')
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

try:
    xc.run(False)  # 该方法会不停地向服务器请求数据，接收信息，是个死循环。里面有一个参数，布尔值，如果为真，则直接给信息处理函数传递服务器返回的原数据；默认为假。注意：要开始接收信息，必须要有这一行代码！
except:
    print('机器人运行时一下异常：\n' + traceback.format_exc() + '\n现在重启！')
    py = sys.executable
    os.execl(py, py, *sys.argv)
    os._exit(0)
