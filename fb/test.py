from __future__ import division
import csv
import dateutil.parser as timeparser
import nltk
from stemming.porter2 import stem
import re
from itertools import islice, izip
from collections import Counter


filename = "D:/UMD/INST735/project/resulttest.csv"
reader = csv.reader(open(filename))


"""
#put together (stopwords stemming lowercase charonly)
dictauthor = {}

for author, status, time, n, gender, neu in reader:
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
            splitedstatus = status.lower().split()
            stemmed = []
            for word in splitedstatus:
                if word in nltk.corpus.stopwords.words('english'): 
                    splitedstatus.remove(word)
                else:
                    stemmed.append(stem(word))
            strstatus = " ".join(stemmed)
            dictauthor[author] = [strstatus,gender,neu]
        




#output

csvfile = file('resultfortest.csv','wb')
writer = csv.writer(csvfile)
writer.writerow(['author','status','gender','neuro'])
data = []
for (k,v) in dictauthor.items():
    data.append((k,v[0],v[1],v[2]))
writer.writerows(data)
csvfile.close()
print "done"
"""



#unigram bigram
filename = "D:/UMD/INST735/project/resulttest.csv"
reader = csv.reader(open(filename))
unigrampos = {}
unigramneg = {}
bigrampos = {}
bigramneg = {}
unipos = 0
unineg = 0
bipos = 0
bineg = 0
temp = ""
for author, status, gender, neu in reader:
    if (author == "author"):
        continue
    else:
        if (gender == ""):
            temp = status
            continue
        elif (len(author) > 40):
            temp = temp + author
            splited = temp.split()
            for word in splited:
                if (gender == "+"):
                    unipos += 1
                    if word in unigrampos:
                        unigrampos[word] += 1
                    else:
                        unigrampos[word] = 1
                else:
                    unineg += 1
                    if word in unigramneg:
                        unigramneg[word] += 1
                    else:
                        unigramneg[word] = 1
            bicnt = Counter(izip(splited, islice(splited, 1, None)))
            for bi in bicnt.keys():
                if (gender == "+"):
                    if bi in bigrampos:
                        bigrampos[bi] += bicnt[bi]
                        bipos += bicnt[bi]
                    else:
                        bigrampos[bi] = bicnt[bi]
                        bipos += bicnt[bi]
                else:
                    if bi in bigramneg:
                        bigramneg[bi] += bicnt[bi]
                        bineg += bicnt[bi]
                    else:
                        bigramneg[bi] = bicnt[bi]
                        bineg += bicnt[bi]
        else:
            splited = status.split()
            for word in splited:
                if (neu == "+"):
                    unipos += 1
                    if word in unigrampos:
                        unigrampos[word] += 1
                    else:
                        unigrampos[word] = 1
                else:
                    unineg += 1
                    if word in unigramneg:
                        unigramneg[word] += 1
                    else:
                        unigramneg[word] = 1
            bicnt = Counter(izip(splited, islice(splited, 1, None)))
            for bi in bicnt.keys():
                if (neu == "+"):
                    if bi in bigrampos:
                        bigrampos[bi] += bicnt[bi]
                        bipos += bicnt[bi]
                    else:
                        bigrampos[bi] = bicnt[bi]
                        bipos += bicnt[bi]
                else:
                    if bi in bigramneg:
                        bigramneg[bi] += bicnt[bi]
                        bineg += bicnt[bi]
                    else:
                        bigramneg[bi] = bicnt[bi]
                        bineg += bicnt[bi]
            


#pos - neg
unidiff = {}

for word in unigrampos.keys():
	if (unigramneg.has_key(word)):
		unidiff[word] = [(unigrampos[word]/unipos)/(unigramneg[word]/unineg),(unigrampos[word]/unipos),(unigramneg[word]/unineg)]
#	else:
#		unidiff[word] = 999999

#for word in unigramneg.keys():
#	if (unidiff.has_key(word)):
#		continue
#	else:
#		unidiff[word] = 0

bidiff = {}
for bi in bigrampos.keys():
	if (bigramneg.has_key(bi)):
		bidiff[bi] = [(bigrampos[bi]/bipos)/(bigramneg[bi]/bineg),(bigrampos[bi]/bipos),(bigramneg[bi]/bineg)]
#	else:
#		continue

#for bi in bigramneg.keys():
#	if (bidiff.has_key(bi)):
#		continue
#	else:
#		bidiff[bi] = 0


