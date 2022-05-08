import pymysql as mysql
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import datetime
import time
from itertools import combinations

import geatpy as ea
import numpy as np


def solve(c1,c2,c3):
    # 构建问题
    @ea.Problem.single
    def evalVars(Vars):  # 定义目标函数（含约束）
        f = np.abs(np.sqrt((Vars[0]-c1[0])**2 + (Vars[1]-c1[1])**2)-c1[2]) / c1[2] \
          + np.abs(np.sqrt((Vars[0]-c2[0])**2 + (Vars[1]-c2[1])**2)-c2[2]) / c2[2] \
          + np.abs(np.sqrt((Vars[0]-c3[0])**2 + (Vars[1]-c3[1])**2)-c3[2]) / c3[2]
        return f, np.array([0,0])

    problem = ea.Problem(name='soea quick start demo',
                            M=1,  # 目标维数
                            maxormins=[1],  # 目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标
                            Dim=2,  # 决策变量维数
                            varTypes=[0, 0],  # 决策变量的类型列表，0：实数；1：整数
                            lb=[-10, -10],  # 决策变量下界
                            ub=[10,10],  # 决策变量上界
                            evalVars=evalVars)
    # 构建算法
    algorithm = ea.soea_SEGA_templet(problem,
                                        ea.Population(Encoding='RI', NIND=20),
                                        MAXGEN=50,  # 最大进化代数。
                                        logTras=0,  # 表示每隔多少代记录一次日志信息，0表示不记录。
                                        trappedValue=1e-8,  # 单目标优化陷入停滞的判断阈值。
                                        maxTrappedCount=10)  # 进化停滞计数器最大上限值。
    # 求解
    res = ea.optimize(algorithm, seed=1, verbose=True, drawing=0, outputMsg=True, drawLog=False, saveFlag=False, dirName='result')
    return res['Vars'].squeeze()

def showCircle(c):
    theta = np.arange(0, 2*np.pi, 0.01)
    x = c[0] + c[2] * np.cos(theta)
    y = c[1] + c[2] * np.sin(theta)
    plt.plot(x, y)
    

def Apollonius(point1, point2,k):
    a = np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    r = a*k/(k*k - 1)
    ao = a*k*k/(k*k-1)
    x0 = point1[0] + (point2[0] - point1[0]) * ao / a
    y0 = point1[1] + (point2[1] - point1[1]) * ao / a
    return [x0,y0,r]


def CrossPoint(circle1, circle2):
    x = circle1[0]
    y = circle1[1]
    R = circle1[2]
    a = circle2[0]
    b = circle2[1]
    S = circle2[2]
    d = np.sqrt((abs(a-x))**2 + (abs(b-y))**2)
    if d > R + S or d < abs(R - S): return None, None
    A = (R**2 - S**2 + d**2) / (2 * d)
    h = np.sqrt(R**2 - A**2)
    x2 = x + A * (a-x)/d
    y2 = y + A * (b-y)/d
    x3 = round(x2 - h * (b - y) / d,2)
    y3 = round(y2 + h * (a - x) / d,2)
    x4 = round(x2 + h * (b - y) / d,2)
    y4 = round(y2 - h * (a - x) / d,2)
    return np.array([x3, y3]), np.array([x4, y4])


class SourceLocator(object):
    def __init__(self, recv, punit=-48.125, eps=1e-3) -> None:
        self.recv = recv
        self.punit = punit
        self.eps = 1e-3

    def __call__(self, p, plot=True):
        r0 = np.pow(10, -p[0]/20 + self.punit/20)
        r1 = np.pow(10, -p[1]/20 + self.punit/20)
        r2 = np.pow(10, -p[2]/20 + self.punit/20)
        print("distance : ",r0,r1,r2)
        circle0 = [self.recv[0][0], self.recv[0][1], r0]
        circle1 = [self.recv[1][0], self.recv[1][1], r1]
        circle2 = [self.recv[2][0], self.recv[2][1], r2]
        target = solve(circle0, circle1,circle2)
        if plot:
            showCircle(circle0)
            showCircle(circle1)
            showCircle(circle2)
            plt.scatter(self.recv[0][0],self.recv[0][1])
            plt.scatter(self.recv[1][0],self.recv[1][1])
            plt.scatter(self.recv[2][0],self.recv[2][1])
            plt.scatter(target[0], target[1], marker='x')

        return target

if __name__ == '__main__':

    recvs = [[0,0],[2.3,0],[0.45,3.05]]
    locator = SourceLocator(recvs)
    num = 0
    pos_x = []
    pos_y = []
    while True:
        time.sleep(8)
        num = num + 1
        #src = locator([4, 6, 1.1])
        
        mysql_conn = mysql.connect(host = "127.0.0.1",
                                    port = 3306,
                                    user = 'test',
                                    password = 'test123456',
                                    db = 'network_lab1')
        ps = [0,0,0]
        sql = "SELECT msg.* FROM (SELECT GatewayMAC, MAX(Time) AS Time FROM msg GROUP BY GatewayMAC) A LEFT JOIN msg ON A.GatewayMAC = msg.GatewayMAC AND A.Time = msg.Time;"
        try:
            with mysql_conn.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                for result in results:
                    #print(result)
                    if result[1] == 'E0E2E69C1E6C':
                        ps[0] = result[3]
                    elif result[1] == 'E0E2E69C1FD0':
                        ps[1] = result[3]
                    else:
                        ps[2] = result[3]
        except Exception as e:
            print(e)
        mysql_conn.close()
        
        pos = locator(ps, False)
        pos_x.append(pos[0])
        pos_y.append(pos[1])
        plt.scatter(recvs[0][0],recvs[0][1])
        plt.scatter(recvs[1][0],recvs[1][1])
        plt.scatter(recvs[2][0],recvs[2][1])
        plt.scatter(pos_x, pos_y, marker = 'x')
        plt.plot(pos_x, pos_y)
        plt.title('iBeacon Positioning (Last Updated: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ')')
        
        
        plt.axis('equal')
        #plt.show()
        plt.savefig("save/image.png")
        plt.close()
        