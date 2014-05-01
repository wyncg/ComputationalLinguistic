Python 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> import nltk
>>> from nltk.corpus import brown
>>> text = brown.tagged_words()
>>> text
[('The', 'AT'), ('Fulton', 'NP-TL'), ...]
>>> data = nltk.FreqDist(word for (word, tag) in text)
>>> data
<FreqDist with 56057 samples and 1161192 outcomes>
>>> data['cut'].keys()

Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    data['cut'].keys()
AttributeError: 'int' object has no attribute 'keys'
>>> data['cut']
180
>>> data[0]
0
>>> data[1]
0
>>> data = nltk.ConditionalFreqDist((word, tag) in text)

Traceback (most recent call last):
  File "<pyshell#10>", line 1, in <module>
    data = nltk.ConditionalFreqDist((word, tag) in text)
NameError: name 'word' is not defined
>>> data = nltk.ConditionalFreqDist((word.lower(), tag) for (word, tag) in text)
>>> data
<ConditionalFreqDist with 49815 conditions>
>>> data = nltk.ConditionalFreqDist((word, tag) for (word, tag) in text)
>>> data
<ConditionalFreqDist with 56057 conditions>
>>> for i in range(1,11):
	print i
	print 'tag(s):'
	count = 0
	for word in data.conditions():
		if len(data[word]) == i:
			count = count + 1
	print count
	print '\n'

	
1
tag(s):
47328


2
tag(s):
7186


3
tag(s):
1146


4
tag(s):
265


5
tag(s):
87


6
tag(s):
27


7
tag(s):
12


8
tag(s):
1


9
tag(s):
1


10
tag(s):
2


>>> maxlen = 0
>>> for word in data.conditions(): 
	if len(data[word]) >= maxlen:
		maxword = word
		maxlen = len(data[word])

		
>>> maxlen
12
>>> maxword
'that'
>>> for word in data.conditions():
	if len(data[word]) == 12:
		print word

		
that
>>> brown.tagged_sent()

Traceback (most recent call last):
  File "<pyshell#32>", line 1, in <module>
    brown.tagged_sent()
AttributeError: 'CategorizedTaggedCorpusReader' object has no attribute 'tagged_sent'
>>> brown.tagged_sents()
[[('The', 'AT'), ('Fulton', 'NP-TL'), ('County', 'NN-TL'), ('Grand', 'JJ-TL'), ('Jury', 'NN-TL'), ('said', 'VBD'), ('Friday', 'NR'), ('an', 'AT'), ('investigation', 'NN'), ('of', 'IN'), ("Atlanta's", 'NP$'), ('recent', 'JJ'), ('primary', 'NN'), ('election', 'NN'), ('produced', 'VBD'), ('``', '``'), ('no', 'AT'), ('evidence', 'NN'), ("''", "''"), ('that', 'CS'), ('any', 'DTI'), ('irregularities', 'NNS'), ('took', 'VBD'), ('place', 'NN'), ('.', '.')], [('The', 'AT'), ('jury', 'NN'), ('further', 'RBR'), ('said', 'VBD'), ('in', 'IN'), ('term-end', 'NN'), ('presentments', 'NNS'), ('that', 'CS'), ('the', 'AT'), ('City', 'NN-TL'), ('Executive', 'JJ-TL'), ('Committee', 'NN-TL'), (',', ','), ('which', 'WDT'), ('had', 'HVD'), ('over-all', 'JJ'), ('charge', 'NN'), ('of', 'IN'), ('the', 'AT'), ('election', 'NN'), (',', ','), ('``', '``'), ('deserves', 'VBZ'), ('the', 'AT'), ('praise', 'NN'), ('and', 'CC'), ('thanks', 'NNS'), ('of', 'IN'), ('the', 'AT'), ('City', 'NN-TL'), ('of', 'IN-TL'), ('Atlanta', 'NP-TL'), ("''", "''"), ('for', 'IN'), ('the', 'AT'), ('manner', 'NN'), ('in', 'IN'), ('which', 'WDT'), ('the', 'AT'), ('election', 'NN'), ('was', 'BEDZ'), ('conducted', 'VBN'), ('.', '.')], ...]
>>> data['that'].keys()
['CS', 'DT', 'WPS', 'WPO', 'QL', 'DT-NC', 'WPS-NC', 'CS-NC', 'WPS-HL', 'CS-HL', 'NIL', 'WPO-NC']
>>> brown.tagged_sents[0]

