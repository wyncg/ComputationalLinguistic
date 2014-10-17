#Yining Wang 112569631
# -*- coding: cp936 -*-
import re
import csv

def singlepub(singlepub):#extract single pub info
#single pub
    ignore = re.compile("(\[3\])|(\[3)|(3\])")
    remove = re.compile("[\)\(\}\{]")
    removeb = re.compile("[\[\]]")
    singlepub = remove.sub("",singlepub)
    singlepub=re.sub(r'(numero|plus minus)','', singlepub)
    flag = 0
    tempatt = []
    
    tempdict = {"Time:":"","EDCS-ID:":"","Publication:":"","Province:":"","Place:":""}
    attribute = ""
    tempcon = []
    place = []
    tempID = []
    for char in singlepub:
        if (flag == 0):#find publication
            if (char == "*"):
                tempdict[attribute] = "".join(tempcon)
                tempcon = []
                tempatt = []
                flag = 1
                continue
            else:
                tempcon.append(char)
                continue
        elif (flag == 1):#find pub, province, ID
            if (char != "*"):
                tempatt.append(char)
                continue
            else:
                flag = 0
                attribute = "".join(tempatt)
                if (attribute == "Place:"):
                    tempdict[attribute] = ""
                    flag = 2
                continue
        elif (flag == 2):#find place
            if (char != "/" and tempdict[attribute] != ("" or " ")):
                tempcon.append(char)
                continue
            else:
                tempdict[attribute] = "".join(tempcon)
                flag = 3
                continue
        else:#find time
            if (char != "\n"):
                place.append(char)
            else:
                place.append(" ")
            tempdict["Time:"] = "".join(place)

    for char in tempdict["Publication:"]:
        if (char != "="):
            tempID.append(char)
        else:
            tempdict["Publication:"] = "".join(tempID)
            break
    
    try:
        if ignore.search(tempdict["Time:"]):
            tempdict["Time:"] = ""
        else:
            tempdict["Time:"] = removeb.sub("",tempdict["Time:"])
    except KeyError:
        None
    return tempdict    



def dealtime(text):
    if (text == ""):
        return ""
    else:
        totalspan = []
        cat = ""
        marriage = re.compile("(cum qua vix)|(cum quo vix)")
        vixit = re.compile("(vixit)|(vixsit)")
        mili = re.compile("militavit")
        splited = text.split(" ")
        for i in range(0,len(splited)):
            span = [] #[Y, M, D, H, C]
            cat = ""
            if ((vixit.search(splited[i])) and (splited[i-1] != "quo" and splited[i-1] != "qua")):
                span = gettime(i,splited)
                span.append("L")
                totalspan.append(span)
            elif (mili.search(splited[i])):
                span = gettime(i,splited)
                span.append("Mi")
                totalspan.append(span)
            elif (i+2 < len(splited)):
                if (splited[i] == "cum" and (splited[i+1] == "qua" or splited[i+1] == "quo") and vixit.search(splited[i+2])):
                    span = gettime(i+2,splited)
                    span.append("Ma")
                    totalspan.append(span)
                
                
    return totalspan


def gettime(index, textlist):
    if (index + 8 >= len(textlist)):
        text = textlist[index:]
    else:
        text = textlist[index:index + 8]
    marriage = re.compile("(cum qua vix)|(cum quo vix)")
    vixit = re.compile("(vixit)|(vixsit)")
    mili = re.compile("militavit")
    text = " ".join(text)
    year=re.findall(r'(annis|anno|annos|annum) ?([DCLXVI]+)',text)
    month=re.findall(r'(mensibus|menses|mensem) ?([DCLXVI]+)',text)
    day=re.findall(r'(diebus|dies|diem) ?([DCLXVI]+)',text)
    hour=re.findall(r'(horis|horas|hora|horam) ?([DCLXVI]+)',text)
    y = 0
    m = 0
    d = 0
    h = 0
    if year != []:
        y = from_roman(year[0][1])
    if month != []:
        m = from_roman(month[0][1])
    if day != []:
        d = from_roman(day[0][1])
    if hour != []:
        h = from_roman(hour[0][1])
    
    return [y,m,d,h]


def from_roman(s):#http://hi.baidu.com/qianyuanke/item/3ca0051dfcc1fd0a1894ec9d
    if not roman_numeral_pattern.search(s):
        return 99999
    result = 0
    index = 0
    for numeral, integer in roman_numeral_map:
        while s[index:index+len(numeral)] == numeral:
            result += integer;
            index += len(numeral)
    return result



def processfile(filename):
#open file
    f = open(filename)          
    alldata = f.read()            
    lines = alldata.splitlines()
    flag = 0
    p = re.compile("\*Publication:\*")
    ignore = re.compile("(\[3\])|(\[3)|(3\])")

#get each pub
    data = []
    for line in lines:
        if (flag == 0):
            if (p.match(line)):
                flag = 1
                #if ignore.match(line):
                #    continue
                #else:
                data.append(line)
                continue
            else:
                continue   
        else:
            if (p.match(line)):
                data.append(line)
                continue
            else:
                data.append(data.pop() + line)

#output
    
    for eachdata in data:
        info = singlepub(eachdata)
        
        timeinfo = dealtime(info["Time:"]) #[[YMDHC]]
        
        for time in timeinfo:
            tempinfo = []
            tempinfo.append(info["EDCS-ID:"])
            tempinfo.append(info["Publication:"])
            tempinfo.append(info["Province:"])
            tempinfo.append(info["Place:"])
            tempinfo.append(time[0])
            tempinfo.append(time[1])
            tempinfo.append(time[2])
            tempinfo.append(time[3])
            tempinfo.append(time[4])
            writer.writerow(tempinfo)       

    
    f.close()

csvfile = file('sample_output.csv','wb')
writer = csv.writer(csvfile)

writer.writerow(["ID","Publication","Province","Place","Year","Month","Day","Hour","Class"])
#roman
roman_numeral_map = (('M',1000),
                     ('CM',900),
                     ('D',500),
                     ('CD',400),
                     ('C',100),
                     ('XC',90),
                     ('L',50),
                     ('XL',40),
                     ('X',10),
                     ('IX',9),
                     ('V',5),
                     ('IV',4),
                     ('I',1))
roman_numeral_pattern = re.compile('^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})', re.VERBOSE)


processfile("hour")
processfile("hours")
csvfile.close()
print "done"


#test = singlepub(data[2])["Time:"]
#print test
#t = dealtime(singlepub(data[2])["Time:"])
#print t

#dealtime(singlepub(data[2])["Time:"])




   



