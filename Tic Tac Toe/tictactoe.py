import os
import random

def clear_output():
	os.system('cls')
	
def display_board(board):
    print('   |   |   ')
    print(' ' + board[0] + ' | ' + board[1] + ' | ' + board[2] + ' ')
    print('   |   |   ')
    print('-----------')
    print('   |   |   ')
    print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5] + ' ')
    print('   |   |   ')
    print('-----------')
    print('   |   |   ')
    print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8] + ' ')
    print('   |   |   \n')
	
def player_input():
    player1 = ""
    player2 = ""
    
    while player1 == "":
        player1 = input("Player 1 (X): ").strip()
        
        if player1 == "":
            print("Sorry, invalid player name")
            
            
    while player2 == "":
        player2 = input("Player 2 (O): ").strip()
        
        if player2 == "":
            print("Sorry, invalid player name")
            
    return [player1, player2]
	
def place_marker(board, marker, position):
    board[position - 1] = marker
    return board
	
def check_win(board, mark):    
    win1 = (board[0] == board[1] == board[2] == mark)
    win2 = (board[3] == board[4] == board[5] == mark)
    win3 = (board[6] == board[7] == board[8] == mark)
    win4 = (board[0] == board[3] == board[6] == mark)
    win5 = (board[1] == board[4] == board[7] == mark)
    win6 = (board[2] == board[5] == board[8] == mark)
    win7 = (board[0] == board[4] == board[8] == mark)
    win8 = (board[2] == board[4] == board[6] == mark)
    
    for win in [win1, win2, win3, win4, win5, win6, win7, win8]:
        if win:
            return True
        
    return False;
	
def choose_first():
    return random.randint(0,1)
	
def space_check(board, position):
    return board[position - 1] == ' '
	
def full_board_check(board):
    for position in range(0,9):
        if space_check(board, position):
            return False
        
    return True
	
def player_choice(board):
    choice = 'wrong'
    
    while choice not in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] or not space_check(board, int(choice)):
        choice = input("Choose a position on the board (1-9): ").strip()
        
        if choice not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            print("Sorry, invalid position. Try again.")
        elif not space_check(board, int(choice)):
            print("Sorry, that space is already taken. Try again.")
    
    return int(choice)
	
def replay():
    choice = 'wrong'
    
    while choice not in ['y', 'n']:
        choice = input("Would you like to keep playing? (y/n): ").strip().lower()
        
        if choice not in ['y', 'n']:
            print("Sorry, that is not a valid response. Please try again")
            
    if choice == 'y':
        return True
    else:
        return False
		



print("Welcome to Tic Tac Toe!")
print("\nHere are the positions on the board")
display_board(['1', '2', '3', '4', '5', '6', '7', '8', '9'])

play = True
while play:

	board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
	marks = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O']
	players = player_input()
	players = [players[0], players[1], players[0], players[1], players[0], players[1], players[0], players[1], players[0], players[1]]
	index = choose_first()
	
	clear_output()
	print(f'{players[index]} goes first!')
	display_board(board)

	while not (full_board_check(board) or check_win(board, 'X') or check_win(board, 'O')):
		position = player_choice(board)
		board = place_marker(board, marks[index], position)
		
		clear_output()
		display_board(board)

		if check_win(board, marks[index]):
			print(f"Congratulations {players[index]}! You win!")
		elif full_board_check(board):
			print("It's a draw!")

		index = index + 1
		
		
	play = replay()
	if play:
		clear_output()