Traceback (most recent call last):
  File "<pyshell#35>", line 1, in <module>
    brown.tagged_sents[0]
TypeError: 'instancemethod' object has no attribute '__getitem__'
>>> brown.tagged_sents(0)

Traceback (most recent call last):
  File "<pyshell#36>", line 1, in <module>
    brown.tagged_sents(0)
  File "D:\tools\python\lib\site-packages\nltk\corpus\reader\tagged.py", line 211, in tagged_sents
    self, self._resolve(fileids, categories), simplify_tags)
  File "D:\tools\python\lib\site-packages\nltk\corpus\reader\tagged.py", line 150, in tagged_sents
    for (fileid, enc) in self.abspaths(fileids, True)])
  File "D:\tools\python\lib\site-packages\nltk\corpus\reader\api.py", line 167, in abspaths
    paths = [self._root.join(f) for f in fileids]
TypeError: 'int' object is not iterable
>>> list(brown.tagged_sents())[0]
[('The', 'AT'), ('Fulton', 'NP-TL'), ('County', 'NN-TL'), ('Grand', 'JJ-TL'), ('Jury', 'NN-TL'), ('said', 'VBD'), ('Friday', 'NR'), ('an', 'AT'), ('investigation', 'NN'), ('of', 'IN'), ("Atlanta's", 'NP$'), ('recent', 'JJ'), ('primary', 'NN'), ('election', 'NN'), ('produced', 'VBD'), ('``', '``'), ('no', 'AT'), ('evidence', 'NN'), ("''", "''"), ('that', 'CS'), ('any', 'DTI'), ('irregularities', 'NNS'), ('took', 'VBD'), ('place', 'NN'), ('.', '.')]
>>> data['that'].keys()[0]
'CS'
>>> thatlist = data['that'].keys()
>>> thatlist
['CS', 'DT', 'WPS', 'WPO', 'QL', 'DT-NC', 'WPS-NC', 'CS-NC', 'WPS-HL', 'CS-HL', 'NIL', 'WPO-NC']
>>> numlist = []
>>> testlist = [1,2]
>>> testlist
[1, 2]
>>> for i in range(1,3) and i not in testlist:
	print i

	

Traceback (most recent call last):
  File "<pyshell#56>", line 1, in <module>
    for i in range(1,3) and i not in testlist:
TypeError: 'bool' object is not iterable
>>> for taggedsents in list(brown.tagged_sents()):
	for i in range (0, 12):
		if i in numlist:
			continue
		if ('that', data['that'].keys()[i]) in taggedsents:
			print 'that/'
			print data['that'].keys()[i]
			print ': '
			print taggedsents
			numlist.append(i)
			if len(numlist) == 12:
				break

			
