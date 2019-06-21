from flask import Flask, request, redirect, render_template
import cgi
import random

app = Flask(__name__)

app.config['DEBUG'] = True

def deal():
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)
    card = deck.pop()
    suits = ['H', 'D', 'C', 'S']
    random.shuffle(suits)
    suit = suits.pop()
    card = str(card) + suit
    return card

def deal_hands():   
    user_hand = [deal(), deal()]
    #user_hand = ['A', 'A']  #FOR TESTING
    dealer_hand = [deal(), deal()]
    return user_hand, dealer_hand

@app.route("/hit")
#hand = get.
def hit(hand):
    new_card = deal()
    hand.append(new_card)
    return hand

@app.route("/play") 
def print_hands():
    user_hand, dealer_hand = deal_hands()
    dealer_print_str = "<img src=https://raw.githubusercontent.com/peterlokey/Blackjack/front-end-dev/images/cardback.png>"
    user_print_str = ''
    for card in user_hand:
        user_print_str += "<img src=https://raw.githubusercontent.com/peterlokey/Blackjack/front-end-dev/images/{card}.png>".format(card=card)
    i=1
    for card in dealer_hand:
        if i == 1: #skips the first card, which must be displayed as face-down
            i += 1
            continue
        dealer_print_str +="<img src=https://raw.githubusercontent.com/peterlokey/Blackjack/front-end-dev/images/{card}.png>".format(card=card)
    
    #TODO there's a problem with my print strings. The problem could be because they're concatenated on the same line? Try """ ?
    return render_template("base.html", user_hand=user_print_str, dealer_hand=dealer_print_str)

@app.route("/")


def main():
    bank = 100
    wager = 10
    user_input = 0
    
    return render_template('menu.html')

        
#        if user_input == 1: 
#            user_hand, dealer_hand = deal_hands()
#            result, end_wager = play_hand(user_hand, dealer_hand, wager) 
#            if result == 'BJ':
#                bank += (wager * 1.5)
#            if result == 'Win':
#                bank += end_wager
#            if result == 'Lose':
#                bank -= end_wager
#        if user_input == 2:
#            wager = change_wager(bank, wager)

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
app.run()