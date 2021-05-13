![threp](https://github.com/wasupandceacar/threp/actions/workflows/main.yml/badge.svg)

一、介绍
---------
threp用于解析东方project系列游戏的replay文件，即游戏回放文件，可以获取replay文件的通关情况，机师，难度，通关情况，机体，处理落，日期，屏幕移动，按键记录。
支持TH06-18整数作以及TH9.5、12.5、TH12.8、TH14.3、TH16.5（即现有所有非黑历史的东方STG全部支持）。

二、安装方法
-------------
在 Python 3.6+ 下使用，用 pip 安装：

    pip install threp

三、使用方法
-------------

	from threp import THReplay
 
    # 载入一个replay文件，参数为路径
    tr=THReplay('th14_03.rpy')

    # 获取rep基本信息，包含机体，难度，通关情况，字符串
    # etc. Reimu A normal all
    print(tr.getBaseInfo())

    # 获取rep基本信息的字典，包含机体，难度，通关情况，字符串
    # 字典的键分别为 character shottype rank stage
    # etc. Reimu A Normal All
    print(tr.getBaseInfoDic())

    # 获取rep每个stage的分数，list，包含一串整数
    # etc. [13434600, 50759200, 103025260, 152519820, 230440680, 326777480]
    print(tr.getStageScore())

    # 获取rep的屏幕移动，list，包含一些字符串
    # etc.
    # 其中一个字符串：[0     ]→→→→→→→→→→→→→→→→↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↖↖↖↖↖↖↖↖↖↑↑○○○○○○○○○○○○○○○○○○
    # 开头括号里的数字表示这是在该stage的第几帧，箭头表示方向，圆圈表示不动
    print(tr.getScreenAction())

    # 获取rep的按键记录，list，包含一些子list，每个子list包含60个字符串，代表一秒
    # etc.
    # 其中一个子list：['→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑←', '↑←', '↑←', '↑←', '↑←', '↑←', '↑←', '↑←', '↑←', '↑', '↑', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○']
    # 每个字符串记录了这帧按下的方向键，箭头表示方向，圆圈表示没按
    print(tr.getKeyboardAction())

    # 获取rep的机签，字符串
    # etc. WASUP
    print(tr.getPlayer())

    # 获取rep的处理落，浮点数
    # etc. 0.03
    print(tr.getSlowRate())

    # 获取rep的时间，字符串
    # etc. 2015/02/17 22:23
    print(tr.getDate())

    # 获取解析错误信息，list，包含一些字典
    # etc. 共有三种错误
    # 1.length so short error，单面长度过短错误
    # 2.frame read error，单面帧数读取错误
    # 3.length read error，单面长度读取错误
    print(tr.getError())

    # 获取rep的总帧数，整数
    # etc. 84565
    print(tr.getFrameCount())

    # 获取rep中按下Z键的帧数的list，帧数从1开始数
    # etc. [63, 98, 136]
    print(tr.getZ())

    # 获取rep中按下X键的帧数的list，帧数从1开始数
    # etc. [193, 480, 766]
    print(tr.getX())

    # 获取rep中按下C键的帧数的list，帧数从1开始数，这个按键从TH128开始记录，TH125及以前无记录
    # etc. [1046, 1260]
    print(tr.getC())

    # 获取rep中按下Shift键的帧数的list，帧数从1开始数
    # etc. [1495, 1532, 1568]
    print(tr.getShift())

    #载入一个新的replay文件，参数为路径
    tr.reload_replay("th15_02.rpy")
