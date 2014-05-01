#Yining Wang
# -*- coding: cp936 -*-
from string import punctuation
from math import log
import pickle

from numpy import logaddexp
from scipy.stats import poisson

from nltk.corpus import dependency_treebank as dt



kROOT = "<ROOT>"
kNEG_INF = float("-inf")


def correct_positions(dependency_parse):
    """
    Given a correct NLTK parse tree, return an iterator over the correct
    tuples.  Excludes punctuation.
    """

    for ii in dependency_parse.to_conll(10).split('\n'):
        if not ii:
            continue

        fields = ii.split('\t')
        child_pos = int(fields[0])
        head_pos = int(fields[6])
        child_word = fields[1]
        if not all(x in punctuation for x in child_word):
            yield (head_pos, child_pos)


def dependency_element(dependency_parse, key='word'):
    """
    Returns an iterator over the elements in the original sentence (given the key)

    @param key The key of the element to return
    """
    pos = 1
    while dependency_parse.contains_address(pos):
        yield dependency_parse.get_by_address(pos)[key].lower()
        pos += 1


class BigramInterpScoreFunction:
    """
    Class that matches score function API.  Uses cached score function values.
    """

    def __init__(self, pickled_word, pickled_tag):
        """
        Read cached scores from a file
        """

        self._word_scores = pickle.load(open(pickled_word, 'rb'))
        self._tag_scores = pickle.load(open(pickled_tag, 'rb'))
        self._poisson = poisson(1.9)

    def word_score(self, h_word, c_word):
        if h_word != kROOT and all(x in punctuation for x in h_word):
            val = kNEG_INF
        elif c_word == kROOT:
            val = kNEG_INF
        else:
            val = self._word_scores.get((h_word, c_word), -100)
        #print(h_word, c_word, val)
        return val

    def tag_score(self, h_tag, c_tag):
        val = self._tag_scores.get((h_tag, c_tag), -100)
        #print(h_tag, c_tag, val)
        return val

    def dist_score(self, h_ind, c_ind):
        val = self._poisson.pmf(abs(h_ind - c_ind))
        #print(h_ind, c_ind, val)
        if val == 0:
            return kNEG_INF
        return log(val)

    def __call__(self, h_word, c_word, h_tag, c_tag, h_pos=0, c_pos=0):
        """
        Given a potential dependency, give score
        """

        val = logaddexp(self.word_score(h_word, c_word),
                        self.tag_score(h_tag, c_tag))
        val = logaddexp(val, self.dist_score(h_pos, c_pos))

        return val

def unlabeled_accuracy(truth, answer):
    """
    Returns the accuracy as the number edges right and the total number of
    edges.
    """
    right = 0
    total = 0
    answer_lookup = dict((y, x) for x, y in answer)

    for parent, child in correct_positions(truth):
        total += 1
        if answer_lookup[child] == parent:
            right += 1

    return right, total


