#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf8")
import jieba
import json
import datetime
jieba.load_userdict("userdict.txt")


path = "../data/test_icdc.data"

tokens = ['，','？','。',' ',' ','、','；','：','\n',"#",'/','~','·','（',')','（','）','《','》','<','>','{','}','{','}','[',']','.',',','?','【','】',
          '=','——','-','','…','—','¨','｜','～','『','』','〃','＂','＇','”','“','々','‖','！','!',';','@','&','*']
stop_words = ['严格','的','是','是否','按照','一般','然后','然而','根据','月底','最近','每','以便','数月','各','并','和','每天','每周','每月','前一天','对于','在','对','及时',
              '后面','以及','及','向','当月','日常','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','根据','今后','虽然','但是','仍然','仍','个',
              '每日','当日','每段','于','对于','中','与','月末','上月','年度','工作','自己','年底','从事','一定','一周','这','这个','之前','等','等等','为','为了','描述','现在',
              '也','会','如','比如','例如','地','通过','能','能够','不同','了','一些','小','后','可以','其他','各项','方面','情况','一','一个','二','三','四','五','六','七','八','九',
              '上','并且','来','有','由于','想','于是','之中','更好','别家','还','还有','经常','很','非常','好','相当','可以','每个','到','来到','一下','或者','包括','将',
              '各种','其它','上级','交代','任务','工作','各种','了解','时','多','从中','我','我们','他们','不到','学','更加','深刻','深动','更','参与','职责','负责','所需','所',
              '按规定','做好','保证','随时','进行','使用','采取','要求','当天','必须','做到','本月','得到','把','做','学到','主要','进行','很多','按时','完成','或','确保','参加']


def get_value(data_dict,key):
    if key in data_dict:
        return data_dict[key]
    return None

def prior(mouth_salary1,mouth_salary2):
    if mouth_salary1:
        return mouth_salary1
    return mouth_salary2

def isExit_time(time):
    if time:
        return time
    else:
        #t = datetime.date.today()
        #time1 = str(t.year) + '年'+ str(t.month) + '月'
        time1 = '至今'.encode('utf8')
    return time1

#cut string
def segment(str1):
    if str1:
        str1 = str1.lower()
        seg = jieba.cut(str1)
        texts = [word for word in seg if (word not in tokens and word not in stop_words)]
        return ' '.join(texts)
    return None

def work_experience(work):
    if work:
        works = dict()
        for i in work:
            position = get_value(work[i], 'position_name')
            responsibility = get_value(work[i], 'responsibilities')
            responsibilities = segment(responsibility)
            corporation = get_value(work[i], 'corporation_name')
            industry = get_value(work[i], 'industry_name')
            month_salary1 = get_value(work[i], 'month_salary')
            month_salary2 = get_value(work[i], 'basic_salary_to')
            salary = prior(month_salary1, month_salary2)
            start_time = get_value(work[i], 'start_time')
            end_time = get_value(work[i], 'end_time')
            end_time = isExit_time(end_time)
            time = start_time + '-' + end_time
            works[time] = {'position': position, 'corporation': corporation, 'industry': industry, 'month_salary': salary,
                       'responsibilities': responsibilities}
        return works
    return  None

def get_education(education):
    if education:
        educations = dict()
        for e in education:
            start_time = get_value(education[e],'start_time')
            end_time = get_value(education[e], 'end_time')
            end_time = isExit_time(end_time)
            school = get_value(education[e],'school_name')
            discipline = get_value(education[e],'discipline_name')
            time = start_time + '-' + end_time
            educations[time] = {'school':school,'discipline':discipline}
        return educations
    return None

def get_skill(skill):
    if skill:
        skills1 = str()
        skills2 = dict()
        for s in skill:
            name = get_value(skill[s],'name')
            level = get_value(skill[s],'level')
            if level:
                skills2[name] = level + name
                skills1 = skills1 + name + level + ';'
            else:
                skills2[name] = name
                # skills1 = skills1 + name + ';'

        return skills1,skills2
    return None, None

with open(path,'r') as fp:
    cv = dict()
    for i, line in enumerate(fp):
        if i < 100:
            line = line.strip('\r\n')
            line = line.strip(' '.encode("utf8"))
            cv_dict = json.loads(line)
            # print json.dumps(cv_dict['contact'], ensure_ascii=False, encoding='utf8', indent=4)
            # print json.dumps(cv_dict, ensure_ascii=False, encoding='utf8', indent=4)
            resume_id = get_value(cv_dict,'resume_id')
            # get person name
            basic = get_value(cv_dict, 'basic')
            # contact = get_value(cv_dict, 'contact')
            # name1 = get_value(contact[0], 'name')
            # name2 = get_value(basic[0],'name')
            # person_name = prior(name1,name2)
            # get work experice ,if works is not None, then use works,else use remark,else use other_info
            work = get_value(cv_dict, 'work')
            works = work_experience(work)

            remark = segment(get_value(basic[0],'remark'))
            other_info = segment(get_value(basic[0],'other_info'))
            experience = prior(works,remark)
            experience = prior(experience,other_info)

            # get education information
            educ = get_value(cv_dict,'education')
            education = get_education(educ)
            # get skills
            skill = get_value(cv_dict,'skill')
            skills1,skills2 = get_skill(skill)
            cv[resume_id] = {'work_experience':experience,'education':education,'skills':skills2}

            # print person_name
            # print skills1
            # # print experience
            # # print remark
            print json.dumps(cv, ensure_ascii=False, encoding='utf8', indent=4)
            print i
            # print json.dumps(experience,ensure_ascii=False,encoding='utf8',indent=4)
            #print json.dumps(cv_dict, ensure_ascii=False, encoding='utf8', indent=4)

