import re
from collections import defaultdict
from Stemmer import Stemmer

from . import (
    normalize_locale, get_stop_words, known_languages, DummyStemmer)


class StemSet(set):
    def __init__(self):
        super(StemSet, self).__init__()
        self.counter = 0.0

    def add(self, word, weight=1.0):
        super(StemSet, self).add(word)
        self.counter += weight

    def shortest(self):
        all_words = list(self)
        all_words.sort(key=len)
        return all_words[0]

    def __repr__(self):
        return super(StemSet, self).__repr__()[:-1] + ", %f)" % (
            self.counter)


class WordCounter(defaultdict):
    non_words = re.compile('\W+', re.U)

    def __init__(self, langs, min_len=3):
        super(WordCounter, self).__init__(StemSet)
        self.min_len = min_len
        self.langs = []
        # We will base stemmer on first known language.
        stemmer = None
        stopwords = set()
        for lang in langs:
            lang = normalize_locale(lang)
            if lang in known_languages:
                stopwords.update(get_stop_words(lang))
            self.langs.append(lang)
            if lang in known_languages and not stemmer:
                stemmer = Stemmer(lang)
        if stemmer:
            self.stemmer = stemmer
        else:
            self.stemmer = DummyStemmer()
        self.stop_words = stopwords

    def add_text(self, text, weight=1.0):
        for word in self.non_words.split(text):
            self.add_word(word, weight)

    def add_word(self, word, weight=1.0):
        if word.lower() in self.stop_words:
            return
        if len(word) < self.min_len:
            return
        stemmed = self.stemmer.stemWord(word.lower())
        self[stemmed].add(word, weight)

    def best(self, num=10):
        all_words = self.values()
        all_words.sort(key=lambda x: x.counter, reverse=True)
        if len(all_words) > num:
            all_words = all_words[:num]
        return [x.shortest() for x in all_words]
