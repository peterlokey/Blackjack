from flask import Flask, request

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
                <button type="button" id="hit_button">Hit</button>
                <button type="button" id="stand_button">Stand</button>
            </div>
        </div>
    </body>    
</html>
"""

@app.route("/")
def print_hands():
    hands_html = """
        <div id="game_box">
            <div id="dealer_hand">
                <img src=images/cardback.png>
                <img src=images/2H.png>
            </div>
            <div id="user_hand">
                <img src=images/AS.png>
                <img src=images/JH.png>
            </div>
            """
    content = page_header + hands_html + page_footer
    return content

app.run()