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
node = []
decision = dict()

trained = 0
tip = dict()
user = dict()
review = dict()
business = dict()
sample = dict()
totalReviews = 0
revWithWord = dict()
tfidf = dict()
scores = dict()
lowceiling = 0
highfloor = 0
high = 0
low = 0
mid = 0
stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
initialmonths = 18


#imports the business id's of the sample data
file = open('sample.csv', 'rt')
reader = csv.reader(file)
for row in reader:
    sample[row[1]] = row[2]         
file.close()


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
                                    #r1     - 8
                                    #s1     - 9
                                    #r2    - 10
                                    #s2     - 11
                                    #conglom - 12
                                    #rank   - 13
    
    
file.close()

'''
file = open('user.csv', 'rt')
reader = csv.reader(file)
for row in reader:
    #a1 = dict()
    #a2 = dict()
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
suma = 0

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
    #business[row[0]][6][row[1]] = temp
    #temp.pop(6)
    #temp.append(row[0]) #b_id   - 6
    #user[row[1]][7].append(temp)
    #user[row[1]][7][row[0]] = temp
                        #matrix - 7
    
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
    #business[row[0]][7][row[1]] = temp
    temp.pop(3)
    temp.append(row[0]) #b_id   - 3
    user[row[1]][8].append(temp)
    #user[row[1]][8][row[0]] = temp
    
file.close()
'''

errorcount = 0


#this block creates hashtables for the words in every review
flag = 0
masterDict = dict()
for key, value in enumerate(business):
    if value in sample:
        s1 = 0
        r1 = 0
        s2 = 0
        r2 = 0
        for key1, value1 in enumerate(business[value][6]):
            '''
            if value in sample:
                thedate = business[value][6][key1][1].split("-", 2)
            
                time = int(thedate[0]) * 12 + int(thedate[1])
                if time < int(sample[value]) + initialmonths:
                    s1 += int(business[value][6][key1][0])
                    r1 += 1
                else:
                    s2 += int(business[value][6][key1][0])
                    r2 += 1
            else:'''
            s1 += int(business[value][6][key1][0])
            r1 += 1
            s2 += int(business[value][6][key1][0])
            r2 += 1
            
            totalReviews += 1
            theDict = dict()
            textline = business[value][6][key1][5].split(" ")
            for word in textline:
                if word != "":
                    if word in theDict:
                        theDict[word] += 1
                    else:
                        theDict[word] = 1
                    if word in masterDict:
                        masterDict[word] += 1
                    else:
                        masterDict[word] = 1
            business[value][6][key1].append(theDict)
            for key2, word in enumerate(theDict):
                if word in revWithWord:
                    revWithWord[word] += 1
                else:
                    revWithWord[word] = 1
        '''    
        if r1 == 0:
            errorcount += 1
            print(value)
            print(value1)
            print(float(int(sample[value])/12))
            print()
           
        if flag < 10:
            print(value)
            print(value1)
            print(sample[value])
            for key2, value2 in enumerate(business[value][6]):
                print(business[value][6][value2][1])'''
            
            
        business[value].append(r1)
        if r1 == 0:
            business[value].append(0)
        else:
            business[value].append(float(s1/r1))
            
        business[value].append(r2)
        if r2 == 0:
            business[value].append(0)
        else:
            business[value].append(float(s2/r2))
        

#make a conglomerate tfidf for each business
#I chose to do it this way because having a tfidf for each review
#is just to much data to try and crunch
for key, value in enumerate(sample):
    cong = dict()
    for key1, value1 in enumerate(business[value][6]):
        thedate = business[value][6][key1][1].split("-", 2)
        time = int(thedate[0]) * 12 + int(thedate[1]) 
        if (business[value][6][key1][7] and time <= int(sample[value]) + initialmonths):
            
            for key2, value2 in enumerate(business[value][6][key1][7]): 
                if value2 in cong:
                    cong[value2] += business[value][6][key1][7][value2]
                else:
                    cong[value2] = business[value][6][key1][7][value2]
    business[value].append(cong)

#create the tfidf vector for each individual review
flag = 0
for key, value in enumerate(sample):
    for key1, value1 in enumerate(business[value][6]):
        if (business[value][6][key1][7]):
            for key2, value2 in enumerate(business[value][6][key1][7]):
                business[value][6][key1][7][value2] = (1 + math.log10(business[value][6][key1][7][value2])) * math.log10(totalReviews / revWithWord[value2])
                
