
def levenshtein(str1, str2, case_sensitive=False,
				insertion=1, deletion=1, skip=0, transform=1):
	operations = {
		"deletion" : deletion,
		"insertion" : insertion,
		"skip" : 0,
		"transform " : 1
	}
	return edit_dist(str1, str2, operations, case_sensitive, minimise=True)

def seq_align(str1, str2, case_sensitive=False,
			  match=1, mismatch=-1, skip=-2):
	operations = {
		"insertion" : skip,
		"deletion" : skip,
		"skip" : match,
		"transform" : mismatch
	}
	return edit_dist(str1, str2, operations, case_sensitive, minimise=False)

def edit_dist(str1, str2, operations, case_sensitive=False, minimise=True):
	'''
	Compute the edit distance between two strings.
	Returns int.

	Parameters:
	-----------
	str1 : str
		first string to compare.
	str2 : str
		second string to compare.
	operations : { str -> int }
		operations to use and their associated cost

	Keyword Arguments:
	------------------

	'''
	if not case_sensitive:
		str1 = str1.lower()
		str2 = str2.lower()

	# init rows
	# use optimisation - we only care about score, so we only need to know last two rows
	rows = len(str1) + 1
	cols = len(str2) + 1
	botrow = [operations["insertion"] * i for i in range(cols)]
	row = 0

	# fill out rows
	for row in range(1,rows):
		toprow = botrow
		botrow = [row * operations["deletion"]] + [0]*(cols-1) # pre-allocate row
		for col in range(1, cols):

			# compute scores for each operation
			scores = []
			if "deletion" in operations:
				score = toprow[col] + operations["deletion"]
				scores.append(score)
			if "insertion" in operations:
				score = botrow[col-1] + operations["insertion"]
				scores.append(score)
			if "transform" in operations and str1[row-1] != str2[col-1]:
				score = toprow[col-1] + operations["transform"]
				scores.append(score)
			if "skip" in operations and str1[row-1] == str2[col-1]:
				score = toprow[col-1] + operations["skip"]
				scores.append(score)

			# get appropriate score
			if minimise:
				score = min(scores)
			else:
				score = max(scores)
			botrow[col] = score

	return botrow[-1]

def alignment(str1, str2, match=1, mismatch=-1, skip=-2, case_sensitive=False, pad_character="_"):
	'''
	Compute the optimal alignment of two strings.
	Returns (str,str).


	Parameters:
	-----------
		str1 : str
			first string to align.
		str2 : str
			second string to align.

	Keyword Arguments:
	------------------
		match : int
			score that should be applied when two identical characters are aligned.
			(default=1)
		mismatch : int
			score that should be applied when two different characters are aligned.
			(default=-1)
		skip : int
			score that should be applied when a character has to be aligned with a skip.
			(default=-2)
		pad_character : str
			character that should be used to represent padding. For example:
				hello		hello
				hell_		_ill_
			(default="_")
		case_sensitive : bool
			whether you should treat uppercase and lowercase chars the same
			(default=False)
	'''

	if not case_sensitive:
		str1 = str1.lower()
		str2 = str2.lower()

	#------------------ helper function
	def matching(c1, c2):
		if (c1 == c2):
			return match
		else:
			return mismatch

	#------------------ init table
	rows = len(str1) + 1
	cols = len(str2) + 1
	table = [[0 for col in range(cols)] for row in range(rows)]

	# fill first row and col with zeroes
	for i in range(cols):
		table[0][i] = skip * i
	for j in range(rows):
		table[j][0] = skip * j

	#------------------ fill out table
	for row in range(1,rows):
		for col in range(1,cols):

			# get scores
			match_score = matching(str1[row-1], str2[col-1]) + table[row-1][col-1]
			skip_str1 = skip + table[row-1][col]
			skip_str2 = skip + table[row][col-1]

			# take largest
			table[row][col] = max(match_score, skip_str1, skip_str2)

	#------------------ recover alignment
	row = rows-1
	col = cols-1
	align1 = ""
	align2 = ""

	# when you're at table[0][0] you've matched everything
	while row != 0 or col != 0:

		# score in current cell came from up, left, or up-left
		score = table[row][col]

		# came from above-left, append char to str1 and str2
		if row > 0 and col > 0 and table[row-1][col-1] + matching(str1[row-1], str2[col-1]) == score:
			row = row - 1
			col = col - 1
			align1 = align1 + str1[row]
			align2 = align2 + str2[col]

		# came from above, append char to str1, space to str2
		elif row > 0 and table[row-1][col] + skip == score:
			row = row - 1
			align1 = align1 + str1[row]
			align2 = align2 + pad_character

		# came from left, append char to str2, space to str1
		elif col > 0 and table[row][col-1] + skip == score:
			col = col - 1
			align1 = align1 + pad_character
			align2 = align2 + str2[col]

		# this shouldn't happen, but just in case it does, let's be explicit....
		else:
			raise IndexError("Something spooky happened while recovering optimal alignment. There is a cosmic logic error with this function.")

	#------------------ return strings
	# this reverses strings.
	# thank you guido :^)
	align1 = align1[::-1]
	align2 = align2[::-1]
	return (align1, align2)
