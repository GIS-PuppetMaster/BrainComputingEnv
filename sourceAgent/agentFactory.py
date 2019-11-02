# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 20:01:38 2019

@author: C-82
"""

from SPARQLWrapper import SPARQLWrapper, JSON

'''
head -> vars
results -> bindings -> (type,value)
'''

import brain
import os
from multiprocessing import Process
'''
knowledge是每一个agent默认的知识
'''
knowledge = """
PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ex:   <http://example.org/>

INSERT DATA {
ex:stomach        rdf:feeling             ex:hungry     .
ex:brain        rdf:feeling             ex:sleepy     .
ex:oralCavity        rdf:feeling             ex:thirsty     .
ex:skin        rdf:feeling             ex:pain     .
ex:genitals        rdf:feeling             ex:sexy     .
ex:sleepy        rdf:use             ex:sleep     .
ex:hungry        rdf:use             ex:catchfish     .
ex:hungry        rdf:use             ex:pick     .
ex:pick        rdf:parameter1             ex:target     .
ex:hungry        rdf:use             ex:eat     .
ex:eat        rdf:parameter1             ex:foodType     .
ex:eat        rdf:parameter2             ex:speed     .
ex:thirsty        rdf:use             ex:collectRainwater     .
ex:collectRainwater        rdf:parameter1             ex:tool     .
ex:collectRainwater        rdf:parameter2             ex:target_x     .
ex:collectRainwater        rdf:parameter3             ex:target_y     .
ex:collectRainwater        rdf:parameter4             ex:target_z     .
ex:thirsty        rdf:use             ex:fetchWater     .
ex:fetchWater        rdf:parameter1             ex:tool     .
ex:fetchWater        rdf:parameter2             ex:target_x     .
ex:fetchWater        rdf:parameter3             ex:target_y     .
ex:fetchWater        rdf:parameter4             ex:target_z     .
ex:thirsty        rdf:use             ex:drink     .
ex:drink        rdf:parameter1             ex:drinkType     .
ex:drink        rdf:parameter2             ex:speed     .
}
"""
class AGENT():
    def __init__(self,name):
        self.stm = brain.STM(name)
        self.name = name
        '''
        知识图谱操作对象
        self.query(用于查询操作)
        self.update(更改，insert或者insert)
        '''
        self.query = SPARQLWrapper("http://localhost:3030/" + self.name + "/query")
        self.update = SPARQLWrapper("http://localhost:3030/" + self.name + "/update")
        self.query.setReturnFormat(JSON)
        self.update.setMethod('POST')
        '''
        初始化知识
        '''
        self.getInitKnowledge()
        self.stm.start()
        import time
        while True:
            time.sleep(100000)
        return
    """
#    getInitKnowledge方法
#    初始化agent拥有的知识，包括名字，技能，尝试等
    """
    def getInitKnowledge(self):
        self.update.setQuery(knowledge)
        self.update.query()
        self.update.setQuery(
        "PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
        +"PREFIX ex:   <http://example.org/>"
        
        +"INSERT DATA {"
        +"ex:self        rdf:name             ex:" + self.name + "     ."
        +"}")
        self.update.query()
        return
    def __del__(self):
        return
#if __name__ == '__main__':
