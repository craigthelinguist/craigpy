import math as math
import craigpy as cp

def __init_table__(rows,cols):
    ''' initialise a 2d array with the specified number of rows and cols.
        the first row and first col will contain entries that are multiples
        of -2. Everything in the middle will be zero. '''
    table = [[0 for col in range(cols)] for row in range(rows)]
    for i in range(cols):
        table[0][i] = -2 * i
    for j in range(rows):
        table[j][0] = -2 * j
    return table

def __match__(char1,char2):
    ''' return a score based on whether char1 == char2 '''
    if char1 == char2:
        return 1
    else:
        return -1

def __compute_table__(str1,str2):
    rows = len(str1)+1
    cols = len(str2)+1
    table = __init_table__(rows,cols)
    for i in range(1,rows):
        for j in range(1,cols):
            matching = __match__(str1[i-1],str2[j-1]) + table[i-1][j-1]
            skip_str1 = -2 + table[i-1][j]
            skip_str2 = -2 + table[i][j-1]
            table[i][j] = max(matching,skip_str1,skip_str2)
    return table

def __reconstruct_alignment__(t,str1,str2):

    # row is str1, col is str2
    row = len(str1)
    col = len(str2)

    # they make the code nicer to look at
    cangodiag = lambda : row > 0 and col > 0
    cangoabov = lambda : row > 0
    cangoleft = lambda : col > 0
    align1 = ""
    align2 = ""
   
    # when you're at t[0][0] you've matched everything in the TWO STRINGS
    while row != 0 or col != 0:

        # score in current cell either came from up, left, or up-left
        score = t[row][col]

        # move up a row, across a col, append char to str1 and str2
        if cangodiag() and t[row-1][col-1] + __match__(str1[row-1],str2[col-1]) == score:
            row = row - 1
            col = col - 1
            align1 = align1 + str1[row]
            align2 = align2 + str2[col]

        # move up a row, append char to str1, space to str2
        elif cangoabov() and t[row-1][col] - 2 == score:
            row = row - 1
            align1 = align1 + str1[row]
            align2 = align2 + "_"

        # move across a col, append char to str2, space to str1
        elif cangoleft() and t[row][col-1] - 2 == score:
            col = col - 1
            align1 = align1 + "_"
            align2 = align2 + str2[col]

        # shouldn't happen, but just in case.
        else:
            print "something fucked up"
            print "returning what has been computed so far...."
            return (align1,align2)
            
    # this reverses strings
    # thank you guido :^)
    align1 = align1[::-1]
    align2 = align2[::-1]
    return (align1,align2)

def align(str1, str2):
    ''' return the likeness of str1 to str2 based on their optimal alignment.
        return : int'''
    table = __compute_table__(str1,str2)
    return table[len(str1)][len(str2)]

def get_align(str1, str2):
    ''' return the optimal way to align str1, str2
        the return format is a 2-tuple with '_' inserted where there are spaces padding the string '''
    table = __compute_table__(str1,str2)
    return __reconstruct_alignment__(table,str1,str2)

def entropy(string):
    ''' return the shannon entropy of the specified string. returns a value between 0 and 1. 
        a higher value denotes a more uncertain string. '''
    
    # empty string contains no information
    if string == "":
        return 0
    
    # compute probability distribution
    histogram = {}
    for c in string:
        if c in histogram:
            histogram[c] = histogram[c] + 1
        else:
            histogram[c] = 1
    histogram = { char : histogram[char]*1.0 / len(string) for char in histogram.keys() }
    
    # compute entropy
    total_entropy = 0
    for prob in histogram.values():
        entropy = prob * math.log(prob, 2)
        total_entropy = total_entropy + entropy
    total_entropy = -1 * total_entropy

    # return metric entropy scaled to be between 0 and 1
    return total_entropy*1.0 / len(string)


class CompositeFilter:
    ''' A CompositeFilter is a series of Filter. It will match a string by trying to match it to each of its constituent
        filters. There are two modes "or", "and".
            "or": match a string if it matches any of the filters
            "and": match a string if it matches all of the filters '''

    def __init__(self, filters, type="or"):
        ''' create a CompositeFilter.
                filters : a list of Filter instances.
                type : "or", match a string if it matches any filter
                       "and", match a string if it matches all filters '''
        self.__inclusion__ = True
        self.__filters__ = filters
        self.__type__ = type

    def match(self, string):
        ''' Return true if this string belongs to any of the filters in this CompositeFilter, or false if it does not. '''

        # create map, map
        matching = lambda fil : fil.match(string)
        bool_vector = map(matching, self.__filters__)

        # create reduce
        if self.__type__ == "or":
            reduction = lambda x,y : x or y
        elif self.__type__ == "and":
            reduction = lambda x,y : x and y
        else:
            print "unknown matching parameter: ", self.__type__
            return None

        # reduce
        return reduce(reduction, bool_vector)

    def match_words(self, words):
        ''' Take a list of words. Return those words which pass the filter. '''
        trie = Trie()

        if self.__inclusion__:
            mapping = lambda x : self.match(x)
        else:
            mapping = lambda x : not self.match(x)

        bool_vector = map(mapping, words)

        return [word for (word, bool) in zip(words, bool_vector) if bool]
    
    def set_inclusion(self, b):
        ''' Set whether you should match by inclusion of the set, or exclusion.
                bool : if True, a string matches if it belongs in the training set. If False, a string matches if it does not belong
                        in the training set. '''
        self.__inclusion__ = b

