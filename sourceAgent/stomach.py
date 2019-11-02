# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 20:01:38 2019

@author: C-82
"""
import globalvar as gl
class STOMACH():
    def __init__(self,initFeeling = 10):
        self.label = 'stomach'
        self.feeling = 'hungry'
        gl.set_value(self.label,initFeeling)
    """
#    checkState方法
#    仅仅考虑这个feeling随时间因素的变化
    """
    def checkState(self):
        """
        暂且认为一分钟消耗0.55
        """
        delta = 0.005
        def content():
            gl.set_value(self.label,gl.get_value(self.label) - delta)
            return
        def periodicExec(func,inc = 5):
            import time,sched
            s = sched.scheduler(time.time,time.sleep)
            def perform(inc):
                s.enter(inc,0,perform,(inc,))
                func()
            s.enter(0,0,perform,(inc,))
            s.run()
            return
        from threading import Thread
        state_update_thread = Thread(target = periodicExec,args = (content,))
        state_update_thread.setDaemon(True)
        state_update_thread.start()
        return
    """
#    getNeedIntensity方法
#    根据自身的状态返回需求强度
#    返回值是一个元组
    """
    def getNeedIntensity(self):
        needOfHungry = 10 / self.label
        return (needOfHungry,self.feeling)