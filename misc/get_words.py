from ast import literal_eval
import requests


words = []
js_file_url = "https://www.powerlanguage.co.uk/wordle/main.e65ce0a5.js"
js_file = requests.get(js_file_url).text
start1 = js_file.find("var La=") + len("var La=")
end1 = js_file.find("],", start1) + 1
# print(js_file[start1: end1])
words.extend(literal_eval(js_file[start1: end1]))

start2 = js_file.find("Ta=", end1) + len("Ta=")
end2 = js_file.find("],", start2) + 1
# print(js_file[start2: end2][0])
words.extend(literal_eval(js_file[start2: end2]))

print(words)
