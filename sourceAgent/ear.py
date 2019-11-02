# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 20:01:38 2019

@author: C-82
"""

import os
agentControlPath = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + "agentControl.json"
environmentMessagePath = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + "environmentMessage.json"
shortTimeKnowledgePath = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + "shortTimeKnowledge.json"
longTimeKnowledgePath = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + "longTimeKnowledge.json"
class EAR():
    def __init__(self):
        return
    def collectMessage(self):
        def content():
            while True:
                '''检测文件是否更新'''
                timeStamp = os.stat(environmentMessagePath).st_mtime
                while timeStamp == os.stat(agentControlPath).st_mtime:
                    import time
                    time.sleep(1)
                '''检测到环境信息文件更新，就进行信息的提取和整合'''
                '''shortTimeKnowledge中维护100个知识'''
                file = open(environmentMessagePath,'r')
                import json
                visionMessage = json.load(file)['hearing']
                file.close()
                file = open(shortTimeKnowledgePath,'r')
                shortTimeMessage = json.load(file)
                file.close()
                newshortTimeMessage = {}
                i = 1
                for i in range(1,101):
                    if visionMessage.__contain__(i):
                        newshortTimeMessage[i] = visionMessage[i]
                    else:
                        break
                id = 1
                for x in range(i,101):
                    if shortTimeMessage.__contains__(id):
                        newshortTimeMessage[x] = shortTimeMessage[id]
                        id = id + 1
                    else:
                        break
                file = open(shortTimeKnowledgePath,'w')
                dic = json.dumps(newshortTimeMessage)
                file.write(str(dic))
                file.close()
            return
        from threading import Thread
        problem_detect_thread = Thread(target = content)
        problem_detect_thread.setDaemon(True)
        problem_detect_thread.start()
        return
