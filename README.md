# Wordle Solver

Program to solve the wordle puzzle

## About

"Wordle," [Wikipedia](https://en.wikipedia.org/wiki/Wordle), The Free Encyclopedia:

Wordle is a web-based word game created and developed by Welsh software engineer Josh Wardle. Players have six attempts to guess a five-letter word, with feedback given for each guess in the form of colored tiles indicating when letters match or occupy the correct position.

## Running

### Cloning the repository

```sh
git clone https://github.com/animesh-chouhan/wordle-solver.git
cd wordle-solver
```

### Install requirements

```sh
pip install -r requirements.txt
```

### Run

```python
python3 main.py 2> log.txt 
```

## Example

![preview](https://raw.githubusercontent.com/animesh-chouhan/wordle-solver/main/assets/preview.gif)

## Output

Word is:  phony
Guessed in  4  tries
Wordle 862 4/6

⬜🟨⬜⬜🟩  
⬜🟨🟩⬜🟩  
🟩⬜🟩🟩🟩  
🟩🟩🟩🟩🟩

## Built With

* [pyppeteer](https://github.com/pyppeteer/pyppeteer) - Python port of puppeteer JavaScript (headless) chrome/chromium browser automation library
