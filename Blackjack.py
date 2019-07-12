#TODO 

#!!!!issues with split() - shouldn't be able to get BJ after split
#consult LC Studio Fireside Story when fixed. Walk through "New Pull," merge, etc.

import random

def deal():
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)
    card = deck.pop()
    suits = ['H', 'D', 'C', 'S']
    random.shuffle(suits)
    suit = suits.pop()
    card = str(card) + suit
    return card
    
    
def hand_total(hand):
    tot = 0
    for card in hand:
        if card[0] == 'J' or card[0] == 'Q' or card[0] == 'K' or card[0] == '1': 
            val = 10
        elif card[0] == 'A':
            val = 11
        else: val = int(card[0])
        tot += val
    if tot > 21 and 'A' in hand:   #scores Aces as 1 if total is > 21 
        clone = hand.copy()
        while tot > 21 and 'A' in clone:
            clone.remove('A')
            tot -= 10
    return tot

def is_blackjack(hand): 
    if hand[0][0] == 'A':
        if hand[1][0] == 'K' or hand[1][0] == 'Q' or hand[1][0] == 'J' or hand[1][0] == '1':
            return True
    if hand[0][0] == 'K' or hand[0][0] == 'Q' or hand[0][0] == 'J' or hand[0][0] == '1':
        if hand[1][0] == 'A':
            return True
    return False

def print_hands(user, dealer):
    user_string = ' '.join(str(x) for x in user)
    print('\nYour Hand:', user_string, '=', hand_total(user))
    print('Dealer is showing', dealer[0])
 
def print_final_hands(user,dealer):
    user_string = ' '.join(str(x) for x in user)
    dealer_string = ' '.join(str(x) for x in dealer)
    print('\nYour Hand:', user_string, '=', hand_total(user))
    print('Dealer   :', dealer_string, '=', hand_total(dealer))

def hit(hand):
    new_card = deal()
    hand.append(new_card)
    return hand

def double_down(hand, wager):
    wager = wager * 2
    hand = hit(hand)
    return wager

def split(hand, dealer_hand, wager):
    hand1 = [hand[0], deal()]
    hand2 = [hand[1], deal()]
    print('\nHAND 1')
    result1, wager1 = play_hand(hand1, dealer_hand, wager)
    print('\nHAND 2')
    result2, wager2 = play_hand(hand2, dealer_hand, wager)
    winnings = 0
    if result1 == 'BJ':
        winnings += (wager1 * 1.5)
    if result1 == 'Win':
        winnings += wager1
    if result1 == 'Lose':
        winnings -= wager1
    if result2 == 'BJ':
        winnings += (wager2 * 1.5)
    if result2 == 'Win':
        winnings += wager2
    if result2 == 'Lose':
        winnings -= wager2
    return winnings

def deal_hands():   
    user_hand = [deal(), deal()] 
    #user_hand = ['A', 'A']  #FOR TESTING
    dealer_hand = [deal(), deal()]
    return user_hand, dealer_hand

def play_dealer_hand(hand):
    score = hand_total(hand)
    while score < 17:
        hand = hit(hand)
        score = hand_total(hand)
    return hand

def decide_winner(user, dealer, wager):
    user_score = hand_total(user)
    dealer_score = hand_total(dealer)    
    #if user_score > 21:
    #    print('You bust!')
    #    input('Press Enter to continue...\n')
    #    return 'Lose'
    if dealer_score > 21:
        print('DEALER BUSTS - You win '+ str(wager)+'!')
        input('Press Enter to continue...\n')
        return 'Win'
    if user_score > dealer_score:
        print('WIN - You win '+ str(wager)+'!')
        input('Press Enter to continue...\n')
        return 'Win'
    if user_score < dealer_score:
        print('LOSE')
        input('Press Enter to continue...\n')
        return 'Lose'
    if user_score == dealer_score:
        print('PUSH')
        input('Press Enter to continue...')
        return 'Push'

def change_wager(bank, wager):
    new_wager = 0
    while new_wager < 10 or new_wager > 300:
        new_wager = int(input('Enter wager: '))
        if new_wager < 10:
            print('Minimum bet is 10')
            continue
        if new_wager > 300:
            print('Maximum bet is 300')
            continue
        if new_wager > bank:
            print("You don't have that much")
            continue
    return new_wager

