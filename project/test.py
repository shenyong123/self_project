#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import datetime as dt
import re

str1 = "今天是2015年10月1日国庆节,明天是2015年10月2日";
result = str1.replace("2015年10月1日", "00") #只能用于字符串替换
print result;

result, number = re.subn("\d+年\d+月\d+日", "\d-\d", str1) #可以用于正则的替换
print result;
print number;

t = dt.date.today()
print t
print str(t.year) + '年'+ str(t.month) + '月'
#
# m = dt.date.max
#
# s = m - t
print type(t)
# print t,m,s

a = "2009年05月"
print type(a)
li = list(a)
r1,n1 = re.subn('年','-',a)
r,n = re.subn('月','-0',r1)
print r,li
#print t - r

