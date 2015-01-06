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
    
    def __add__(self,word,index):
        if index == len(word):
            self.isTerminal = True
            return True
        char = word[index]
        if char in self.kids:
            child = self.kids[char]
        else:
            child = __Node__(char)
            self.kids[char] = child
        return child.__add__(word,index+1)
        
class __TrieIterator__:
	'''
	An iterator for the Trie. Uses a stack, and depth-first-search, to keep track of what node needs to come next.
	'''

	def __init__(self, trie):
		self.trie = trie
		self.stack = []
		head = trie.head
		children = head.kids
		childkeys = list(children.keys())
		childkeys.sort(reverse=True)
		for key in childkeys:
			self.stack.append((children[key],""))

	def __iter__(self):
		return self

	def __next__(self):
		while len(self.stack) > 0:

			# pop next node from stack
			pair = self.stack.pop()
			node = pair[0]
			string_sofar = pair[1]

			# construct string
			string = string_sofar + node.value

			# push children onto stack
			children = node.kids
			childkeys = list(children.keys())
			childkeys.sort(reverse=True) #stack is FILO, we want smaller children i.e.: a, b, c to be the last in so they first out
			for key in childkeys:
				childnode = children[key]
				self.stack.append((childnode, string))

			# check if we need to return value
			if node.isTerminal:
				return string

		raise StopIteration()

class Trie:
        
    def __init__(self, words=[]):
        '''
        Create and initialise a Trie.

        Keyword Arguments:
        ------------------
        	words : iterable
        		collection of words to put into the Trie.
        		(default=[])
        '''
        self.count = 0
        self.head = __Node__("")
        for word in words:
            self.add(word)

    def __iter__(self):
    	return __TrieIterator__(self)

    def __len__(self):
        return self.count
    
    def __contains__(self,word):
        return self.head.__contains__(word,0)
    
    def add(self, word):
    	'''
    	Add a word to this Trie.
    	Return bool : whether the word was added or not.

    	Parameters:
    	-----------
    		word : str
    			word to be added to the Trie.
    	'''
    	if word in self:
    		return False
    	if self.head.__add__(word,0):
    		self.count = self.count + 1
    		return True
    	else:
    		return False
    
    def contains_substr_of(self,string):
    	'''
    	Check if any word in this Trie is a substring of the given string.
    	Returns bool.

    	Parameters:
    	-----------
    		string : str
    			check to see if Trie contains a substring of this str
    	'''
    	root = self.head
    	for char in root.kids:
    		kid = root.kids[char]
    		result = kid.__substr__(string, char)
    		if result:
    			return True
    	return False

t = Trie(["can","cat","cool","coal","coals"])
for word in t:
	print(word)