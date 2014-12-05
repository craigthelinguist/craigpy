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
        if cangodiag and t[row-1][col-1] + __match__(str1[row-1],str2[col-1]) == score:
            row = row - 1
            col = col - 1
            align1 = align1 + str1[row]
            align2 = align2 + str2[col]

        # move up a row, append char to str1, space to str2
        elif cangoabov and t[row-1][col] - 2 == score:
            row = row - 1
            align1 = align1 + str1[row]
            align2 = align2 + "_"

        # move across a col, append char to str2, space to str1
        elif cangoleft and t[row][col-1] - 2 == score:
            col = col - 1
            align1 = align1 + "_"
            align2 = align2 + str2[col]

        # shouldn't happen, but just in case.
        else:
            print "something fucked up"
            print "returning what has been computed so far...."
            return (align1,aling2)
            
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
