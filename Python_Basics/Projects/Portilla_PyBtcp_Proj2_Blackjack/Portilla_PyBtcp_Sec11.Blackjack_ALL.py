#!/usr/bin/env python
# coding: utf-8

# # Milestone Project 2 - Blackjack game - DRAFT - Short - V2
# ## A. J. Zerouali (2021/06/10)
# 
# This is my second draft for this project (Section 11 of Pierian Data's Python Bootcamp). See first draft for description.
# 
# Table of contents:
# 
# I - Classes
# 
# II - Functions
# 
# III - Main game
# 
# 

# ________________________
# 
# # I - Classes
# 

# ________________________
# 
# ## I.1 - The card class
# 
# All crucial objects of the game will be lists of objects of this card class.
# 
# **Important note:** When writing the function that evaluates hands, I will have to be **very** careful with how it works on aces.
# 
# 

# In[1]:


class Card():
    # Suite and face
    def __init__(self, face= 'Ace', suite = 'Hearts'):
        self.face  = face
        self.suite  = suite
    
                    
    # String representation of an instance
    def __str__(self):
        #return ('Card is '+ self.face + ' of '+ self.suite)
        return f'\u2022 {self.face} of {self.suite}'
    
    # Methods (subject) to change
    
    def get_face(self):
        return self.face
        


# ________________________
# 
# ## I.2 - The Deck class
# 
# Main attribute: A list of 52 cards. Methods: shuffle, deal.
# 
# **Important note:** Each game will have one instance of this class.
# 
# 

# In[2]:


# Where should I put this inclusion for the main() file?
from random import shuffle as shuffle
class Deck():
    # Suite and face
    def __init__(self):
        self.cards  = []
        lst_suites = ['Hearts', 'Clubs', 'Spades', 'Diamonds']
        lst_faces = ['Ace', '2', '3', '4', '5', '6', '7',                       '8', '9', '10', 'Jack', 'Queen', 'King']
        #Build unshuffled deck
        for i in lst_suites:
            for j in lst_faces:
                self.cards.append(Card(j,i))
                    
    # Methods (subject) to change
    
    ## Shuffle the Deck
    def shuffle_deck(self):
        shuffle(self.cards)
    
    ## Deal the last card in the self.cards list. Beware if Deck is empty
    def deal_card(self):
        if len(self.cards) == 0:
            print('Deck is impty!')
            return None
        elif len(self.cards) == 1:
            print('Last card!')
            out_card = self.cards[-1]
            self.cards = []
            return out_card
        elif len(self.cards) > 1:
            out_card = self.cards[-1]
            # Replace by all cards except last in Deck
            self.cards = self.cards[0:-2+1] 
            # Return last card in Deck
            return out_card
            


# ________________________
# 
# ## I.3 - The Player class
# 
# There will be 2 players: Main player and dealer.
# 
# **Important note:** This class will interact with the Card() and Deck() classes
# 
# 

# In[3]:


class Player():
    # If the player is 'Dealer', object needn't have money
    # When prompting the player to enter her name, check that she doesn't choose the keyword 'Dealer'
    def __init__(self, name= 'Player', money = 3000):
        
        # Important: Either 
        self.name = name
        
        # Player's wallet. Set to -1 if dealer?
        self.money  = money
        
        # Important: This has to be a list of Card() objects
        self.hand = []
        
        # Current bet
        self.cur_bet = 0
    
                    
    # String representation of an instance
    def __str__(self):
        if self.name=='Dealer':
            return 'This is the Dealer.'
        else:
            return f'Player {self.name}, with ${self.money} left.'
    
    # Methods (subject) to change. IMPORTANT: Most methods are never used by 'Dealer'.
    ## I'm implementing the Dealer as a player because he also has a hand.
    ## BEWARE: When displaying each "Player's" hand at the beginning of the round,
    ## the dealer's second card IS FACE DOWN.
    
    def receive_card(self, in_card):
        self.hand.append(in_card)
    
    # This method displays the player's hand:
    def display_hand(self, ini_hand):
        ## ini_hand = True only when the dealer gives 2 cards each at beginning of round
        if self.name=='Dealer' and ini_hand:
            print(f'\u2022\u2022 {self.name}\'s hand \u2022\u2022')
            # Hide first card, i.e. dealer.hand[0]
            print('\u2022 CARD IS FACE DOWN')
            print(self.hand[1])
            print('\n')
        else:
            print(f'\u2022\u2022 {self.name}\'s hand \u2022\u2022')
            for i in self.hand:
                print(i)
            print('\n')
    
    # If the Player wins the round, this method adds the amount bet to his wallet         
    def win_round(self):
        self.money = self.money + self.cur_bet
    
    # If Player loses the round, this method decreases the amount bet to his wallet  
    def lose_round(self):
        # Beware: The Player shouldn't be allowed to place a bet unless player_bet <= self.money
        self.money = self.money - self.cur_bet
        


# ____________________________
# 
# # II - Functions
# 
# Here are the functions that we'll need during the game:
# 
# **- Display Player's hand:** This function displays the Player or the Dealer's hand. Should refresh each time a player hits. 
# 
# **- Prompt player:** A function with 2 modes: "Continue game" (Yes/No) and "Make move" (Hit/Stand). Checks if input is valid and returns a specific string to be used elsewhere in main game.
# 
# **- Place bet:** Function taking main player as input, and which prompts him to place a bet which doesn't exceed the wallet.
# 
# 
# 

# In[4]:


# Function that evaluates hands
def eval_hand(in_hand):
    # INPUT: Must be a list of Card() objects
    # Initializations
    out_val_hand = 0 # Final output
    tmp_val_hand = 0 # Total value of hand excluding FIRST 'Ace'
    
    
    lst_suites = ['Hearts', 'Clubs', 'Spades', 'Diamonds']
    lst_number_faces = ['2', '3', '4', '5', '6', '7', '8', '9']
    lst_10_faces = ['10', 'Jack', 'Queen', 'King']
    ## This is the list of positions of 'Ace's in the hand
    ### Do I even need it?
    lst_aces = []
    
    # First: Loop to find the 'Ace's and get total excluding them
    for i in range(len(in_hand)):
        
        if in_hand[i].suite in lst_suites:
        
            ## If the card at position i is an 'Ace', record its position in lst_aces
            if in_hand[i].face == 'Ace':
                lst_aces.append(i)

            ## If the card at position i is in the lst_number_faces, add number to tmp_val_hand 
            elif in_hand[i].face in lst_number_faces:
                tmp_val_hand = tmp_val_hand + int(in_hand[i].face)

            ## If the card at position i is in the lst_10_faces, add 10 to tmp_val_hand 
            elif in_hand[i].face in lst_10_faces:
                tmp_val_hand = tmp_val_hand + 10
                
            ## Just in case
            else:
                print('ERROR: There\'s an issue with last player\'s hand, CONTAINS UNKNOWN CARD')
                return -404
                
        # Just in case
        else:
            print('ERROR: There\'s an issue with last player\'s hand, CONTAINS UNKNOWN CARD')
            return -404
    
    # Secondly: Look at values with 'Ace's
    ## If there are no 'Ace'':
    if len(lst_aces)==0:
        out_val_hand = tmp_val_hand
        
    ## If there's at least one 'Ace':
    else:
         # tmp_val_hand without the first 'Ace'
        if len(lst_aces)>1:
            # If the number of Ace's>1, each additional 'Ace' counts for 1
            tmp_val_hand = tmp_val_hand + (len(lst_aces)-1)
    
        # Value of the hand considering the first 'Ace'
        if tmp_val_hand>10:
            ## If tmp_val_hand>10, first 'Ace' must have value 1
            out_val_hand = tmp_val_hand + 1
        elif (tmp_val_hand+1)<=(tmp_val_hand+11)<=21:
            ## If 11 is the best value for the hand
            out_val_hand = tmp_val_hand + 11
        
    
    return out_val_hand


