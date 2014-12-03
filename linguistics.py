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

def align(str1, str2):
    ''' return the likeness of str1 to str2 based on their optimal alignment.
        return : int'''
    rows = len(str1)+1
    cols = len(str2)+1
    table = __init_table__(rows,cols)
    print table
    for i in range(1,rows):
        for j in range(1,cols):
            matching = __match__(str1[i-1],str2[j-1]) + table[i-1][j-1]
            skip_str1 = -2 + table[i-1][j]
            skip_str2 = -2 + table[i][j-1]
            table[i][j] = max(matching,skip_str1,skip_str2)
    return table[len(str1)][len(str2)]
