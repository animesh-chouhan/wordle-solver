from bs4 import BeautifulSoup

html_text = """
    <game-tile letter="a" evaluation="absent" reveal=""></game-tile><game-tile letter="u" evaluation="absent"></game-tile><game-tile letter="d" evaluation="absent"></game-tile><game-tile letter="i" evaluation="absent"></game-tile><game-tile letter="o" evaluation="present"></game-tile>
"""
soup = BeautifulSoup(html_text, "html.parser")

for tile in soup.find_all("game-tile"):
    letter = tile["letter"]
    evaluation = tile["evaluation"]
    print(letter, evaluation)
