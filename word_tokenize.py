# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import re

SYMBOLS = {
    'symbols': u'~!@#$%^&*()-+={}[]\|/?.,><;:"»«',
    'specials': [u'...'],
    'inside': u'~!#$%^&*()+={}[]\|/?.,><;:"»«',
    'fixed_forms': [re.compile(u'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')]
}

class WordTokenizer(object):
    @classmethod
    def tokenize(cls, text):
        arr = text.strip().split(u' ')
        tokenized = []
        for el in arr:
            if cls.is_simple_word(el):
                tokenized.append(el)
                continue
            new = cls.split_word(el)
            tokenized += new
        return tokenized


    @classmethod
    def split_word(cls, w):
        new = []
        w, new = cls.remove_specials_begin(w, new)
        end_spec = []
        w, end_spec = cls.remove_specials_end(w, end_spec)
        end_spec = end_spec[::-1]
        w, new = cls.remove_symbols_begin(w, new)
        end_symb = []
        w, end_symb = cls.remove_symbols_end(w, end_symb)
        end_symb = end_symb[::-1]
        splitted_w = cls.split_word_inside(w)
        new += splitted_w
        new += end_symb
        new += end_spec
        return new

    @classmethod
    def split_word_inside(cls, w):
        new = []
        for pattern in SYMBOLS['fixed_forms']:
            if pattern.search(w):
                return [w]
        for litera in w:
            if litera in SYMBOLS['inside']:
                arr = w.split(litera)
                if arr[0] != u'':
                    new.append(arr[0])
                new.append(litera)
                w = litera.join(arr[1:])
        if w:
            new.append(w)
        return new

    @classmethod
    def remove_symbols_begin(cls, w, new):
        for litera in SYMBOLS['symbols']:
            if len(w) >= 1:
                if litera == w[0]:
                    new.append(litera)
                    w = w[1:]
                    w, new = cls.remove_symbols_begin(w, new)
        return w, new

    @classmethod
    def remove_symbols_end(cls, w, new):
        for litera in SYMBOLS['symbols']:
            if len(w) >= 1:
                if litera == w[-1]:
                    new.append(litera)
                    w = w[:-1]
                    w, new = cls.remove_symbols_end(w, new)
        return w, new

    @classmethod
    def remove_specials_begin(cls, w, new):
        for s in SYMBOLS['specials']:
            if len(w) > len(s):
                if w[:len(s)] == s:
                    new.append(s)
                    w = w[len(s):]
                    w, new = cls.remove_specials_begin(w, new)
        return w, new

    @classmethod
    def remove_specials_end(cls, w, new):
        for s in SYMBOLS['specials']:
            if len(w) > len(s):
                if w[(len(s))*-1:] == s:
                    new.append(s)
                    w = w[:-1*(len(s))]
                    w, new = cls.remove_specials_end(w, new)
        return w, new

    @classmethod
    def is_simple_word(cls, w):
        for litera in SYMBOLS['symbols']:
            if litera in w:
                return 0
        return 1

# a = WordTokenizer()
# b = a.tokenize(u'...тест... токенизатора.')
# b = a.split_word_inside(u'email@mail.com')
# b = a.tokenize(u'обычно[мъ] своемъ мѣстѣ, подлѣ барометра, разставивъ ноги на приличное раз[стояніе], заложивъ руки назадъ и приводя за спиною пальцы въ движеніе тѣмъ быстрѣе, чѣмъ болѣе горячился [13] папа, спереди не выказывалъ ни малѣйшаго знака безпокойства, но, напротивъ, выраженіемъ лица выказывалъ совершенное сознаніе своей правоты и вмѣстѣ съ тѣмъ подвластности.')
# b = a.tokenize(u'«скоб[к»и]»')
# print u'\n'.join(b)