'''         
#normalize the tfidf vector    
for key, value in enumerate(sample):
    for key1, value1 in enumerate(business[value][6]):
        tempsum = 0
        for key2, value2 in enumerate(business[value][6][key1][7]): 
            tempsum += business[value][6][key1][7][value2] ** 2
        tempsum = math.sqrt(tempsum)
        for key2, value2 in enumerate(business[value][6][key1][7]):
            business[value][6][key1][7][value2] = business[value][6][key1][7][value2] / tempsum
'''           

#normalize the tfidf conglomerate vectors  
for key, value in enumerate(sample):
    tempsum = 0
    for key1, value1 in enumerate(business[value][12]):
        tempsum += business[value][12][value1] ** 2
    tempsum = math.sqrt(tempsum)
    for key1, value1 in enumerate(business[value][12]):
        business[value][12][value1] = business[value][12][value1] / tempsum
  
#separate the business into categories of success
#business are crudely score by multiplying average reviews with log10(number of reviews)
for key, value in enumerate(sample):
    scores[value] = math.log10(business[value][10]) * business[value][11]
    #scores[value] = business[value][11]

    
#business are classified as
#0 - bottom 33%
#1 - middles 33%
#2 - top 33%
results = sorted(scores.items(), key=lambda x: x[1])
lowceiling = results[round(len(sample)/3)][1]
highfloor = results[2 * round(len(sample)/3)][1]        


for x in range(0, round(len(sample)/3) + 1):
    business[results[x][0]].append(0)
    low += 1
for x in range( round(len(sample)/3) + 1, 2 * round(len(sample)/3)):
    business[results[x][0]].append(1)
    mid += 1
for x in range(2 * round(len(sample)/3) , len(sample)):
    business[results[x][0]].append(2)
    high += 1

'''
print()
print(lowceiling)
print(highfloor)
print(low)  
print(mid)
print(high) 
''' 
      
def cossim(dict1, dict2):
    similarity = 0
    #crossproduct of the file tfidf vectors
    for word in dict1:
        if word in dict2:
            similarity += dict1[word] * dict2[word]
    return similarity

def squery(qstring):
    global sample, business, low, mid, high
    stringity = ""
    tokencount = dict()
    score = []
    for  j in range(0, 3):
        score.append(0)
    tokens = tokenizer.tokenize(qstring)
    for i, item in enumerate(tokens):
        tokens[i] = (stemmer.stem(item)).lower()
    for item in tokens:
        if item in tokencount:
            tokencount[item] += 1
        else:
            tokencount[item] = 1
    for word in tokencount:
        if word in revWithWord:
            tokencount[word] = (1 + math.log10(tokencount[word])) * math.log10(totalReviews / revWithWord[word])
        else:
            tokencount[word] = 0
    tempsum = 0
    for word in tokencount:
        tempsum += tokencount[word] ** 2
    tempsum = math.sqrt(tempsum)
    for word in tokencount:        
        tokencount[word] = tokencount[word] / tempsum    
    
    for key, value in enumerate(sample):
        score[business[value][13]] += cossim(tokencount, business[value][12])
    score[0] = score[0] / low
    score[1] = score[1] / mid
    score[2] = score[2] / high
    stringity += str(score[0])
    stringity += " "
    stringity += str(score[1])
    stringity += " "
    stringity += str(score[2])
    stringity += " "
    if trained == 1:
        if score[0] <= node[0]:
            if score[1] <= node[1]:
                if score[2] <= node[3]:
                    val = decision[0][0]
                else:
                    val = decision[0][1]
            else:
                if score[2] <= node[4]:
                    val = decision[1][0]
                else:
                    val = decision[1][1]
        else:
            if score[1] <= node[2]:
                if score[2] <= node[5]:
                    val = decision[2][0]
                else:
                    val = decision[2][1]
            else:
                if score[2] <= node[6]:
                    val = decision[3][0]
                else:
                    val = decision[3][1]
    else:
        if max(score) == score[0]:
            val = 0
        elif max(score) == score[1]:
            val = 1
        else:
            val = 2
        
                
                
    if (val == 0):
        print("Estimation: negative")
    elif (val == 1):
        print("Estimation: nuetral")
    else :
        print("Estimation: positive")
    return val

