#Charles Jacobsen
#1000717663
#started 3/30/2015
#last edited 4/1/2015
#Data Mining 4334
#Yelp Data Challenge

import math
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import csv


stemmer = PorterStemmer()
stopstuff = stopwords.words('english')
re.dotall = True
tokeit = RegexpTokenizer(r'[a-zA-Z]+')

tokenizer = RegexpTokenizer(r'"[^"]+":*|(?<="stars": )\d.\d|(?<="review_count": )\d+|(?<=itude": )-*\d+.\d+')
business = dict()

#pulls information for businesses
file = open('yelp_academic_dataset_business.json', 'rt')
q = 0
for line in file:
    temp = tokenizer.tokenize(line)
    if q == 60125:
        print(temp)
    business[q] = dict()
    for index,item in enumerate(temp):
        if item == r'"business_id":':
            business[q]['b_id'] = temp[index + 1].strip('\"')
        elif item == r'"state":':
            business[q]['state'] = temp[index + 1].strip('\"')
        elif item == r'"city":':
            business[q]['city'] = temp[index + 1].strip('\"')
        elif item == r'"stars":':
            business[q]['stars'] = temp[index + 1]
        elif item == r'"review_count":':
            business[q]['count'] = temp[index + 1]
        elif item == r'"latitude":':
            business[q]['lat'] = temp[index + 1]
        elif item == r'"longitude":':
            business[q]['long'] = temp[index + 1]
        elif item == r'"categories":':
            business[q]['cat'] = []
            j = index + 1
            while temp[j] != r'"city":':
                business[q]['cat'].append(temp[j].strip('\"')) 
                j+= 1
    q += 1


print('business done!')

    
tokenizer = RegexpTokenizer(r'(?<="text": )".*"(?=, "type":)|"[^"]+":*|(?<="stars": )\d|(?<="funny": )\d+|(?<="useful": )\d+|(?<="cool": )\d+')
review = dict()

#pulls information for reviews
file = open('yelp_academic_dataset_review.json', 'rt')
q = 0
jjj = 0
for line in file:
    
    temp = tokenizer.tokenize(line)
    review[q] = dict()
    for index,item in enumerate(temp):
        if item == r'"business_id":':
            review[q]['b_id'] = temp[index + 1].strip('\"')
        elif item == r'"user_id":':
            review[q]['u_id'] = temp[index + 1].strip('\"')
        elif item == r'"text":':
            
            trash = tokeit.tokenize(temp[index + 1]) 
            for zzz in stopstuff:
                while zzz in trash:
                    trash.remove(zzz)
            thingy = ""
            for i, www in enumerate(trash):
                trash[i] = stemmer.stem(www)
                thingy = thingy + " " + trash[i]
            
                
            review[q]['text'] = thingy
        elif item == r'"stars":':
            review[q]['stars'] = temp[index + 1]
        elif item == r'"date":':
            review[q]['date'] = temp[index + 1].strip('\"')
        elif item == r'"votes":':
            review[q]['funny'] = temp[index + 2]
            review[q]['useful'] = temp[index + 4]
            review[q]['cool'] = temp[index + 6]
    q += 1
print('review done!') 


