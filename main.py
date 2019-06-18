from flask import Flask, request
import random

app = Flask(__name__)

app.config['DEBUG'] = True

page_header="""
<!DOCTYPE html>
<html>
    <style>
        body {
            background-color: gray;
        }

        header {
            position: relative;
            margin-top: 10px;
            width: 800px;
            height: 50px;
            text-align: center;
            color: white;
            font-size: 40px;
        }

        #game_box {
            width: 800px;
            height: 550px; 
            border-style: solid;
            border-width: 5px;
            border-color: black;
            background-color: green;
        }

        #dealer_hand {
            position: fixed;
            left: 250px;
            top: 80px;
            width: 550px;
            height: 170px;
            border-style: hidden;
            border-width: 2px;
            border-color: black;
        }

        #user_hand {
            position: fixed;
            left: 250px;
            top: 330px;
            width: 550px;
            height: 170px;
            border-style: hidden;
            border-width: 2px;
            border-color: black;
        }

        img {
            width: 100px;
            height: 154px;
        }

        #hit_button {
            position: fixed;
            left: 300px;
            top: 530px;
        }

        #stand_button {
            position: fixed;
            left: 400px;
            top: 530px;
        }
    </style>
    <head>
        <link href="style.css" type="text/css" rel="stylesheet">
    </head>
    <body>
        <header>
            BLACKJACK
        </header>
"""

page_footer="""
            <div>
                <button type="button" id="hit_button" action="/hit">Hit</button>
                <button type="button" id="stand_button">Stand</button>
            </div>
        </div>
    </body>    
</html>
"""
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
    dealer_print_str = '<img src=https://raw.githubusercontent.com/peterlokey/Blackjack/front-end-dev/images/cardback.png>'
    user_print_str = ''
    for card in user_hand:
        user_print_str += '<img src=https://raw.githubusercontent.com/peterlokey/Blackjack/front-end-dev/images/{card}.png>'.format(card=card)
    i=1
    for card in dealer_hand:
        if i == 1: #skips the first card, which must be displayed as face-down
            i += 1
            continue
        dealer_print_str +='<img src=https://raw.githubusercontent.com/peterlokey/Blackjack/front-end-dev/images/{card}.png>'.format(card=card)
    hands_html = "<div id='game_box'><div id='dealer_hand'>"+dealer_print_str+"</div><div id='user_hand'>"+user_print_str +"</div>"
    content = page_header + hands_html + page_footer
    return content

@app.route("/")


def main():
    bank = 100
    wager = 10
    user_input = 0
    
    menu = """
<!DOCTYPE html>
<html>
    <head>
        <link href="style.css" type="text/css" rel="stylesheet">
    </head>
    <body>
        <header>
            BLACKJACK
        </header>
        <form action="/play">
            <input type="submit" value = "Deal" />
        </form>
    </body>
</html>
"""
    return menu

        
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