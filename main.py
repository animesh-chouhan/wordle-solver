import random
import logging
import asyncio
import requests
import pyperclip
from ast import literal_eval
from pyppeteer import launch
from bs4 import BeautifulSoup

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

word_list = []


def get_words():
    js_file_url = "https://www.powerlanguage.co.uk/wordle/main.e65ce0a5.js"
    js_file = requests.get(js_file_url).text
    start1 = js_file.find("var La=") + len("var La=")
    end1 = js_file.find("],", start1) + 1
    # print(js_file[start1: end1])
    word_list.extend(literal_eval(js_file[start1: end1]))

    start2 = js_file.find("Ta=", end1) + len("Ta=")
    end2 = js_file.find("],", start2) + 1
    # print(js_file[start2: end2][0])
    word_list.extend(literal_eval(js_file[start2: end2]))


def modify_word_list(position, letter, evaluation):
    global word_list
    new_word_list = []
    logging.info(str(position) + " " + evaluation + " " + letter)
    if evaluation == "absent":
        new_word_list = [word for word in word_list if letter not in word]

    if evaluation == "correct":
        new_word_list = [
            word for word in word_list if word[position] == letter]

    if evaluation == "present":
        for word in word_list:
            if letter in word and word[position] != letter:
                new_word_list.append(word)

    word_list = new_word_list
    logging.info(len(word_list))
    logging.info(word_list)


async def main():
    get_words()
    browser = await launch(headless=False, args=["--start-maximized"])
    page = await browser.newPage()
    await page.setViewport({"width": 1920, "height": 1080})
    await page.goto("https://www.powerlanguage.co.uk/wordle/")
    await asyncio.sleep(1)

    await page.evaluate('() => { document.querySelector("body > game-app").shadowRoot.querySelector("#game > game-modal").shadowRoot.querySelector("div > div > div").click() }')

    for j in range(6):
        guessed_word = random.choice(word_list)
        logging.info(guessed_word)
        await asyncio.sleep(1)
        await page.keyboard.type(guessed_word)
        await page.keyboard.press("Enter")
        await asyncio.sleep(1)

        html_text = await page.evaluate('() => { return document.querySelector("body > game-app").shadowRoot.querySelector("#board > game-row:nth-child(' + str(j+1) + ')").shadowRoot.querySelector("div").outerHTML }')
        soup = BeautifulSoup(html_text, "html.parser")

        flag = True
        chars = []
        for i, tile in enumerate(soup.find_all("game-tile")):
            letter = tile["letter"]
            evaluation = tile["evaluation"]
            if evaluation != "correct":
                flag = False

            if letter not in chars:
                modify_word_list(i, letter, evaluation)
            chars.append(letter)

        if flag == True:
            print("Word is: ", guessed_word)
            print("Guessed in ", j + 1, " tries")
            await asyncio.sleep(5)
            await page.evaluate('() => { document.querySelector("body > game-app").shadowRoot.querySelector("#game > game-modal > game-stats").shadowRoot.querySelector("#share-button").click() }')
            print(pyperclip.paste())
            await asyncio.sleep(5)
            await browser.close()
            return 0

    print("Couldn't guess the word. Try again!")

    await asyncio.sleep(5)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