that/
CS
: 
[('The', 'AT'), ('Fulton', 'NP-TL'), ('County', 'NN-TL'), ('Grand', 'JJ-TL'), ('Jury', 'NN-TL'), ('said', 'VBD'), ('Friday', 'NR'), ('an', 'AT'), ('investigation', 'NN'), ('of', 'IN'), ("Atlanta's", 'NP$'), ('recent', 'JJ'), ('primary', 'NN'), ('election', 'NN'), ('produced', 'VBD'), ('``', '``'), ('no', 'AT'), ('evidence', 'NN'), ("''", "''"), ('that', 'CS'), ('any', 'DTI'), ('irregularities', 'NNS'), ('took', 'VBD'), ('place', 'NN'), ('.', '.')]
that/
WPS
: 
[('Regarding', 'IN'), ("Atlanta's", 'NP$'), ('new', 'JJ'), ('multi-million-dollar', 'JJ'), ('airport', 'NN'), (',', ','), ('the', 'AT'), ('jury', 'NN'), ('recommended', 'VBD'), ('``', '``'), ('that', 'CS'), ('when', 'WRB'), ('the', 'AT'), ('new', 'JJ'), ('management', 'NN'), ('takes', 'VBZ'), ('charge', 'NN'), ('Jan.', 'NP'), ('1', 'CD'), ('the', 'AT'), ('airport', 'NN'), ('be', 'BE'), ('operated', 'VBN'), ('in', 'IN'), ('a', 'AT'), ('manner', 'NN'), ('that', 'WPS'), ('will', 'MD'), ('eliminate', 'VB'), ('political', 'JJ'), ('influences', 'NNS'), ("''", "''"), ('.', '.')]
that/
DT
: 
[('``', '``'), ('Actually', 'RB'), (',', ','), ('the', 'AT'), ('abuse', 'NN'), ('of', 'IN'), ('the', 'AT'), ('process', 'NN'), ('may', 'MD'), ('have', 'HV'), ('constituted', 'VBN'), ('a', 'AT'), ('contempt', 'NN'), ('of', 'IN'), ('the', 'AT'), ('Criminal', 'JJ-TL'), ('court', 'NN-TL'), ('of', 'IN-TL'), ('Cook', 'NP'), ('county', 'NN'), (',', ','), ('altho', 'CS'), ('vindication', 'NN'), ('of', 'IN'), ('the', 'AT'), ('authority', 'NN'), ('of', 'IN'), ('that', 'DT'), ('court', 'NN'), ('is', 'BEZ'), ('not', '*'), ('the', 'AT'), ('function', 'NN'), ('of', 'IN'), ('this', 'DT'), ('court', 'NN'), ("''", "''"), (',', ','), ('said', 'VBD'), ('Karns', 'NP'), (',', ','), ('who', 'WPS'), ('is', 'BEZ'), ('a', 'AT'), ('City', 'NN-TL'), ('judge', 'NN'), ('in', 'IN'), ('East', 'JJ-TL'), ('St.', 'NP-TL'), ('Louis', 'NP-TL'), ('sitting', 'VBG'), ('in', 'IN'), ('Cook', 'NP-TL'), ('County', 'NN-TL'), ('court', 'NN-TL'), ('.', '.')]
that/
QL
: 
[('While', 'CS'), ('the', 'AT'), ('city', 'NN'), ('council', 'NN'), ('suggested', 'VBD'), ('that', 'CS'), ('the', 'AT'), ('Legislative', 'JJ-TL'), ('Council', 'NN-TL'), ('might', 'MD'), ('perform', 'VB'), ('the', 'AT'), ('review', 'NN'), (',', ','), ('Mr.', 'NP'), ('Notte', 'NP'), ('said', 'VBD'), ('that', 'QL'), ('instead', 'RB'), ('he', 'PPS'), ('will', 'MD'), ('take', 'VB'), ('up', 'RP'), ('the', 'AT'), ('matter', 'NN'), ('with', 'IN'), ('Atty.', 'NN-TL'), ('Gen.', 'JJ-TL'), ('J.', 'NP'), ('Joseph', 'NP'), ('Nugent', 'NP'), ('to', 'TO'), ('get', 'VB'), ('``', '``'), ('the', 'AT'), ('benefit', 'NN'), ('of', 'IN'), ('his', 'PP$'), ('views', 'VBZ'), ("''", "''"), ('.', '.')]
that/
WPO
: 
[('He', 'PPS'), ('was', 'BEDZ'), ('able', 'JJ'), ('to', 'TO'), ('smell', 'VB'), ('a', 'AT'), ('bargain', 'NN'), ('--', '--'), ('and', 'CC'), ('a', 'AT'), ('masterpiece', 'NN'), ('--', '--'), ('a', 'AT'), ('continent', 'NN'), ('away', 'RB'), (',', ','), ('and', 'CC'), ('the', 'AT'), ('Museum', 'NN-TL'), ('of', 'IN-TL'), ('Modern', 'JJ-TL'), ("Art's", 'NN$-TL'), ('Alfred', 'NP'), ('Barr', 'NP'), ('said', 'VBD'), ('of', 'IN'), ('him', 'PPO'), (':', ':'), ('``', '``'), ('I', 'PPSS'), ('have', 'HV'), ('never', 'RB'), ('mentioned', 'VBN'), ('a', 'AT'), ('new', 'JJ'), ('artist', 'NN'), ('that', 'WPO'), ('Thompson', 'NP'), ("didn't", 'DOD*'), ('know', 'VB'), ('about', 'IN'), ("''", "''"), ('.', '.')]
that/
CS-HL
: 
[('According', 'IN'), ('to', 'IN'), ('the', 'AT'), ('official', 'JJ'), ('interpretation', 'NN'), ('of', 'IN'), ('the', 'AT'), ('Charter', 'NN-TL'), (',', ','), ('a', 'AT'), ('member', 'NN'), ('cannot', 'MD*'), ('be', 'BE'), ('penalized', 'VBN'), ('by', 'IN'), ('not', '*'), ('having', 'HVG'), ('the', 'AT'), ('right', 'NN'), ('to', 'TO'), ('vote', 'VB'), ('in', 'IN'), ('the', 'AT'), ('General', 'JJ-TL'), ('Assembly', 'NN-TL'), ('for', 'IN'), ('nonpayment', 'NN'), ('of', 'IN'), ('financial', 'JJ'), ('obligations', 'NNS'), ('to', 'IN'), ('the', 'AT'), ('``', '``'), ('special', 'JJ'), ("''", "''"), ('United', 'VBN-TL'), ("Nations'", 'NNS$-TL'), ('budgets', 'NNS'), (',', ','), ('and', 'CC'), ('of', 'IN'), ('course', 'NN'), ('cannot', 'MD*'), ('be', 'BE'), ('expelled', 'VBN'), ('from', 'IN'), ('the', 'AT'), ('Organization', 'NN-TL'), ('(', '('), ('which', 'WDT'), ('you', 'PPSS'), ('suggested', 'VBD'), ('in', 'IN'), ('your', 'PP$'), ('editorial', 'NN'), (')', ')'), (',', ','), ('due', 'RB'), ('to', 'IN-HL'), ('the', 'AT-HL'), ('fact', 'NN-HL'), ('that', 'CS-HL'), ('there', 'EX'), ('is', 'BEZ'), ('no', 'AT'), ('provision', 'NN'), ('in', 'IN'), ('the', 'AT'), ('Charter', 'NN-TL'), ('for', 'IN'), ('expulsion', 'NN'), ('.', '.')]
that/
DT-NC
: 
[('He', 'PPS'), ('has', 'HVZ'), ('his', 'PP$'), ('own', 'JJ'), ('system', 'NN'), ('of', 'IN'), ('shorthand', 'NN'), (',', ','), ('devised', 'VBN'), ('by', 'IN'), ('abbreviations', 'NNS'), (':', ':'), ('``', '``'), ('humility', 'NN'), ("''", "''"), ('will', 'MD'), ('be', 'BE'), ('``', '``'), ('humly', 'NN-NC'), ("''", "''"), (',', ','), ('``', '``'), ('with', 'IN-NC'), ("''", "''"), ('will', 'MD'), ('be', 'BE'), ('``', '``'), ('w', 'NN'), ("''", "''"), (',', ','), ('and', 'CC'), ('``', '``'), ('that', 'DT-NC'), ("''", "''"), ('will', 'MD'), ('be', 'BE'), ('``', '``'), ('tt', 'NN'), ("''", "''"), ('.', '.')]
that/
NIL
: 
[('Thus', 'NIL'), (',', ','), ('as', 'NIL'), ('a', 'NIL'), ('development', 'NIL'), ('program', 'NIL'), ('is', 'NIL'), ('being', 'NIL'), ('launched', 'NIL'), (',', ','), ('commitments', 'NIL'), ('and', 'NIL'), ('obligations', 'NIL'), ('must', 'NIL'), ('be', 'NIL'), ('entered', 'NIL'), ('into', 'NIL'), ('in', 'NIL'), ('a', 'NIL'), ('given', 'NIL'), ('year', 'NIL'), ('which', 'NIL'), ('may', 'NIL'), ('exceed', 'NIL'), ('by', 'NIL'), ('twofold', 'NIL'), ('or', 'NIL'), ('threefold', 'NIL'), ('the', 'NIL'), ('expenditures', 'NIL'), ('to', 'NIL'), ('be', 'NIL'), ('made', 'NIL'), ('in', 'NIL'), ('that', 'NIL'), ('year', 'NIL'), ('.', '.')]
that/
WPS-NC
: 
[('In', 'IN'), ('of', 'IN-NC'), ('all', 'ABN-NC'), ('the', 'AT-NC'), ('suggestions', 'NNS-NC'), ('that', 'WPS-NC'), ('were', 'BED-NC'), ('made', 'VBN-NC'), (',', ',-NC'), ('his', 'PP$-NC'), ('was', 'BEDZ-NC'), ('the', 'AT-NC'), ('silliest', 'JJT-NC'), ('the', 'AT'), ('possessive', 'NN'), ('his', 'PP$-NC'), ('represents', 'VBZ'), ('his', 'PP$-NC'), ('suggestion', 'NN-NC'), ('and', 'CC'), ('is', 'BEZ'), ('stressed', 'VBN'), ('.', '.')]
that/
WPO-NC
: 
[('Thus', 'RB'), ('to', 'IN-NC'), ('has', 'HVZ'), ('light', 'JJ'), ('stress', 'NN'), ('both', 'ABX'), ('in', 'IN'), ('that', 'DT-NC'), ('was', 'BEDZ-NC'), ('the', 'AT-NC'), ('conclusion', 'NN-NC'), ('that', 'WPO-NC'), ('I', 'PPSS-NC'), ('came', 'VBD-NC'), ('to', 'IN-NC'), ('and', 'CC'), ('in', 'IN'), ('that', 'DT-NC'), ('was', 'BEDZ-NC'), ('the', 'AT-NC'), ('conclusion', 'NN-NC'), ('I', 'PPSS-NC'), ('came', 'VBD-NC'), ('to', 'IN-NC'), ('.', '.')]
that/
CS-NC
: 
[('But', 'CC'), ('when', 'WRB'), ('to', 'TO-NC'), ('represents', 'VBZ'), ('to', 'IN-NC'), ('consciousness', 'NN-NC'), ('in', 'IN'), ('that', 'WPS-NC'), ('was', 'BEDZ-NC'), ('the', 'AT-NC'), ('moment', 'NN-NC'), ('that', 'CS-NC'), ('I', 'PPSS-NC'), ('came', 'VBD-NC'), ('to', 'IN-NC'), (',', ','), ('and', 'CC'), ('similarly', 'RB'), ('in', 'IN'), ('that', 'WPS-NC'), ('was', 'BEDZ-NC'), ('the', 'AT-NC'), ('moment', 'NN-NC'), ('I', 'PPSS-NC'), ('came', 'VBD-NC'), ('to', 'IN-NC'), (',', ','), ('there', 'EX'), ('is', 'BEZ'), ('much', 'QL'), ('stronger', 'JJR'), ('stress', 'NN'), ('on', 'IN'), ('to', 'IN-NC'), ('.', '.')]
that/
WPS-HL
: 
[('Factors', 'NNS-HL'), ('that', 'WPS-HL'), ('inhibit', 'VB-HL'), ('learning', 'VBG-HL'), ('and', 'CC-HL'), ('lead', 'VB-HL'), ('to', 'IN-HL'), ('maladjustment', 'NN-HL')]
>>> a = 'a'
>>> a
'a'
>>> print 'hahaha'+a
hahahaa
>>> for taggedsents in list(brown.tagged_sents()):
	for i in range (0, 12):
		if i in numlist:
			continue
		if ('that', data['that'].keys()[i]) in taggedsents:
			print 'that/'+data['that'].keys()[i]+
			print 
			print 
			print taggedsents
			numlist.append(i)
			if len(numlist) == 12:
				break
