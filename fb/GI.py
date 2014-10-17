from __future__ import division
import csv
from itertools import islice, izip
from collections import Counter
import nltk
from stemming.porter2 import stem
import re

filename = "D:/UMD/INST735/project/testdata.csv"
reader = csv.reader(open(filename)) 

filename = "D:/UMD/INST735/project/stemmedGI.csv"
GIreader = csv.reader(open(filename))
GIdict = {}
for label, words in GIreader:
    if (label == "Feature"):
        continue
    else:
        GIdict[label] = []
        words = re.sub(" ","",words)
        words = re.sub("'","",words)
        splitedwords = words.split(",")
        for word in splitedwords:
            GIdict[label].append(word)
        

tempstatus = ""
tempauthor = ""
tempgender = ""
tempneuro = ""
GIcsvforR = file('testdataGIforR.csv','wb')
writer = csv.writer(GIcsvforR)

for author, status, gender, neuro in reader:
    if (author == "author"):
        continue
    else:
        if (gender == ""):
            tempstatus = status
            tempauthor = author
            continue
        elif (len(author)) > 40:
            authorGI = {}
            for label in GIdict.keys():
                authorGI[label] = 0
            GIcount = 0
            authordata = [tempauthor]
            tempstatus += author
            splited = tempstatus.split()
            for word in splited:
                GIcount += 1
                for label in GIdict.keys():
                    if word in GIdict[label]:
                        authorGI[label] += 1
            for label in GIdict.keys(): 
                authordata.append(authorGI[label]/GIcount)
            writer.writerow(authordata)
            #print sorted(authordata.items(), key=lambda d: d[0])
            
        else:
            authorGI = {}
            for label in GIdict.keys():
                authorGI[label] = 0
            GIforR = {}
            GIcount = 0
            authordata = [author]
            splited = status.split()
            for word in splited:
                GIcount += 1
                for label in GIdict.keys():
                    if word in GIdict[label]:
                        authorGI[label] += 1
            #print sorted(authordata.items(), key=lambda d: d[0])
            for label in GIdict.keys(): 
                authordata.append(authorGI[label]/GIcount)
            writer.writerow(authordata)
                
print "done"


"""
#stemmed
filename = "D:/UMD/INST735/project/inquiry_cat.csv"
reader = csv.reader(open(filename))
csvfile = file('stemmedGI.csv','wb')
writer = csv.writer(csvfile)

for feature, words in reader:
    stemmed = []
    words = re.sub(" ","",words)
    words = re.sub("'","",words)
    splitedwords = words.split(",")
    for word in splitedwords:
        stemmed.append(stem(word))
    writer.writerow((feature,stemmed))

csvfile.close()
print "done"    
""" 
