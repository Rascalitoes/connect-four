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
    -1 if there are no spots left   """
def recursive_gravity(array, arr_index=0):
    try:
        if(array[arr_index] == None):
            return recursive_gravity(array, arr_index+1)+1
        else:
            return -1
    except IndexError:
        return -1



def vertical_win():

    win_result = False

    # Poorly named, but this recursively goes through 4 rows to see if they match by
    # comparing one row to the next and aggregating the results through boolean AND logic
    def going_through(row, col, count=0):
        # count < (connect-2) because else takes care of the final 2 compares
        #   for connect = 4 that's 0==1, 1==2, and else takes care of 2==3
        # starting at 1, that'd be 1==2, 2==3, and else takes card of 3==4
        if(count < (connect-2)):
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
        if(count<(connect-2)):
            return ((board[col+count][row] == board[col+count+1][row] and board[col+count][row] != None) and going_through(row,col,count+1))
        else:
            return (board[col+count][row] == board[col+count+1][row])

    for row in range(height):
        for column in range(width-3):
            win_result = win_result or going_through(row,column)
    
    return win_result

def SE_diagonal_win():
    
    win_result = False

    def going_through(row,col,count=0):
        if(count<(connect-2)):
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
        if(count<(connect-2)):
            return (board[col-count][row+count] == board[col-count-1][row+count+1] and board[col-count][row+count] != None) and going_through(row,col,count+1)
        else:
            return board[col-count][row+count] == board[col-count-1][row+count+1]

    for row in range(height-3):
        for column in range(width-3):
            win_result = win_result or going_through(row,width-column-1)

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

    final_score = vertical_win() or horizontal_win() or SE_diagonal_win() or SW_diagonal_win()
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