# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import Tkinter as tk
from tkMessageBox import askyesno
from meta_data import META
from enter_data import EnterText

class Dialog:
    def __init__(self, parent, text):
        top = self.top = tk.Toplevel(parent)
        top.title(u'Имена файлов')
        lab = tk.Label(top, text = u"Пожалуйста, введите названия выходных файлов:").grid(row=0, column=0)
        out_lab = tk.Label(top, text = u"Результат").grid(row=1, column=0)
        log_lab = tk.Label(top, text = u"Файл изменений").grid(row=2, column=0)
        self.out = tk.Entry(top, width = 18, bd = 3)
        self.out.grid(row = 1, column = 1)
        self.log = tk.Entry(top, width = 18, bd = 3)
        self.log.grid(row = 2, column = 1)

        self.out.insert(0, 'result')
        self.log.insert(0, 'changes')

        sc_button = tk.Button(top, text="OK", command=lambda: self.ok(text, parent)).grid(row=3, column=0)

    def ok(self, text, root):
        META['result_name'] = self.out.get()
        META['log_name'] = self.log.get()

        if META['result_name'] == '':
            META['result_name'] = 'result'
        if META['log_name'] == '':
            META['log_name'] = 'changes'
        text.config(state = 'normal')
        res_name = u"Выходной файл: " + META['result_name'] + '.txt\n'
        log_name = u"Файл лога: " + META['log_name'] + '.txt\n'

        text.insert("end", res_name)
        text.insert("end", log_name)
        text.insert("end", u"В обработке...\n")
        text.config(state = 'disabled')
        text.configure(cursor = 'watch')

        META['flag'] = 1
        root.update()
        self.top.destroy()

    @classmethod
    def dialog(cls, root, text):
        d = Dialog(root, text)
        root.wait_window(d.top)

    @classmethod
    def dialog_translit(cls, root):
        root.text.config(state = 'normal')
        root.text.delete("1.0", "end")
        root.text.insert('end', u'Текст транслитерирован')
        root.text.config(state = 'disabled')

    @classmethod
    def help_text(cls, root):
        help_text = """
        Справка:
        Программа работает с файлами .txt в кодировке UTF-8,
        файлами xml и html.

        Возможности программы:
        1. Транслитерировать текст, введенный вручную.
        Для получения транслитерированного текста требуется нажать кнопку
        'Транслитерировать'. Вы можете сохранить введенный оригинальный текст,
        нажав 'Сохранить текст', сохранить транслитерированный текст, нажав
        'Сохранить результат'. Кроме того имеется возможность просмотреть
        произведенные замены по нажатию кнопки 'Показать произведенные замены'
        и сохранить их в файл.
        2. Tранслитерировать загруженный файл в формате .txt.
        Файл должен иметь кодировку utf-8.
        3. Транслитерировать один файл в формате xml или html.
        4. Транслитеровать несколько файлов в формате xml или html.
        Для того, чтобы программа работала с файлами в формате xml или html
        нужно, чтобы эти файлы имели валидную структуру. Если структура содержит
        ошибки, программа об этом сообщит. Получить указание на конкретные ошибки
        в структуре файла можно с помощью валидатора (например, http://www.xmlvalidation.com)

        О сохранении результатов:
        В начале работы программа просит указать папку, куда будут сохраняться результаты
        работы. Если папка не будет указана, результаты будут сохраняться в папку results
        в корневой директории программы.
        Результаты обработки нескольких файлов xml/html (пункт 4) будут сохраняться в ту
        же папку, где лежат оригинальные файлы. Обработанные файлы будут сохранены в
        подпапку transliterated, файлы с историей замен в папку log, информация о файлах,
        которые не были обработаны, в подпапку passed.
                    """
        h = HelpWindow(root, help_text)
        root.wait_window(h.top)

    @classmethod
    def close_win(cls, root):
        """
        Closing window
        """
        if askyesno(u"Выход", u"Хотите закрыть программу?"):
              root.destroy()

    @classmethod
    def open_text(cls, root):
        META['parent'] = root
        d = EnterText(root)
        root.wait_window(d.top)

class HelpWindow:
    def __init__(self, parent, help_text):
        top = self.top = tk.Toplevel(parent)
        top.title('Help')
        help_lab = tk.Label(top, text=help_text, justify='left').grid(row=0, column=0)
        sc_button = tk.Button(top, text="OK", command=self.ok).grid(row=2, column=0)

    def ok(self):
        self.top.destroy()








