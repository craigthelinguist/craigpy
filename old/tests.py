from linguistics import *

# test for the constructor for words
def test_constructor_empty():
    ''' Test creation of an empty Trie. '''
    print "======"
    print "test_constructor_empty"
    trie = Trie()
    if len(trie) != 0:
        print "Length of trie should be 0, but it is: ", len(trie)
    else:
        print "passed"
    print "======"
    
def test_constructor_wordset():
    ''' Test creation of a Trie with a set of words. '''
    print "======"
    print "test_constructor_wordset"
    words = ["hell", "help", "bro"]
    trie = Trie(words)
    if len(trie) != 3:
        print "Length of trie should be 3, but it is: ", len(trie)
    else:
        wordsnotinset = frozenset([word for word in words if word not in trie.iterwords()])
        if len(wordsnotinset) > 0:
            print "These words should be in the Trie, but they aren't: "
            print wordsnotinset
        else:
            print "passed"
    print "======"        
    
def test_constructor_wordlist():
    ''' Test creation of a Trie with a list of words (has duplicates). '''
    print "======"
    print "test_constructor_wordset"
    words = ["hell","help","bro","hell","help"]
    trie = Trie(words)
    if len(trie) != 3:
        print "Length of trie should be 3, but it is: ", len(trie)
        return
    else:
        wordsnotinset = frozenset([word for word in words if word not in trie.iterwords()])
        if len(wordsnotinset) > 0:
            print "These words should be in the Trie, but they aren't: "
            print wordsnotinset
        else:
            print "passed"
    print "======"        

def test_insertion():
    ''' Test adding one word to a Trie. '''
    print "======"
    print "test_insertion"
    trie = Trie()
    word = "hello"
    trie.insert(word)
    if len(trie) != 1:
        print "Length of trie should be 1 but it is ", len(trie)
    elif word not in trie:
        print word, " should be in trie but it isn't."
    else:
        print "passed"

def test_insertion_multiple():
    ''' Test adding multiple disjoint words to a Trie. '''
    print "======"
    print "test_insertion_multiple"
    trie = Trie()
    words = ["hello","johnny","salmonella"]
    for word in words:
        trie.insert(word)
    if len(trie) != 3:
        print "Length of trie should be 3, but it is ", len(trie)
    else:
        words_not_in_trie = frozenset([word for word in words if word not in trie])
        if len(words_not_in_trie) != 0:
            print "Could not find following words in Trie: "
            for word in words_not_in_trie:
                print word
        else:
            print "passed"
    print "======="
    
def test_insertion_multiple_overlapping():
    ''' Test adding multiple words that have common prefices. '''
    print "======"
    print "test_insertion_multiple_overlapping"
    trie = Trie()
    words = ["hello","hell","help","hilbert","johnny"]
    for word in words:
        trie.insert(word)
    if len(trie) != len(words):
        print "Length of trie should be ", len(words), " but is ", len(trie)
    else:
        words_not_in_trie = frozenset([word for word in words if word not in trie])
        if len(words_not_in_trie) != 0:
            print "Could not find following words in Trie: "
            for word in words_not_in_trie:
                print word
        else:
            print "passed"
    print "======"
    
def test_insert_duplicates():
    ''' Test adding duplicates to a Trie that have no common prefices with any other strings. '''
    print "======"
    print "test_insert_duplicates"
    trie = Trie()
    words = ["hello","hello"]
    for word in words:
        trie.insert(word)
    if len(trie) != 1:
        print "Length of trie should be 1, but is ", len(trie)
    else:
        words_not_in_trie = frozenset([word for word in words if word not in trie])
        if len(words_not_in_trie) != 0:
            print "Could not find following words in Trie: "
            for word in words_not_in_trie:
                print word
        else:
            print "passed"
    print "======"
            
def test_insert_duplicates_trickier():
    ''' Test adding duplicates that share prefices with some other strings. '''
    print "======"
    print "test_insert_duplicates_trickier"
    trie = Trie()
    words = ["hello","helper","hell","helper"]
    for word in words:
        trie.insert(word)
    if len(trie) != 3:
        print "Length of trie should be 3, but is ", len(trie)
        trie.print_tree()
        trie.print_words()
    else:
        words_not_in_trie = frozenset([word for word in words if word not in trie])
        if len(words_not_in_trie) != 0:
            print "Could not find following words in Trie: "
            for word in words_not_in_trie:
                print word
        else:
            print "passed"
    print "======"

def test_substrs():
    ''' Test substr method. '''
    print "======"
    print "test_substrs"
    substrs = ["hell","help","bro"]
    substr_trie = Trie(substrs)
    valid_substrs = ["hello","helper","hellas","brother","bro","broken"]
    invalid_substrs = ["hip", "kek"]
    passed = True
    for word in valid_substrs:
        if not substr_trie.contains_substr(word):
            print "Trie doesn't contain substring for ", word, " but it should!"
            passed = False
    for word in invalid_substrs:
        if substr_trie.contains_substr(word):
            print "Trie contains substring for ", word, " but it shouldn't!"
            passed = False
    if passed:
        print "passed"
    print "======"
 
def main():
    test_constructor_empty()
    test_constructor_wordset()
    test_constructor_wordlist()
    test_insertion()
    test_insertion_multiple()
    test_insertion_multiple_overlapping()
    test_insert_duplicates()
    test_insert_duplicates_trickier()
    test_substrs()
