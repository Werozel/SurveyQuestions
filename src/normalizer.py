from globals import sessionmaker
import re
import nltk


def split_str(s: str) -> list[str]:
    return re.split("[,.-;!?_: ]", s)


def has_alpha(s: str) -> bool:
    return any([x.isalpha() for x in s])


def tokenize_word(word: str) -> str:
    return


def normalize_str(s: str, morph: ) -> str:
    splitted_s: list[str] = [x.lower() for x in split_str(s) if x and has_alpha(x)]
    return ' '.join(splitted_s)


if __name__ == "__main__":
    nltk.download("punkt")
    nltk.download("stopwords")


    print(normalize_str("Сделал/сделаю это - то, да! Се."))
