#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 18.01.2017 12:50:03 MSK

import re
import sys

from process import Processor

def main(args):
    print_log = False
    text = ' '.join(args[1:])
    try:
        new_txt = Processor.process_text(text, [u'@', u'{', u'}'], [u'', u'{', u'}'], print_log)
    except:
        try:
            text = text.decode('utf-8')
            new_txt = Processor.process_text(text, [u'@', u'{', u'}'], [u'', u'{', u'}'], print_log)
        except:
            return 0
    new_txt = new_txt[0]
    print new_txt
    
    return 0

if __name__ == '__main__':
    main(sys.argv)
