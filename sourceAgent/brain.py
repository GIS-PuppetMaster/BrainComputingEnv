# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 20:01:38 2019

@author: C-82
"""
import globalvar as gl
import time
import stomach
import oralCavity
import skin
import genitals
import eye
import ear
from SPARQLWrapper import SPARQLWrapper, JSON
import os
global query
global update
global agentControlPath
global environmentMessagePath
global beingsolved
class STM():
    def __init__(self,name):
        '''
        gl用于保存全局变量
        线程之间共享，进程之间独立
        '''
        gl._init()
        self.name = name
        gl.set_value('name',self.name)
        '''
        agentControlPath
        environmentMessagePath
        保存交互文件的位置
        '''
        global agentControlPath
        global environmentMessagePath        
        agentControlPath = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + self.name + os.path.sep + "agentControl.json"
        environmentMessagePath = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "data" + os.path.sep + self.name + os.path.sep + "environmentMessage.json"
        global query
        global update
        query = SPARQLWrapper("http://localhost:3030/" + self.name + "/query")
        update = SPARQLWrapper("http://localhost:3030/" + self.name + "/update")
        query.setReturnFormat(JSON)
        update.setMethod('POST')
        '''
        beingsolved
        正在被解决的需求
        '''
        global beingsolved
        beingsolved = []
        self.states = []
        '''
        states
        记录了五种需求
        '''
        self.states.append('brain')
        self.states.append('stomach')
        self.states.append('oralCavity')
        self.states.append('skin')
        self.states.append('genitals')
        '''
        配备ltm
        '''
        self.brain = BRAIN()
        self.eye = eye.EYE()
        self.ear = ear.EAR()
        self.stomach = stomach.STOMACH()
        self.oralCavity = oralCavity.ORALCAVITY()
        self.skin = skin.SKIN()
        self.genitals = genitals.GENITALS()
        '''
        abnormalOrganList记录是哪个器官出现的需求
        '''
        self.abnormalOrganList = []
        '''
        slots代表注意力，定长队列7
        '''
        self.slots = []
        return
    """
#    start方法
#    内部开始感知自己的状态
#    外部开始收集信息
#    stm开始检测需求，检测声明是否存在
    """
    def start(self):
        self.brain.checkState()
        self.stomach.checkState()
        self.oralCavity.checkState()
        self.skin.checkState()
        self.genitals.checkState()
        self.eye.collectMessage()
        self.ear.collectMessage()
        self.detectProblem()
        self.decide()
        self.detectLife()
        return
    """
#    detectLife方法
#    检测声明是否存在
    """
    def detectLife(self):
        def content():
            while True:
                die = False
                ans = {}
                ans['brain'] = gl.get_value('brain')
                ans['stomach'] = gl.get_value('stomach')
                ans['oralCavity'] = gl.get_value('oralCavity')
                ans['skin'] = gl.get_value('skin')
                ans['genitals'] = gl.get_value('genitals')
                if gl.get_value('brain') < 0:
                    die = True
                if gl.get_value('stomach') < 0:
                    die = True
                if gl.get_value('oralCavity') < 0:
                    die = True
                if gl.get_value('skin') < 0:
                    die = True
                if gl.get_value('genitals') < 0:
                    die = True
                if die == True:
                    import os
                    cmd = "taskkill /F /PID " + str(os.getpid())
                    os.system(cmd)
                import time
                time.sleep(1)
                print(self.name)
                print(ans)
            return
        from threading import Thread
        state_update_thread = Thread(target = content)
        state_update_thread.setDaemon(True)
        state_update_thread.start()
    """
#    detectProblem方法
#    检测自身当前是否遇到problem
#    如果没有遇到problem就阻塞当前线程
#    如果有problem就放行
#    
#    problem有特殊含义
#    自身状态发生变化，需要通过产生需求进行恢复状态
#    making decision和executing decision时产生
    """
    def detectProblem(self):
        def content():
            while True:
                for x in self.states:
                    if gl.get_value(x) < 5 and x not in self.abnormalOrganList and x not in beingsolved:
                        self.abnormalOrganList.append(x)
                print('abnormalOrganList')
                print(self.abnormalOrganList)
                time.sleep(5)
        from threading import Thread
        state_update_thread = Thread(target = content)
        state_update_thread.setDaemon(True)
        state_update_thread.start()
        return
    """
