# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import Tkinter as tk
from meta_data import META

class OutputSettings:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        top = self.top
        top.title(u'Настройки вывода результатов')
        self.text_settings = tk.StringVar()
        self.xml_settings = tk.StringVar()
        lab = tk.Label(top, text = u'Формат .txt (из файла и для ввода текста вручную)').grid(row=0, column=0)
        self.br_text00 = tk.Text(top, width = 15, heigh = 1, font = ('Arial', 12))
        self.br_text00.insert('end', META['old_new_delimiters']['tei'][0])
        self.br_text00.config(state = 'disabled')
        self.br_text00.grid(row = 1, column = 1)
        lab_new_text0 = tk.Label(top, text = u'пример').grid(row=1, column=2)
        self.br_text01 = tk.Text(top, width = 10, heigh = 1, font = ('Arial', 12))
        self.br_text01.insert('end', META['old_new_delimiters']['tei'][1])
        self.br_text01.config(state = 'disabled')
        self.br_text01.grid(row = 1, column = 3)
        lab_new_old0 = tk.Label(top, text = u'примеръ').grid(row=1, column=4)
        self.br_text02 = tk.Text(top, width = 15, heigh = 1, font = ('Arial', 12))
        self.br_text02.insert('end', META['old_new_delimiters']['tei'][2])
        self.br_text02.config(state = 'disabled')
        self.br_text02.grid(row = 1, column = 5)
        self.rb_text0 = tk.Radiobutton(top, text=u'TEI', value='tei', variable=self.text_settings)
        self.rb_text0.grid(row=1, column=6)

        self.br_text10 = tk.Text(top, width = 3, heigh = 1, font = ('Arial', 12))
        self.br_text10.insert('end', META['old_new_delimiters']['simple'][0])
        self.br_text10.config(state = 'disabled')
        self.br_text10.grid(row = 2, column = 1)
        lab_new_text1 = tk.Label(top, text = u'пример').grid(row=2, column=2)
        self.br_text11 = tk.Text(top, width = 3, heigh = 1, font = ('Arial', 12))
        self.br_text11.insert('end', META['old_new_delimiters']['simple'][1])
        self.br_text11.config(state = 'disabled')
        self.br_text11.grid(row = 2, column = 3)
        lab_new_old1 = tk.Label(top, text = u'примеръ').grid(row=2, column=4)
        self.br_text12 = tk.Text(top, width = 3, heigh = 1, font = ('Arial', 12))
        self.br_text12.insert('end', META['old_new_delimiters']['simple'][2])
        self.br_text12.config(state = 'disabled')
        self.br_text12.grid(row = 2, column = 5)
        self.rb_text1 = tk.Radiobutton(top, text=u'simple', value='simple', variable=self.text_settings)
        self.rb_text1.grid(row=2, column=6)

        self.br_text20 = tk.Text(top, width = 10, heigh = 1, font = ('Arial', 12))
        self.br_text20.insert('end', META['old_new_delimiters']['manual_text'][0])
        self.br_text20.grid(row = 3, column = 1)
        lab_new_text2 = tk.Label(top, text = u'пример').grid(row=3, column=2)
        self.br_text21 = tk.Text(top, width = 10, heigh = 1, font = ('Arial', 12))
        self.br_text21.insert('end', META['old_new_delimiters']['manual_text'][1])
        self.br_text21.grid(row = 3, column = 3)
        lab_new_old2 = tk.Label(top, text = u'примеръ').grid(row=3, column=4)
        self.br_text22 = tk.Text(top, width = 10, heigh = 1, font = ('Arial', 12))
        self.br_text22.insert('end', META['old_new_delimiters']['manual_text'][2])
        self.br_text22.grid(row = 3, column = 5)
        self.rb_text2 = tk.Radiobutton(top, text=u'manual', value='manual_text', variable=self.text_settings)
        self.rb_text2.grid(row=3, column=6)

        lab1 = tk.Label(top, text = u'Формат html/xml').grid(row=5, column=0)
        self.br_xml00 = tk.Text(top, width = 15, heigh = 1, font = ('Arial', 12))
        self.br_xml00.insert('end', META['old_new_delimiters']['tei'][0])
        self.br_xml00.config(state = 'disabled')
        self.br_xml00.grid(row = 6, column = 1)
        lab_new_text3 = tk.Label(top, text = u'пример').grid(row=6, column=2)
        self.br_xml01 = tk.Text(top, width = 10, heigh = 1, font = ('Arial', 12))
        self.br_xml01.insert('end', META['old_new_delimiters']['tei'][1])
        self.br_xml01.config(state = 'disabled')
        self.br_xml01.grid(row = 6, column = 3)
        lab_new_old3 = tk.Label(top, text = u'примеръ').grid(row=6, column=4)
        self.br_xml02 = tk.Text(top, width = 15, heigh = 1, font = ('Arial', 12))
        self.br_xml02.insert('end', META['old_new_delimiters']['tei'][2])
        self.br_xml02.config(state = 'disabled')
        self.br_xml02.grid(row = 6, column = 5)
        self.rb_xml0 = tk.Radiobutton(top, text=u'TEI', value='tei', variable=self.xml_settings)
        self.rb_xml0.grid(row=6, column=6)

        self.br_xml10 = tk.Text(top, width = 3, heigh = 1, font = ('Arial', 12))
        self.br_xml10.insert('end', META['old_new_delimiters']['simple'][0])
        self.br_xml10.config(state = 'disabled')
        self.br_xml10.grid(row = 7, column = 1)
        lab_new_text4 = tk.Label(top, text = u'пример').grid(row=7, column=2)
        self.br_xml11 = tk.Text(top, width = 3, heigh = 1, font = ('Arial', 12))
        self.br_xml11.insert('end', META['old_new_delimiters']['simple'][1])
        self.br_xml11.config(state = 'disabled')
        self.br_xml11.grid(row = 7, column = 3)
        lab_new_old4 = tk.Label(top, text = u'примеръ').grid(row=7, column=4)
        self.br_xml12 = tk.Text(top, width = 3, heigh = 1, font = ('Arial', 12))
        self.br_xml12.insert('end', META['old_new_delimiters']['simple'][2])
        self.br_xml12.config(state = 'disabled')
        self.br_xml12.grid(row = 7, column = 5)
        self.rb_xml1 = tk.Radiobutton(top, text=u'simple', value='simple', variable=self.xml_settings)
        self.rb_xml1.grid(row=7, column=6)

        self.br_xml20 = tk.Text(top, width = 10, heigh = 1, font = ('Arial', 12))
        self.br_xml20.insert('end', META['old_new_delimiters']['manual_xml'][0])
        self.br_xml20.grid(row = 8, column = 1)
        lab_new_text5 = tk.Label(top, text = u'пример').grid(row=8, column=2)
        self.br_xml21 = tk.Text(top, width = 10, heigh = 1, font = ('Arial', 12))
        self.br_xml21.insert('end', META['old_new_delimiters']['manual_xml'][1])
        self.br_xml21.grid(row = 8, column = 3)
        lab_new_old5 = tk.Label(top, text = u'примеръ').grid(row=8, column=4)
        self.br_xml22 = tk.Text(top, width = 10, heigh = 1, font = ('Arial', 12))
        self.br_xml22.insert('end', META['old_new_delimiters']['manual_xml'][2])
        self.br_xml22.grid(row = 8, column = 5)
        self.rb_xml2 = tk.Radiobutton(top, text=u'manual', value='manual_xml', variable=self.xml_settings)
        self.rb_xml2.grid(row=8, column=6)

        save_settings = tk.Button(top, text=u'Сохранить настройки', command=self.save_settings).grid(row=9, column=6)

        if META['current_delimiters_text'] == 'tei':
            self.rb_text0.select()
        elif META['current_delimiters_text'] == 'simple':
            self.rb_text1.select()
        elif META['current_delimiters_text'] == 'manual_text':
            self.rb_text2.select()
        if META['current_delimiters_xml'] == 'tei':
            self.rb_xml0.select()
        elif META['current_delimiters_xml'] == 'simple':
            self.rb_xml1.select()
        elif META['current_delimiters_xml'] == 'manual_xml':
            self.rb_xml2.select()

    def save_settings(self):
        META['current_delimiters_text'] = self.text_settings.get()
        META['current_delimiters_xml'] = self.xml_settings.get()
        if META['current_delimiters_text'] == 'manual_text':
            self.init_manual_delimiters('manual_text', self.br_text20, self.br_text21, self.br_text22)
        if META['current_delimiters_xml'] == 'manual_xml':
            self.init_manual_delimiters('manual_xml', self.br_xml20, self.br_xml21, self.br_xml22)
        # print 'META', META['current_delimiters_text'], META['current_delimiters_xml']
        # print u','.join(META['old_new_delimiters']['manual_text'])
        # print u','.join(META['old_new_delimiters']['manual_xml'])

    @classmethod
    def init_manual_delimiters(cls, key, d0, d1, d2):
        value0 = d0.get('1.0', 'end')
        value0 = value0.replace(u'\r', u'').replace(u'\n', u'')
        value1 = d1.get('1.0', 'end')
        value1 = value1.replace(u'\r', u'').replace(u'\n', u'')
        value2 = d2.get('1.0', 'end')
        value2 = value2.replace(u'\r', u'').replace(u'\n', u'')
        META['old_new_delimiters'][key] = [value0, value1, value2]


class OpenSettings(object):
    @classmethod
    def edit_settings(cls, root):
        d = OutputSettings(root)
        root.wait_window(d.top)