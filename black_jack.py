"""
 1) The computer plays the Black Jack Game with One Human player where the computer itself is the dealer.
 2) The player and the dealer each are dealt two cards.
 2) The player goes first and can bet money depending on the number of available chips and has the option to
    hit or stand.
 3) The computer(dealer) follows the soft 17 rule.
 4) Face cards (Jack, Queen and King) have the value of 10 and Aces have the value of either 1 or 11, depending
    on the player's preference
 5) A card sum of 21 is 'BLACK JACK', anything above 21 is a 'BUST'

Courtesy : This code has been developed by following the walk through exercise of Pierian-Data
"""

import random


# Global Variables
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

# Dictionary to map the cards to the corresponding values
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        # Called with the print function and displays the cards in the following format "Ace of Spades"
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        # start with an empty list
        self.deck = []
        # Create a deck by iterating through al the suits and ranks
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return "The deck has: " + deck_comp

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.deck)

    def deal(self):
        # Make sure to pop the card to avoid repetition
        return self.deck.pop()


class Hand:
    def __init__(self):
        # start with an empty list
        self.cards = []
        # start with zero value
        self.value = 0
        # add an attribute to keep track of aces
        self.aces = 0

    def add_card(self, card):
        # Card passed in from Deck.deal()
        self.cards.append(card)
        # Pass the rank as a key to the dictionary and add the corresponding value
        self.value += values[card.rank]
        # Track Aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        # If the total exceeds 21, and there is an ace in the hand, adjust the Ace = 11 value to Ace = 1
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self):
        #  This can be set to a default value or supplied by a user input
        self.total = 100
        self.bet = 0

    def win_bet(self):
        # If the player wins, add twice the bet amount to their chips
        self.total += 2 * self.bet

    def lose_bet(self):
        # If the player loses, subtract the bet amount from the chips
        self.total -= self.bet


def take_bet(chips):
    # Function to ask the player to place a bet
    while True:
        # Make sure the player enters an integer
        try:
            chips.bet = int(input("How many chips would you like to bet ? "))
        except ValueError:
            print("Sorry, please provide an integer")
        else:
            # Make sure the player has enough chips
            if chips.bet > chips.total:
                print("Sorry !! You don't have enough chips !! You have {}".format(chips.total))
            else:
                break


def hit(decks, hand):
    # Function to draw a card and add it to the player/dealer hand when called
    single_card = decks.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def hit_or_stand(decks, hand):
    # Function to ask the player if they want to hit or stand
    global playing
    while True:
        x = input("Hit of Stand ? Enter 'h' or 's': ")
        # If someone misunderstands and types HIT/hit/H/STAND/stand/S
        # So assuming that the player meant s/h
        if x[0].lower() == 'h':
            hit(decks, hand)
        elif x[0].lower() == 's':
            print("Player Stands \nDealer's turn !!")
            playing = False
        else:
            # When the player doesn't enter something starting with s/h
            print("Sorry, I didn't get you ! Please Enter 'h' or 's' only !!!!")
            continue
        break


def show_some(player, dealer):
    # Function to hide one dealer card while the player is playing
    print("Dealer's Hand: ")
    print("One card hidden")
    print(dealer.cards[1])
    print("\nPlayer's Hand: ")
    for card in player.cards:
        print(card)


def show_all(player, dealer):
    # Function to show all cards after the player stays
    print("Dealer's Hand: ")
    for card in dealer.cards:
        print(card)
    print("\nPlayer's Hand: ")
    for card in player.cards:
        print(card)


# Consider all scenarios
# Player Busts (>21)
def player_busts(chips):
    print("Player BUSTS")
    chips.lose_bet()


# Player wins
def player_wins(chips):
    print("Player WINS")
    chips.win_bet()


# Dealer Busts (>21)
def dealer_busts(chips):
    print("Player WINS \nDealer BUSTED ")
    chips.win_bet()


# Dealer Wins
def dealer_wins(chips):
    print("Dealer WINS")
    chips.lose_bet()


# When both the player and the dealer get 21
def push():
    print("Dealer and Player Tie !!! \nPUSH !!!")


# Game starts here
while True:
    print("Welcome to BLACKJACK")
    # Create and Shuffle the Deck
    deck = Deck()
    deck.shuffle()

    # Player Hand
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    # Dealer Hand
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up Player's Chips
    player_chips = Chips()

    # Ask the player for their bet
    take_bet(player_chips)

    # Show cards (Keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:
        # Ask the player if they want to hit or stand
        hit_or_stand(deck, player_hand)

        # Show cards
        show_some(player_hand, dealer_hand)

        # Check for player bust
        if player_hand.value > 21:
            player_busts(player_chips)
            break

    # If the player hasn't busted, play dealer's hand until it reaches 17
    # Soft 17 : Rule of most casinos (dealer hits until he reaches 17 or busts)
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Go through different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)
        else:
            push()

    # Show the player their funds
    print("You have {} chips".format(player_chips.total))

    # Ask the player if they want to play again
    new_game = input("Would you like to play another hand ? y/n")
    # Make sure to account for typos (yes, no, YES, NO, Y, N)
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thank you for playing !! \nGood Bye !!")
        break
