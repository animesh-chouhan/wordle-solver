import random
import logging
import asyncio
import requests
import pyperclip
from ast import literal_eval
from pyppeteer import launch
from bs4 import BeautifulSoup

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

JS_URL = "https://www.nytimes.com/games-assets/v2/wordle.0184c33d9a3561750c6f.js"
URL = "https://www.nytimes.com/games/wordle/index.html"

word_list = []


def get_words():
    js_file_url = JS_URL
    js_file = requests.get(js_file_url).text
    start1 = js_file.find('"wordle/moogle/SET_INITIAL_STATE"),ba=') + len(
        '"wordle/moogle/SET_INITIAL_STATE"),ba='
    )
    end1 = js_file.find("],", start1) + 1
    # print(js_file[start1: end1])
    word_list.extend(literal_eval(js_file[start1:end1]))
    if len(word_list) == 0:
        raise Exception("Unable to fetch word list. Contact developer.")


def modify_word_list(letter, position, evaluation):
    global word_list
    new_word_list = []
    logging.info(str(position) + " " + evaluation + " " + letter)
    if evaluation == "absent":
        temp_word_list = [word for word in word_list if word[position] != letter]
        new_word_list = [word for word in temp_word_list if letter not in word]

    if evaluation == "correct":
        new_word_list = [word for word in word_list if word[position] == letter]

    if evaluation == "present":
        for word in word_list:
            if letter in word and word[position] != letter:
                new_word_list.append(word)

    word_list = new_word_list
    logging.info(f"Words remaining in dictionary: {str(len(word_list))}")
    # logging.info(word_list)


async def main():
    get_words()
    browser = await launch(headless=False, args=["--start-maximized", "--no-sandbox"])
    page = await browser.newPage()
    await page.setViewport({"width": 1920, "height": 1080})
    await page.goto(URL)
    await asyncio.sleep(1)
    # Click on Play button
    await page.click(
        "body > div > div > div > div > div > div.Welcome-module_buttonContainer__K4GEw > button:nth-child(3)"
    )
    await asyncio.sleep(1)
    # Close instructions
    await page.click("#help-dialog > div > button")

    # To handle repetition of char in guessed word
    evaluation_priority = {"correct": 2, "present": 1, "absent": 0}
    for j in range(6):
        guessed_word = random.choice(word_list)
        logging.info(f"Guessed word: {guessed_word}")
        await asyncio.sleep(1)
        await page.keyboard.type(guessed_word)
        await page.keyboard.press("Enter")
        await asyncio.sleep(3)

        query = (
            '() => { return document.querySelector("#wordle-app-game > div.Board-module_boardContainer__TBHNL > div > div:nth-child('
            + str(j + 1)
            + ')").outerHTML }'
        )
        # Get each row
        html_text = await page.evaluate(query)
        soup = BeautifulSoup(html_text, "html.parser")

        flag = True
        char_status = {}
        for i, tile in enumerate(soup.find_all("div", "Tile-module_tile__UWEHN")):
            letter = tile.get_text()
            evaluation = tile["data-state"]
            if evaluation != "correct":
                flag = False
            current_char_status = {letter: evaluation}
            # Updating the evaluation in case of repetition
            if letter in char_status.keys():
                if (
                    evaluation_priority[current_char_status[letter]]
                    > evaluation_priority[char_status[letter]["evaluation"]]
                ):
                    char_status[letter]["evaluation"] = current_char_status[letter]
                    char_status[letter]["position"] = i
            else:
                char_status[letter] = {
                    "position": i,
                    "evaluation": current_char_status[letter],
                }

        for letter, value in char_status.items():
            modify_word_list(letter, value["position"], value["evaluation"])
        # Triggers when all letters are correct
        if flag == True:
            print("Word is: ", guessed_word)
            print("Guessed in ", j + 1, " tries")
            await asyncio.sleep(3)
            await page.click(
                "#stats-dialog > div > div > div.Stats-module_ctaContainer__1Krdy > div.Footer-module_bottomSheet__i4haF.Footer-module_sbButtonFooter__IW3NP > div > button"
            )
            print(pyperclip.paste())
            await asyncio.sleep(5)
            await browser.close()
            return 0
        else:
            if guessed_word in word_list:
                word_list.remove(guessed_word)

    print("Couldn't guess the word. Try again!")

    await asyncio.sleep(1)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
