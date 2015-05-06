#Charles Jacobsen
#1000717663
#started 4/1/2015
#last edited 4/1/2015
#Data Mining 4334
#Yelp Data Challenge

import math
import random
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import csv


random.seed(666)

tip = dict()
user = dict()
review = dict()
business = dict()

#can be changed to increase or decrease the sample size
#15 means the sample size will be 1/15th the size of the data
samplefraction = 10





file = open('business.csv', 'rt')
reader = csv.reader(file)
for row in reader:
    a1 = []
    a2 = []
    business[row[0]] = []           #b_id
    business[row[0]].append(row[1]) #state - 0
    business[row[0]].append(row[2]) #stars - 1
    business[row[0]].append(row[3]) #rcount- 2
    business[row[0]].append(row[4]) #lat   - 3
    business[row[0]].append(row[5]) #long  - 4
    business[row[0]].append(row[6]) #check - 5
    business[row[0]].append(a1)     #review- 6
    business[row[0]].append(a2)     #tip   - 7
file.close()


'''
file = open('user.csv', 'rt')
reader = csv.reader(file)
for row in reader:
    a1 = []
    a2 = []
    user[row[0]] = []           #u_id
    user[row[0]].append(row[1]) #stars  - 0
    user[row[0]].append(row[2]) #rcount - 1
    user[row[0]].append(row[3]) #fans   - 2
    user[row[0]].append(row[4]) #joined - 3
    user[row[0]].append(row[5]) #funny  - 4
    user[row[0]].append(row[6]) #useful - 5
    user[row[0]].append(row[7]) #cool   - 6
    user[row[0]].append(a1)     #review - 7
    user[row[0]].append(a2)     #tip    - 8
file.close()
'''

file = open('review.csv', 'rt')
reader = csv.reader(file)
for row in reader:
    temp = []           
    temp.append(row[2]) #stars  - 0
    temp.append(row[3]) #date   - 1
    temp.append(row[4]) #funny  - 2
    temp.append(row[5]) #useful - 3
    temp.append(row[6]) #cool   - 4
    temp.append(row[7]) #text   - 5
    temp.append(row[1]) #u_id   - 6
    business[row[0]][6].append(temp)
    temp.pop(6)
    temp.append(row[0]) #b_id   - 6
    #user[row[1]][7].append(temp)
    
file.close()
'''
file = open('tip.csv', 'rt')
reader = csv.reader(file)
for row in reader:
    temp = []           
    temp.append(row[2]) #date   - 0
    temp.append(row[3]) #likes  - 1
    temp.append(row[4]) #text   - 2
    temp.append(row[1]) #u_id   - 3
    business[row[0]][7].append(temp)
    temp.pop(3)
    temp.append(row[0]) #b_id   - 3
    user[row[1]][8].append(temp)
    
file.close()

key, value = dict.popitem(business)
key1, value1 = dict.popitem(user)
print(value)
print(value1)
'''

byState = dict()
mindate = dict()


#the intention of this block was to only take businesses
#that have had reviews over at least 3 years
countable = 0
for key, value in enumerate(business):
    mini = 99999
    maxi = 0
    for key1, value1 in enumerate(business[value][6]):
  

        thedate = value1[1].split("-", 2)
        time = int(thedate[0]) * 12 + int(thedate[1])
        if time < mini:
            mini = time
        elif time > maxi:
            maxi = time            
    if (maxi - mini) >= 36:
        mindate[value] = mini
        if business[value][0] in byState:
            byState[business[value][0]].append(value)
        else:
            byState[business[value][0]] = []
            byState[business[value][0]].append(value)
            


sample = []
  

#this block randomly selects a proportional 
#number of businesses based on their state     
for key, value in enumerate(byState):
    statetotal = len(byState[value])
    countable += statetotal
    selected = 0
    #print()
    #print(value)
    
    while selected < (statetotal / samplefraction):
        for key1, value1 in enumerate(byState[value]):
            if random.randrange(1, samplefraction + 1) == 1:
                sample.append(value1)
                #print(str(key1) + " - " + str(value1))
                byState[value].pop(key1)
                selected += 1
            if selected >= (statetotal / samplefraction):
                break

#print(countable)


with open('sample.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    for q, qqq in enumerate(sample):
        print(q)
        temp = []
        temp.append(q)
        temp.append(qqq)
        temp.append(mindate[qqq])
        a.writerow(temp)
           
            
        
        
        
        
        
        