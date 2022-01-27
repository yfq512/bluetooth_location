# coding: utf-8
import numpy as np
import matplotlib.pylab as plt
from numpy.linalg import solve as np_solve
from sympy import *


def plot_show(data1=[1, 2, 3, 4, 5, 6, 7, 8, 9], data2=[1, 1, 1, 2, 3, 4, 5, 6, 6]):  # data = [1,2,3...]
    z1 = np.polyfit(data1, data2, 3)  # 拟合
    p1 = np.poly1d(z1)
    pp1 = p1(data1)
    plt.plot(data1, data2, color='r')
    plt.plot(data1, pp1, color='b')
    plt.show()


def gaussian_filer():  # 高斯滤波，自定义尺寸与强度
    pass


def rssi2distance(rssi, db_1m=50, n=2):  # 距离估计，A为发射端和接收端相隔一米时的信号强度N为环境衰减因子
    """蓝牙RSSI计算距离"""
    endRSSI = abs(rssi) - db_1m
    endN = 10 * n
    d = 10 ** (endRSSI / endN)  # 单位:米
    return d


def get_fun(data1, data2):  # data1 => {"x",x1, "y":y1, "L":L1}  # 舍弃虚数根
    x1, y1, L1 = data1.get("x"), data1.get("y"), data1.get("L")
    x2, y2, L2 = data2.get("x"), data2.get("y"), data2.get("L")
    # if x1 == x2:
    #     x2 = x2 + 0.000001
    # if y1 == y2:
    #     y2 = y2 + 0.000001

    x = Symbol('x')
    y = Symbol('y')
    value = solve([(x - x1) ** 2 + (y - y1) ** 2 - L1 ** 2, (x - x2) ** 2 + (y - y2) ** 2 - L2 ** 2], [x, y])
    # print('>>>>>>', value, type(value[0][0]))
    _len = len(value)
    if not _len == 2:
        raise Exception
    res = [np.array(value[0][0].evalf(), dtype='float'),
           np.array(value[0][1].evalf(), dtype='float'),
           np.array(value[1][0].evalf(), dtype='float'),
           np.array(value[1][1].evalf(), dtype='float')]  # [_x1, _y1, _x2, _y2]
    k = (res[3] - res[1]) / (res[2] - res[0])
    b = res[1] - k * res[0]
    return k, b


def get_point(data1, data2):  # data => [k, b]
    k1, b1 = data1
    k2, b2 = data2
    if k1 == k2:
        print('此处不可微分')
        raise [Exception]
    a = np.mat([[-k1, 1], [-k2, 1]])
    b = np.mat([b1, b2]).T
    x = np_solve(a, b)
    return [x[0, 0], x[1, 0]]  # [x, y]


def blue_location(data_list):  # [{'x':x1, 'y':y1, 'L':L1}...]
    funs = []
    for i in range(1, len(data_list)):
        try:
            funs.append(get_fun(data_list[i - 1], data_list[i]))
        except:
            pass
    try:
        funs.append(get_fun(data_list[-1], data_list[0]))
    except:
        pass
    if len(funs) <= 1:
        print('失效情况')
        return None
    xys = []
    for i in range(1, len(funs)):
        xys.append(get_point(funs[i - 1], funs[i]))
    xys.append(get_point(funs[-1], funs[0]))
    xs = []
    ys = []
    for n in xys:
        xs.append(n[0])
        ys.append(n[1])

    return [round(np.mean(xs), 4), round(np.mean(ys))]


def main(data_list):
    pass  # x信号预处理
    for i, data in enumerate(data_list):
        data_list[i].update({"L": rssi2distance(data.get('RSSI'))})
    xy = blue_location(data_list)
    return xy


if __name__ == "__main__":
    xy = main([{'x': 2, 'y': 4, 'RSSI': -70}, {'x': 8, 'y': 1, 'RSSI': -68}, {'x': 10, 'y': 4, 'RSSI': -62},
                       {'x': 4, 'y': 8, 'RSSI': -65.5}])
    print(xy)

