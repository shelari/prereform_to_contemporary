# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import codecs
from meta_data import META

class SaveText(object):
    @classmethod
    def save_translit_text(cls, text, new_text, changes):
            res_name = META['default_directory'] + META['result_name'] + '.txt'

            with codecs.open(res_name, 'w', 'utf-8') as ouf:
                ouf.write(new_text)

            log_name = META['default_directory'] + META['log_name'] + '.txt'

            with codecs.open(log_name, 'w', 'utf-8') as ouf2:
                ouf2.write(changes)

            text.config(state = 'normal')
            text.delete('4.0', 'end')
            text.insert('end', u'\nВыполнено\n')
            text.configure(cursor = 'arrow')
            text.config(state = 'disabled')

    @classmethod
    def save_passed(cls, arr, dir_name):
        fn = dir_name +'/passed/passed_files_and_folders.txt'
        print 'THIS IS IN PASSED', arr
        with codecs.open(fn, 'w', 'utf-8') as ou:
            print 'FILE IS OPENED'
            # ou.write(u'\n'.join(arr))
            for el in arr:
                print el
                ou.write(el.decode('utf-8'))
                ou.write(u'\n')
