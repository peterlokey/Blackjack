from flask import Flask, request, redirect, render_template
import cgi
import random
import ast

#TODO:
'''
Create functions for Double Down & Split

Implement Betting!!
'''

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
    dealer_hand = [deal(), deal()]
    return user_hand, dealer_hand

def hand_total(hand):
    tot = 0
    suitless_hand = []
    for card in hand:
        suitless_hand.append(card[0])
    for card in suitless_hand:
        if card == 'J' or card == 'Q' or card == 'K' or card == '1': 
            val = 10
        elif card == 'A':
            val = 11
        else: val = int(card)
        tot += val
    if tot > 21 and 'A' in suitless_hand:   #scores Aces as 1 if total is > 21 
        while tot > 21 and 'A' in suitless_hand:
            suitless_hand.remove('A')
            tot -= 10
    return tot

def play_dealer_hand(hand):
    score = hand_total(hand)
    while score < 17:
        hand.append(deal())
        score = hand_total(hand)
    return hand

def decide_winner(user, dealer, wager):
    user_score = hand_total(user)
    dealer_score = hand_total(dealer)    
    if user_score > 21:
        return 'BUST'
    if dealer_score > 21:
        #print('DEALER BUSTS - You win '+ str(wager)+'!')
        return 'DEALER BUSTS - YOU WIN'
    if user_score > dealer_score:
        #print('WIN - You win '+ str(wager)+'!'
        return 'YOU WIN'
    if user_score < dealer_score:
        return 'LOSE'
    if user_score == dealer_score:
        return('PUSH')

def is_blackjack(hand): 
    suitless_hand = []
    for card in hand:
        suitless_hand.append(card[0])
    
    if suitless_hand[0][0] == 'A':
        if suitless_hand[1][0] == 'K' or suitless_hand[1][0] == 'Q' or suitless_hand[1][0] == 'J' or suitless_hand[1][0] == '1':
            return True
    if suitless_hand[0][0] == 'K' or suitless_hand[0][0] == 'Q' or suitless_hand[0][0] == 'J' or suitless_hand[0][0] == '1':
        if suitless_hand[1][0] == 'A':
            return True
    return False
  

@app.route("/hit", methods=['POST'])
def hit():
    user_hand = request.args.get("user_hand")
    dealer_hand = request.args.get("dealer_hand")

    user_hand = ast.literal_eval(user_hand)
    dealer_hand = ast.literal_eval(dealer_hand)
    
    user_hand.append(deal())
    user_total = hand_total(user_hand)
    dealer_total = hand_total(dealer_hand)

    if user_total > 21:
        dealer_hand = play_dealer_hand(dealer_hand)
        dealer_total = hand_total(dealer_hand)
        result = decide_winner(user_hand, dealer_hand, None)
        return render_template("end.html", user_hand=user_hand, dealer_hand=dealer_hand, user_total=user_total, dealer_total=dealer_total, result=result)

    return render_template("play.html", user_hand=user_hand, dealer_hand=dealer_hand, user_total=user_total)
    


@app.route("/play") 
def print_hands():
    user_hand, dealer_hand = deal_hands()
    user_total = hand_total(user_hand)
    dealer_total = hand_total(dealer_hand)
    paired = "False"
    if user_hand[0][0] == user_hand[1][0]:
        paired = "True"

    result = decide_winner(user_hand, dealer_hand, None)

    if is_blackjack(user_hand):
        result = "BLACKJACK!!!"
        if is_blackjack(dealer_hand):
            result = "PUSH"
        return render_template("end.html", user_hand=user_hand, dealer_hand=dealer_hand, user_total=user_total, dealer_total=dealer_total, result=result)
    if is_blackjack(dealer_hand):
        result = "DEALER BLACKJACK. YOU LOSE."
        return render_template("end.html", user_hand=user_hand, dealer_hand=dealer_hand, user_total=user_total, dealer_total=dealer_total, result=result)
    return render_template("play.html", user_hand=user_hand, dealer_hand=dealer_hand, user_total=user_total, result=result, paired=paired)

@app.route("/stand", methods=['POST'])
def stand():
    user_hand = request.args.get("user_hand")
    dealer_hand = request.args.get("dealer_hand")

    user_hand = ast.literal_eval(user_hand)
    dealer_hand = ast.literal_eval(dealer_hand)
    user_total = hand_total(user_hand)
    dealer_hand = play_dealer_hand(dealer_hand)
    dealer_total = hand_total(dealer_hand)
    result = decide_winner(user_hand, dealer_hand, None)
    return render_template("end.html", user_hand=user_hand, dealer_hand=dealer_hand, user_total=user_total, dealer_total=dealer_total, result=result)

@app.route("/menu")
def menu():
    return render_template('menu.html')

@app.route("/")
def main():
    bank = 100
    wager = 10
    user_input = 0
    
    return render_template('menu.html')

"""     
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
"""
app.run()