class Filter:
    ''' A very basic string classifier. It works by checking the probability that one character follows another. It does this
        for all successive pairs of strings, then computes the average and tells you whether the string belongs using a
        specified threshold.
        
        The Filter needs to be trained by initialising with a list of words, or by calling train(trainingSet). You must also
        specify a threshold, which is a value between 0 and 1. If the mean probability in a string exceeds the threshold, then
        the string belongs. If it is below the threshold, the string does not belong. '''
    
    def __init__(self, trainingSet=None, threshold=0):
        ''' create a filter.
                trainingSet : list of words to train the filter on. If you do not specify a trainingSet, then no string will
                    belong.
                threshold : how probable a word has to be in order to match. percentage between 0 and 1. '''
        self.__mean__ = None
        self.__stdev__ = None
        self.__acceptable_stdev__ = None
        self.__substr_filter__ = None
        self.__word_filter__ = None
        self.__inclusion__ = True
        self.__threshold__ = threshold
        self.__composite__ = False
        self.__composition__ = None
        
        if trainingSet:
            self.__trainingSet__ = trainingSet
            self.train(trainingSet)
        else:
            self.__frequencies__ = {}

    
    def set_substr_filter(self, substrs):
        ''' Specify the give substrings as meaningful. If you try to match a string and something in substrs
            is a substring of the string, then it will return a matching value of 1. '''
        if isinstance(substrs, Trie):
            self.__substr_filter__ = substrs
        else:
            self.__substr_filter__ = Trie(substrs)
    
    def set_word_filter(self, words):
        ''' Specify the given words as meaningful. If you try to a match a string contained
            in this colleciton of words it will return a matching value of 1. '''
        if isinstance(words, Trie):
            self.__word_filter__ = words
        else:
            self.__word_filter__ = Trie(words)
    
    def set_stdev_filter(self, stdevs):
        ''' Add an additional filter with the given number of standard deviations. if you try to match a string, and its length
            is more than the specified number of standard deviations away from the mean, then it will return a matching value of 0.
                stdevs : how many stdevs away from mean is acceptable for the length of a string. '''
        strlens = [len(word) for word in self.__trainingSet__]
        self.__mean__ = cp.mean(strlens)
        self.__stdev__ = cp.stdev(strlens)
        self.__acceptable_stdev__ = stdevs

    def __get_value__(self,c1,c2):
        ''' Helper function. Return the probability that c2 follows c1. '''
        if c1 not in self.__frequencies__:
            return 0
        elif c2 not in self.__frequencies__[c1]:
            return 0
        else:
            return self.__frequencies__[c1][c2]
    
    def set_inclusion(self, b):
        ''' Set whether you should match by inclusion of the set, or exclusion.
                bool : if True, you will match strings if they are included in the training Set. if False, you will match strings
                    if they are not included in the training Set. '''
        self.__inclusion__ = b

    def set_threshold(self, value):
        ''' Specify the threshold - how probable a string has to be before it is declared as a match. '''
        value = min(1.0,value)
        value = max(0.0,value)
        self.__threshold__ = value

    def train(self, trainingSet):
        ''' Train this filter using the given list of words. '''
        frequencies = {}
        
        # helper method
        def insert(c1, c2):
            if c1 not in frequencies:
                frequencies[c1] = {}
            if c2 not in frequencies[c1]:
                frequencies[c1][c2] = 1
            else:
                frequencies[c1][c2] = frequencies[c1][c2] + 1
        
        # get word count
        for word in trainingSet:
            for i in range(len(word)-1):
                c1 = word[i]
                c2 = word[i+1]
                insert(c1,c2)
        
        # normalise
        for char in frequencies:
            fmap = frequencies[char]
            total = reduce(lambda x,y : x+y, fmap.values())
            for successor in fmap:
                value = fmap[successor]
                normed = value * 1.0 / total
                fmap[successor] = normed
        
        self.__frequencies__ = frequencies

    def match_value(self, string):
        ''' Return the probability that this is a valid string, as a value from 0 to 1. '''
        sum_value = 0
        
        # check how many standard deviations away the len(string) is
        if self.__acceptable_stdev__:
            lower = self.__mean__ - self.__stdev__ * self.__acceptable_stdev__
            upper = self.__mean__ + self.__stdev__ * self.__acceptable_stdev__
            length = len(string)
            if length < lower or length > upper:
                return 2 if self.__inclusion__ else -1
        
        # check for explicit substrings
        if self.__substr_filter__:
            if self.__substr_filter__.contains_substr(string):
                return 2 if self.__inclusion__ else -1
        
        # check for explicit words
        if self.__word_filter__:
            if string in self.__word_filter__:
                return 2 if self.__inclusion__ else -1
        
        # sum up probabilities that each character follows on from previous, take average
        for i in range(len(string)-1):
            c1 = string[i]
            c2 = string[i+1]
            val = self.__get_value__(c1,c2)
            sum_value = sum_value + val
        value2return = sum_value / (len(string)-1)
        
        # set inclusion: return how probable it is that this string matches.
        # set exclusion: return how probable it is that this string doesn't match.
        return value2return if self.__inclusion__ else 1 - value2return

    def match(self, string):
        ''' Return true if this string belongs, or false if it does not. '''
        value = self.match_value(string)
        if self.__inclusion__:
            #print "checking ", value, " >= ", self.__threshold__
            #print value >= self.__threshold__
            return value >= self.__threshold__
        else:
            #print "checking ", value, " > 1 - ", self.__threshold__
            #print value > 1 - self.__threshold__
            return value >= 1 - self.__threshold__

    def match_words(self, words):
        ''' Take a list of words. Return those words which pass the filter. '''
        wordstoreturn = Trie()
        for word in words:
            if self.match(word):
               wordstoreturn.insert(word)
        return wordstoreturn.iterwords()