#    decide方法
#    决定解决哪一种需求，并开始执行
    """
    def decide(self):
        def content():
            while True:
                '''初始化一些变量'''
                organs = []
                for x in self.abnormalOrganList:
                    if x not in beingsolved:
                        organs.append(x)
                self.abnormalOrganList = []
                methods = []
                '''知识搜索一些方法'''
                for x in organs:
                    tmp = self.brain.getMethodsFromOrgan(x)
                    for y in tmp:
                        methods.append(y)
                '''通过模拟计算出最好的方法'''
                bestMethod = None
                maxReward = 0
                for x in methods:
                    self.brain.setFactors(x)
                    tmpReward = self.brain.calReward('happy')
                    print('method')
                    print(x)
                    print('tmpReward')
                    print(tmpReward)
                    if maxReward < tmpReward:
                        bestMethod = x
                        maxReward = tmpReward
                print("bestMethod")
                print(bestMethod)
                if bestMethod != None:
                    global canexe
                    canexe = True
#                    for x in self.slots:
#                        if self.brain.judgeConflict(x,bestMethod):
#                            canexe = False
                    if canexe:
                        eval(bestMethod)()
                        self.slots.append(bestMethod)
                import time
                time.sleep(5)
            return
        from threading import Thread
        problem_detect_thread = Thread(target = content)
        problem_detect_thread.setDaemon(True)
        problem_detect_thread.start()
        return
    """
#    think方法
#    slots有空位置的时候就进行思考
#    两个版本，一个是基于知识图谱的搜索推理完成的，当然也可以通过强化学习完成
    """
    def think(self):
        def content():
            
            return
        from threading import Thread
        problem_detect_thread = Thread(target = content)
        problem_detect_thread.setDaemon(True)
        problem_detect_thread.start()
        return

class BRAIN():
    def __init__(self,initFeeling = 5):
        self.label = "brain"
        self.feeling = "sleepy"
        gl.set_value(self.label,initFeeling)
        """
        self.__ingraph
        入度邻接表
        """
        self.__ingraph = {}
        """
        self.__outgrpah
        出度邻接表
        """
        self.__outgraph = {}
        """
        self.__intensity
        记录各个需求强度（reward）
        """
        self.__intensity = {}
        """
        self.__factors
        记录所有概念在此决策中的参与程度
        """
        self.__factors = []
        """
        建立原始图
        """
        self.addEdge("unhungry","happy",1)
        self.addEdge("unthirsty","happy",1)
        self.addEdge("unpain","happy",1)
        self.addEdge("unsleepy","happy",1)
        self.addEdge("sexy","happy",1)
        self.addEdge("catchfish","unhungry",2)
        self.addEdge("pick","unhungry",1)
        self.addEdge("eat","unhungry",2)
        self.addEdge("collectRainwater","unthirsty",2)
        self.addEdge("fetchWater","unthirsty",1)
        self.addEdge("drink","unthirsty",2)
        self.addEdge("sleep","unsleepy",2)
        return
    def judgeConflict(x,y):
        return False
    """
#    checkState方法
#    仅仅考虑这个feeling随时间因素的变化
    """
    def checkState(self):
        """
        暂且认为一分钟消耗0.015
        """
        delta = 0.5
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
        needOfSleepy = 10 / gl.get_value(self.label)
        return (self.feeling,needOfSleepy)
    """
#    add_Edge方法
#    添加一个关系
    """
    def addEdge(self,s,t,weight):
        '''
        处理需求序列
        '''
        if self.__intensity.__contains__(s) == False:
            self.__intensity[s] = 0
        if self.__intensity.__contains__(t) == False:
            self.__intensity[t] = 0
        '''
        处理in图
        '''
        tmp_tuple = (s,weight)
        if self.__ingraph.__contains__(t):
            self.__ingraph[t].append(tmp_tuple)
        else:
            self.__ingraph[t] = [tmp_tuple]
        '''
        处理out图
        '''
        tmp_tuple = (t,weight)
        if self.__outgraph.__contains__(s):
            self.__outgraph[s].append(tmp_tuple)
        else:
            self.__outgraph[s] = [tmp_tuple]
        return
    """
#    removeEdge方法
#    删除一个关系
    """
    def removeEdge(self,s,t):
        '''
        处理需求序列
        '''
        if self.__intensity.__contains__(s):
            self.__intensity.pop(s)
        if self.__intensity.__contains__(t):
            self.__intensity.pop(t)
        '''
        处理in图
        '''
        if self.__ingraph.__contains__(t) == True:
            for tmp_vertex in self.__ingraph[t]:
                if tmp_vertex[0] == s:
                    self.__ingraph[t].remove(tmp_vertex)
                    break
        '''
        处理out图
        '''
        if self.__outgraph.__contains__(s) == True:
            for tmp_vertex in self.__outgraph[s]:
                if tmp_vertex[0] == t:
                    self.__outgraph[s].remove(tmp_vertex)
                    break
        return
    """
