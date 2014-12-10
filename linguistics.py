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

class Filter:
    ''' A very basic string classifier. It works by checking the probability that one character follows another. It does this
        for all successive pairs of strings, then computes the average and tells you whether the string belongs using a
        specified threshold.
        
        The Filter needs to be trained by initialising with a list of words, or by calling train(trainingSet). You must also
        specify a threshold, which is a value between 0 and 1. If the mean probability in a string exceeds the threshold, then
        the string belongs. If it is below the threshold, the string does not belong. '''
    
    def __init__(self, trainingSet=None, threshold=0, length_stdevs=None, inclusion=True):
        ''' create a filter.
                trainingSet : list of words to train the filter on. If you do not specify a trainingSet, then no string will
                    belong.
                threshold : how probable a word has to be in order to match. percentage between 0 and 1. Default threshold is 0
                length_stdevs : if you specify an integer value then Filter will compute the mean and standard deviation of the length
                    of words in the supplied trainingSet.
                inclusion : if true, will match strings that belong to the training set. If false, will match strings that do NOT
                    belong to the trainingSet.
                '''
        self.mean = None
        self.stdev = None
        self.acceptable_stdev = None
        self.inclusion = inclusion
        
        self.threshold = threshold
        if trainingSet:
            self.trainingSet = trainingSet
            self.train(trainingSet)
            if length_stdevs:
                self.set_acceptable_length_stdevs(length_stdevs)
        else:
            self.frequencies = None
    
    def __get_value__(self,c1,c2):
        ''' helper function. return the probability that c2 follows c1 '''
        if c1 not in self.frequencies:
            if self.inclusion:
                return 0
            else:
                return 1
        elif c2 not in self.frequencies[c1]:
            if self.inclusion:
                return 0
            else:
                return 1
        else:
            return self.frequencies[c1][c2]
    
    def match_value(self, string):
        ''' Return the probability that this is a valid string, as a value from 0 to 1. '''
        sum_value = 0
        if self.acceptable_stdev:
            lower = self.mean - self.stdev * self.acceptable_stdev
            upper = self.mean + self.stdev * self.acceptable_stdev
            length = len(string)
            if length < lower or length > upper:
                return 0
        for i in range(len(string)-1):
            c1 = string[i]
            c2 = string[i+1]
            val = self.__get_value__(c1,c2)
            sum_value = sum_value + val
        return sum_value / (len(string)-1)
    
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
        
        self.frequencies = frequencies

    def set_acceptable_length_stdevs(self, stdevs):
        ''' This method will determine whether you should prune based on the length of the word.
                stdevs : if filter encounters a word more than this amount of standard deviations from the mean, it will prune '''
        strlens = [ len(word) for word in self.trainingSet ]
        self.mean = cp.mean(strlens)
        self.stdev = cp.stdev(strlens)
        self.acceptable_stdev = stdevs

    def match(self, string):
        ''' Return true if this string belongs, or false if it does not. '''
        value = self.match_value(string)
        return value >= self.threshold and self.inclusion

    def filter_words(self, words):
        ''' Take a list of words. Return those words which pass the filter. '''
        return [word for word in words if self.match(word)]

    def set_inclusion(self, b):
        ''' Set whether you should match by inclusion of the set, or exclusion.
                bool : if True, you will match strings if they are included in the training Set. if False, you will match strings
                    if they are not included in the training Set. '''
        self.inclusion = b
