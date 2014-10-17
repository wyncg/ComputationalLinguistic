Python 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> from cl1hw.demo import shop
>>> fs = shop.FruitShop()

Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    fs = shop.FruitShop()
TypeError: __init__() takes exactly 3 arguments (1 given)
>>> fs = shop.FruitShop("Joe's", {"oranges": 3.0, "apples":1.5})
Welcome to the Joe's fruit shop
>>> fs.getCostPerPound("k")
Sorry we don't have k
>>> fs.getCostPerPound("oranges")
3.0
>>> import nltk, re
>>> sent = "Mares eat oats and does eat oats, and little lambs eat ivy; a kid'll eat ivy too, wouldn't you?"
>>> help(nltk.re_show)
Help on function re_show in module nltk.util:

re_show(regexp, string, left='{', right='}')
    Return a string with markers surrounding the matched substrings.
    Search str for substrings matching ``regexp`` and wrap the matches
    with braces.  This is convenient for learning about regular expressions.
    
    :param regexp: The regular expression.
    :type regexp: str
    :param string: The string being matched.
    :type string: str
    :param left: The left delimiter (printed before the matched substring)
    :type left: str
    :param right: The right delimiter (printed after the matched substring)
    :type right: str
    :rtype: str

>>> nltk.re_show("(oats|eat)", sent)
Mares {eat} {oats} and does {eat} {oats}, and little lambs {eat} ivy; a kid'll {eat} ivy too, wouldn't you?
>>> re.findall("(eat)", sent)
['eat', 'eat', 'eat', 'eat']
>>> re.findall("(eat|oats)", sent)
['eat', 'oats', 'eat', 'oats', 'eat', 'eat']
>>> from nltk.tokenize import WordPunctTokenizer
>>> from nltk.stem import PorterStemmer
>>> t = WordPunctTokenizer()
>>> s = PorterStemmer()
>>> t.tokenize(sent)
['Mares', 'eat', 'oats', 'and', 'does', 'eat', 'oats', ',', 'and', 'little', 'lambs', 'eat', 'ivy', ';', 'a', 'kid', "'", 'll', 'eat', 'ivy', 'too', ',', 'wouldn', "'", 't', 'you', '?']
>>> s.stem(sent)
"Mares eat oats and does eat oats, and little lambs eat ivy; a kid'll eat ivy too, wouldn't you?"
>>> [s.stem(x) for x in t.tokenize(sent)]
['Mare', 'eat', 'oat', 'and', 'doe', 'eat', 'oat', ',', 'and', 'littl', 'lamb', 'eat', 'ivi', ';', 'a', 'kid', "'", 'll', 'eat', 'ivi', 'too', ',', 'wouldn', "'", 't', 'you', '?']
>>> [s.stem(x) for x in t.tokenize(sent.lower())]
['mare', 'eat', 'oat', 'and', 'doe', 'eat', 'oat', ',', 'and', 'littl', 'lamb', 'eat', 'ivi', ';', 'a', 'kid', "'", 'll', 'eat', 'ivi', 'too', ',', 'wouldn', "'", 't', 'you', '?']
>>> [s.stem(x) for x in t.tokenize(sent.lower()) if len(x) >= 2]
['mare', 'eat', 'oat', 'and', 'doe', 'eat', 'oat', 'and', 'littl', 'lamb', 'eat', 'ivi', 'kid', 'll', 'eat', 'ivi', 'too', 'wouldn', 'you']
>>> 