KeyboardInterrupt
>>> for taggedsents in list(brown.tagged_sents()):
	for i in range (0, 12):
		if i in numlist:
			continue
		if ('that', data['that'].keys()[i]) in taggedsents:
			print 'that/'+data['that'].keys()[i]+': '
			print taggedsents
			numlist.append(i)
			if len(numlist) == 12:
				break

			
>>> numlist = []
>>> for taggedsents in list(brown.tagged_sents()):
	for i in range (0, 12):
		if i in numlist:
			continue
		if ('that', data['that'].keys()[i]) in taggedsents:
			print 'that/'+data['that'].keys()[i]+': '
			print taggedsents
			numlist.append(i)
			if len(numlist) == 12:
				break

			
that/CS: 
[('The', 'AT'), ('Fulton', 'NP-TL'), ('County', 'NN-TL'), ('Grand', 'JJ-TL'), ('Jury', 'NN-TL'), ('said', 'VBD'), ('Friday', 'NR'), ('an', 'AT'), ('investigation', 'NN'), ('of', 'IN'), ("Atlanta's", 'NP$'), ('recent', 'JJ'), ('primary', 'NN'), ('election', 'NN'), ('produced', 'VBD'), ('``', '``'), ('no', 'AT'), ('evidence', 'NN'), ("''", "''"), ('that', 'CS'), ('any', 'DTI'), ('irregularities', 'NNS'), ('took', 'VBD'), ('place', 'NN'), ('.', '.')]
that/WPS: 
[('Regarding', 'IN'), ("Atlanta's", 'NP$'), ('new', 'JJ'), ('multi-million-dollar', 'JJ'), ('airport', 'NN'), (',', ','), ('the', 'AT'), ('jury', 'NN'), ('recommended', 'VBD'), ('``', '``'), ('that', 'CS'), ('when', 'WRB'), ('the', 'AT'), ('new', 'JJ'), ('management', 'NN'), ('takes', 'VBZ'), ('charge', 'NN'), ('Jan.', 'NP'), ('1', 'CD'), ('the', 'AT'), ('airport', 'NN'), ('be', 'BE'), ('operated', 'VBN'), ('in', 'IN'), ('a', 'AT'), ('manner', 'NN'), ('that', 'WPS'), ('will', 'MD'), ('eliminate', 'VB'), ('political', 'JJ'), ('influences', 'NNS'), ("''", "''"), ('.', '.')]
that/DT: 
[('``', '``'), ('Actually', 'RB'), (',', ','), ('the', 'AT'), ('abuse', 'NN'), ('of', 'IN'), ('the', 'AT'), ('process', 'NN'), ('may', 'MD'), ('have', 'HV'), ('constituted', 'VBN'), ('a', 'AT'), ('contempt', 'NN'), ('of', 'IN'), ('the', 'AT'), ('Criminal', 'JJ-TL'), ('court', 'NN-TL'), ('of', 'IN-TL'), ('Cook', 'NP'), ('county', 'NN'), (',', ','), ('altho', 'CS'), ('vindication', 'NN'), ('of', 'IN'), ('the', 'AT'), ('authority', 'NN'), ('of', 'IN'), ('that', 'DT'), ('court', 'NN'), ('is', 'BEZ'), ('not', '*'), ('the', 'AT'), ('function', 'NN'), ('of', 'IN'), ('this', 'DT'), ('court', 'NN'), ("''", "''"), (',', ','), ('said', 'VBD'), ('Karns', 'NP'), (',', ','), ('who', 'WPS'), ('is', 'BEZ'), ('a', 'AT'), ('City', 'NN-TL'), ('judge', 'NN'), ('in', 'IN'), ('East', 'JJ-TL'), ('St.', 'NP-TL'), ('Louis', 'NP-TL'), ('sitting', 'VBG'), ('in', 'IN'), ('Cook', 'NP-TL'), ('County', 'NN-TL'), ('court', 'NN-TL'), ('.', '.')]
that/QL: 
[('While', 'CS'), ('the', 'AT'), ('city', 'NN'), ('council', 'NN'), ('suggested', 'VBD'), ('that', 'CS'), ('the', 'AT'), ('Legislative', 'JJ-TL'), ('Council', 'NN-TL'), ('might', 'MD'), ('perform', 'VB'), ('the', 'AT'), ('review', 'NN'), (',', ','), ('Mr.', 'NP'), ('Notte', 'NP'), ('said', 'VBD'), ('that', 'QL'), ('instead', 'RB'), ('he', 'PPS'), ('will', 'MD'), ('take', 'VB'), ('up', 'RP'), ('the', 'AT'), ('matter', 'NN'), ('with', 'IN'), ('Atty.', 'NN-TL'), ('Gen.', 'JJ-TL'), ('J.', 'NP'), ('Joseph', 'NP'), ('Nugent', 'NP'), ('to', 'TO'), ('get', 'VB'), ('``', '``'), ('the', 'AT'), ('benefit', 'NN'), ('of', 'IN'), ('his', 'PP$'), ('views', 'VBZ'), ("''", "''"), ('.', '.')]
that/WPO: 
[('He', 'PPS'), ('was', 'BEDZ'), ('able', 'JJ'), ('to', 'TO'), ('smell', 'VB'), ('a', 'AT'), ('bargain', 'NN'), ('--', '--'), ('and', 'CC'), ('a', 'AT'), ('masterpiece', 'NN'), ('--', '--'), ('a', 'AT'), ('continent', 'NN'), ('away', 'RB'), (',', ','), ('and', 'CC'), ('the', 'AT'), ('Museum', 'NN-TL'), ('of', 'IN-TL'), ('Modern', 'JJ-TL'), ("Art's", 'NN$-TL'), ('Alfred', 'NP'), ('Barr', 'NP'), ('said', 'VBD'), ('of', 'IN'), ('him', 'PPO'), (':', ':'), ('``', '``'), ('I', 'PPSS'), ('have', 'HV'), ('never', 'RB'), ('mentioned', 'VBN'), ('a', 'AT'), ('new', 'JJ'), ('artist', 'NN'), ('that', 'WPO'), ('Thompson', 'NP'), ("didn't", 'DOD*'), ('know', 'VB'), ('about', 'IN'), ("''", "''"), ('.', '.')]
that/CS-HL: 
[('According', 'IN'), ('to', 'IN'), ('the', 'AT'), ('official', 'JJ'), ('interpretation', 'NN'), ('of', 'IN'), ('the', 'AT'), ('Charter', 'NN-TL'), (',', ','), ('a', 'AT'), ('member', 'NN'), ('cannot', 'MD*'), ('be', 'BE'), ('penalized', 'VBN'), ('by', 'IN'), ('not', '*'), ('having', 'HVG'), ('the', 'AT'), ('right', 'NN'), ('to', 'TO'), ('vote', 'VB'), ('in', 'IN'), ('the', 'AT'), ('General', 'JJ-TL'), ('Assembly', 'NN-TL'), ('for', 'IN'), ('nonpayment', 'NN'), ('of', 'IN'), ('financial', 'JJ'), ('obligations', 'NNS'), ('to', 'IN'), ('the', 'AT'), ('``', '``'), ('special', 'JJ'), ("''", "''"), ('United', 'VBN-TL'), ("Nations'", 'NNS$-TL'), ('budgets', 'NNS'), (',', ','), ('and', 'CC'), ('of', 'IN'), ('course', 'NN'), ('cannot', 'MD*'), ('be', 'BE'), ('expelled', 'VBN'), ('from', 'IN'), ('the', 'AT'), ('Organization', 'NN-TL'), ('(', '('), ('which', 'WDT'), ('you', 'PPSS'), ('suggested', 'VBD'), ('in', 'IN'), ('your', 'PP$'), ('editorial', 'NN'), (')', ')'), (',', ','), ('due', 'RB'), ('to', 'IN-HL'), ('the', 'AT-HL'), ('fact', 'NN-HL'), ('that', 'CS-HL'), ('there', 'EX'), ('is', 'BEZ'), ('no', 'AT'), ('provision', 'NN'), ('in', 'IN'), ('the', 'AT'), ('Charter', 'NN-TL'), ('for', 'IN'), ('expulsion', 'NN'), ('.', '.')]
that/DT-NC: 
[('He', 'PPS'), ('has', 'HVZ'), ('his', 'PP$'), ('own', 'JJ'), ('system', 'NN'), ('of', 'IN'), ('shorthand', 'NN'), (',', ','), ('devised', 'VBN'), ('by', 'IN'), ('abbreviations', 'NNS'), (':', ':'), ('``', '``'), ('humility', 'NN'), ("''", "''"), ('will', 'MD'), ('be', 'BE'), ('``', '``'), ('humly', 'NN-NC'), ("''", "''"), (',', ','), ('``', '``'), ('with', 'IN-NC'), ("''", "''"), ('will', 'MD'), ('be', 'BE'), ('``', '``'), ('w', 'NN'), ("''", "''"), (',', ','), ('and', 'CC'), ('``', '``'), ('that', 'DT-NC'), ("''", "''"), ('will', 'MD'), ('be', 'BE'), ('``', '``'), ('tt', 'NN'), ("''", "''"), ('.', '.')]
that/NIL: 
[('Thus', 'NIL'), (',', ','), ('as', 'NIL'), ('a', 'NIL'), ('development', 'NIL'), ('program', 'NIL'), ('is', 'NIL'), ('being', 'NIL'), ('launched', 'NIL'), (',', ','), ('commitments', 'NIL'), ('and', 'NIL'), ('obligations', 'NIL'), ('must', 'NIL'), ('be', 'NIL'), ('entered', 'NIL'), ('into', 'NIL'), ('in', 'NIL'), ('a', 'NIL'), ('given', 'NIL'), ('year', 'NIL'), ('which', 'NIL'), ('may', 'NIL'), ('exceed', 'NIL'), ('by', 'NIL'), ('twofold', 'NIL'), ('or', 'NIL'), ('threefold', 'NIL'), ('the', 'NIL'), ('expenditures', 'NIL'), ('to', 'NIL'), ('be', 'NIL'), ('made', 'NIL'), ('in', 'NIL'), ('that', 'NIL'), ('year', 'NIL'), ('.', '.')]
that/WPS-NC: 
[('In', 'IN'), ('of', 'IN-NC'), ('all', 'ABN-NC'), ('the', 'AT-NC'), ('suggestions', 'NNS-NC'), ('that', 'WPS-NC'), ('were', 'BED-NC'), ('made', 'VBN-NC'), (',', ',-NC'), ('his', 'PP$-NC'), ('was', 'BEDZ-NC'), ('the', 'AT-NC'), ('silliest', 'JJT-NC'), ('the', 'AT'), ('possessive', 'NN'), ('his', 'PP$-NC'), ('represents', 'VBZ'), ('his', 'PP$-NC'), ('suggestion', 'NN-NC'), ('and', 'CC'), ('is', 'BEZ'), ('stressed', 'VBN'), ('.', '.')]
that/WPO-NC: 
[('Thus', 'RB'), ('to', 'IN-NC'), ('has', 'HVZ'), ('light', 'JJ'), ('stress', 'NN'), ('both', 'ABX'), ('in', 'IN'), ('that', 'DT-NC'), ('was', 'BEDZ-NC'), ('the', 'AT-NC'), ('conclusion', 'NN-NC'), ('that', 'WPO-NC'), ('I', 'PPSS-NC'), ('came', 'VBD-NC'), ('to', 'IN-NC'), ('and', 'CC'), ('in', 'IN'), ('that', 'DT-NC'), ('was', 'BEDZ-NC'), ('the', 'AT-NC'), ('conclusion', 'NN-NC'), ('I', 'PPSS-NC'), ('came', 'VBD-NC'), ('to', 'IN-NC'), ('.', '.')]
that/CS-NC: 
[('But', 'CC'), ('when', 'WRB'), ('to', 'TO-NC'), ('represents', 'VBZ'), ('to', 'IN-NC'), ('consciousness', 'NN-NC'), ('in', 'IN'), ('that', 'WPS-NC'), ('was', 'BEDZ-NC'), ('the', 'AT-NC'), ('moment', 'NN-NC'), ('that', 'CS-NC'), ('I', 'PPSS-NC'), ('came', 'VBD-NC'), ('to', 'IN-NC'), (',', ','), ('and', 'CC'), ('similarly', 'RB'), ('in', 'IN'), ('that', 'WPS-NC'), ('was', 'BEDZ-NC'), ('the', 'AT-NC'), ('moment', 'NN-NC'), ('I', 'PPSS-NC'), ('came', 'VBD-NC'), ('to', 'IN-NC'), (',', ','), ('there', 'EX'), ('is', 'BEZ'), ('much', 'QL'), ('stronger', 'JJR'), ('stress', 'NN'), ('on', 'IN'), ('to', 'IN-NC'), ('.', '.')]
that/WPS-HL: 
[('Factors', 'NNS-HL'), ('that', 'WPS-HL'), ('inhibit', 'VB-HL'), ('learning', 'VBG-HL'), ('and', 'CC-HL'), ('lead', 'VB-HL'), ('to', 'IN-HL'), ('maladjustment', 'NN-HL')]
>>> 