'''
tokenizer = RegexpTokenizer(r'"[^"]+":*|(?<=_stars": )\d.\d+|(?<="funny": )\d+|(?<="useful": )\d+|(?<="cool": )\d+|(?<="fans": )\d+|(?<=_count": )\d+')
user = dict()
file = open('yelp_academic_dataset_user.json', 'rt')
q = 0
for line in file:
    temp = tokenizer.tokenize(line)
    user[q] = dict()
    for index,item in enumerate(temp):
        if item == r'"user_id":':
            user[q]['u_id'] = temp[index + 1].strip('\"')
        elif item == r'"average_stars":':
            user[q]['stars'] = temp[index + 1]
        elif item == r'"review_count":':
            user[q]['count'] = temp[index + 1]
        elif item == r'"fans":':
            user[q]['fans'] = temp[index + 1]
        elif item == r'"yelping_since":':
            user[q]['join'] = temp[index + 1].strip('\"')
        elif item == r'"votes":':
            user[q]['funny'] = temp[index + 2]
            user[q]['useful'] = temp[index + 4]
            user[q]['cool'] = temp[index + 6]
    q += 1  
print('user done!')  

tokenizer = RegexpTokenizer(r'(?<="text": )".*"(?=, "business_id":)|"[^"]+":*|(?<="likes": )\d+')
tip = dict()
file = open('yelp_academic_dataset_tip.json', 'rt')
q = 0
for line in file:
    temp = tokenizer.tokenize(line)
    tip[q] = dict()
    for index,item in enumerate(temp):
        if item == r'"user_id":':
            tip[q]['u_id'] = temp[index + 1].strip('\"')
        elif item == r'"business_id":':
            tip[q]['b_id'] = temp[index + 1].strip('\"')
        elif item == r'"likes":':
            tip[q]['likes'] = temp[index + 1]
        elif item == r'"date":':
            tip[q]['date'] = temp[index + 1].strip('\"')
        elif item == r'"text":':
            
            trash = tokeit.tokenize(temp[index + 1]) 
            for zzz in stopstuff:
                while zzz in trash:
                    trash.remove(zzz)
            thingy = ""
            for i, www in enumerate(trash):
                trash[i] = stemmer.stem(www)
                thingy = thingy + " " + trash[i]
            
                
            tip[q]['text'] = thingy
            
    q += 1  
print('tip done!')   

tokenizer = RegexpTokenizer(r'"[^"]+":*|(?<="\d-\d": )\d+|(?<="\d\d-\d": )\d+')
check = dict()
file = open('yelp_academic_dataset_checkin.json', 'rt')
q = 0
regexp = re.compile(r'"\d+-\d"')
for line in file:
    temp = tokenizer.tokenize(line)
    check[q] = dict()
    check[q]['check'] = 0
    for index,item in enumerate(temp):
        if item == r'"business_id":':
            check[q]['b_id'] = temp[index + 1].strip('\"')
        elif regexp.search(item) is not None:
            check[q]['check'] += int(temp[index + 1])
    q += 1  

print('checkin done!') 
for item in business[1]:
    print(business[1][item])
for item in review[1]:
    print(review[1][item])
for item in user[1]:
    print(user[1][item])
for item in tip[1]:
    print(tip[1][item])
for item in check[1]:
    print(check[1][item])
    

for q in range (1, 20):
    for item in business[q]:
        print(business[q][item])
'''
#rewrites and trims down the business json as a cvs  
with open('business.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    for q, qqq in enumerate(business):
        sup = 0
        for key, item in enumerate(business[q]['cat']):
            sup += 1
        temp = []
        temp.append(business[q]['b_id'])
        temp.append(business[q]['state'])
        temp.append(business[q]['stars'])
        temp.append(business[q]['count'])
        temp.append(business[q]['lat'])
        temp.append(business[q]['long'])
        temp.append(sup)
        for key, item in enumerate(business[q]['cat']):
            temp.append(item)
        a.writerow(temp)

#rewrites and trims down the review json as a cvs 
#after time consuming opperations like stemming and 
#using those regular expressions 
with open('review.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    for q, qqq in enumerate(review):
        print(q)
        temp = []
        temp.append(review[q]['b_id'])
        temp.append(review[q]['u_id'])
        temp.append(review[q]['stars'])
        temp.append(review[q]['date'])
        temp.append(review[q]['funny'])
        temp.append(review[q]['useful'])
        temp.append(review[q]['cool'])
        temp.append(review[q]['text'].lower())
        a.writerow(temp) 

'''

with open('user.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    for q, qqq in enumerate(user):
        print(q)
        temp = []
        temp.append(user[q]['u_id'])
        temp.append(user[q]['stars'])
        temp.append(user[q]['count'])
        temp.append(user[q]['fans'])
        temp.append(user[q]['join'])
        temp.append(user[q]['funny'])
        temp.append(user[q]['useful'])
        temp.append(user[q]['cool'])
        a.writerow(temp) 
  
   
with open('tip.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    for q, qqq in enumerate(tip):
        print(q)
        temp = []
        temp.append(tip[q]['b_id'])
        temp.append(tip[q]['u_id'])
        temp.append(tip[q]['date'])
        temp.append(tip[q]['likes'])
        temp.append(tip[q]['text'])
        a.writerow(temp)
      
      
with open('check.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    for q, qqq in enumerate(check):
        print(q)
        temp = []
        temp.append(check[q]['b_id'])
        temp.append(check[q]['check'])
        a.writerow(temp)
'''
    
    