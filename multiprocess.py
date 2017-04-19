#-*- coding: utf-8 -*-
# @Date    : '2017/2/7 0007'
# @Author  : Terry feng  (fengshaomin@qq.com)
from multiprocessing import Pool
# from multiprocessing.dummy import Pool
import time
def func(msg):
	print("msg:", msg)
	time.sleep(5)
	print("end")
if __name__ == '__main__':
    pool = Pool(processes=3)
    for i in range(3):
        msg = "Hello %d" % i
        pool.apply_async(func=func,args=(msg,))
    print( "Mark~ Mark~ Mark~" )
    pool.close()
    pool.join()
    print( "Sub-process(es) done!" )
