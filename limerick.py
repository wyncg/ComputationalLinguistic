# -*- coding: cp936 -*-
# Author: Yining Wang
# Date: DATE SUBMITTED

# Use word_tokenize to split raw text into words
from string import punctuation
from curses.ascii import isdigit
import nltk
from nltk.tokenize import word_tokenize
import re

class LimerickDetector:

    
    
    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()
        self._entries = nltk.corpus.cmudict.entries()

    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        s = word.lower()
        if s not in self._pronunciations:
            return 1
        else:
            return min([len([y for y in x if isdigit(y[-1])]) for x in self._pronunciations[word.lower()]])
        


    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """
        firstword = a.lower()
        secondword = b.lower()
        #take the length of syllable of two words
        firstwordlen = self.num_syllables(firstword)
        secondwordlen = self.num_syllables(secondword)
        
        #take syllable into two lists
        firstwordsyllable = [p for (w, p) in self._entries if w == firstword]
        secondwordsyllable = [p for (w, p) in self._entries if w == secondword]
        
        #if word not found in dict, return false
        #if word not found in dict, while it is a past tense(as strewed in text1), try to fix it by adding the pronounce into dict
        #while it could only handle standard past tense...
        if (len(firstwordsyllable) == 0 or len(secondwordsyllable) == 0): 
            if (len(firstwordsyllable) == 0): 
                if (list(firstword)[-2:] == ['e', 'd']):
                    firstwordnum = len(firstword)
                    presentfirstword = firstword[0:firstwordnum-2]
                    pfwsyll = [p for (w, p) in self._entries if w == presentfirstword]
                    if (len(pfwsyll) == 0):
                        return False
                    else:
                        for i in range (0, len(pfwsyll)):
                            pfwsyll[i] += "D"
                    self._pronunciations[firstword] = pfwsyll
                    firstwordsyllable = pfwsyll
                    #why cant do this? firstwordsyllable = [p for (w, p) in self._entries if w == firstword]
                else:
                    return False
            if (len(secondwordsyllable) == 0):
                if (list(secondword)[-2:] == ['e', 'd']):
                    secondwordnum = len(secondword)
                    presentsecondword = secondword[0:len(secondword)-2]
                    pswsyll = [p for (w, p) in self._entries if w == presentsecondword]
                    if (len(pswsyll) == 0):
                        return False
                    else:
                        for i in range (0, len(pswsyll)):
                            pswsyll[i] += "D"
                    self._pronunciations[secondword] = pswsyll
                    secondwordsyllable = pswsyll
                    #why cant do this? secondwordsyllable = [p for (w, p) in self._entries if w == secondword]
                else:
                    return False
        #the above code could be inclued into a function          
        
        """
        Put the sound of the shortest syllable of word a into firstwordshortestsyllable
        """
        firstwordshortestsyllable = firstwordsyllable[0]
        firstshort = []
        firstshort.append(firstwordsyllable[0])
        if len(firstwordsyllable) > 1:  
            for i in range(1, len(firstwordsyllable)):
                if len(firstwordshortestsyllable) > len(firstwordsyllable[i]):
                    firstwordshortestsyllable = firstwordsyllable[i]
            """
            The following for is to catch all the pronounciation of the shortest sound so that
            it can solve words such as "bog", that has multi shortest proun.
            """
            for i in range(0, len(firstwordsyllable)):
                if len(firstwordshortestsyllable) == len(firstwordsyllable[i]):
                    firstshort.append(firstwordsyllable[i])
                    
        """
        Put the sound of the shortest syllable of word b into secondwordshortestsyllable
        """
        secondwordshortestsyllable = secondwordsyllable[0]
        secondshort = []
        secondshort.append(secondwordsyllable[0])
        if len(secondwordsyllable) > 1:  
            for i in range(1, len(secondwordsyllable)):
                if len(secondwordshortestsyllable) > len(secondwordsyllable[i]):
                    secondwordshortestsyllable = secondwordsyllable[i]
            """
            The following for is to catch all the pronounciation of the shortest sound so that
            it can solve words such as "bog", that has multi shortest proun.
            """
            for i in range(0, len(secondwordsyllable)):
                if len(secondwordshortestsyllable) == len(secondwordsyllable[i]):
                    secondshort.append(secondwordsyllable[i])
                    
        #compare the lengthe of two words' shortest sound, then compare if they ryhme with any instances of the other's pronounciation
        if (len(firstwordshortestsyllable)< len(secondwordshortestsyllable)):
            t = len(firstwordshortestsyllable)
            # check if self._pronunciations[word][shortest][-t:] is same
            for i in range (0, len(firstshort)):
                for j in range (0, len(secondshort)):
                    if (firstshort[i][-t+1:] == secondshort[j][-t+1:]):
                        return True
            return False
                                
        else:
            t = len(secondwordshortestsyllable)
            # check if self._pronunciations[word][shortest][-t:] is same
            for i in range (0, len(secondshort)):
                for j in range (0, len(firstshort)):
                    if (secondshort[i][-t+1:] == firstshort[j][-t+1:]):
                        return True
            return False

        """# check if self._pronunciations[word][shortest][-t:] is same
        if (self._pronunciations[a][-t:] == self._pronunciations[b][-t:]):
            return True
        else:
            return False
            """

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other (and not the A
        lines).

        (English professors may disagree with this definition, but that's what
        we're using here.)
        """
        textsplit = text.split('\n')
        token = [word_tokenize(s) for s in textsplit]
        lastword = [sentence[-1] for sentence in token if len(sentence) != 0]
        #should use a function
        #handle errors like testb
        try:
            first = lastword[0]
        except IndexError:
            first = ""
        try:
            second = lastword[1]
        except IndexError:
            first = ""
        try:
            third = lastword[2]
        except IndexError:
            first = ""
        try:
            fourth = lastword[3]
        except IndexError:
            first = ""
        try:
            fifth = lastword[4]
        except IndexError:
            first = ""
            

        """
        Handle past tense
        
        edlastword = []
        for i in range (0, len(lastword)):
            if (list(lastword[i])[-2:] == ['e', 'd']):
                edlastword.append(lastword[i])
        """
        if self.rhymes(first,second) and self.rhymes(first,fifth) and self.rhymes(third,fourth):
            return True
        else:
            return False
        
    def apostrophe_tokenize(self, word):
        """
        a new function called apostrophe_tokenize that handles apostrophes
        in words correctly so that “can’t” would rhyme with “pant”.
        prondict['blog'] = [['B', 'L', 'AA1', 'G']]
        """
        
        
        """#Handle n't case
        if (list(word[-3:] == ['n', "'", 't'])):
            wordsplit = word.split("'")
        
        wordsplitpron = [p for (w, p) in self._entries if w == wordsplit[0]]
        for i in range (0, len(wordsplitpron)):
            wordsplitpron[i].append("T")
        word += "\'t"
        self._pronunciations[word] = wordsplitpron"""

        wordsplit = word.split(' ')
        apostrophetokenized = [token for token in wordsplit]
        return apostrophetokenized
        
            

    def guess_syllables(self, word):
        """
        Make reasonable guesses about the number of syllables in unknown words
        """
        word = word.lower()
        word = word.replace("'", "")#delete apostrophe
        deletefinale = re.compile('e$')
        word = deletefinale.sub('', word)#delete final e
        sylnum = 0
        #split word by vowels
        vowels = re.compile('[aeiou]+')
        wordsplit = vowels.split(word)
        sylnum = len(wordsplit)-1 #count vowel groupings

        #handel special cases (final e is deleted and not considered in re)(Collect from a perl module from CPAN)
        #sylnum + 1 when specialaddcase; - 1 when specialsubcase
        specialsubcase = ['cial','tia','cius','cious','giu','ion$','iou','sia$','.ely$']
        specialaddcase = ['ia','riet','dien','iu','io','ii','[aeiouym]bl$', '[aeiou]{3}', '^mc', 'ism$', '([^aeiouy]{2})l$','[^l]lien','^coa[dglx].', '[^gq]ua[^auieo]','dnt$']
        subre = []
        for i in range (0, len(specialsubcase)):
            subre.append(re.compile(specialsubcase[i]))
        addre = []
        for i in range (0, len(specialaddcase)):
            addre.append(re.compile(specialaddcase[i]))
        for i in range (0, len(subre)):
            if re.search(subre[i], word):
                sylnum -= 1
        for i in range (0, len(addre)):
            if re.search(addre[i], word):
                sylnum += 1

        #handle single alphabat
        if (word == ("f" or "h" or "l" or "m" or "n" or "s" or "z" or "x")):
            sylnum = 1
        if (word == ("w")):
            sylnum = 3
        if sylnum == 0:
            sylnum = 1 #the, crwth ...
        return sylnum
        
        













