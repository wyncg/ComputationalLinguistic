#Name = Yining Wang
from __future__ import division

from itertools import islice, izip #for good_turing

from math import log, exp
from collections import defaultdict

from collections import Counter

from numpy import mean

import nltk
from nltk import FreqDist
from nltk.util import bigrams

kLM_ORDER = 2
kUNK_CUTOFF = 3
kNEG_INF = -1e6

kSTART = "<s>"
kEND = "</s>"



class BigramLanguageModel:

    def __init__(self, unk_cutoff, jm_lambda=0.5, dirichlet_alpha=0.1,
                 katz_cutoff=5, kn_discount=0.1, py_a=0.1, py_b=0.1):
        #self._unk_cutoff = unk_cutoff
        self._jm_lambda = jm_lambda
        self._dirichlet_alpha = dirichlet_alpha
        self._katz_cutoff = katz_cutoff
        self._kn_discount = kn_discount
        self._py_a = py_a
        self._py_b = py_b 
        self._vocab_final = False
        self._cnt = Counter()
        self._defaultdictionary = defaultdict(list)
        self._bgGT = []
        self._sentGT = []
        self._unicount = {}
        
    def train_seen(self, word, count=1):
        """
        Tells the language model that a word has been seen @count times.  This
        will be used to build the final vocabulary.
        """
        assert not self._vocab_final
        "Trying to add new words to finalized vocab"
        self._cnt[word] = self._cnt[word] + count
        #None

    def vocab_lookup(self, word):
        """
        Given a word, provides a vocabulary representation.  Words under the
        cutoff threshold shold have the same value.  All words with counts
        greater than or equal to the cutoff should be unique and consistent.
        """
        assert self._vocab_final
        "Vocab must be finalized before looking up words"
        if word == kSTART or word == kEND or self._cnt[word] >= kUNK_CUTOFF:
            return word   
        else: 
            return '<UNK>'

    def finalize(self):
        """
        Fixes the vocabulary as static, prevents keeping additional vocab from
        being added
        """
        self._vocab_final = True

    def censor(self, sentence):
        """
        Given a sentence, yields a sentence suitable for training or testing.
        Prefix the sentence with <s>, replace words not in the vocabulary with
        <UNK>, and end the sentence with </s>.
        """
        yield self.vocab_lookup(kSTART)
        for ii in sentence:
            yield self.vocab_lookup(ii)
        yield self.vocab_lookup(kEND)

    def mle(self, context, word):
        """
        Return the log MLE estimate of a word given a context.
        """
        numerator = self._defaultdictionary[context].count(word)
        denominator = len(self._defaultdictionary[context])
        if numerator == 0:
            return kNEG_INF #didnt work with float('-inf') on my python... why?
        else:
            return log(numerator/denominator)

    def laplace(self, context, word):
        """
        Return the log MLE estimate of a word given a context.
        """
        numerator = self._defaultdictionary[context].count(word) + 1
        denominator = len(self._defaultdictionary[context]) \
                      + len(list(self._cnt)) + 3 #3:<s>, </s>, <UNK>
        return log(numerator/denominator)

    def dirichlet(self, context, word):
        """
        Return the log Jelinek-Mercer estimate of a word given a context;
        interpolates context probability with the overall corpus probability.
        """
        #assume 0.1
        numerator = self._defaultdictionary[context].count(word) + self._dirichlet_alpha
        denominator = len(self._defaultdictionary[context]) \
                      + len(list(self._cnt)) * self._dirichlet_alpha + 3 * self._dirichlet_alpha #3:<s>, </s>, <UNK>
        return log(numerator/denominator)
        

    def jelinek_mercer(self, context, word):
        """
        Return the log Jelinek-Mercer estimate of a word given a context;
        interpolates context probability with the overall corpus probability.
        p(wi|wi-1) = a * pML(wi|wi-1) + (1-a)pML(wi)
        """
        unitotal = sum(self._unicount.values())
        unipML = self._unicount.get(word, 0)/unitotal
        a = self._jm_lambda
        numerator = self._defaultdictionary[context].count(word)
        denominator = len(self._defaultdictionary[context])
        bipML = numerator/denominator
        jm = a * bipML + (1 - a) * unipML
        return log(jm)

    def knesser_ney(self, context, word):
        """
        pKN = max(c(wi-1wi)-d,0)/cwi-1 + du*x/(cwi-1*sumbi)
        u:c(wi-1u)>0   x:c(xwi)>0
        u, x, sumbi     these are count of unique!!!
        """
        numerator = self._defaultdictionary[context].count(word) #c(wi-1wi)
        denominator = len(self._defaultdictionary[context]) #cwi-1  ????
        u = len(set(defaultdictionary[context])) #u
        x = []
        for c, w in bg:
            if w == word:
                if c in x:
                    continue
                else:
                    x.append(c)
            else:
                continue

        x = len(x)  #x
        sentencebigramKN = self._bgGT
        uniquebi = len(set(sentencebigramKN))
        #cxwi = 0 #x
        #for c, w in bg:
        #    if w == word:
        #        cxwi = cxwi + 1     #wrong
        d = self._kn_discount
        if numerator > d:
            numerator = numerator - d
        else:
            numerator = 0
        pKN = numerator/denominator + d*x*u/(denominator*uniquebi)
        return log(pKN)

    def good_turing(self, context, word):
        """
        r*=(r+1)(Nr+1)/Nr
        """
        countContextWord = self._bgGT((context, word)) #r
        cntGT = Count(izip(self._sentGT, islice(self._sentGT, 1, None)))
        sumPossibleBigram = len(self._sentGT) * len(self._sentGT) #total possible bigram
        sumExistBigram = sum(cntGT.values()) #total existing bigram
        uniqueBigram = len(cntGT)
        missingBigram = sumPossibleBigram - uniqueBigram #equals to N0
        rplusone = countContextWord + 1 # r+1
        Nr = 0 #Nr
        if countContextWord == 0:
            Nr = missingBigram
        else:
            for bigram, count in countext.items():
                if count == countContextWord:
                    Nr += 1
        Nrplus1 = 0 #Nr+1
        for bigram, count in countext.items():
            if count == rplusone:
                Nrplus1 += 1
        
        return rplusone*Nrplus1/Nr

    def pitman_yor(self, context, word):
        """
        p(w|h) = (c(w|h)-d*thw)/(theta+c(h)) + p(w|h')(theta+d*th)/(theta+c(h))
        p(w|h') = using a n-1 gram context h'
        """
        #self._py_a = py_a
        #self._py_b = py_b
        numerator = self._defaultdictionary[context].count(word)
        denominator = len(self._defaultdictionary[context])
        unitotal = sum(self._unicount.values())
        uni = self._unicount.get(word, 0)/unitotal #p(w|h')
        countwh = self._defaultdictionary[context].count(word)
        counth = len(self._defaultdictionary[context])
        bi = (countwh - self._py_a)/(self._py_b + counth) + uni*(self._py_b + self._py_a)/(self._py_b+counth)
        return bi

    def sample(self, samples=25):
        """
        Sample words from the language model.

        @arg samples The number of samples to return.
        """
        
        return

    def add_train(self, sentence):
        """
        Add the counts associated with a sentence.
        """

        # You'll need to complete this function, but here's a line of code that
        # will hopefully get you started.
        for word in sentence:
            self._unicount[word] = self._unicount.get(word, 0) + 1
        bg = bigrams(self.censor(sentence))
        self._bgGT = bg #bigram of sentence, also used in KN
        """
        add<s></s>in the original sentence for good_turing function
        """
        self._sentGT = sentence
        self._sentGT.append(kEND)
        self._sentGT.insert(0, kSTART)
        
        for context, word in bg:
            self._defaultdictionary[context].append(word)
            #None
        
    def perplexity(self, sentence, method):
        try:
            return exp(-1.0 * mean([method(context, word) for context, word \
                                        in bigrams(self.censor(sentence))]))
        except OverflowError:
            return kNEG_INF

if __name__ == "__main__":
    lm = BigramLanguageModel(kUNK_CUTOFF)

    for ii in nltk.corpus.brown.words():
        lm.train_seen(ii)

    lm.finalize()

    for ii in nltk.corpus.brown.sents():
        lm.add_train(ii)

    for ii in nltk.corpus.treebank.sents()[0:5]:
        scores = (lm.perplexity(ii, lm.mle),
                  lm.perplexity(ii, lm.laplace),
                  lm.perplexity(ii, lm.dirichlet))
        print(scores, " ".join(ii))
