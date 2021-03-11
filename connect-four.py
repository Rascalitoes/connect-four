width = 7
height = 6

board = [[None for i in range(height)]for h in range(width)]

"""
# board[COL][ROW]
board[3][0] = "x"
board[2][1] = "x"
board[1][2] = "x"
board[0][3] = "x"
"""

""" This recursive function will give you the index of the lowest
    available spot the connect4 piece can drop to. It will return
    -1 if there are no spots left   """


def recursive_gravity(array, arr_index=0):
    try:
        if(array[arr_index] == None):
            return recursive_gravity(array, arr_index+1)+1
        else:
            return -1
    except IndexError:
        return -1

def add_chip(col,chip):
    position = recursive_gravity(board[col])
    if(position >= 0):
        board[col][position] = chip



def vertical_win():

    win_result = False

    # Poorly named, but this recursively goes through 4 rows to see if they match by
    # comparing one row to the next and aggregating the results through boolean AND logic
    def going_through(row, col, count=0):
        # count < 2 because that's 0==1, 1==2, and else takes care of 2==3
        # starting at 1, that'd be 1==2, 2==3, and else takes card of 3==4
        if(count < 2):
            return ((board[col][row+count] == board[col][row+count+1] and board[col][row+count] != None) and going_through(row, col, count+1))
        else:
            return (board[col][row+count] == board[col][row+count+1])


    # Since going_through() goes through the next 4 rows, this loop stops 4 short of total width
    for column in range(width):
        for row in range(height-3):
            win_result = win_result or going_through(row, column)

    return win_result

def horizontal_win():

    win_result = False

    def going_through(row,col,count=0):
        if(count<2):
            return (board[col+count][row] == board[col+count+1][row] and board[col+count][row] != None) and going_through(row,col,count+1)
        else:
            return board[col+count][row] == board[col+count+1][row]

    for row in range(height):
        for column in range(width-3):
            win_result = win_result or going_through(row,column)
    
    return win_result

def SE_diagonal_win():
    
    win_result = False

    def going_through(row,col,count=0):
        if(count<2):
            return (board[col+count][row+count] == board[col+count+1][row+count+1] and board[col+count][row+count] != None) and going_through(row,col,count+1)
        else:
            return board[col+count][row+count] == board[col+count+1][row+count+1]

    for row in range(height-3):
        for column in range(width-3):
            win_result = win_result or going_through(row,column)
    
    return win_result

def SW_diagonal_win():

    win_result = False

    def going_through(row,col,count=0):
        if(count<2):
            return (board[col-count][row+count] == board[col-count-1][row+count+1] and board[col-count][row+count] != None) and going_through(row,col,count+1)
        else:
            return board[col-count][row+count] == board[col-count-1][row+count+1]

    for row in range(height-3):
        for column in range(width-3):
            win_result = win_result or going_through(row,width-column-1)

    return win_result


add_chip(0,"x")



final_score = vertical_win() or horizontal_win() or SE_diagonal_win() or SW_diagonal_win()

board