from pykeyboard import *
from pymouse import *
import time
import pyautogui as pg
import sys
#左右技能升级
skill_left = list()
skill_right = list()
sell = list()

#函数功能 封装基本操作
def MyClick(xy):
    mouse.click(xy[0],xy[1])
    time.sleep(0.7)
def MyMove(xy):
    mouse.move(xy[0],xy[1])
    time.sleep(0.8)

def MyHoldKey(key,ti):
    start = time.time()
    while True:
        kb.press_key(key)
        if time.time() - start > ti:
            break
    kb.release_key(key)
    time.sleep(0.5)
    return

def altf4():
    pg.hotkey('alt','f4')
    print("alt f4")
    return

#快捷键建造
def build_unit(unit_key,build_xy):
    MyMove(build_xy)
    MyHoldKey(unit_key,0.3)
    MyClick(build_xy)
    return

def build_unit2(unit_xy,build_xy):
    MyClick(unit_xy)
    MyClick(build_xy)
    return
#技能升级 state为x-x-x posi为升级栏位置是左还是右
def skill_up(unit_xy,state,posi):
    MyClick(unit_xy)
    skill_posi = list()
    if posi == 'left':
        skill_posi = skill_left.copy()
    elif posi == 'right':
        skill_posi = skill_right.copy()
    print("技能位置",skill_posi)
    for i in range(3):
        for j in range(state[i]):
            MyClick(skill_posi[i])
    return
#变卖
def sell_unit(unit_xy,posi):
    #暂时只有左出售
    MyClick(unit_xy)
    time.sleep(1)
    MyClick(sell)
    time.sleep(0.5)
    return

#函数功能 将所需要的坐标读入保存成字典
def read_data():
    data = {}
    data_path = r"./bloons.txt"
    file =  open(data_path,'r',encoding='utf-8')
    while True:
        content =  file.readline()
        if not content:
            break
        ct = content.split()
        xy = [int(ct[1]),int(ct[2])]
        # 分辨率转换
        data[ct[0]] = xy
    return data

# 进入到地图
def go_to_map(coordinate):
    sequence = ['开始', '专家', '下一页', '城堡', '简单', '放气']  # 执行序列
    for item in sequence:
        MyClick(coordinate[item])
    time.sleep(6)
    MyClick(coordinate['好的'])
    return

def run_game(coordinate):
    wait = 0
    click_time = 0
    time.sleep(3)
    while click_time < 10:
        time.sleep(1)
        wait += 1 #等待时钟
        if wait % 5 == 0: #5秒检查一次
            target = (1850,995)
            game_done = (29,59,0)
            quick_game = (176,245,0)
            while True:
                pix = pg.screenshot().getpixel(target)
                if pix == game_done:
                    click_time = 100 #退出标记
                    time.sleep(4)
                    MyClick(coordinate['下页'])
                    time.sleep(2)
                    MyClick(coordinate['主页'])
                    print("正常退出")
                    break
                elif pix != quick_game:
                    print(pix)
                    MyClick(target)
                    time.sleep(1)
                    click_time +=1
                    if click_time > 10:
                        print("10次退出")
                        break
                else:
                    break
    print("done")
#进入游戏
#准备猴子 造塔
def prepare(coordinate):
    shortcut = {'村子': 'k', '魔法猴': 'a', '昆西': 'u', '炼金': 'f', '潜艇': 'x'}  # 类型快捷键
    build_unit(shortcut['村子'], coordinate['村子1'])
    skill_up(coordinate['村子1'], [0, 0, 2], 'left')
    build_unit(shortcut['村子'], coordinate['村子2'])
    skill_up(coordinate['村子2'], [1, 0, 2], 'left')
    build_unit(shortcut['潜艇'], coordinate['潜艇1'])
    skill_up(coordinate['潜艇1'], [2, 0, 4], 'left')
    build_unit(shortcut['潜艇'], coordinate['潜艇2'])
    skill_up(coordinate['潜艇2'], [2, 0, 4], 'left')
    build_unit(shortcut['昆西'], coordinate['昆西'])
    build_unit(shortcut['魔法猴'], coordinate['魔法猴'])
    skill_up(coordinate['魔法猴'], [0, 2, 3], 'right')
    MyClick((850, 854))  # 随意点击 让左侧升级
    sell_unit(coordinate['村子2'], 'left')
    build_unit(shortcut['炼金'], coordinate['炼金'])
    skill_up(coordinate['炼金'], [4, 0, 1], 'left')
    print("准备开始")

def start_game(coordinate):
    #技能位置初始化
    global skill_left,skill_right
    skill_left.extend([coordinate['左一升级'],coordinate['左二升级'],coordinate['左三升级']])
    skill_right.extend([coordinate['右一升级'],coordinate['右二升级'],coordinate['右三升级']])
    global sell
    sell = coordinate['左出售']
    go_to_map(coordinate)
    #地图开始战斗界面
    prepare(coordinate)
    print("准备开始")
    run_game(coordinate)
    print("退出界面")
    time.sleep(2)
    print('结束')

#逻辑死亡判断
def dead_judge(coordinate):
    #没有回到标准流程上重启下程序
    time.sleep(3)
    tmp = (844,799)
    pix = pg.screenshot().getpixel(tmp)
    dead = False
    if pix != (250,227,154):
        #关闭软件
        altf4()
        #等待程序结束
        time.sleep(10)
        MyClick(coordinate['外开始'])
        tmp2 = (1055,984)
        while pix != (105,221,0):
            pix = pg.screenshot().getpixel(tmp2)
            print("wait")
            time.sleep(1)
        MyClick(coordinate['界面开始'])
        tmp3 = (844, 799)
        while pix != (250, 227, 154):
            pix = pg.screenshot().getpixel(tmp3)
            print("wait to start")
            time.sleep(1)
        time.sleep(4)
    print("准备完毕")
    return





if __name__ == '__main__':
    mouse = PyMouse()
    kb = PyKeyboard()
    time.sleep(3)
    coordinate = read_data() #初始化坐标
    print("坐标初始化成功")
    #设置循环次数
    loop_times = 100
    for i in range(loop_times):
        #start_game(coordinate)
        dead_judge(coordinate)
