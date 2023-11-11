import random


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
        
