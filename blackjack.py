# John Curran

# A simple version of single player blackjack. The player starts out
# with 100 chips in the bank, and can continue to bet at least 10%
# of their bank each round


import random
import time
import os
import colored

# downloads colored if user does not have it already
try:
	print(colored.fg("red") + "" + colored.attr("reset"), end="")
except:
	os.system('pip install colored')
	os.system('cls')
	import colored

#list of card suits and ranks, and the values paired with each rank
suits = ('Hearts', 'Spades', 'Diamonds', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,'Nine': 9, 'Ten': 10, 'Jack': 10,
         'Queen': 10, 'King': 10, 'Ace': 11}

# different text colors used in this game
red = colored.fg("#FF0000")
green = colored.fg("#08DD00")
yellow = colored.fg("#F7E000")
blue = colored.fg("#2865FF")
dark = colored.fg("#AF0000")
reset = colored.attr("reset")

# used for continuous playing
playing_game = True
playing_round = True


# the Card class represents a single card, with a suit, rank, and value 
# and a string representation
class Card():
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
		self.value = values[self.rank]
		
	def __str__(self):
		return self.rank + " of " + self.suit
	
# the Deck class represents a traditional deck of 52 playing cards	
class Deck():
	def __init__(self):
		self.cards = []
		
		#instantiates the traditional deck by going through each suit and rank
		for suit in suits:
			for rank in ranks:
				self.cards.append(Card(suit, rank))
				
	def __str__(self):
		deck = ""
		for card in self.cards:
			deck += str(card) + "\n"
			
		return deck.strip()
		
	# shuffles the deck into a completely random order
	def shuffle(self):
		random.shuffle(self.cards)
		
	# pops one card off of the top of the deck
	def deal(self):
		# reshuffles the deck if every card has been dealt
		if self.cards == []:
			print("New Deck!")
			self.__init__()
			self.shuffle()
			
		return self.cards.pop(0)
		
# the Hand class represents a hand of cards in blackjack, with an associated value
class Hand():
	def __init__(self):
		self.cards = []
		self.value = 0
		
	# adds a card to the hand
	def add_card(self, card):
		self.cards.append(card)
		self.value += card.value
		
	# adjusts the value of the hand based on the aces in the hand.
	# in blackjack, aces have a value of 1 or 11 depending on which
	# is better. This method changes certain ace cards to a value
	# of 1 if it improves the value of the hand
	def aces_adjust(self):
		for card in self.cards:
			if card.rank == "Ace" and card.value == 11 and self.busts():
				self.value -= 10
				card.value = 1
	
		# determines whether the given hand busts
	def busts(self):
		return self.value > 21
	
# the Chips class represents the chips that the player is using to
# bet in the game, including the current bet and the total value of the chips	
class Chips():
	def __init__(self, total):
		self.total = total
		self.bet = 0
		
	# used when the player wins. Add the bet to the total
	def win(self):
		self.total += self.bet
		
	# used when the player loses. Subtract the bet from the total
	def lose(self):
		self.total -= self.bet
		
	# used when the player gets a blackjack. Add the bet and another half of the bet to the total
	def blackjack(self):
		self.total += int(self.bet * 1.5)
		
# the following are functions used in the game
	

# accepts a bet as an input and sets the corresponding chips values. Verifies that the
# input is valid, a positive integer, and at least 10% of the total chips value	
def take_bet(player_chips):
	try:
		bet = float(input(f"Place your bet out of {int(player_chips.total)}: "))
		if bet % 1 != 0 or bet <= 0:
			print("Please use a positive integer value\n")
			take_bet(player_chips)
		elif bet > player_chips.total:
			print("You cannot bet more than you have\n")
			take_bet(player_chips)
		elif bet < player_chips.total * 0.1:
			print("You must bet at least 10% of your bank total\n")
			take_bet(player_chips)
		else:
			player_chips.bet = bet
		
	except:
		print("Invalid input\n")
		take_bet()
		
