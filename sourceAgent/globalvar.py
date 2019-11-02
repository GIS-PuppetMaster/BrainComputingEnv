# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 21:47:16 2019

@author: C-82
"""



def _init():
    global _global_dict
    _global_dict = {}

def set_value(name, value):
    _global_dict[name] = value

def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue