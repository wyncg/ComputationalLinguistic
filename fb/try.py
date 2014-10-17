from __future__ import division
import csv
from itertools import islice, izip
from collections import Counter

filename = "D:/UMD/INST735/project/training_release_unfiltered.csv"
reader = csv.reader(open(filename))



#put together (stopwords stemming lowercase charonly)
dictauthor = {}

for author, status, time, n, gender,neu in reader:
    if (author == "userid"):
        continue
    else:
        if author in dictauthor:
            status = re.sub("-"," ",status)
            status = re.sub("[^((A-Za-z)| )]","",status) #charonly
            status = re.sub("[.?!,:;()[]{}/\@#$%^&*_=+~]","",status) #charonly
            #stopwords
            splitedstatus = status.lower().split()
            stemmed = []#stemming
            for word in splitedstatus:
                if word in nltk.corpus.stopwords.words('english'): 
                    splitedstatus.remove(word)
                else:
                    stemmed.append(stem(word))
            strstatus = " ".join(stemmed)
            dictauthor[author][0] = dictauthor[author][0] + " " + strstatus
        else:
            status = re.sub("-"," ",status)
            status = re.sub("[^((A-Za-z)| )]","",status) #charonly
            status = re.sub("[.?!,:;()[]{}/\@#$%^&*_=+~]","",status) #charonly
            splitedstatus = status.lower().split()
            stemmed = []
            for word in splitedstatus:
                if word in nltk.corpus.stopwords.words('english'): 
                    splitedstatus.remove(word)
                else:
                    stemmed.append(stem(word))
            strstatus = " ".join(stemmed)
            dictauthor[author] = [strstatus,gender]
        




#output

csvfile = file('resultfortest.csv','wb')
writer = csv.writer(csvfile)
writer.writerow(['author','status','gender'])
data = []
for (k,v) in dictauthor.items():
    data.append((k,v[0],v[1]))
writer.writerows(data)
csvfile.close()
print "done"







"""
#traindata author neu
dictauthor = {}
for author, status, time, n, gender, neu in reader:
    if (author == "userid"):
        continue
    else:
        if author in dictauthor:
            continue
        else:
            dictauthor[author] = neu
csvfile = file('neu.csv','wb')
writer = csv.writer(csvfile)
writer.writerow(['author','neuro'])
data = []
for (k,v) in dictauthor.items():
    data.append((k,v))
writer.writerows(data)
csvfile.close()
print "done"            

"""


"""
#bi sort
sortedbi = {}
bi = {}
for biword, count in reader:
    if (biword == "biword"):
        continue
    else:
        bi[biword] = float(count)


a = sorted(bi.items(), key=lambda d: d[1])

bisorted = file('bisorted.csv','wb')
writer = csv.writer(bisorted)

for i in range(1,10000):
    writer.writerow(a[i])
    writer.writerow(a[-i])
writer.writerow(a[0])            
print "done"
bisorted.close()
#filename = "D:/UMD/INST735/project/biresult.csv"
"""


tempstatus = ""
tempauthor = ""
tempgender = ""
tempneuro = ""
#unigram bigram for R
gramcsvforR = file('gramforR.csv','wb')
writer = csv.writer(gramcsvforR)
for author, status, gender in reader:
    if (author == "author"):
        continue
    else:
        
        if (gender == ""):
            tempstatus = status
            tempauthor = author
            continue
        elif (len(author)) > 40:
            uniforR = {}
            biforR = {}
            unicount = 0
            bicount = 0
            authordata = []
            tempstatus += author
            tempgender = status
            tempneuro = gender
            authordata.append(tempauthor)
            authordata.append(tempgender)
            authordata.append(tempneuro)
            splited = tempstatus.split()
            for word in splited:
                unicount += 1
                if word in uniforR:
                    uniforR[word] += 1
                else:
                    uniforR[word] = 1
            #bicnt = Counter(izip(splited, islice(splited, 1, None)))
            #for bi in bicnt.keys():
            #    bicount += bicnt[bi]
            #    if bi in biforR:
            #        biforR[bi] += bicnt[bi]
            #    else:
            #        biforR[bi] = bicnt[bi]
            filename = "D:/UMD/INST735/project/unipart.csv" #need to redifine everytime
            dictunidiff = csv.DictReader(file(filename,'rb'))
            #filename = "D:/UMD/INST735/project/bipart.csv"
            #dictbidiff = csv.DictReader(file(filename,'rb'))
            for row in dictunidiff:
                if row["uniword"] in uniforR:
                    authordata.append(float(row["count"])*uniforR[row["uniword"]]/unicount)
                else:
                    authordata.append(0)
            #for row in dictbidiff:
            #    if row["biword"] in biforR:
            #        authordata.append(float(row["count"])*biforR[row["biword"]]/bicount)
            #    else:
            #        authordata.append(0)
            writer.writerow(authordata)
        else:
        
            uniforR = {}
            biforR = {}
            unicount = 0
            bicount = 0
            authordata = []
            authordata.append(author)
            authordata.append(gender)
            authordata.append(neuro)
            splited = status.split()
            for word in splited:
                unicount += 1
                if word in uniforR:
                    uniforR[word] += 1
                else:
                    uniforR[word] = 1
            #bicnt = Counter(izip(splited, islice(splited, 1, None)))
            #for bi in bicnt.keys():
            #    bicount += bicnt[bi]
            #    if bi in biforR:
            #        biforR[bi] += bicnt[bi]
            #    else:
            #        biforR[bi] = bicnt[bi]
            filename = "D:/UMD/INST735/project/unipart.csv" #need to redifine everytime
            dictunidiff = csv.DictReader(file(filename,'rb'))
            #filename = "D:/UMD/INST735/project/bipart.csv"
            #dictbidiff = csv.DictReader(file(filename,'rb'))
            for row in dictunidiff:
                if row["uniword"] in uniforR:
                    authordata.append(float(row["count"])*uniforR[row["uniword"]]/unicount)
                else:
                    authordata.append(0)
            #for row in dictbidiff:
            #    if row["biword"] in biforR:
            #        authordata.append(float(row["count"])*biforR[row["biword"]]/bicount)
            #    else:
            #        authordata.append(0)
            writer.writerow(authordata)
            

gramcsvforR.close()
print "done"
             