class EisnerParser:
    """
    Parses a sentence using Eisner's algorithm
    """

    def __init__(self, sentence, tag_sequence, score_function):
        self._chart = {}
        self._pointer = {} #didnt see this....
        self._sent = [kROOT] + sentence
        self._tags = [kROOT] + tag_sequence
        self._sf = score_function
        self._score = {} #λ(ws,wt)
        self._breadcrumb = {} #pointer
        
        
        self.initialize_chart()
        

    def initialize_chart(self):
        """
        Create a chart with singleton spans
        """
        # Complete this!
        for n in range(0,len(self._sent)):
            self._chart[(n,n,True,True)]=0
            self._chart[(n,n,True,False)]=0
            self._chart[(n,n,False,True)]=0
            self._chart[(n,n,False,False)]=0
        for ibc in range(0, len(self._sent)):
            for jbc in range(0, len(self._sent)):
                if ibc>jbc:
                    continue
                self._breadcrumb[(ibc, jbc, True, True)] = []
                self._breadcrumb[(ibc, jbc, False, True)] = []
                self._breadcrumb[(ibc, jbc, True, False)] = []
                self._breadcrumb[(ibc, jbc, False, False)] = []
        

        return None

    def get_score(self, start, stop, right_dir, complete):
        return self._chart[(start, stop, right_dir, complete)]

    def reconstruct(self):
        """
        Return an iterator over edges in the discovered dependency parse tree
        """

        return self._reconstruct((0, len(self._sent) - 1, True, True))

    def _reconstruct(self, span):
        """
        Return an iterater over edges in a cell in the parse chart
        span --->  (0, len(self._sent) - 1, True, True)
        """
        #if (span[2] == True):
        #    a = span[0]
        #    b = span[1]
        #else:
        #    a = span[1]
        #    b = span[0]
        # Complete this!
        return self._breadcrumb[span]

    def STLI(self, start, stop):
        """
        c[s][t][<-][o]
        """
        if (stop == start):
            return 0
        elif (stop - start == 1):
            if (stop,start) not in self._breadcrumb[(start, stop, False, False)]:
                self._breadcrumb[(start, stop, False, False)].append((stop, start))
            return self._score[(stop, start)]
        else:
            stlinum = stop - start #how many "q"s
            findmaxSTLI = []
            for q in range(0,stlinum):
                findmaxSTLI.append(self._chart[(start,start+q,True,True)]+self._chart[(start+q+1,stop,False,True)]+self._score[(stop, start)])
            q = findmaxSTLI.index(max(findmaxSTLI)) # q for the max
            #below are for breadcrumb
            for i in range(0,len(self._breadcrumb[(start,start+q,True,True)])):
                if self._breadcrumb[(start,start+q,True,True)][i] not in self._breadcrumb[(start, stop,False, False)]:
                    self._breadcrumb[(start, stop,False, False)].append(self._breadcrumb[(start,start+q,True,True)][i])
            for i in range(0,len(self._breadcrumb[(start+q+1,stop,False,True)])):
                if self._breadcrumb[(start+q+1,stop,False,True)][i] not in self._breadcrumb[(start, stop, False, False)]:
                    self._breadcrumb[(start, stop, False, False)].append(self._breadcrumb[(start+q+1,stop,False,True)][i])
 
            return max(findmaxSTLI)
        
    def STRI(self, start, stop):
        """
        c[s][t][->][o]
        """
        if (stop == start):
            return 0
        elif (stop - start == 1):
            if (start,stop) not in self._breadcrumb[(start,stop,True,False)]:
                self._breadcrumb[(start,stop,True,False)].append((start,stop))
            return self._score[(start, stop)]
        else:
            strinum = stop - start #how many "q"s
            findmaxSTRI = []
            for q in range(0,strinum):
                findmaxSTRI.append(self._chart[(start,start+q,True,True)]+self._chart[(start+q+1,stop,False,True)]+self._score[(start, stop)])
            q = findmaxSTRI.index(max(findmaxSTRI)) # q for the max
            for i in range(0,len(self._breadcrumb[(start,start+q,True,True)])):
                if self._breadcrumb[(start,start+q,True,True)][i] not in self._breadcrumb[(start,stop,True,False)]:
                    self._breadcrumb[(start,stop,True,False)].append(self._breadcrumb[(start,start+q,True,True)][i])
            for i in range(0,len(self._breadcrumb[(start+q+1,stop,False,True)])):
                if self._breadcrumb[(start+q+1,stop,False,True)][i] not in self._breadcrumb[(start,stop,True,False)]:
                    self._breadcrumb[(start,stop,True,False)].append(self._breadcrumb[(start+q+1,stop,False,True)][i])

            return max(findmaxSTRI)
        
    def STLC(self, start, stop):
        """
        c[s][t][<-][.]
        """
        if (stop == start):
            return 0
        elif (stop - start == 1):
            if (stop,start) not in self._breadcrumb[(start,stop,False,True)]:
                self._breadcrumb[(start,stop,False,True)].append((stop,start))
            return self.STLI(start, stop)            
        else:
            stlcnum = stop - start #how many "q"s
            findmaxSTLC = []
            for q in range(0,stlcnum):
                findmaxSTLC.append(self._chart[(start,start+q,False,True)]+self._chart[(start+q,stop,False,False)])
            q = findmaxSTLC.index(max(findmaxSTLC)) # q for the max
            if (stop, start+q) not in self._breadcrumb[(start,stop,False,True)]:
                self._breadcrumb[(start,stop,False,True)].append((stop, start+q))
            for i in range(0, len(self._breadcrumb[(start+q,stop,False,False)])):
                if self._breadcrumb[(start+q,stop,False,False)][i] not in self._breadcrumb[(start,stop,False,True)]:
                    self._breadcrumb[(start,stop,False,True)].append(self._breadcrumb[(start+q,stop,False,False)][i])
            for i in range(0,len(self._breadcrumb[(start,start+q,False,True)])):
                if self._breadcrumb[(start,start+q,False,True)][i] not in self._breadcrumb[(start,stop,False,True)]:
                    self._breadcrumb[(start,stop,False,True)].append(self._breadcrumb[(start,start+q,False,True)][i])

            return max(findmaxSTLC)
        
    def STRC(self, start, stop):
        """
        c[s][t][->][.]
        """
        if (stop == start):
            return 0
        elif (stop - start == 1):
            if (start,stop) not in self._breadcrumb[(start,stop,True,True)]:
                self._breadcrumb[(start,stop,True,True)].append((start,stop))
            return self.STRI(start, stop)
        else:
            strcnum = stop - start #how many "q"s
            findmaxSTRC = []
            for q in range(0,strcnum):
                findmaxSTRC.append(self._chart[(start,start+q+1,True,False)]+self._chart[(start+q+1,stop,True,True)])
            q = findmaxSTRC.index(max(findmaxSTRC)) # q for the max
            if (start, start+q+1) not in self._breadcrumb[(start,stop,True,True)]:
                self._breadcrumb[(start,stop,True,True)].append((start, start+q+1))
            for i in range(0,len(self._breadcrumb[(start,start+q+1,True,False)])):
                if self._breadcrumb[(start,start+q+1,True,False)][i] not in self._breadcrumb[(start,stop,True,True)]:
                    self._breadcrumb[(start,stop,True,True)].append(self._breadcrumb[(start,start+q+1,True,False)][i])
            for i in range(0,len(self._breadcrumb[(start+q+1,stop,True,True)])):
                if self._breadcrumb[(start+q+1,stop,True,True)][i] not in self._breadcrumb[(start,stop,True,True)]:
                    self._breadcrumb[(start,stop,True,True)].append(self._breadcrumb[(start+q+1,stop,True,True)][i])

            return max(findmaxSTRC)
        
    def typemyself(self,p,q):
        if self._sent[p] != kROOT and all(x in punctuation for x in self._sent[p]):
            val = kNEG_INF
        elif self._sent[q] == kROOT:
            val = kNEG_INF
        else:
            val = self._sf._word_scores.get((self._sent[p], self._sent[q]), -100)
        return val
    
    def fill_chart(self):
        """
        Complete the chart and fill in back pointers
        """
        

        #I tried to use word_score function but failed...So I typed myself.
        sentlen = len(self._sent)
        for p in range(0,sentlen):
            for q in range(0,sentlen):
                if (p == q):
                    continue
                self._score[(p,q)] = self.typemyself(p,q)

                                                                  
        for span in range(1,sentlen):
            for start in range (0, sentlen-1):
                if (span+start >= sentlen):
                    break
                self._chart[(start,start+span,False,False)]=self.STLI(start,start+span)
                self._chart[(start,start+span,True,False)]=self.STRI(start,start+span)
                self._chart[(start,start+span,False,True)]=self.STLC(start,start+span)
                self._chart[(start,start+span,True,True)]=self.STRC(start,start+span)
                
                
                
        # Complete this!

def custom_sf():
    """
    Return a custom score function that obeys the BigramScoreFunction interface.
    It can use information stored in the local file sf.dat
    """
    # Complete this if you want extra credit

    return None

if __name__ == "__main__":

    # Load the score function
    sf = BigramInterpScoreFunction("tb_counts.words", "tb_counts.tag")

    total_right = 0
    total_edges = 0

    for ss in dt.parsed_sents():
        words = list(dependency_element(ss, 'word'))
        tags = list(dependency_element(ss, 'tag'))

        chart = EisnerParser(words, tags, sf)

        chart.initialize_chart()
        chart.fill_chart()

#        for ii, jj in correct_positions(ss):
        for ii, jj in chart.reconstruct():
            # Subtract 1 to account for the head we added
            print(ii, jj, words[ii - 1], words[jj - 1],
                  tags[ii - 1], tags[jj - 1],
                  sf(words[ii - 1], words[jj - 1],
                     tags[ii - 1], tags[jj - 1], ii, jj))

        right, edges = unlabeled_accuracy(ss, chart.reconstruct())

        total_right += right
        total_edges += edges

        print("============================ Acc (%i): %f" % \
                  (total_edges, float(total_right) / float(total_edges)))
