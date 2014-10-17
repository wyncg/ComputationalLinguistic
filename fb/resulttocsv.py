from __future__ import division
import csv


#result to csv
filename = "D:/UMD/INST735/project/1210avg100GI.csv"
reader = csv.reader(open(filename))
csvfile = file('faith.csv','wb')
writer = csv.writer(csvfile)
pos = {}
pos["+"] = ""
for author, neu, ksvm in reader:
    if (neu == "+"):
        if (pos["+"] == ""):
            pos["+"] = author
        else:
            pos["+"] = pos["+"] + " " + author
writer.writerow(['class','predictions'])
data = []
for (k,v) in pos.items():
    data.append((k,v))
writer.writerows(data)
csvfile.close()
print "done"


"""
#complete random row
filename = "D:/UMD/INST735/project/1_train_avg100GI.csv"
dictf = csv.DictReader(file(filename,'rb'))
filename = "D:/UMD/INST735/project/trainhh.csv"
dicthh = csv.DictReader(file(filename,'rb'))
added = file('added.csv','wb')
writer = csv.writer(added)
for rowhh in dicthh: 
    for row in dictf:
        if (row["Author"] == rowhh["Author"]):
            data = []
            for i in range (1,28):
                a = "GI" + str(i)
                data.append(float(row[a]))
    writer.writerow(data)
added.close()
print "done"   
"""

"""
#features sum to 1 
filename = "D:/UMD/INST735/project/testdataGIforR1.csv"
dictf = csv.DictReader(file(filename,'rb'))
n = []

for row in dictf:
    count = 0
    for i in range(1,28):
        a = "GI" + str(i)
        count = count + float(row[a])
    n.append(count)

norfeature = file('testnorGIforR.csv','wb')
writer = csv.writer(norfeature)
dictf = csv.DictReader(file(filename,'rb'))
t = 0
for row in dictf:
    norfea = []
    for i in range(1,28):
        a = "GI" + str(i)
        try:
            norfea.append(float(row[a])/float(n[t]))
        except ZeroDivisionError:
            norfea.append(0)
    t = t + 1
    writer.writerow(norfea)
norfeature.close()
print "done"
"""
