import tkinter as tk
from tkinter.messagebox import showinfo,showwarning

#Width: how many cells wide the board is
#Height: how many cells tall the board is
#Connect: How many chips you need in a row to win
width = 7
height = 6
connect = 4
player1_turn = True
board = [[None for i in range(height)]for h in range(width)]

"""board[COL][ROW]"""


""" This recursive function will give you the index of the lowest
    available spot the connect4 piece can drop to. It will return
    -1 if there are no spots left                                 """
def recursive_gravity(array, arr_index=0):
    try:
        if(array[arr_index] == None):
            return recursive_gravity(array, arr_index+1)+1
        else:
            return -1
    except IndexError:
        return -1



def vertical_win(coord):

    win_result = False
    
    def win_check(col,row,count=0):
        if(count > (connect-2)):
            return True
        elif(board[col][row+count] == board[col][row+count+1]):
            return True and win_check(col,row,count+1)
        else:
            return False

    #Vertical win has the unique clause that a chip must at least be
    #4 units high to even consider the possibility of a win scenario
    if((height - coord[1])  < connect):
        win_result = False
    else:
        win_result = win_check(coord[0],coord[1])

    return win_result

def horizontal_win(coord):
    #coord is the coords of the most recent chip placement
    win_result = False

    """Three checks are being made here
        1.  Checking to see if 4-in-a-row (or custom connect size) have been compared yet.
            In a normal game, 3 comparisons must be made (0==1,1==2,2==3) to determine if 
            this is a winning row. If 3 comparisons have been made, then we know that it's
            a winning row because we've met the criteria to get here. (More info in next point)
        2.  Checking to see if the current chip is equal to the next chip. If yes, then continue
            recursion. If no, go to the else statement, and return False, getting out of the
            function.
    """
    def win_check(col,row,count=0):
        if(count > (connect-2)):
            return True
        elif(board[col+count][row] == board[col+count+1][row]):
            return True and win_check(col,row,count+1)
        else:
            return False
    
    for column in range(max(coord[0]-connect+1,0),min(coord[0]+1,width-3)):
        win_result = win_result or win_check(column,coord[1])
    
    return win_result

def NE_diagonal_win(coord):
    
    win_result = False

    def win_check(col,row,count=0):
        if(count > (connect-2)):
            return True
        elif(board[col+count][row-count] == board[col+count+1][row-count-1]):
            return True and win_check(col,row,count+1)
        else:
            return False

    #the if statement checks to see if the coordinates are in a place where there are
    #at least 4 places for chips in a row. Not 100% efficient, but good enough
    for i in range(connect):
        if(coord[0]-i <= width-connect and coord[0]-i >= 0 and coord[1]+i >= connect-1 and coord[1]+i < height):
            win_result = win_result or win_check(coord[0]-i,coord[1]+i)
    
    return win_result

def NW_diagonal_win(coord):

    win_result = False

    def win_check(col,row,count=0):
        if(count > (connect-2)):
            return True
        elif(board[col-count][row-count] == board[col-count-1][row-count-1]):
            return True and win_check(col,row,count+1)
        else:
            return False

    #the if statement checks to see if the coordinates are in a place where there are
    #at least 4 places for chips in a row. Not 100% efficient, but good enough
    for i in range(connect):
        if(coord[0]+i >= connect-1 and coord[0]+i < width and coord[1]+i >= connect-1 and coord[1]+i < height):
            print(i)
            win_result = win_result or win_check(coord[0]+i,coord[1]+i)

    return win_result




window = tk.Tk()
window.title("Connect 4")

def drop_chip(col):
    global player1_turn
    position = recursive_gravity(board[col])

    if(player1_turn):
        chip = "x"
        color = "red"
    else:
        chip = "o"
        color = "yellow"

    if(position >= 0):
        board[col][position] = chip
        slots[col][position]["background"] = color
        player1_turn = not player1_turn
    else:
        showwarning('Cannot Place Chip','Column already full!\n\nTry somewhere else')

    final_score = vertical_win([col,position]) or horizontal_win([col,position]) or NE_diagonal_win([col,position]) or NW_diagonal_win([col,position])
    if(final_score):
        showinfo("Winner!",f"{color} wins!")

    globals()['final_score'] = True

choose_area = tk.Frame()
choose_area.pack()

play_area = tk.Frame()
play_area.pack(fill=tk.BOTH)

for cols in range(7):
    choice = tk.Button(
        master = choose_area,
        text = "Drop",
        command = lambda arg1=cols: drop_chip(arg1)
    )
    choice.grid(column=cols,row=0)

slots = [[None for i in range(height)]for h in range(width)]
for row in range(6):
    for col in range(7):
        slots[col][row] = tk.Frame(
            master=play_area,
            relief=tk.RAISED,
            borderwidth=1,
            width = 62,
            height = 62
        )
        slots[col][row].grid(row=row, column=col, padx=3, pady=3)
        #grid_label = tk.Label(master=slot) #text=f"Row {row}\nColumn {col}")
        #grid_label.pack()


window.mainloop()