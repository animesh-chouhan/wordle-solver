from ast import literal_eval
import requests

JS_URL = "https://www.nytimes.com/games-assets/v2/wordle.0184c33d9a3561750c6f.js"

words = []
js_file_url = JS_URL
js_file = requests.get(js_file_url).text
start1 = js_file.find('"wordle/moogle/SET_INITIAL_STATE"),ba=') + len(
    '"wordle/moogle/SET_INITIAL_STATE"),ba='
)
end1 = js_file.find("],", start1) + 1
# print(js_file[start1: end1])
words.extend(literal_eval(js_file[start1:end1]))


print(words)