# Function that prompts player
def prompt_player(prompt_mode):
    
    # Prompt to continue game
    if prompt_mode == 'Continue game': # Ask: 'Continue game? Y/N'
        valid_input = False
        while not valid_input:
            in_str = input('Continue game? Y/N\n')
            if in_str in ['Y', 'y', 'Yes', 'yes', '1']:
                valid_input = True
                out_str = 'Yes'
            elif in_str in ['N', 'n', 'No', 'no', '0']:
                valid_input = True
                out_str = 'No'
            else:
                print('Sorry, your answer is not valid. Let\'s try again.')
        # Return valid answer
        return out_str
    
    # Prompt player to Hit or Stand
    elif prompt_mode == 'Next move': # Ask: 'What is your next move? Hit or Stand? H/S'
        valid_input = False
        while not valid_input:
            in_str = input('What is your next move? Hit or Stand? H/S\n')
            if in_str in ['H', 'h', 'Hit', 'hit', '1']:
                valid_input = True
                out_str = 'Hit'
            elif in_str in ['S', 's', 'Stand', 'stand', '0']:
                valid_input = True
                out_str = 'Stand'
            else:
                print('Sorry, your answer is not valid. Let\'s try again.')
        # Return valid answer
        return out_str
    
    else:
        print('Error: Invalid mode for function prompt_player().')
        return 'ERROR: INVALID MODE'

# Function that prompts the player to place a bet
def place_bet(in_player):
    valid_bet = False
    while not valid_bet:
        try:
            in_int = int(input('Place your next bet please (integer multiple of 10).\n'))
            if in_int%10 != 0:
                print('Sorry, your bet is not a multiple of 10. \nLet\'s try again.')
            # If the input number is a multiple of 10, check if player has enough money.
            else:
                if in_int>in_player.money:
                    print('Sorry, you do not have enough funds for this bet. \nLet\'s try again.')
                # When the bet is valid
                else:
                    valid_input = True
                    print(f'{player.name} bets ${in_int} on the next hand.')
                    return in_int
        # If player's input cannot be converted to an integer
        except:
            print('Sorry, your input is invalid. \nLet\'s try again.')


# ____________________________
# 
# # III - Main Game
# 
# 

# In[14]:


# To clear the screen
from IPython.display import clear_output

# Welcome player, ask if want to play
print('Welcome to the (simplified) Blackjack game!!')
continue_game = prompt_player('Continue game')

if continue_game == 'No':
    pass
    
