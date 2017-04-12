# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
import codecs
import os
import sys
import re
import subprocess
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


            check_brackets = 1 # учитывать скобки
            if META['flag'] == 1: #???????
                new_text, changes, wrong_changes, _ = Processor.process_text(data, 1, delimiters, check_brackets)  #транслитерировали
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
        # print 1
        encoding = tree.docinfo.encoding
        root = tree.getroot()
        doctype = tree.docinfo.doctype
        standalone = tree.docinfo.standalone
        log_data = []
        wrong_log = []
        # markers = u'іѣъiѢЪIѣъѣіі'
        check_brackets = 1
        new_markers = [u']']
        markers = [u'i', u'I', u'і', u'ѣ', u'Ѣ', u'ъ', u'Ъ', u'ѣ', u'і']
        markers += new_markers
        for child in root.iter():
            # print 'GO CHILD', child
            try:
                # print 'TRY CHILD TEXT', child.text
                # if u'i' in child.text or u'I' in child.text or u'і' in child.text or u'ѣ' in child.text or u'Ѣ' in child.text or u'ъ' in child.text or u'Ъ' in child.text or u'ѣ' in child.text or u'і' in child.text:
                if u'Евстратъ-то' in child.text:
                    print 1
                for marker in markers:
                    # print 'MARKER', marker
                    if child.text is not None and marker in child.text:
                        # print 'IN'
                        # old = child.text

                        new_text, changes, wrong_changes, _ = Processor.process_text(child.text, 1, META['old_new_delimiters'][META['current_delimiters_xml']], check_brackets)
                        child.text = new_text
                        if changes:
                            log_data.append(changes)
                        if wrong_changes:
                            wrong_log.append(wrong_changes)
                        break
            except:
                pass
            try:
                #for marker in markers:
                # if u'i' in child.tail or u'I' in child.tail or u'і' in child.tail or u'ѣ' in child.tail or u'Ѣ' in child.tail or u'ъ' in child.tail or u'Ъ' in child.tail or u'ѣ' in child.tail or u'і' in child.tail:
                    # old = child.tail
                # print 'TRY CHILD TAIL', child.tail
                if u'Евстратъ-то' in child.tail:
                    print 1
                for marker in markers:
                    # print 'MARKER', marker
                    if child.tail is not None and marker in child.tail:
                        # print 'IN'
                        new_text, changes, wrong_changes, _ = Processor.process_text(child.tail, 1, META['old_new_delimiters'][META['current_delimiters_xml']], check_brackets)
                        child.tail = new_text
                        if changes:
                            log_data.append(changes)
                        if wrong_changes:
                            wrong_log.append(wrong_changes)
                        break
            except:
                pass
            print 'CHECKED'

        print 'FINISHED'
        new_text = etree.tostring(root, xml_declaration=True, encoding=encoding, standalone=standalone, doctype = doctype)

        new_text = new_text.replace('&lt;choice&gt;', '<choice>')
        new_text = new_text.replace('&lt;reg&gt;', '<reg>')
        new_text = new_text.replace('&lt;/choice&gt;', '</choice>')
        new_text = new_text.replace('&lt;/reg&gt;', '</reg>')
        new_text = new_text.replace('&lt;orig&gt;', '<orig>')
        new_text = new_text.replace('&lt;/orig&gt;', '</orig>')
        new_text = new_text.replace('&lt;sic&gt;', '<sic>')
        new_text = new_text.replace('&lt;/sic&gt;', '</sic>')
        new_text = new_text.replace('&lt;corr&gt;', '<corr>')
        new_text = new_text.replace('&lt;/corr&gt;', '</corr>')
        new_text = new_text.replace('&lt;choice original_editorial_correction', '<choice original_editorial_correction')
        new_text = new_text.replace("'&gt;<sic>", "'><sic>")
        # print 'CHANGE ORDER'
        # print new_text
        # new_text = re.sub(ur"&lt;(choice original_editorial_correction=\'[^\']+\')&gt;", "<\1>", new_text)
        # print 'CHANGE RE'
        return new_text, log_data, wrong_log

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
                    new_text, changes, wrong_changes, _ = Processor.process_text(child.text, 1, META['old_new_delimiters'][META['current_delimiters_xml']], 0)
                    child.text = new_text
                    if changes:
                        log_data.append(changes)
            except:
                pass
            try:
                #for marker in markers:
                if u'i' in child.tail or u'I' in child.tail or u'і' in child.tail or u'ѣ' in child.tail or u'Ѣ' in child.tail or u'ъ' in child.tail or u'Ъ' in child.tail or u'ѣ' in child.tail or u'і' in child.tail:
                    # old = child.tail
                    new_text, changes, wrong_changes, _ = Processor.process_text(child.tail, 1, META['old_new_delimiters'][META['current_delimiters_xml']], 0)
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
            print 'REALLY OPENED'
        except:
            print 'NOT OPENED'
            return 0
        if '<reg>' not in data and '<orig>' not in data:
            print 'REG NOT IN'
            return 1
        else:
            print 'REG IS IN'
            with codecs.open(u'/Users/el/PycharmProjects/PTC/prereformtocontemporary/transliterated_before', 'a', 'utf-8') as lf:
                lf.write(fn.decode('utf-8').split(u'/')[-1])
                lf.write(u'\n')
            return 0

    @classmethod
    def load_several_html(cls, text, root):
        proc_log = []
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
                spelling = 1 # SPELLING
                for curr_filename in filenames_set:
                    # print 'CURRENT FILE', curr_filename
                    if cls.check_transliterated(curr_filename, dir_name):
                        # print 'IS CHECKED'
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
                                # print 'START ITERATE'
                                proc_log.append('START')
                                new_text, log_data, wrong_log = cls.iterate_root(temp_filename, root, 0)
                                # print 'STOP ITERATE'
                                proc_log.append('STOP')

                                suffix = os.path.splitext(META['filename'])[1]

                                META['result_name'] = dir_name + '/transliterated/' + name + suffix

                                with codecs.open(META['result_name'], 'w') as inf:
                                    inf.write(new_text)


                                log_name = dir_name + '/log/' + name + '_log.txt'
                                wrong_changes = []
                                # print 'CREATE LOG NAME'
                                if log_data:
                                    print 'IS LOG DATA'
                                    log_data = u'\n'.join(log_data)
                                    log_data = log_data.split(u'\n')
                                    # print 'LD'
                                    check_log = [h.split(u' --> ')[1] for h in log_data]
                                    # print '-->'
                                    raw_log_forms = [h.replace(u']', u'').replace(u'[', u'') for h in check_log]
                                    # wrong_changes = []
                                    print 'RAW LOG'
                                    if len(raw_log_forms) < 22000:
                                        check_log_forms = [u' '.join(raw_log_forms)]
                                        print 'CREATE LOG FORMS'
                                    else:
                                        check_log_forms = []
                                        tmp_clf = []
                                        for o, uu in enumerate(raw_log_forms):
                                            if o != 0 and not o%22000:
                                                check_log_forms.append(u' '.join(tmp_clf))
                                                tmp_clf = []
                                            tmp_clf.append(uu)
                                        if tmp_clf:
                                            check_log_forms.append(u' '.join(tmp_clf))

                                    with codecs.open('log_forms', 'w', 'utf-8') as chlf:
                                        chlf.write(u'\n'.join(check_log_forms))
                                    print 'CHECK LOG'
                                    if spelling:
                                        print 'SPELLING'
                                        spelled_raw = []
                                        for chlf in check_log_forms:
                                            print 'PART LOG'
                                            cmd = "echo " + chlf + " | hunspell -d ru_Ru"
                                            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable="/bin/bash")
                                            spelled, err_sp = p.communicate()
                                            spelled_parts = spelled.decode('utf-8').split('\n')[1:][:-2]
                                            spelled_raw += spelled_parts
                                        print 'SPELLED ALL PARTS'
                                        # with codecs.open('spell_test.txt', 'w', 'utf-8') as spw:
                                        #     spw.write(u'\n'.join(spelled))
                                    # with codecs.open('log_test_2.txt', 'w', 'utf-8') as ss:
                                    #     ss.write(u'\n'.join(log_data))
                                        # for j, sp in enumerate(spelled):
                                        #     if sp[0] == u'&':
                                        #         print j, sp, u'=', log_data[j]
                                        #         wrong_changes.append(log_data[j])
                                        #         log_data[j] = log_data[j] + u' *'
                                        # print 'DECODED SPELLED'
                                        spelled = []
                                        for s in spelled_raw:
                                            if s.strip() != u'':
                                                spelled.append(s)
                                        # print 'GET SPELLED LIST'
                                        gap = 0
                                        num_gap = 0
                                        for j, sp in enumerate(log_data):
                                            prev_pos = j + gap - num_gap
                                            # if j == 31:
                                            #     pass
                                            # print 'IM IN', j, sp, gap
                                            # print 'DATA', j + gap, len(spelled)
                                            curr_word = sp.split(u' --> ')[1]
                                            # if curr_word == u'Дон-Кихоте':
                                            #     pass
                                            if re.search(u'^[0-9\-]+$', curr_word):
                                                num_gap += 1
                                                continue
                                            if j + gap - num_gap >= len(spelled):
                                                break
                                            # print 'NOW SPELL'
                                            # print 'THIS', j + gap - num_gap, spelled[j + gap - num_gap]
                                            # print u'%%%%'.join(spelled[686:690])
                                            if spelled[j + gap - num_gap][0] == u'&':
                                                print j, spelled[j + gap - num_gap], u'=', log_data[j]
                                                spell_ans = u' '.join(spelled[j + gap - num_gap].split(u':')[0].split(u' ')[1:-2])
                                                # wrong_changes.append(log_data[j])
                                                wrong_changes.append(spell_ans)
                                                log_data[j] = log_data[j] + u' *'
                                            # print 'NOW HYP'
                                            if u' ' in curr_word:
                                                curr_arr_space = curr_word.split(u' ')
                                                gap += len(re.findall(u' ', curr_word))
                                            else:
                                                curr_arr_space = [curr_word]
                                            curr_arr = []
                                            for m, curr_p in enumerate(curr_arr_space):
                                                if u'-' in curr_p:
                                                    gap += len(re.findall(u'-', curr_p))
                                                    curr_p = curr_p.split(u'-')
                                                    if curr_p == [u'', u'']:
                                                        gap -= 1
                                                        continue
                                                    for cwp in curr_p:
                                                        if re.search(u'^[0-9]+$', cwp) or cwp == u'':
                                                            gap -= 1
                                                        if cwp != u'':
                                                            curr_arr.append(cwp)


                                                else:
                                                    curr_arr.append(curr_p)
                                            # print 'CHECK -'
                                            new_curr_arr = []
                                            for m, curr_p in enumerate(curr_arr):
                                                if re.search(u'[0-9]', curr_p):
                                                    # new_curr_arr = []
                                                    # for cwp in curr_arr:
                                                    tmp_cwp = re.split(u'[0-9]+', curr_p)
                                                    if tmp_cwp[0] == u'':
                                                        tmp_cwp = tmp_cwp[1:]
                                                    if tmp_cwp and tmp_cwp[-1] == u'':
                                                        tmp_cwp = tmp_cwp[:-1]
                                                    if tmp_cwp:
                                                        new_curr_arr += tmp_cwp
                                                    if len(new_curr_arr) > len(curr_arr):
                                                        num_gap += len(new_curr_arr) - len(curr_arr)
                                                else:
                                                    new_curr_arr.append(curr_p)
                                            # print 'CHECK NUM'
                                            if j + gap - num_gap > prev_pos:
                                                # print 'IS DIFF'
                                                # diff = j + gap - num_gap - prev_pos
                                                try_pos = 1
                                                while prev_pos + try_pos < j + gap - num_gap + 1:
                                                    if spelled[prev_pos + try_pos][0] == u'&':
                                                        # print j, spelled[prev_pos + try_pos], u'=', log_data[j]
                                                        wrong_changes.append(log_data[j])
                                                        log_data[j] = log_data[j] + u' *'
                                                        break
                                                    try_pos += 1
                                            # print 'CHECK DIFF'




                                    print 'SPELLED'
                                with codecs.open(log_name, 'w', 'utf-8') as logf:
                                    logf.write(u'\n'.join(log_data))
                                    # logf.write(log_data)
                                print 'SAVE LOG'

                                wrong_log_name = dir_name + '/log/' + name + '_err_spelled.txt'
                                with codecs.open(wrong_log_name, 'w', 'utf-8') as wrf:
                                    wrf.write(u'\n'.join(wrong_changes))
                                print 'SAVE WRONG'
                            except:
                                #print 'PASSED', meta.filename
                                if proc_log[-1] == 'STOP':
                                    try:
                                        with codecs.open('err_in_spell', 'a', 'utf-8') as eis:
                                            eis.write(META['filename'])
                                            eis.write(u'\n')
                                    except:
                                        try:
                                            with codecs.open('err_in_spell', 'a', 'utf-8') as eis:
                                                eis.write(META['filename'].decode('utf-8'))
                                                eis.write(u'\n')
                                        except:
                                            pass
                                elif proc_log[-1] == 'START':
                                    try:
                                        with codecs.open('err_in_struct', 'a', 'utf-8') as eis:
                                            eis.write(META['filename'])
                                            eis.write(u'\n')
                                    except:
                                        try:
                                            with codecs.open('err_in_struct', 'a', 'utf-8') as eis:
                                                eis.write(META['filename'].decode('utf-8'))
                                                eis.write(u'\n')
                                        except:
                                            pass
                                passed_files.append(META['filename'])
                    else:
                        # passed_files.append(META['filename'])
                        print 'DIDNT CHECKED'
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