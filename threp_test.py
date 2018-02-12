from api import THReplay

if __name__ == '__main__':

    # 载入一个replay文件，参数为路径
    tr=THReplay('th6_01.rpy')

    # 获取rep基本信息，包含机体，难度，通关情况，字符串
    # etc. Reimu A normal all
    print(tr.getBaseInfo())

    # 获取rep每个stage的分数，list，包含一串整数
    # etc. [13434600, 50759200, 103025260, 152519820, 230440680, 326777480]
    print(tr.getStageScore())

    # 获取rep的屏幕移动，list，包含一些字符串
    # etc.
    # 其中一个字符串：[0     ]→→→→→→→→→→→→→→→→↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↖↖↖↖↖↖↖↖↖↑↑○○○○○○○○○○○○○○○○○○
    # 开头括号里的数字表示这是在该stage的第几帧，箭头表示方向，圆圈表示不动
    #print(tr.getScreenAction())

    # 获取rep的按键记录，list，包含一些子list，每个子list包含60个字符串，代表一秒
    # etc.
    # 其中一个子list：['→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '→', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑', '↑←', '↑←', '↑←', '↑←', '↑←', '↑←', '↑←', '↑←', '↑←', '↑', '↑', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○', '○']
    # 每个字符串记录了这帧按下的方向键，箭头表示方向，圆圈表示没按
    #print(tr.getKeyboardAction())

    # 获取rep的机签，字符串
    # etc. WASUP
    print(tr.getPlayer())

    # 获取rep的处理落，浮点数
    # etc. 0.03
    print(tr.getSlowRate())

    # 获取rep的时间，字符串
    # etc. 2015/02/17 22:23
    print(tr.getDate())

    #载入一个新的replay文件，参数为路径
    tr.reload_replay("th15_02.rpy")