# adds a card to the hand from the deck, adjusting for aces
def hit(deck, hand):
	hand.add_card(deck.deal())
	hand.aces_adjust()
	
# requests from the player whether to hit or stand, ending the round if the
# player stands
def hit_or_stand(deck, hand):
	global playing_round

	hit_stand = input("Hit or stand? : ").lower()
	if hit_stand == "hit":
		hit(deck, hand)
		
	elif hit_stand == "stand":
		playing_round = False
		
	else:
		print("Invalid input\n")
		hit_or_stand(deck, hand)
       
# displays the cards of the dealer and player, along with hand values and the chips of the player	   
def show(player, dealer, player_chips):
	os.system('cls')
	print(red + "Dealer:" + reset)
	for card in dealer.cards:
		print(card)
	print(f"Total: {dealer.value}\n\n")


	print(green + "Player:" + reset)
	for card in player.cards:
		print(card)
	print(f"Total: {player.value}")
		
	print(f"\n\nBank Total: {int(player_chips.total)}")
	print(f"Bet: {int(player_chips.bet)}\n")
	
# requests from the player whether to play another round, adjusting the 
# boolean value accordingly 
def play_again():
	global playing_game

	x = input("Do you want to play again? (y/n): ").lower()
	if x == "y":
		playing_game = True
		os.system('cls')
	elif x == "n":
		playing_game = False
	else:
		print("Invalid input\n")
		play_again()
		
# determines whether the player or the dealer won, and displays the new bank total for the player
def winner(player, dealer, player_chips):
	time.sleep(0.25)
	if dealer.busts() or (dealer.value < player.value and not player.busts()):
		print(green + "PLAYER wins!" + reset)
		player_chips.win() # player wins
		
	elif player.busts() or (player.value < dealer.value and not dealer.busts()):
		print(red + "DEALER wins" + reset)
		player_chips.lose() # player loses
		
	else:
		print(yellow + "Push" + reset) # tie (push)
		
	print(f"New Bank Total: {int(player_chips.total)}")
		
		

# main function
def main():
	os.system('cls')

	global playing_game
	global playing_round
	
	chips = Chips(100) # start out with 100 chips

	print("Welcome to Blackjack!")
	while playing_game:
		# create new deck, player, and dealer
		deck = Deck()
		deck.shuffle()
		
		dealer = Hand()
		player = Hand()
		take_bet(chips) # start bet
		
		# dealer starts with one card, player starts with two
		hit(deck, dealer)
		hit(deck, player)
		hit(deck, player)
		show(player, dealer, chips)
		
		# a blackjack immediately ends the round
		if player.value == 21:
			print(blue + "BLACKJACK\n" + reset)
			chips.blackjack()
			print(f"Bank Total: {int(chips.total)}")
			play_again()
			
		else:
			playing_round = True
			while playing_round:
				hit_or_stand(deck, player) # continue to hit until the player stands or busts
				show(player, dealer, chips)
				
				if player.busts():
					time.sleep(0.25)
					print(dark + "BUST\n" + reset)
					playing_round = False
					
			# after the player stands, the dealer hits until they reach at least 17
			while dealer.value < 17 and not player.busts():
				hit(deck, dealer)
				time.sleep(2) # 2 second delay to improve the visuals of the dealer adding cards
				show(player, dealer, chips)
			
			# declares winner
			winner(player, dealer, chips)
		
			# if the player has no more chips, they have lost the game and cannot continue playing
			if chips.total == 0:
				print(dark + "\nYou have run out of money...\nThanks for playing!" + reset)
				playing_game = False
			else:
				play_again()
				
	# game ends with a final tally
	print("\nYou ended the game with ", end="")
	print(blue + str(int(chips.total)) + reset, end="")
	print(" chips in your bank!")
		

if __name__ == "__main__":
	main()