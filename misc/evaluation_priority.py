current_char_status = {letter: evaluation}
# Updating the evaluation in case of repetition
if current_char_status[letter] in char_status.keys():
    if (
        evaluation_priority[current_char_status[letter]]
        > evaluation_priority[char_status[letter]["evaluation"]]
    ):
        char_status[letter]["evaluation"] = current_char_status[letter]
else:
    char_status[letter] = {
        "position": i,
        "evaluation": current_char_status[letter],
    }