# If player chooses 'Yes'
elif continue_game == 'Yes':
    
    ## Get player's name ##
    player_name = input('Please enter your name:\n')
    
    ##### 0 - INITIALIZATIONS OF PLAYERS #####
    player = Player(player_name, 3000)
    print(f'{player.name} joined the game with ${player.money}')
    dealer = Player('Dealer', -1)
    
    ##### MAIN GAME LOOP #####
    while continue_game == 'Yes': # and (player.money>0)
        ## Clear the prompt ##
        clear_output()  # Remember, this only works in jupyter!
        
        ##### INITIALIZATIONS OF PLAYER'S HANDS #####
        player.hand = []
        dealer.hand = []
        
        ###############################
        ##### 1 - BEGIN NEW ROUND #####
        ###############################
        
        ## (1.a) Initialize deck and shuffle ##
        main_deck = Deck()
        main_deck.shuffle_deck()
        
        ## (1.b) Player places bet ##
        # Gets updated in Part 4
        player_bet = place_bet(player)
        player.cur_bet = player_bet
        
        ## (1.c) Dealer distributes 4 cards ##
        for i in range(2):
            player.receive_card(main_deck.deal_card())
            print(f'{player.name} received a card.')
            dealer.receive_card(main_deck.deal_card())
            print(f'{dealer.name} received a card.')
        print('\n')
        
        ## (1.d) Display initial hands##
        player.display_hand(True)
        dealer.display_hand(True)
        
        ## (1.e) Compute hand values and initialize state variables for loops below ##
        player_hand_val = eval_hand(player.hand)
        dealer_hand_val = eval_hand(dealer.hand)
        
        # Updated in Part 2
        player_bust = False
        
        # If player got a Blackjack, skip his turn
        if (player_hand_val == 21):
            print(f'{player.name} has a BLACKJACK!\n')
            player_turn = False
        elif (player_hand_val<21):
            player_turn = True
            
        
        ###############################
        ##### 2 - PLAYER'S TURN   #####
        ###############################
        
        
        ## SECOND GAME LOOP ##
        while player_turn and not player_bust:
            # There's a problem below. The player could have been dealt a Blackjack from beginning.
            
            ## (2.b) Prompt player for next move ##
            # Ask if player wants to hit or stand
            player_input = prompt_player('Next move')
            
            # If player stands
            if player_input == 'Stand':
                print(f'{player.name} stands.')
                
                # Break while loop
                player_turn = False
            
            ## (2.c) If player hits ##
            elif player_input == 'Hit':
                print(f'{player.name} hits.')
                
                # Player receives a new card
                player.receive_card(main_deck.deal_card())
                
                # Display new hand
                player.display_hand(False)
            
                ## (2.d) Player's current hand ##

                # Evaluate Player's current hand
                player_hand_val = eval_hand(player.hand)

                # If player is bust, announce and break loop
                if (player_hand_val > 21):
                    print(f'{player.name} is BUST!\n')
                    player_bust = True
                    player_turn = False

                # If player has a Blackjack, announce and break loop
                elif (player_hand_val == 21):
                    print(f'{player.name} has a BLACKJACK!\n')
                    player_turn = False
                
         
                    
        ###############################
        ##### 3 - DEALER'S TURN   #####
        ###############################
        
        ## (3.a) Display Dealer's hand ##
        dealer_bust = False
        dealer.display_hand(False)
        dealer_hand_val = eval_hand(dealer.hand)
        
        ## (3.b) Decide if Dealer's turn ##
        # Dealer has a Blackjack
        if (dealer_hand_val == 21):
            print(f'{dealer.name} has a BLACKJACK!\n')
            dealer_turn = False
        
        # Player is bust, Dealer does nothing
        elif player_bust and (dealer_hand_val <21):
            dealer_turn = False
            
        # Dealer will hit
        elif (not player_bust) and (dealer_hand_val < 21) and (dealer_hand_val <= player_hand_val):
            dealer_turn = True
        
        ## (3.c) Start Dealer's HITTING loop ##
        # To enter this loop, must have player_bust = False
        while dealer_turn:
            # Deal new card to dealer
            dealer.receive_card(main_deck.deal_card())
            
            # Display Dealer's new hand
            dealer.display_hand(False)
            dealer_hand_val = eval_hand(dealer.hand)
            
            ## (3.d) Decide dealer_turn value ##
            # Dealer has a Blackjack, announce and break loop
            if (dealer_hand_val == 21):
                print(f'{dealer.name} has a BLACKJACK!\n')
                dealer_turn = False
                
            # Dealer is BUST, announce and break loop
            elif (dealer_hand_val > 21):
                print(f'{dealer.name} is BUST!\n')
                dealer_bust = True
                dealer_turn = False
                
            elif (dealer_hand_val < 21) and (dealer_hand_val <= player_hand_val):
                dealer_turn = True
            
                
        
        ###############################
        ##### 4 - DETERMINE WINNER   ##
        ###############################
        
        ## (4.a) PUSH cases ##
        if (player_hand_val==dealer_hand_val) or (player_bust and dealer_bust):
            print('PUSH!! No winner this round...\n')
            
            # Reinitialize player's bet (Just in case)
            player_bet =0
            player.cur_bet = 0
            
        ## (4.b) LOSING cases
        elif (player_bust or (player_hand_val<dealer_hand_val)) and (not dealer_bust):
            print(f'{player.name} has LOST!!\n')
            
            # Subtract player's bet from wallet
            player.lose_round()
            player_bet = 0
            player.cur_bet = 0
        
        ## (4.c) WINNING cases
        elif (dealer_bust or (player_hand_val>dealer_hand_val)) and (not player_bust):
            print(f'{player.name} has WON ${player_bet}!! Congratulations!!\n')
            
            # Subtract player's bet from wallet
            player.win_round()
            player_bet = 0
            player.cur_bet = 0
            
        
        
        ##### END OF ROUND - CHECK PLAYER'S WALLET AND ASK IF PLAYER WANTS TO CONTINUE #####
        print(f'{player.name} has ${player.money}.\n')
        if (player.money>0):
            continue_game = prompt_player('Continue game')
        elif (player.money == 0):
            print(f'{player.name} has no funds left. Game over.\n')
            continue_game = 'No'
            
    
print('Thank you! Please come again!')


# In[ ]:




