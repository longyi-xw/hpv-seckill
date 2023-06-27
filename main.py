# 这是一个示例 Python 脚本。
import sys
import time

from seckill import MiaoApp
from threading import Timer, Thread
from client import MiaoWidgets
from PySide6 import QtWidgets
import datetime
import math

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。

TK = "wxapptoken:10:fbfb2a85b315f0948eafd817a0b17676_99f16c5a2f14e1ffa1dd541e8cb039d5"


def getTime(start_time: str) -> int:
    current_time = datetime.datetime.now().timestamp() * 1000
    _target_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timestamp() * 1000
    return math.floor((_target_time - current_time) / 1000)


def seckill(app, vaccines: list):
    """
    秒杀逻辑
    :param app:
    :param vaccines:
    :return:
    """

    def invoke(vaccine):
        print(f"{vaccine['name']}-----任务开始\n")
        # 秒杀开始
        try:
            while True:
                checkStock = app.checkStock(vaccine['id'])
                if int(checkStock['stock']) == 0:
                    break
                result = app.submitOrder(vaccine['id'], user['id'], user['idCardNo'], checkStock['st'])
                if result['code'] == "0000":
                    print("---------------秒杀成功！---------------")
                    break
                time.sleep(1)
        except Exception as e:
            print(e)

    # TODO 多线程
    threads = []
    for vc in vaccines:
        # 多线程似乎容易被监测，所以取消单线程
        # vc_t = Thread(target=invoke, args=[vc])
        # vc_t.start()
        # threads.append(vc_t)
        invoke(vc)

    # for thread in threads: thread.join()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    miao = MiaoApp(tk=TK)
    user = miao.getUser("", "")
    miao_list = miao.getMiaoList()
    hpv9_list = len(miao_list) > 0 and [m for m in miao_list]

    # 时间段秒杀任务
    timer_dict = { }
    for _9 in hpv9_list:
        target_time = getTime(_9['startTime'])
        if target_time in timer_dict:
            timer_dict[target_time].append(_9)
        else:
            timer_dict[target_time] = [_9]

    # 多个时间段的定时器
    for key, value in timer_dict.items():
        key = key if key > 0 else 1.0
        print(f"----------开始秒杀-----------{key}秒后开始---------")
        t = Timer(1, seckill, args=[miao, value])
        t.start()