class __Node__:    
    def __init__(self, char, term=False):
        self.value = char
        self.kids = {}
        self.isTerminal = term
        
    def __str__(self):
        return self.value
    
    def __contains__(self,word,index):  
        if index == len(word):
            return self.isTerminal
        char = word[index]
        if char not in self.kids:
            return False
        else:
            child = self.kids[char]
            return child.__contains__(word,index+1)
    
    def __insert__(self,word,index):
        if index == len(word):
            self.isTerminal = True
            return True
        char = word[index]
        if char in self.kids:
            child = self.kids[char]
        else:
            child = __Node__(char)
            self.kids[char] = child
        return child.__insert__(word,index+1)
        
    def __print_tree__(self, depth):
        print "-" * depth + self.value
        for child in self.kids.itervalues():
            child.__print_tree__(depth+1)
    
    def __print_words__(self, word):
        if self.isTerminal:
            print word
        keys = self.kids.keys()
        keys.sort()
        for k in keys:
            self.kids[k].__print_words__(word + k)
    
    def __construct_list__(self, word, words):
        if self.isTerminal:
            words.append(word)
        keys = self.kids.keys()
        keys.sort()
        for k in keys:
            words = self.kids[k].__construct_list__(word + k, words)
        return words
    
    def __substr__(self, word, string):
        ''' Return true if this subtree contains a word that is a substring of the given string
                word : word that you're checking for substrings
                string : the word built up so far in the trie '''
        
        # if the string so far is not contained in word, then nothing in this subtree will be
        if string not in word:
            return False
        
        # if this node is a word, either string is in word or it doesn't
        if self.isTerminal:
            return string in word
        
        # check if the substring is in this subtree
        for char in self.kids:
            kid = self.kids[char]
            result = kid.__substr__(word, string + char)
            if result:
                return True
        
        # substring not in this node nor its subtree
        return False
        
class Trie:
        
    def __init__(self, words=[]):
        ''' Create a Trie that contains the given collection of words. '''
        self.count = 0
        self.head = __Node__("")
        for word in words:
            self.insert(word)

    def __len__(self):
        ''' Return the number of words in this Trie. '''
        return self.count
    
    def __contains__(self,word):
        ''' Return true if the given word is in the Trie. '''
        return self.head.__contains__(word,0)
    
    def insert(self, word):
        ''' Insert the given word into the Trie. Words can only be contained once
            in the Trie. The empty string "" is considered to not be in the Trie
            and it cannot be added.
                return : true if the word was inserted, false otherwise. '''
        if word in self:
            return False
        if self.head.__insert__(word,0):
            self.count = self.count + 1
            return True
        else:
            return False
    
    def print_tree(self):
        ''' Print a little picture representing the structure of this Trie. '''
        print "TRIE\n===="
        self.head.__print_tree__(-1)

    def print_words(self):
        ''' Print the words in this Trie. '''
        print "WORDS\n====="
        self.head.__print_words__("")
        
    def iterwords(self):
        ''' Returns an iterable sequence containing those words in this Trie. '''
        words = []
        return self.head.__construct_list__("",words)
    
    def contains_substr(self,string):
        ''' Return true if this Trie contains a word that is a substring of the given string. 
                string : any string '''
        root = self.head
        for char in root.kids:
            kid = root.kids[char]
            result = kid.__substr__(string, char)
            if result:
                return True
        return False
