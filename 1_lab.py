import pymorphy3
from pathlib import Path

from nltk.tokenize import sent_tokenize, word_tokenize


morph = pymorphy3.MorphAnalyzer(lang="ru")


def same_gender(first, second):
    if first.tag.gender is None or second.tag.gender is None:
        return True

    return first.tag.gender == second.tag.gender


def is_matching_pair(first_word, second_word):
    first = morph.parse(first_word)[0]
    second = morph.parse(second_word)[0]

    allowed_pos = {"NOUN", "ADJF"}

    # Оба слова должны быть существительными или прилагательными
    if first.tag.POS not in allowed_pos:
        return False

    if second.tag.POS not in allowed_pos:
        return False

    # Проверяем число
    if first.tag.number != second.tag.number:
        return False

    # Проверяем падеж
    if first.tag.case != second.tag.case:
        return False

    # Проверяем род
    if not same_gender(first, second):
        return False

    return True


file_path = Path("input.txt")
text = file_path.read_text(encoding="utf-8")


sentences = sent_tokenize(text, language="russian")


for sentence in sentences:
    tokens = word_tokenize(sentence, language="russian")

    for i in range(len(tokens) - 1):
        first_word = tokens[i]
        second_word = tokens[i + 1]

        if is_matching_pair(first_word, second_word):
            first = morph.parse(first_word)[0]
            second = morph.parse(second_word)[0]

            print(first.normal_form, second.normal_form)