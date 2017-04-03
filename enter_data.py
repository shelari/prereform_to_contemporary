# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import Tkinter as tk
import codecs
from process import Processor
from show import Show
from meta_data import META

class EnterText:
    def __init__(self, parent):

        self.top = tk.Toplevel(parent)
        top = self.top
        top.title(u'Ввод текста вручную')
        lab = tk.Label(top, text = u'Пожалуйста, введите текст для транслитерирования:').grid(row=0, column=0)
        self.entered = tk.Text(top, width = 50, heigh = 5, font = ('Arial', 12))
        self.entered.grid(row = 1, column = 0)
        do = tk.Button(top, text=u'Транслитерировать', command=self.ok).grid(row=2, column=0)
        lab2 = tk.Label(top, text = u'Транслитерированный текст:').grid(row=3, column=0)

        self.result = tk.Text(top, width = 50, heigh = 5, font = ('Arial', 12))
        self.result.grid(row = 4, column = 0)
        self.result.config(state = 'disabled')

        lab4 = tk.Label(top, text = u'Сохранить введенный текст в файл:').grid(row=5, column=0)
        self.in_text = tk.Entry(top, width = 18, bd = 3)
        self.in_text.grid(row = 6, column = 0)
        save_text = tk.Button(top, text=u'Сохранить текст', command = self.txt).grid(row=7, column=0)

        lab3 = tk.Label(top, text = u'Сохранить транслитерированный текст в файл:').grid(row=8, column=0)
        self.out = tk.Entry(top, width = 18, bd = 3)
        self.out.grid(row = 9, column = 0)
        save_result = tk.Button(top, text=u'Сохранить результат', command = self.res).grid(row=10, column=0)
        in_text = self.entered.get('1.0', 'end')

        self.show_log = tk.Button(top, text=u'Показать произведенные замены', command = self.log)
        self.show_log.grid(row = 11, column = 0)


        self.out.insert(0, 'result')
        self.in_text.insert(0, 'text')

    def ok(self):
        in_text = self.entered.get('1.0', 'end')

        new_text, changes = Processor.process_text(in_text, 1, META['old_new_delimiters'][META['current_delimiters_text']])

        self.result.config(state = 'normal')
        self.result.delete("1.0", "end")
        self.result.insert("end", new_text)
        self.result.config(state = 'disabled')

    def res(self):
        in_text = self.entered.get('1.0', 'end')
        new_text, changes = Processor.process_text(in_text, 1, META['old_new_delimiters'][META['current_delimiters_text']])

        res = self.out.get()
        if res != '':
            res_name = META['default_directory'] + res + '.txt'

        else:
            res_name = META['default_directory'] + 'result.txt'

        with codecs.open(res_name, 'w', 'utf-8') as ouf:
            ouf.write(new_text)

    def txt(self):
        in_text = self.entered.get('1.0', 'end')
        txt = self.in_text.get()
        if txt != '':
            txt_name = META['default_directory'] + txt + '.txt'

        else:
            txt_name = META['default_directory'] + 'text.txt'

        with codecs.open(txt_name, 'w', 'utf-8') as ouf2:
            ouf2.write(in_text)

    def log(self):
        in_text = self.entered.get('1.0', 'end')
        new_text, changes = Processor.process_text(in_text, 1, META['old_new_delimiters'][META['current_delimiters_text']])

        s = Show(self.top, changes)