def play_hand(user_hand, dealer_hand, wager):
    
    if is_blackjack(user_hand):
        winnings = wager * 1.5
        if winnings % 1 == 0: winnings = int(winnings)
        print(user_hand[0], user_hand[1], ' =  BLACKJACK!!\nYou win '+ str(winnings) + '!')
        return 'BJ', wager
    if is_blackjack(dealer_hand):
        print_final_hands(user_hand, dealer_hand)
        print('Dealer has Blackjack. You lose')
        return 'Lose', wager

    print_hands(user_hand, dealer_hand)
    
    first_action = True
    choice = 0
    while choice != '2':
        if user_hand[0][0] == user_hand[1][0]:    #SPLIT
            choice = input('1 - Hit \t2 - Stand \t3 - Double Down \t4 - Split')
            if choice == '4':
                winnings = split(user_hand, dealer_hand, wager)
                if winnings % 1 == 0: winnings = int(winnings) #drops unnecessary decimal point
                if winnings >=0:
                    print('In total, you won '+ str(winnings))
                    return 'Win', winnings
                if winnings <0:
                    print('In total, you lost '+ str(winnings))
                    return 'Lose', winnings * -1
        
        elif first_action: #user can only double down before hitting
            choice = input('1 - Hit \t2 - Stand \t3 - Double Down')
            if choice == '1':       #HIT
                first_action = False
                hit(user_hand)
                print_hands(user_hand, dealer_hand)
                if hand_total(user_hand) > 21:
                    print('LOSE - You Bust.')
                    input('Press Enter to continue...')
                    return 'Lose', wager
                print('\n')
            elif choice == '3':     #DOUBLE DOWN
                wager = double_down(user_hand, wager)
                if hand_total(user_hand) > 21:
                    print('LOSE - You Bust.')
                    input('Press Enter to continue...')
                    return 'Lose', wager
                dealer_hand = play_dealer_hand(dealer_hand)
                print_final_hands(user_hand, dealer_hand)
                return decide_winner(user_hand, dealer_hand, wager), wager
            elif choice == '2':     #STAND
                dealer_hand = play_dealer_hand(dealer_hand)
                print_final_hands(user_hand, dealer_hand)
                if dealer_hand == 'Bust':
                    return 'Win', wager
                else:
                    return decide_winner(user_hand, dealer_hand, wager), wager
            else:print('Something has gone wrong!')
        
        elif not first_action: #called after user has hit (to prevent doubling after hit)
            choice = input('1 - Hit \t2 - Stand')
            if choice == '1':       #HIT
                hit(user_hand)
                print_hands(user_hand, dealer_hand)
                if hand_total(user_hand) > 21:
                    print('LOSE - You Bust.')
                    input('Press Enter to continue...')
                    return 'Lose', wager
                print('\n')
            elif choice == '2':     #STAND
                dealer_hand = play_dealer_hand(dealer_hand)
                print_final_hands(user_hand, dealer_hand)
                if dealer_hand == 'Bust':
                    return 'Win', wager
                else:
                    return decide_winner(user_hand, dealer_hand, wager), wager
            else:print('Something has gone wrong!')

def main_menu(bank, wager):
    selection = 0
    while selection !=1 and selection !=2 and selection !=3:
        if wager > bank: wager = bank
        print('\n\n\nWelcome to Blackjack!\n=====================\nPlease select an option')
        print('(Type the number to choose)')
        print('1 Deal\t\t\t\t\t Bank : ', bank)
        print('2 Change Wager\t\t\t Current Wager :', wager)
        print('3 Quit')
        selection = input()
        if selection == '1': return 1
        elif selection == '2': return 2
        elif selection == '3':return 3
        else: print('Bad input.')


def main():
    bank = 100
    wager = 10
    user_input = 0
    while user_input != 3:
        user_input = main_menu(bank, wager)
        if user_input == 1: 
            user_hand, dealer_hand = deal_hands()
            result, end_wager = play_hand(user_hand, dealer_hand, wager) 
            if result == 'BJ':
                bank += (wager * 1.5)
            if result == 'Win':
                bank += end_wager
            if result == 'Lose':
                bank -= end_wager
        if user_input == 2:
            wager = change_wager(bank, wager)

if __name__ == '__main__':
    main()