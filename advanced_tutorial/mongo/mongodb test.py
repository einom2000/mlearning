import pymongo
import time
import datetime


cal_date = datetime.date.today()


# print(str(cal_date))


myclient = pymongo.MongoClient("mongodb://einom:paowozhesia00@119.45.4.205:15228/SINA_NEWS")
mydb = myclient["SINA_NEWS"]
mycol = mydb["NEWS"]
calcol_today = mydb["CALC_KEYWORDS_" + str(cal_date)]

mydoc = mycol.find()


def parse_keywords(kwords):
    kwords.replace(' ', ',')
    kwords.replace('|', ',')
    return kwords.split(',')


for x in mydoc:
    kwords = x['keywords']
    time.sleep(0.3)
    if kwords != 'NONE':
        temp_keywords_list = parse_keywords(kwords)
        for word in temp_keywords_list:
            print(word)
            lst = list(calcol_today.find({word: {'$exists': True}}))
        if lst != []:
            calcol_today_docs = calcol_today.find({word: {'$exists': True}})
            for doc in calcol_today_docs:
                myquery = {word: doc[word]}
                doc[word] = doc[word] + 1
                calcol_today.update_one(myquery, {"$set": doc})
        else:
            calcol_today.insert_one({word:1})