#    updateWeight方法
#    更新某两个结点之间的权重
    """
    def updateWeight(self,s,t,weight):
        if self.__ingraph.__contains__(t):
            for tmp_vertex in self.__ingraph[t]:
                if tmp_vertex[0] == s:
                    self.__ingraph[t].remove(tmp_vertex)
                    tmp_vertex[1] = weight
                    self.__ingraph[t].append(tmp_vertex)
                    break
        if self.__outgraph.__contains__(s):
            for tmp_vertex in self.__outgraph[s]:
                if tmp_vertex[0] == t:
                    self.__outgraph[s].remove(tmp_vertex)
                    tmp_vertex[1] = weight
                    self.__outgraph[s].append(tmp_vertex)
                    break
        return
    """
#    updateIntensity方法
#    更新某一个结点的强度
    """
    def updateIntensity(self,vertex,intensity):
        if self.__intensity.__contains__(vertex):
            self.__intensity[vertex] = intensity
            return
        return
    """
#    calReward方法
#    计算到达某一个点可以获得的reward
#    一般用于happy
    """
    def calReward(self,vertex):
        if self.__ingraph.__contains__(vertex) == False:
            return self.__intensity[vertex]
        ans = 1
        for tmp_vertex in self.__ingraph[vertex]:
            if self.__factors.__contains__(tmp_vertex) == False:
                continue
            ans = ans + self.calReward(tmp_vertex) * self.__intensity[tmp_vertex] * self.__factors[tmp_vertex]
        return ans
    """
#    setFactors方法
#    设置每一个概念的参与度
#    概念x科大的每一个概念都认为是参与的
#    否则认为是不参与
    """
    def setFactors(self,targetFactors):
        self.__factors = []
        vis = {}
        from queue import Queue
        q = Queue()
        q.put(targetFactors)
        while q.empty() == False:
            tmp = q.get()
            self.__factors.append(tmp)
            if self.__outgraph.__contains__(tmp) == True:
                for x in self.__outgraph[tmp]:
                    if vis.__contains__(x[0]) == False:
                        q.put(x[0])
                        vis[x[0]] = 1
        return
    """
#    getMethodsFromOrgan(organ)方法
#    适配模式，参数换为organ
    """
    def getMethodsFromOrgan(self,organ):
        query.setQuery(
        "PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
        +"PREFIX ex:   <http://example.org/>"
        
        +"SELECT * WHERE {"
        +"ex:" + organ + "        rdf:feeling             ?ans     ."
        +"}")
        need = query.query().convert()['results']['bindings'][0]['ans']['value'].replace('http://example.org/','')
        return self.getMethodsFromNeed(need)
    """
