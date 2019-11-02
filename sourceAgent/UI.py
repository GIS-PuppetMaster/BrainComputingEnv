# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 20:01:38 2019

@author: C-82
"""


def func1(name):
    from multiprocessing import Process
    Process(target=agentFactory.AGENT, args=[name]).start()


if __name__ == "__main__":
    import agentFactory

    func1('cbz')
    print('开始zkx进程')
    func1('zkx')
