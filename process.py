# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
from copy import deepcopy
from preprocess import Preprocessor
from tokenizer import Tokenizer
from transliterator import Transliterator
from meta_data import META

class Processor(object):
    @classmethod
    def process_text(cls, text, show, delimiters, print_log=True):
        text = Preprocessor.preprocess_text(text)
        if print_log:
            print 'TEXT', text
        tokens = Tokenizer.tokenize(text)
        if print_log:
            print 'TOKENS', tokens
        # print 'tokens'
        for i in tokens.keys():
            if tokens[i].type == 'word':
                word = Transliterator.transliterate(tokens[i].word, print_log)
                if print_log:
                    print 'WORD TR', word
                if word != tokens[i].word:
                    tokens[i].old_word = deepcopy(tokens[i].word)
                    tokens[i].word = word
        text, changes = cls.join_tokens(tokens, show, delimiters)
        return text, changes

    @classmethod
    def join_tokens(cls, tokens, show, delimiters):
        text = []
        changes = []
        for i in range(len(tokens.keys())):
            if tokens[i].old_word:
                if show:
                    new = delimiters[0] + tokens[i].word + delimiters[1] + \
                          tokens[i].old_word + delimiters[2]
                else:
                    new = tokens[i].word
                text.append(new)
                s = tokens[i].old_word + u' --> ' + tokens[i].word
                changes.append(s)
            else:
                text.append(tokens[i].word)
        if changes == []:
            out = u''
        else:
            out = u'\n'.join(changes)
        return u''.join(text), out


# text = u'Пройдя комнату, такъ [называемую], офиціанскую, мы взошли въ кабинетъ Папа. Онъ стоялъ подлѣ письменнаго стола и, показывая на бумаги, запечатанные конверты, кучки денегъ, горячился и что-то толковалъ прикащику Никитѣ Петрову, который на обычно[мъ] своемъ мѣстѣ, подлѣ барометра, разставивъ ноги на приличное раз[стояніе], заложивъ руки назадъ и приводя за спиною пальцы въ движеніе тѣмъ быстрѣе, чѣмъ болѣе горячился [13] папа, спереди не выказывалъ ни малѣйшаго знака безпокойства, но, напротивъ, выраженіемъ лица выказывалъ совершенное сознаніе своей правоты и вмѣстѣ съ тѣмъ подвластности.'
# text = u'df 13 fsdf'
# text = u'офиціанскую'
# text = u' обычно[мъ] '
# text = u'который [на] обычно[мъ] [своемъ] мѣстѣ, подлѣ барометра, разставивъ'
# import codecs
# with codecs.open(u'/Users/el/Downloads/vol. 1/index.html', 'r', 'utf-8') as inf:
#     text = inf.read()
# a = Processor()
# b = a.process_text(text, 1, [u'<choice><reg>', u'</reg><orig>', u'</orig></choice>'])
# print b
