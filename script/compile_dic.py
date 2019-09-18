#!/usr/bin/env python3
from janome.dic import UserDictionary
from janome import sysdic
import os
try:
    os.chdir(os.path.dirname(__file__))
except NameError as e:
    pass

if __name__=="__main__":
    user_dict=UserDictionary("./../dic/csv/user_dic.csv","utf8","ipadic",sysdic.connections)
    user_dict.save("./../dic/user_dic")

