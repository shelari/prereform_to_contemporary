# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import Tkinter as tk
import os
from tkMessageBox import askyesno
from tkFileDialog import askdirectory
from load_data import LoadData
from dialog import Dialog
from output_settings import OpenSettings
from meta_data import META

if __name__ == '__main__':

    root = tk.Tk()
    text = tk.Text(root, font = ('Arial', 12), cursor = 'arrow')
    text.insert('end', u'Вас приветствует транслитератор дореформенной орфографии в современную')
    text.config(state = 'disabled')
    text.pack(fill="both", expand="yes")
    root.title('Transliterator')

    menubar = tk.Menu(root, tearoff=0)
    root.config(menu=menubar)

    my_menu = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label=u"Меню", menu=my_menu)

    my_menu.add_command(label = u"Загрузить и транслитерировать текст из файла .txt", command = lambda: LoadData.load_txt(text, root))
    my_menu.add_command(label = u"Загрузить и транслитерировать текст из файла xml (.html, .xhtml)", command = lambda: LoadData.load_html(text, root))
    my_menu.add_command(label = u"Загрузить и транслитерировать тексты xml (.html, .xhtml) из папки", command = lambda: LoadData.load_several_html(text, root))
    my_menu.add_command(label = u"Ввести текст вручную", command = lambda: LoadData.open_text(text, root))
    my_menu.add_command(label = u"Настройки", command = lambda: OpenSettings.edit_settings(root))
    my_menu.add_command(label = u"Справка", command = lambda: Dialog.help_text(root))
    my_menu.add_command(label = u"Выход", command = lambda: Dialog.close_win(root))

    if askyesno(u"Папка для сохраниния результатов", u"Выберите папку для сохранения результатов"):
        def_dir = askdirectory()
        META['default_directory'] = def_dir + u'/'
    else:
        META['default_directory'] = os.getcwd() + u'/results/'
        try:
            os.mkdir(META['default_directory'])
        except:
            pass

    root.mainloop()