def getdata():
    global sample, business, low, mid, high
    sample1 = sample.copy()
    results = dict()
    correct = 0
    total = 0
    for key, value in enumerate(sample):
        results[value] = []
        score = []
        for  j in range(0, 3):
            score.append(0)
        for key1, value1 in enumerate(sample1):
            score[business[value1][13]] += cossim(business[value1][12], business[value][12])
        results[value].append(score[0])
        results[value].append(score[1])
        results[value].append(score[2])
        results[value].append(business[value][13])
        if max(score) == score[0]:
            temp = 0
        elif max(score) == score[1]:
            temp = 1
        else:
            temp = 2
        if temp == business[value][13]:
            correct += 1
            print(value)
        total += 1
    '''    
    print("correct: " + str(correct))
    print("total:   " + str(total))
    '''
    return results        

#attempts to classify a specific business 
#b_id is the business id, such as 'KayYbHCt-RkbGcPdGOThNg'
def bidquery(b_id):
    global sample, business, low, mid, high, lowceiling, highfloor
    stringity = ""
    temprev = 0
    tempavg = 0
    score = []
    for  j in range(0, 3):
        score.append(0) 
    
    theDict = dict()    
    for key1, value1 in enumerate(business[b_id][6]):
        temprev += 1
        tempavg += int(business[b_id][6][key1][0])
        textline = business[b_id][6][key1][5].split(" ")
        for word in textline:
            if word != "":
                if word in theDict:
                    theDict[word] += 1
                else:
                    theDict[word] = 1
                    
                   
        
        
    for key, value in enumerate(sample):
        score[business[value][13]] += cossim(business[value][12], theDict)
    score[0] = score[0] / low
    score[1] = score[1] / mid
    score[2] = score[2] / high
    stringity += str(score[0])
    stringity += " "
    stringity += str(score[1])
    stringity += " "
    stringity += str(score[2])
    stringity += " "
    if trained == 1:
        if score[0] <= node[0]:
            if score[1] <= node[1]:
                if score[2] <= node[3]:
                    val = decision[0][0]
                else:
                    val = decision[0][1]
            else:
                if score[2] <= node[4]:
                    val = decision[1][0]
                else:
                    val = decision[1][1]
        else:
            if score[1] <= node[2]:
                if score[2] <= node[5]:
                    val = decision[2][0]
                else:
                    val = decision[2][1]
            else:
                if score[2] <= node[6]:
                    val = decision[3][0]
                else:
                    val = decision[3][1]
    else:
        if max(score) == score[0]:
            val = 0
        elif max(score) == score[1]:
            val = 1
        else:
            val = 2
        
                
                
    if (val == 0):
        print("Estimation: poor")
    elif (val == 1):
        print("Estimation: average")
    else :
        print("Estimation: successful")
    if temprev == 0:
        temprev = 1
    tempscore = math.log10(temprev) * (tempavg/temprev)
    #tempscore = (tempavg/temprev)
    if tempscore == 0:
        val2 = 0
        print("Actual: unknown")
    elif (tempscore <= lowceiling):
        val2 = 0
        print("Actual: poor")
    elif (tempscore >= highfloor):
        val2 = 2
        print("Actual: successful")
    else:
        val2 = 1
        print("Actual: average")
    if val == val2:
        return True
    else:
        return False
    
#attempts to classify all the training data
def testsample():
    global sample, business, low, mid, high, decision, node, trained
    total = 0
    correct = 0
    
    
    
    for key, value in enumerate(sample):
        total += 1
        if (bidquery(value) == True):
            correct += 1
        
    print("correct: " + str(correct))
    print("total: " + str(total))
 
#attempts to classify the first 'interger' business    
def testdata(integer):
    global sample, business, low, mid, high, decision, node, trained
    total = 0
    correct = 0
    counter = 0
    
    for key, value in enumerate(business):
        total += 1
        if (bidquery(value) == True):
            correct += 1
        counter += 1
        if counter >= integer:
            break
    
    print("correct: " + str(correct))
    print("total: " + str(total))
       
