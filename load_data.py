# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import codecs
import os
import sys
from lxml import etree
from tkMessageBox import askyesno
from tkFileDialog import askopenfilename, askdirectory, askopenfilenames
from dialog import Dialog
from process import Processor
from save_data import SaveText
from error_dialog import Error
from meta_data import META

class LoadData(object):
    @classmethod
    def load(cls, text, root, delimiters):
        """
    Loading file
        """
        text.config(state = 'normal')
        text.insert("end", u"В обработке...\n")
        text.config(state = 'disabled')

        # name = os.path.basename(meta.filename)
        name = os.path.basename(META['filename'])

        try:
            # with codecs.open(filename, 'r', 'utf-8-sig') as f_dict:
            with codecs.open(META['filename'], 'r', 'utf-8') as f:
                data = f.read() #считали файл
                # s_dict = r_dict.split() #поделили по пробелам
            text.config(state = 'normal')
            text.delete("1.0", "end")
            text.insert("end", u"Файл загружен\n")
            text.config(state = 'disabled')
            Dialog.dialog(root, text)

            if META['flag'] == 1: #???????
                new_text, changes = Processor.process_text(data, 1, delimiters)  #транслитерировали
                SaveText.save_translit_text(text, new_text, changes)
            else:
                text.config(state = 'normal')
                text.delete("1.0", "end")
                text.insert("end", u"Вы не ввели имена выходных файлов\n")
                text.config(state = 'disabled')
            META['flag'] = 0

        except IOError as e:
                err = u"Проблема с чтением файла " + os.path.basename(META['filename']) +\
                          u": I/O error({0}): {1}".format(e.errno, e.strerror) +\
                          u"\nВыберите другой файл."
                Error.dialogError(err, root)
        except ValueError:
                err = u"Проблема с чтением файла " + os.path.basename(META['filename']) +\
                          u": Неверный формат данных." +\
                          u"\nВыберите другой файл."
                Error.dialogError(err, root)
        except:
                err = u"Проблема с чтением файла " + os.path.basename(META['filename']) +\
                          u": Неизвестная ошибка: " + str(sys.exc_info()[0]) +\
                          u"\nВыберите другой файл."
                Error.dialogError(err, root)
                raise

    @classmethod
    def load_txt(cls, text, root):
        if askyesno(u"Открыть файл", u"Открыть новый файл?"):
            filename = askopenfilename()
            META['filename'] = filename
            # meta.filename = fn
            # if meta.filename == '':
            if filename == u'':
                text.config(state='normal')
                text.delete("1.0", "end")
                text.insert("end", u"Пожалуйста, выберите файл.\n")
                text.config(state='disabled')
            else:
                cls.load(text, root, META['current_delimiters_text'])

    @classmethod
    def clean_html(cls, line):
        line = line.replace(u'&nbsp;', u' ')
        line = line.replace(u'&quot;', u'"')
        #line = line.replace(u'&lt;', u'@leftanglebracket@')
        #line = line.replace(u'&gt;', u'@rightanglebracket@')
        line = line.replace(u'&ndash;', u'-')
        line = line.replace(u'&ndash;', u'-')
        return line

    @classmethod
    def get_temp(cls, ind):
        suffix = os.path.splitext(META['filename'])[1]
        temp_name = 'temp_' + ind + suffix
        print 'FILE', temp_name
        with codecs.open(temp_name, 'a', 'utf-8') as temp:
            print 'OPEN'
            with codecs.open(META['filename'], 'r', 'utf-8') as inf:
                print 'OPEN2', META['filename']
                for line in inf:
                    print 'LINE'
                    new_line = cls.clean_html(line)
                    print new_line
                    temp.write(new_line)
                print 'OK'
        return temp_name

    @classmethod
    def get_temp_web(cls, ind, f):
        input_text = f.read().decode('utf-8')
        suffix = os.path.splitext(META['filename'])[1]
        temp_name = 'temp_' + ind + suffix
        with codecs.open(temp_name, 'a', 'utf-8') as temp:
            new_text = cls.clean_html(input_text)
            temp.write(new_text)
        return temp_name

    @classmethod
    def get_temp_in_dir(cls, dir_name):
        suffix = os.path.splitext(META['filename'])[1]
        temp_name = 'temp' + suffix
        with codecs.open(temp_name, 'w', 'utf-8') as temp:
            in_name = dir_name + '/' + META['filename']
            with codecs.open(in_name, 'r', 'utf-8') as inf:
                for line in inf:
                    new_line = cls.clean_html(line)
                    temp.write(new_line)
        return temp_name

    @classmethod
    def load_html(cls, text, root):
        if askyesno(u"Открыть файл", u"Открыть новый файл?"):
            META['filename'] = askopenfilename()
            text.config(state = 'normal')
            text.delete("1.0", "end")
            text.insert("end", u"В обработке...\n")
            text.config(state = 'disabled')
            ##print meta.filename
            name = os.path.splitext(os.path.basename(META['filename']))[0]
            ##print meta.res
            if META['filename'] == '':
                text.config(state = 'normal')
                text.delete("1.0", "end")
                text.insert("end", u"Пожалуйста, выберите файл.\n")
                text.config(state = 'disabled')
            else:
                temp_filename = cls.get_temp(META['tmp_folder'])
                new_text, log_data = cls.iterate_root(temp_filename, root, 1)
                if log_data == -1:
                    text.config(state = 'normal')
                    text.delete('1.0', 'end')
                    text.insert('end', u'\nОшибка в структуре файла. Выберите другой файл.\n')
                    text.configure(cursor = 'arrow')
                    text.config(state = 'disabled')
                    return 1

                suffix = os.path.splitext(META['filename'])[1]

                META['result_name'] = name + '_transliterated' + suffix
                rn = META['default_directory'] + META['result_name']

                with codecs.open(rn, 'w') as ouf:
                    ouf.write(new_text)

                log_name = name + '_log.txt'
                ln = META['default_directory'] + log_name
                with codecs.open(ln, 'w', 'utf-8') as logf:
                    logf.write(u'\n'.join(log_data))

                text.config(state = 'normal')
                text.delete('1.0', 'end')
                text.insert('end', u'\nВыполнено\n')
                text.configure(cursor = 'arrow')
                text.config(state = 'disabled')

    @classmethod
    def iterate_root(cls, temp_filename, int_root, one_iteration):
        if one_iteration:
            try:
                tree = etree.parse(temp_filename)
            except:
                # tree = etree.parse(temp_filename)
                # print tree
                Error.dialogError(u'Ошибка в структуре xml/html', int_root)
                return -1, -1
                # tree = etree.parse(temp_filename)
        else:
            tree = etree.parse(temp_filename)
        print 1
        encoding = tree.docinfo.encoding
        root = tree.getroot()
        doctype = tree.docinfo.doctype
        standalone = tree.docinfo.standalone
        log_data = []
        markers = u'іѣъiѢЪIѣъѣіі'
        for child in root.iter():
            try:
                if u'i' in child.text or u'I' in child.text or u'і' in child.text or u'ѣ' in child.text or u'Ѣ' in child.text or u'ъ' in child.text or u'Ъ' in child.text or u'ѣ' in child.text or u'і' in child.text:
                    # old = child.text
                    new_text, changes = Processor.process_text(child.text, 1, META['old_new_delimiters'][META['current_delimiters_xml']])
                    child.text = new_text
                    if changes:
                        log_data.append(changes)
            except:
                pass
            try:
                #for marker in markers:
                if u'i' in child.tail or u'I' in child.tail or u'і' in child.tail or u'ѣ' in child.tail or u'Ѣ' in child.tail or u'ъ' in child.tail or u'Ъ' in child.tail or u'ѣ' in child.tail or u'і' in child.tail:
                    # old = child.tail
                    new_text, changes = Processor.process_text(child.tail, 1, META['old_new_delimiters'][META['current_delimiters_xml']])
                    child.tail = new_text
                    if changes:
                        log_data.append(changes)
            except:
                pass

        new_text = etree.tostring(root, xml_declaration=True, encoding=encoding, standalone=standalone, doctype = doctype)

        new_text = new_text.replace('&lt;choice&gt;', '<choice>')
        new_text = new_text.replace('&lt;reg&gt;', '<reg>')
        new_text = new_text.replace('&lt;/choice&gt;', '</choice>')
        new_text = new_text.replace('&lt;/reg&gt;', '</reg>')
        new_text = new_text.replace('&lt;orig&gt;', '<orig>')
        new_text = new_text.replace('&lt;/orig&gt;', '</orig>')
        print 2
        return new_text, log_data

    @classmethod
    def iterate_root_web(cls, temp_filename):
        # try:
        tree = etree.parse(temp_filename)
        # except:
        #     return 'error', 'error'
        encoding = tree.docinfo.encoding
        root = tree.getroot()
        doctype = tree.docinfo.doctype
        standalone = tree.docinfo.standalone
        log_data = []
        markers = u'іѣъiѢЪIѣъѣіі'
        for child in root.iter():
            try:
                if u'i' in child.text or u'I' in child.text or u'і' in child.text or u'ѣ' in child.text or u'Ѣ' in child.text or u'ъ' in child.text or u'Ъ' in child.text or u'ѣ' in child.text or u'і' in child.text:
                    # old = child.text
                    new_text, changes = Processor.process_text(child.text, 1, META['old_new_delimiters'][META['current_delimiters_xml']])
                    child.text = new_text
                    if changes:
                        log_data.append(changes)
            except:
                pass
            try:
                #for marker in markers:
                if u'i' in child.tail or u'I' in child.tail or u'і' in child.tail or u'ѣ' in child.tail or u'Ѣ' in child.tail or u'ъ' in child.tail or u'Ъ' in child.tail or u'ѣ' in child.tail or u'і' in child.tail:
                    # old = child.tail
                    new_text, changes = Processor.process_text(child.tail, 1, META['old_new_delimiters'][META['current_delimiters_xml']])
                    child.tail = new_text
                    if changes:
                        log_data.append(changes)
            except:
                pass

        new_text = etree.tostring(root, xml_declaration=True, encoding=encoding, standalone=standalone, doctype = doctype)

        new_text = new_text.replace('&lt;choice&gt;', '<choice>')
        new_text = new_text.replace('&lt;reg&gt;', '<reg>')
        new_text = new_text.replace('&lt;/choice&gt;', '</choice>')
        new_text = new_text.replace('&lt;/reg&gt;', '</reg>')
        new_text = new_text.replace('&lt;orig&gt;', '<orig>')
        new_text = new_text.replace('&lt;/orig&gt;', '</orig>')

        return new_text, u'\n'.join(log_data)

    @classmethod
    def check_transliterated(cls, current_filename, dir_name):
        fn = dir_name + '/' + current_filename
        try:
            with codecs.open(fn, 'r', 'utf-8') as inf:
                data = inf.read()
        except:
            return 0
        if '<reg>' not in data and '<orig>' not in data:
            return 1
        else:
            return 0

    @classmethod
    def load_several_html(cls, text, root):
        if askyesno(u"Загрузить папку", u"Загрузить новую папку?"):
            dir_name = askdirectory()
            print dir_name
            filenames_set = os.listdir(dir_name)
            #filenames_set = askopenfilenames()
            print filenames_set
            text.config(state='normal')
            text.delete("1.0", "end")
            text.insert("end", u"В обработке...\n")
            text.config(state='disabled')
            if filenames_set == []:
                text.config(state='normal')
                text.delete("1.0", "end")
                text.insert("end", u"Пожалуйста, выберите файлы.\n")
                text.config(state='disabled')
            else:
                if not os.path.exists(dir_name + '/transliterated/'):
                    os.mkdir(dir_name + '/transliterated/')
                if not os.path.exists(dir_name + '/log/'):
                    os.mkdir(dir_name + '/log/')
                if not os.path.exists(dir_name + '/passed/'):
                    os.mkdir(dir_name + '/passed/')
                passed_files = []
                for curr_filename in filenames_set:
                    print 'CURRENT FILE', curr_filename
                    if cls.check_transliterated(curr_filename, dir_name):
                        META['filename'] = curr_filename
                        ##print meta.filename
                        name = os.path.splitext(os.path.basename(META['filename']))[0]
                        ##print meta.res
                        if META['filename'] == '':
                            text.config(state = 'normal')
                            text.delete("1.0", "end")
                            text.insert("end", u"Пожалуйста, выберите файлы.\n")
                            text.config(state = 'disabled')
                        else:

                            try:
                                temp_filename = cls.get_temp_in_dir(dir_name)
                                new_text, log_data = cls.iterate_root(temp_filename, root, 0)

                                suffix = os.path.splitext(META['filename'])[1]

                                META['result_name'] = dir_name + '/transliterated/' + name + suffix

                                with codecs.open(META['result_name'], 'w') as inf:
                                    inf.write(new_text)


                                log_name = dir_name + '/log/' + name + '_log.txt'
                                with codecs.open(log_name, 'w', 'utf-8') as logf:
                                    logf.write(u'\n'.join(log_data))
                            except:
                                #print 'PASSED', meta.filename
                                passed_files.append(META['filename'])
                    else:
                        # passed_files.append(META['filename'])
                        passed_files.append(curr_filename)

                text.config(state = 'normal')
                text.delete('1.0', 'end')
                text.insert('end', u'\nВыполнено\n')
                text.configure(cursor = 'arrow')
                text.config(state = 'disabled')

                SaveText.save_passed(passed_files, dir_name)

    @classmethod
    def open_text(cls, text, root):
        text.config(state = 'normal')
        text.delete("1.0", "end")
        text.insert('end', u'Введите текст для транслитерирования')
        text.config(state = 'disabled')
        Dialog.open_text(root)

        text.config(state = 'normal')

        text.delete("1.0", "end")
        text.insert('end', u'Выберите действие')
        text.config(state = 'disabled')

# a = LoadData()
# META['filename'] = u'/Users/el/Downloads/vol. 1/testpart.html'
# tmp = a.get_temp('manual')
# b, c = LoadData.iterate_root_web(tmp)
# print 1