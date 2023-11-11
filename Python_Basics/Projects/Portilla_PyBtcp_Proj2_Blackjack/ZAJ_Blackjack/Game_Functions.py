

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

