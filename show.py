# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import Tkinter as tk
import codecs
from meta_data import META

class Show:
    def __init__(self, parent, show_text):

        top2 = self.top2 = tk.Toplevel(parent)
        top2.title(u'Произведенные изменения')

        self.log = tk.Text(top2, width = 70, heigh = 10, font = ('Arial', 12))
        self.log.grid(row = 0, column = 0)

        self.log.insert('end', show_text)
        self.log.config(state = 'disabled')

        lab3 = tk.Label(top2, text = u'Сохранить произведенные изменения в файл:').grid(row=1, column=0)
        self.log_name = tk.Entry(top2, width = 18, bd = 3)
        self.log_name.grid(row = 2, column = 0)
        save_result = tk.Button(top2, text=u'Сохранить', command = self.log_file).grid(row=3, column=0)

        self.log_name.delete(0, 'end')
        self.log_name.insert(0, 'changes')

    def log_file(self):
        in_text = self.log.get('1.0', 'end')

        log = self.log_name.get()
        if log != '':
            log_n = META['default_directory'] + log + '.txt'

        else:
            log_n = META['default_directory'] + 'changes.txt'

        with codecs.open(log_n, 'w', 'utf-8') as ouf:
            ouf.write(in_text)
        self.top2.destroy()
