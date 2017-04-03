#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 18.01.2017 12:50:03 MSK

import re
import sys

from process import Processor

def main(args):
    text = ' '.join(args[1:])
    new_txt = Processor.process_text(text, [u'@', u'{', u'}'], [u'', u'{', u'}'])
    new_txt = new_txt.replace(u'онѣ', u'они')
    new_txt = new_txt.replace(u'однѣ', u'одни')
    new_txt = new_txt.replace(u'Онѣ', u'Они')
    new_txt = new_txt.replace(u'Однѣ', u'Одни')
    new_txt = new_txt.replace(u'сiю', u'сию')
    print new_txt
    
    return 0

if __name__ == '__main__':
    main(sys.argv)
