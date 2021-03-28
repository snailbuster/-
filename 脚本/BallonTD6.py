#气球塔防挂机脚本v1.01版本
from pykeyboard import *
from pymouse import *
import time
import pyautogui as pg

skill1,skill2,skill3 = tuple(),tuple(),tuple()
#设置分辨率
resolution = (1920,1080)
rate = (resolution[0]/2560,resolution[1]/1440)

def MyClick(xy):
    mouse.click(xy[0],xy[1])
    time.sleep(0.7)
def MyMove(xy):
    mouse.move(xy[0],xy[1])
    time.sleep(0.7)

def MyHoldKey(key,ti):
    start = time.time()
    while True:
        kb.press_key(key)
        if time.time() - start > ti:
            break
    kb.release_key(key)
    time.sleep(0.5)



#函数功能 将所选单位进行建造 并对单位m行#函数功能 将所需要的坐标读入保存成字典
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
        mult_rate(xy, rate)
        data[ct[0]] = xy
        print(data)
    return data技能 升级n次
def build_unit(unit_xy,build_xy):

    MyClick(unit_xy)
    MyClick(build_xy)
    return
#函数功能 在unit_xy的单位m行技能升级n次
def skill_up(unit_xy,m,n):

    MyClick(unit_xy)
    skill_xy = list()
    if m == 1:
        skill_xy = skill1
    elif m ==2 :
        skill_xy = skill2
    elif m == 3:
        skill_xy = skill3
    for i in range(n):
        MyClick(skill_xy)
    time.sleep(1)
    return

#函数功能 无意义点击
def happy_click():
    xy = [1367, 1024]
    mult_rate(xy,rate)
    MyClick(xy)  # 无效位置
    return

#进入游戏
def start_game(coordinate):
    #技能位置初始化
    global skill1,skill2,skill3
    skill1 = coordinate['一号升级']
    skill2 = coordinate['二号升级']
    skill3 = coordinate['三号升级']

    sequence = ['开始','地图','简单','放气'] #执行序列
    for item in sequence:
        MyClick(coordinate[item])
    #点掉提示信息
    happy_click()
    time.sleep(4)
    happy_click()

    #正式开始游戏
    #安装大炮位置
    dp = coordinate['大炮']
    dpwz = coordinate['大炮位置']
    build_unit(dp,dpwz)
    #二号线升三级
    skill_up(dpwz,2,3)
    #安装飞机
    fj = coordinate['飞机']
    fjwz = coordinate['飞机位置']
    build_unit(fj,fjwz)
    #三号升级4次 一号升级2次
    skill_up(fjwz,3,4)
    MyClick(fjwz)
    skill_up(fjwz,1,2)

    # 安装魔法猴
    #快捷键建造
    mfhwz = coordinate['魔位置']
    MyMove(mfhwz)
    kb.tap_key('a', n=1) #魔法猴快捷键
    time.sleep(0.5)
    MyClick(mfhwz)
    # 三号线升四级
    skill_up(mfhwz, 3, 4)
    happy_click()

    #准备工作做完 启动
    for i in range(2):
        MyClick(coordinate['快进'])
    #防止升级一段时间
    wait = 0
    uptimes = 0
    while  1:
        time.sleep(1)
        wait += 1
        #5秒判断一下屏幕
        if wait%3 == 0 :
            target = [1000,1007]
            target = tuple(target)
            pix = pg.screenshot().getpixel(target)
            door = 3
            #屏幕已经不正常运作
            if not(pix == (138,200,36)):
                uptimes+=1 #故障次数加1
                happy_click()
                print("故障",uptimes)
                happy_click()
                #四次都是故障状态 为结束标志
                if uptimes >= 4:
                    print("一轮结束", uptimes)
                    break
            #屏幕正常但是有uptimes计数 说明中途升级弹窗等且被点掉了
            elif pix == (138,200,36) and uptimes == 1:
                print("应该快进")
                MyClick(coordinate['快进'])
                uptimes = 0

    #循环结束
    xyy = coordinate['下一页']
    MyClick(xyy)
    zy = coordinate['主页']
    MyClick(zy)
    time.sleep(5)
    return

#对应项乘以系数
def mult_rate(nums,rate):
    for i in range(2):
        nums[i] *= rate[i]
        nums[i] = int(nums[i])
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
        start_game(coordinate)



