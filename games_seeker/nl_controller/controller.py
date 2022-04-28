import subprocess
import yake
import nltk
import click


def create_extractor(lang='en', max_ngram=1, deduplication_threshold=0.9, num_df_keywords=10):
    return yake.KeywordExtractor(
        lan=lang,
        n=max_ngram,
        dedupLim=deduplication_threshold,
        top=num_df_keywords,
        features=None
    )


def get_keywords(text, extractor=create_extractor()):
    keywords = extractor.extract_keywords(text)
    words = set(map(lambda x: x[0], keywords))
    return keywords, words


class NaturalLanguageController:
    def __init__(self):
        nltk.download("book")
        nltk.download("omw")
        nltk.download("wordnet")
        nltk.download('omw-1.4')
        nltk.download('averaged_perceptron_tagger')
        from nltk.corpus import wordnet as wn
        click.clear()
        self.functions = {
            "builder": lambda: subprocess.run(["python", "main.py", "builder"]),
            "can_run_game": lambda: subprocess.run(["python", "main.py", "can_run_game"]),
            "classifier": lambda: subprocess.run(["python", "main.py", "classifier"]),
            "improver": lambda: subprocess.run(["python", "main.py", "improver"]),
        }
        ss = {
            "builder": [
                wn.synsets("Armar", lang="spa"),
                wn.synsets("Comprar", lang="spa"),
            ],
            "run": [
                wn.synsets("ejecutar", lang="spa"),
                wn.synsets("Jugar", lang="spa"),
            ],
            "improver": [
                wn.synsets("Mejorar", lang="spa"),
                wn.synsets("Arreglar", lang="spa"),
                wn.synsets("Ajustar", lang="spa"),
                wn.synsets("Actualizar", lang="spa"),
            ],
            "classifier": [
                wn.synsets("Clasificar", lang="spa"),
                wn.synsets("Categorizar", lang="spa"),
                wn.synsets("Evaluar", lang="spa"),
            ],
        }
        self.associated_keywords = {
            "builder": set(
                [
                    name for _ss in ss["builder"] for syn in _ss
                    for name in syn.lemma_names() if "_" not in name
                ]
            ) | {"build"},
            "can_run_game": set(
                [
                    name for _ss in ss["run"] for syn in _ss
                    for name in syn.lemma_names() if "_" not in name
                ]
            ) | {"run"},
            "improver": set(
                [
                    name for _ss in ss["improver"] for syn in _ss
                    for name in syn.lemma_names() if "_" not in name
                ]
            ) | {"improve"},
            "classifier": set(
                [
                    name for _ss in ss["classifier"] for syn in _ss
                    for name in syn.lemma_names() if "_" not in name
                ]
            ) | {"classify"}
        }

    def run(self):
        tries = 3
        while tries != 0:
            text = input("What do you do? ").lower()
            _, words = get_keywords(text)
            for function, associated in self.associated_keywords.items():
                diff = words & associated
                if diff:
                    return self.functions[function], function
            print("Can you be more clear?")
            tries -= 1
        return lambda: print("Sorry, I couldn't process your request"), None
