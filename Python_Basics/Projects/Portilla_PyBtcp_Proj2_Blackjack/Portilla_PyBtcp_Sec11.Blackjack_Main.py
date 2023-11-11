# Game classes
# import ZAJ_Blackjack.Classes
from ZAJ_Blackjack.Classes import Card
from ZAJ_Blackjack.Classes import Deck
from ZAJ_Blackjack.Classes import Player
# Game functions
from ZAJ_Blackjack.Game_Functions import eval_hand
from ZAJ_Blackjack.Game_Functions import prompt_player
from ZAJ_Blackjack.Game_Functions import place_bet

import os


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
        #clear_output()  # Remember, this only works in jupyter!
        os.system('cls')
        
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
