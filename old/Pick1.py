# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 09:46:18 2020

@author: nesto
"""

import pickle

example_dict = {0:"1",1:"6",2:"2",3:"f"}

pickle_out = open("C:/Users/nesto/Desktop/Proyectos Pacho/BBox-Label-Tool-Python3.x-master/dict.pickle2","wb")
pickle.dump(example_dict, pickle_out)
pickle_out.close()


try:
    foo = pickle.load(open("var.pickle", "rb"))
    print("false")
except (OSError, IOError) as e:
    foo = 3
    pickle.dump(foo, open("var.pickle", "wb"))
    print("true")