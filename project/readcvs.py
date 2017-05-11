#!/usr/local/env python
# -*- coding: utf-8 -*-

import pandas as pd
import json
import jieba
import re
import sys
reload(sys)
sys.setdefaultencoding("utf8")

path = 'stop_words.txt'
with open(path,'r') as f:
    for i in f:
        i = i.lower()
        print (i)

jieba.load_userdict('userdict.txt')

tokens = ['，','？','。',' ','、','；','：','\n',"#",'/','~','·','（',')','《','》','<','>','{','}','{','}','[',']','.',',','?','【','】',
          '=','——','-','','…','—','¨','｜','～','『','』','〃','＂','＇','”','“','々','‖','！','!',';','@','&','*']

test = "aDcGDbdfdf李小福是创新办主任也是云计算方面的专家？、" \
       ";同时也是一位可靠性工程师和现场安全工程师fpga研发工程师.C#。"
test = test.lower().encode("utf8")


seg = jieba.cut(test)

t = [word for word in seg if word not in tokens]
print ' '.join(t)


# work = str()
# for w in seg:
#     if w not in tokens:
#         work = work + ' ' + w
#
# print work


#print " ".join(seg)

# path = 'userdict.txt'
# w_path = 'userdict1.txt'
#
# with open(path,'r') as f:
#     with open(w_path,'w') as wf:
#         for line in f:
#             line = line.lower()
#             wf.write(line)
#
# print "ok"



