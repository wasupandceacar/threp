![build](https://github.com/wasupandceacar/threp/actions/workflows/build.yml/badge.svg)

![pypi](https://github.com/wasupandceacar/threp/actions/workflows/pypi.yml/badge.svg)

![CodeFactor](https://www.codefactor.io/repository/github/wasupandceacar/threp/badge)

一、介绍
---------
threp 用于解析东方 project 系列游戏的 replay 文件，即游戏回放文件，可以获取 replay 文件的通关情况、机师、难度、通关情况、机体、处理落、日期、屏幕移动、按键记录。
支持 TH06-18 整数作以及 TH9.5、12.5、TH12.8、TH14.3、TH16.5（即现有所有非黑历史的东方 STG 全部支持）。

二、安装方法
-------------
在 Python **3.6+** 下使用，用 pip 安装：

    pip install threp

三、使用方法
-------------

	from threp import THReplay
 
    # 载入一个 replay 文件，参数为路径
    tr = THReplay('th14_03.rpy')

    # 获取 replay 基本信息，包含机体，难度，通关情况，字符串
    # etc. Reimu A normal all
    print(tr.getBaseInfo())

    # 获取 replay 基本信息的字典，包含机体，难度，通关情况，字符串
    # 字典的键分别为 character、shottype、rank、stage
    # etc. Reimu A Normal All
    print(tr.getBaseInfoDic())

    # 获取 replay 每个 stage 的分数，list，包含一串整数
    # etc. [13434600, 50759200, 103025260, 152519820, 230440680, 326777480]
    print(tr.getStageScore())

    # 获取 replay 的屏幕移动，list，包含一些字符串
    # etc.
    # 其中一个字符串：[0     ]→→→→→→→→→→→→→→→→↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↖↖↖↖↖↖↖↖↖↑↑○○○○○○○○○○○○○○○○○○
    # 开头括号里的数字表示这是在该 stage 的第几帧，箭头表示方向，圆圈表示不动
    print(tr.getScreenAction())

    # 获取 replay 的按键记录，list，包含一些子 list，每个子 list 包含 60 个字符串，代表一秒
    # etc.
    # 其中一个子 list：['→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑←', '↑←', '↑←', '↑←', '↑←', '↑←', '↑←', '↑←', '↑←', '↑', '↑', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○']
    # 每个字符串记录了这帧按下的方向键，箭头表示方向，圆圈表示没按
    print(tr.getKeyboardAction())

    # 获取 replay 的机签，字符串
    # etc. WASUP
    print(tr.getPlayer())

    # 获取 replay 的处理落，浮点数
    # etc. 0.03
    print(tr.getSlowRate())

    # 获取 replay 的时间，字符串
    # etc. 2015/02/17 22:23
    print(tr.getDate())

    # 获取解析错误信息，list，包含一些字典
    # 共有三种错误
    # 1.length so short error，单面长度过短错误
    # 2.frame read error，单面帧数读取错误
    # 3.length read error，单面长度读取错误
    print(tr.getError())

    # 获取 replay 的总帧数，整数
    # etc. 84565
    print(tr.getFrameCount())

    # 获取 replay 中按下 Z 键的帧数的 list，帧数从 1 开始数
    # etc. [63, 98, 136]
    print(tr.getZ())

    # 获取 replay 中按下 X 键的帧数的 list，帧数从 1 开始数
    # etc. [193, 480, 766]
    print(tr.getX())

    # 获取 replay 中按下 C 键的帧数的 list，帧数从 1 开始数，这个按键从TH128开始记录，TH125及以前无记录
    # etc. [1046, 1260]
    print(tr.getC())

    # 获取 replay 中按下 Shift 键的帧数的 list，帧数从 1 开始数
    # etc. [1495, 1532, 1568]
    print(tr.getShift())