#this attempts to produce a functional decision tree
#after running train(), bidquery starts using the decision tree
#this also causestestdata() and sampledata() to use the tree      
def train():
    global sample, business, low, mid, high, decision, node, trained
    results = getdata()
    split0 = 0
    split1_0 = 0
    split1_1 = 0
    split2_0 = 0
    split2_1 = 0
    split2_2 = 0
    split2_3 = 0

    trained = 1
    
    best = 100
    for key, value in enumerate(results):
        tempGini = 1
        counter = []
        counter.append(0)
        counter.append(0)
        counter.append(0)
        for key1, value1 in enumerate(results):
            if results[value1][0] <= results[value][0]:
                counter[results[value1][3]] += 1
        tempGini -= (counter[0]/low) ** 2
        tempGini -= (counter[1]/mid) ** 2
        tempGini -= (counter[2]/high) ** 2
        if tempGini < best:
            best = tempGini
            split0 = results[value][0]
            
    best = 100
    totalcounter = []
    totalcounter.append(0)
    totalcounter.append(0)
    totalcounter.append(0)
    for key, value in enumerate(results):
        tempGini = 1
        if (results[value][0] <= split0 ):
            counter = []
            counter.append(0)
            counter.append(0)
            counter.append(0)
            for key1, value1 in enumerate(results):
                if results[value1][0] <= split0:
                    totalcounter[results[value1][3]] += 1
                    if results[value1][1] <= results[value][1]:
                        counter[results[value1][3]] += 1
            tempGini -= (counter[0]/totalcounter[0]) ** 2
            tempGini -= (counter[1]/totalcounter[1]) ** 2
            tempGini -= (counter[2]/totalcounter[2]) ** 2
        if tempGini < best:
            best = tempGini
            split1_0 = results[value][0]
            
    best = 100
    totalcounter = []
    totalcounter.append(0)
    totalcounter.append(0)
    totalcounter.append(0)
    for key, value in enumerate(results):
        tempGini = 1
        if (results[value][0] > split0 ):
            counter = []
            counter.append(0)
            counter.append(0)
            counter.append(0)
            for key1, value1 in enumerate(results):
                if results[value1][0] > split0:
                    totalcounter[results[value1][3]] += 1
                    if results[value1][1] <= results[value][1]:
                        counter[results[value1][3]] += 1
            tempGini -= (counter[0]/totalcounter[0]) ** 2
            tempGini -= (counter[1]/totalcounter[1]) ** 2
            tempGini -= (counter[2]/totalcounter[2]) ** 2
        if tempGini < best:
            best = tempGini
            split1_1 = results[value][0]
            
    best = 100
    totalcounter = []
    totalcounter.append(0)
    totalcounter.append(0)
    totalcounter.append(0)
    for key, value in enumerate(results):
        tempGini = 1
        if (results[value][0] <= split0 and results[value][1] <= split1_0):
            counter = []
            counter.append(0)
            counter.append(0)
            counter.append(0)
            for key1, value1 in enumerate(results):
                if results[value1][0] <= split0 and results[value1][1] <= split1_0:
                    totalcounter[results[value1][3]] += 1
                    if results[value1][2] <= results[value][2]:
                        counter[results[value1][3]] += 1
            tempGini -= (counter[0]/totalcounter[0]) ** 2
            tempGini -= (counter[1]/totalcounter[1]) ** 2
            tempGini -= (counter[2]/totalcounter[2]) ** 2
        if tempGini < best:
            best = tempGini
            split2_0 = results[value][0]
    if counter[0] == max(counter):
        temp1 = 0
    elif counter[1] == max(counter):
        temp1 = 1  
    else:
        temp1 = 2    
    if totalcounter[0] - counter[0] >= totalcounter[1] - counter[1]:
        if totalcounter[0] - counter[0] >= totalcounter[2] - counter[2]: 
            temp2 = 0
        else:
            temp2 = 2
    elif totalcounter[1] - counter[1] >= totalcounter[2] - counter[2]:
        temp2 = 1
    else:
        temp2 = 2
    decision[0] = [temp1, temp2]
            
            
    best = 100
    totalcounter = []
    totalcounter.append(0)
    totalcounter.append(0)
    totalcounter.append(0)
    for key, value in enumerate(results):
        tempGini = 1
        if (results[value][0] <= split0 and results[value][1] > split1_0):
            counter = []
            counter.append(0)
            counter.append(0)
            counter.append(0)
            for key1, value1 in enumerate(results):
                if results[value1][0] <= split0 and results[value1][1] > split1_0:
                    totalcounter[results[value1][3]] += 1
                    if results[value1][2] <= results[value][2]:
                        counter[results[value1][3]] += 1
            tempGini -= (counter[0]/totalcounter[0]) ** 2
            tempGini -= (counter[1]/totalcounter[1]) ** 2
            tempGini -= (counter[2]/totalcounter[2]) ** 2
        if tempGini < best:
            best = tempGini
            split2_1 = results[value][0]
    if counter[0] == max(counter):
        temp1 = 0
    elif counter[1] == max(counter):
        temp1 = 1  
    else:
        temp1 = 2    
    if totalcounter[0] - counter[0] >= totalcounter[1] - counter[1]:
        if totalcounter[0] - counter[0] >= totalcounter[2] - counter[2]: 
            temp2 = 0
        else:
            temp2 = 2
    elif totalcounter[1] - counter[1] >= totalcounter[2] - counter[2]:
        temp2 = 1
    else:
        temp2 = 2
    decision[1] = [temp1, temp2]

            
    best = 100
    totalcounter = []
    totalcounter.append(0)
    totalcounter.append(0)
    totalcounter.append(0)
    for key, value in enumerate(results):
        tempGini = 1
        if (results[value][0] > split0 and results[value][1] <= split1_1):
            counter = []
            counter.append(0)
            counter.append(0)
            counter.append(0)
            for key1, value1 in enumerate(results):
                if results[value1][0] > split0 and results[value1][1] <= split1_1:
                    totalcounter[results[value1][3]] += 1
                    if results[value1][2] <= results[value][2]:
                        counter[results[value1][3]] += 1
            tempGini -= (counter[0]/totalcounter[0]) ** 2
            tempGini -= (counter[1]/totalcounter[1]) ** 2
            tempGini -= (counter[2]/totalcounter[2]) ** 2
        if tempGini < best:
            best = tempGini
            split2_2 = results[value][0]
    if counter[0] == max(counter):
        temp1 = 0
    elif counter[1] == max(counter):
        temp1 = 1  
    else:
        temp1 = 2    
    if totalcounter[0] - counter[0] >= totalcounter[1] - counter[1]:
        if totalcounter[0] - counter[0] >= totalcounter[2] - counter[2]: 
            temp2 = 0
        else:
            temp2 = 2
    elif totalcounter[1] - counter[1] >= totalcounter[2] - counter[2]:
        temp2 = 1
    else:
        temp2 = 2
    decision[2] = [temp1, temp2]
            
    best = 100
    totalcounter = []
    totalcounter.append(0)
    totalcounter.append(0)
    totalcounter.append(0)
    for key, value in enumerate(results):
        tempGini = 1
        if (results[value][0] > split0 and results[value][1] > split1_1):
            counter = []
            counter.append(0)
            counter.append(0)
            counter.append(0)
            for key1, value1 in enumerate(results):
                if results[value1][0] > split0 and results[value1][1] > split1_1:
                    totalcounter[results[value1][3]] += 1
                    if results[value1][2] <= results[value][2]:
                        counter[results[value1][3]] += 1
            tempGini -= (counter[0]/totalcounter[0]) ** 2
            tempGini -= (counter[1]/totalcounter[1]) ** 2
            tempGini -= (counter[2]/totalcounter[2]) ** 2
        if tempGini < best:
            best = tempGini
            split2_3 = results[value][0]
    if counter[0] == max(counter):
        temp1 = 0
    elif counter[1] == max(counter):
        temp1 = 1  
    else:
        temp1 = 2    
    if totalcounter[0] - counter[0] >= totalcounter[1] - counter[1]:
        if totalcounter[0] - counter[0] >= totalcounter[2] - counter[2]: 
            temp2 = 0
        else:
            temp2 = 2
    elif totalcounter[1] - counter[1] >= totalcounter[2] - counter[2]:
        temp2 = 1
    else:
        temp2 = 2
    decision[3] = [temp1, temp2]            
     
     
    node.append(split0)
    node.append(split1_0)
    node.append(split1_1)
    node.append(split2_0)
    node.append(split2_1)
    node.append(split2_2)
    node.append(split2_3)
    print("node")
    print(node)
    print()
    print("dec")
    print(decision)

            
    





       