# Author: YOUR NAME HERE
# Date: DATE SUBMITTED

# Use word_tokenize to split raw text into words
from string import punctuation
from curses.ascii import isdigit
import nltk
from nltk.tokenize import word_tokenize


class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()

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
        firstwordlen = self.num_syllables(firstword)
        secondwordlen = self.num_syllables(secondword)
        entries = nltk.corpus.cmudict.entries()
        firstwordsyllable = [p for (w, p) in entries if w == firstword]
        secondwordsyllable = [p for (w, p) in entries if w == secondword]
        """
        Put the sound of the shortest syllable of word a into firstwordshortestsyllable
        """
        #if word not found in dict, return false
        if (len(firstwordsyllable) == 0 or len(secondwordsyllable) == 0):
            return False
        firstwordshortestsyllable = firstwordsyllable[0]
        if len(firstwordsyllable) > 1:  
            for i in range(1, len(firstwordsyllable)-1):
                if len(firstwordshortestsyllable) > len(firstwordsyllable[i]):
                    firstwordshortestsyllable = firstwordsyllable[i]
            """
            The following for is to catch all the pronounciation of the shortest sound so that
            it can solve words such as "bog", that has multi shortest proun.
            """
            firstshort = []
            for i in range(0, len(firstwordsyllable)-1):
                if len(firstwordshortestsyllable) == len(firstwordsyllable(i)):
                    
        """
        Put the sound of the shortest syllable of word b into secondwordshortestsyllable
        """
        secondwordshortestsyllable = secondwordsyllable[0]
        if len(secondwordsyllable) > 1:  
            for i in range(1, len(secondwordsyllable)-1):
                if len(secondwordshortestsyllable) > len(secondwordsyllable[i]):
                    secondwordshortestsyllable = secondwordsyllable[i]
        if (firstwordlen < secondwordlen):
            t = len(firstwordshortestsyllable)
            # check if self._pronunciations[word][shortest][-t:] is same
            if (firstwordshortestsyllable[-t+1:] == secondwordshortestsyllable[-t+1:]):
                return True
            else:
                return False
        else:
            t = len(secondwordshortestsyllable)
            # check if self._pronunciations[word][shortest][-t:] is same
            if (firstwordshortestsyllable[-t+1:] == secondwordshortestsyllable[-t+1:]):
                return True
            else:
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
        first = lastword[0]
        second = lastword[1]
        third = lastword[2]
        fourth = lastword[3]
        fifth = lastword[4]
        if self.rhymes(first,second) and self.rhymes(first,fifth) and self.rhymes(third,fourth):
            return True
        else:
            return False