#print sorted(unidiff.items(),lambda x,y: cmp(x[1],y[1]),reverse = True)
#print sorted(bidiff.items(),lambda x,y: cmp(x[1],y[1]),reverse = True)
unicsvfile = file('uniresultfortrain.csv','wb')
writer = csv.writer(unicsvfile)
writer.writerow(['uniword','count'])
data = []
for (k,v) in unidiff.items():
    data.append((k,v[0],v[1],v[2]))
writer.writerows(data)
unicsvfile.close()
print "done"

bicsvfile = file('biresultfortrain.csv','wb')
writer = csv.writer(bicsvfile)
writer.writerow(['biword','count'])
data = []
for (k,v) in bidiff.items():
    data.append((k,v[0],v[1],v[2]))
writer.writerows(data)
bicsvfile.close()
print "done"




"""
#record time
authortime = {}
findtime = [19,20,21,22,23,0,1,2,8,10]
p = re.compile("(\d{4})-(\d+)-(\d+)(\s+)(\d+):(\d+):?(\d*)")
#p = re.compile("(\d{4})/(\d+)/(\d+)(\s+)(\d+):(\d+):?(\d*)")
for author, status, time, n, gender, neu in reader:
    if (author == "userid"):
        continue
    elif (author not in authortime):        
        if (p.match(time)):
            authortime[author] = [1,0]
            a = timeparser.parse(time)
            if (a.hour in findtime):
                authortime[author][1] += 1 
        else:
            continue
    else:
        if (p.match(time)):
            authortime[author][0] += 1
            a = timeparser.parse(time)
            if (a.hour in findtime):
                authortime[author][1] += 1


csvfile = file('recordtime.csv','wb')
writer = csv.writer(csvfile)
writer.writerow(['author','timescore'])
data = []
for (k,v) in authortime.items():
    data.append((k,v[1]/v[0]))
writer.writerows(data)
csvfile.close()
print "done"
"""
"""
#time
dicttimeneg = {}
dicttimepos = {}
timeneg = 0
timepos = 0
#p = re.compile("(\d{4})/(\d+)/(\d+)(\s+)(\d+):(\d+):?(\d*)")
p = re.compile("(\d{4})-(\d+)-(\d+)(\s+)(\d+):(\d+):?(\d*)") 
for author, status, time, n, gender, neu in reader:
    #2009/6/21  23:49:00   
    if (p.match(time)):
        if (neu == "-"):
            timeneg += 1
            a = timeparser.parse(time)
            if a.hour in dicttimeneg:
                dicttimeneg[a.hour] += 1
            else:
                dicttimeneg[a.hour] = 1
        else:
            timepos += 1
            a = timeparser.parse(time)
            if a.hour in dicttimepos:
                dicttimepos[a.hour] += 1
            else:
                dicttimepos[a.hour] = 1
    else:
        continue
#print dicttimeneg, dicttimepos
#time diff
timediff = {}

for hour in dicttimepos.keys():
	if (dicttimeneg.has_key(hour)):
		timediff[hour] = dicttimepos[hour]/timepos - dicttimeneg[hour]/timeneg
	else:
		timediff[hour] = dicttimepos[hour]/timepos

for hour in dicttimeneg.keys():
	if (timediff.has_key(hour)):
		continue
	else:
		timediff[hour] = -dicttimeneg[hour]/timeneg

#print sorted(timediff.items(),lambda x,y: cmp(x[1],y[1]),reverse = True)

timecsvfile = file('timeresult.csv','wb')
writer = csv.writer(timecsvfile)
writer.writerow(['time','count'])
data = []
for (k,v) in timediff.items():
    data.append((k,v))
writer.writerows(data)
timecsvfile.close()
print "done"
"""


"""
dictstatus = {}
for author, status, time, n, gender in reader:
    if (author == "userid"):
        next
    else:
        if author in dictstatus:
            dictstatus[author] = dictstatus[author] + "\n" + status
        else:
            dictstatus[author] = status
        
#txt

authors = dictstatus.keys()

for author in authors:
    filename = author + ".txt"
    txtfile = open(filename,'w')
    txtfile.write(dictstatus[author])
    txtfile.close()
print "done"
"""


"""
#output
filename = author + ".txt"
csvfile = file('resulttest.csv','wb')
writer = csv.writer(csvfile)
writer.writerow(['author','status'])
data = []
for (k,v) in dictstatus.items():
    data.append((k,v))
writer.writerows(data)
csvfile.close()
print "done"
"""