#    getMethodsFromNeed(need)方法
#    在知识图谱中查找
    """
    def getMethodsFromNeed(self,need):
        query.setQuery(
        "PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
        +"PREFIX ex:   <http://example.org/>"
        
        +"SELECT * WHERE {"
        +"ex:" + need + "        rdf:use             ?ans     ."
        +"}")
        ans = query.query().convert()['results']['bindings']
        ret = []
        for x in ans:
            ret.append(x['ans']['value'].replace('http://example.org/',''))
        return ret



def sleep():
    beingsolved.append('brain')
    def content():
        print(gl.get_value('name') + " is going to sleep!")
        """
        向环境传递睡觉信息
        """
        dic = {}
        dic[1] = {"operation": "sleep"}
        import json
        dic = json.dumps(dic)
        file = open(agentControlPath,"w")
        file.write(str(dic))
        file.close()
        timeStamp = os.stat(agentControlPath).st_mtime
        while timeStamp == os.stat(agentControlPath).st_mtime:
            print('st_mtime')
            print(os.stat(agentControlPath).st_mtime)
            import time
            time.sleep(1)
        gl.set_value('brain',gl.get_value('brain') + 5)
        beingsolved.remove('brain')
        return
    from threading import Thread
    problem_detect_thread = Thread(target = content)
    problem_detect_thread.setDaemon(True)
    problem_detect_thread.start()
    return
def move(dx,dy,dz,speed = 1):
    def content():
        """
        向环境传递移动信息
        """
        file = open(agentControlPath,"w")
        dic = {}
        dic[1] = {"operation":"move","param1":dx,"param2":dy,"param3":dz,"param4":speed}
        import json
        dic = json.dumps(dic)
        file.write(str(dic))
        file.close()
        timeStamp = os.stat(agentControlPath).st_mtime
        while timeStamp == os.stat(agentControlPath).st_mtime:
            import time
            time.sleep(1)
        return
    from threading import Thread
    problem_detect_thread = Thread(target = content)
    problem_detect_thread.setDaemon(True)
    problem_detect_thread.start()
    return

def observe(target):
    """
    传递观察命令
    正常情况下agent一直在进行视觉的信息提取
    但是在执行观察命令之后agent会获得更多的视觉信息
    """
    file = open(agentControlPath,"w")
    dic = {}
    dic[1] = {"operation":"observe"}
    import json
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        import time
        time.sleep(1)
    '''检索视觉信息,发现target'''
    file = open(environmentMessagePath,'r')
    import json
    visionMessage = json.load(file)['vision']
    file.close()
    for i in range(1,100000):
        if visionMessage.__contains__(i):
            message = visionMessage[i]
            if message['object'] == target:
                return message['pos']
        else:
            break
    return None

def catchfish():
#    print(name + ": I am catching fish!")
    '''找鱼叉(在寻找鱼叉的过程中move的方向需要单独进行考虑)'''
    import random
    dx = random.randint(-2,2)
    dy = random.randint(-2,2)
    dz = random.randint(-2,2)
    move(dx,dy,dz)
    ans = observe('fish spear')
    while ans == None:
        ans = observe('fish spear')
    dx = ans[0]
    dy = ans[1]
    dz = ans[2]
    move(dx,dy,dz)
    '''拾起鱼叉'''
    pick('fish spear')
    '''找鱼塘'''
    import random
    dx = random.randint(-2,2)
    dy = random.randint(-2,2)
    dz = random.randint(-2,2)
    move(dx,dy,dz)
    ans = observe('fish pond')
    while ans == None:
        ans = observe('fish pond')
    dx = ans[0]
    dy = ans[1]
    dz = ans[2]
    move(dx,dy,dz)
    '''投掷鱼叉'''
    import json
    file = open(agentControlPath,"w")
    dic = {}
    dic[1] = {"operation": "catchfish"}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    import os
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        import time
        time.sleep(1)
    return

def pick(target):
    import json
    file = open(__messagePath,"r")
    message = json.load(file)
    file.close()
    agentMessage = message["agent"]
    agentMessage["x"] = target.x
    agentMessage["y"] = target.y
    agentMessage["height"] = target.z
    message["agent"] = agentMessage
    file = open(__messagePath,"w")
    message = json.dumps(message)
    file.write(str(message))
    file.close()
    print(name + ": I pick " + target)
    file = open(agentControlPath,"w")
    dic = {"operation": "pick",
           "param": target}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        import time
        time.sleep(1)

def eat(food_type,speed):
    import json
    import time
    begintime = time.time()
    print(name + ": I eat " + food_type)
    file = open(agentControlPath,"w")
    dic = {"operation": "eat",
           "param1": food_type,
           "param2": speed}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        endtime = time.time()
        lenOfTime = endtime - begintime
        state["hungry"]+= lenOfTime * speed
        time.sleep(1)

def collectRainwater(tool,target_x,target_y,target_z):
    import json
    file = open(__messagePath, "r")
    message = json.load(file)
    file.close()
    agentMessage = message["agent"]
    agentMessage["x"] = target_x
    agentMessage["y"] = target_y
    agentMessage["height"] = target_z
    message["agent"] = agentMessage
    file = open(__messagePath, "w")
    message = json.dumps(message)
    file.write(str(message))
    file.close()
    print(name + ": I collect rainwater with " + tool)
    file = open(agentControlPath,"w")
    dic = {"operation":"collect_rainwater",
           "param1": tool,
           "param2": target_x,
           "param3": target_y,
           "param4": target_z}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        import time
        time.sleep(1)

def fetch_water(tool,target_x,target_y,target_z):
    import json
    file = open(__messagePath, "r")
    message = json.load(file)
    file.close()
    agentMessage = message["agent"]
    agentMessage["x"] = target_x
    agentMessage["y"] = target_y
    agentMessage["height"] = target_z
    message["agent"] = agentMessage
    file = open(__messagePath, "w")
    message = json.dumps(message)
    file.write(str(message))
    file.close()
    print(name + ": I fetch water with " + tool)
    file = open(agentControlPath,"w")
    dic = {"operation":"fetch_water",
           "param1": tool,
           "param2": target_x,
           "param3": target_y,
           "param4": target_z}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        import time
        time.sleep(1)

def drink( drink_type, speed):
    import json
    import time
    begintime = time.time()
    print(name + ": I drink " + drink_type)
    file = open(agentControlPath,"w")
    dic = {"operation": "drink",
           "param1": drink_type,
           "param2": speed}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        endtime = time.time()
        lenOfTime = endtime - begintime
        state["thirsty"] += lenOfTime * speed
        time.sleep(1)

def defense(tool,target_x,target_y,target_z):
    import json
    print(name + "I defense with" + tool)
    file = open(agentControlPath,"w")
    dic = {"operation":"defense",
           "param1": tool,
           "param2": target_x,
           "param3": target_y,
           "param4": target_z}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        import time
        time.sleep(1)

def attack(tool,target_x,target_y,target_z):
    import json
    print(name + "I attack with" + tool)
    file = open(agentControlPath,"w")
    dic = {"operation":"attack",
           "param1": tool,
           "param2": target_x,
           "param3": target_y,
           "param4": target_z}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        import time
        time.sleep(1)

def give_up(target_x,target_y,target_z):
    import json
    print(name + "I give up!")
    file = open(agentControlPath,"w")
    dic = {"operation":"give_up)",
           "param1": target_x,
           "param2": target_y,
           "param3": target_z}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        import time
        time.sleep(1)

def chat(object):
    import json
    file = open(__messagePath, "r")
    message = json.load(file)
    file.close()
    agentMessage = message["agent"]
    agentMessage["x"] = object.x
    agentMessage["y"] = object.y
    agentMessage["height"] = object.z
    message["agent"] = agentMessage
    file = open(__messagePath, "w")
    message = json.dumps(message)
    file.write(str(message))
    file.close()
    print(name + ": I am searching an object to chat!")
    file = open(agentControlPath,"w")
    dic = {"operation":"chat",
           "param1": "object"}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        import time
        time.sleep(1)

def care(object):
    import json
    file = open(__messagePath, "r")
    message = json.load(file)
    file.close()
    agentMessage = message["agent"]
    agentMessage["x"] = object.x
    agentMessage["y"] = object.y
    agentMessage["height"] = object.z
    message["agent"] = agentMessage
    file = open(__messagePath, "w")
    message = json.dumps(message)
    file.write(str(message))
    file.close()
    print(name + ": I am caring" + object)
    file = open(agentControlPath,"w")
    dic = {"operation":"care",
           "param1": "object"}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        import time
        time.sleep(1)

def make_new_friends(object):
    import json
    file = open(__messagePath, "r")
    message = json.load(file)
    file.close()
    agentMessage = message["agent"]
    agentMessage["x"] = object.x
    agentMessage["y"] = object.y
    agentMessage["height"] = object.z
    message["agent"] = agentMessage
    file = open(__messagePath, "w")
    message = json.dumps(message)
    file.write(str(message))
    file.close()
    print(name + ": I make new friends with" + object)
    file = open(agentControlPath,"w")
    dic = {"operation":"mnf",
           "param1": "object"}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        import time
        time.sleep(1)

def func1(target,agent):
    import json
    file = open(__messagePath, "r")
    message = json.load(file)
    file.close()
    agentMessage = message["agent"]
    agentMessage["x"] = agent.x
    agentMessage["y"] = agent.y
    agentMessage["height"] = agent.z
    message["agent"] = agentMessage
    file = open(__messagePath, "w")
    message = json.dumps(message)
    file.write(str(message))
    file.close()
    print(name + ": I ask the " + agent +"for the " + target)
    file = open(agentControlPath,"w")
    dic = {"operation": "func1",
           "param1": "target",
           "param2": "agent"}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        import time
        time.sleep(1)

def func2(target,agent):
    import json
    file = open(__messagePath, "r")
    message = json.load(file)
    file.close()
    agentMessage = message["agent"]
    agentMessage["x"] = agent.x
    agentMessage["y"] = agent.y
    agentMessage["height"] = agent.z
    message["agent"] = agentMessage
    file = open(__messagePath, "w")
    message = json.dumps(message)
    file.write(str(message))
    file.close()
    print(name + ": I cooperate with " + agent +"for the " + target)
    file = open(agentControlPath,"w")
    dic = {"operation": "func2",
           "param1": "target",
           "param2": "agent"}
    dic = json.dumps(dic)
    file.write(str(dic))
    file.close()
    timeStamp = os.stat(agentControlPath).st_mtime
    while timeStamp == os.stat(agentControlPath).st_mtime:
        import time
        time.sleep(1)
