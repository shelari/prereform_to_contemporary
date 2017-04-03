# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'
from flask import Flask, render_template, request, make_response, Response
from werkzeug.utils import secure_filename
import os
from flask_recaptcha import ReCaptcha
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import codecs
from zipfile import ZIP_DEFLATED
import time
import zipstream
import shutil
from process import Processor
from meta_data import META
from load_data import LoadData


# BEGIN: UGLY MONKEYPATCH
import pkgutil
orig_get_loader = pkgutil.get_loader
def get_loader(name):
    try:
        return orig_get_loader(name)
    except AttributeError:
        pass
pkgutil.get_loader = get_loader
# END: UGLY MONKEYPATCH

app = Flask(__name__)
app.config['RECAPTCHA_SITE_KEY'] = "6LeAcggTAAAAALCNTpHX5Qpa0DnHExVZrFMXiESF"
app.config['RECAPTCHA_SECRET_KEY'] = "6LeAcggTAAAAAAPVJ8qalCwkvSBLOpy8Yg2bswwM"

recaptcha = ReCaptcha(app)


#@app.route('/')
def index():
    new_text = ''
    input_text = ''
    return render_template("prereform_to_contemporary.html", output_text=new_text, input_text=input_text)

@app.route("/", methods=['GET', 'POST'])
def web_converter():

    input_text = ''
    output_text = ''
    new_text = ''
    if request.method == 'POST':
        if META['tmp_folder'] != '':
            shutil.rmtree(META['tmp_folder'])
            META['tmp_folder'] = ''

        input_text = request.values.get('inp_text')
        #app.logger.info(input_text)
        both = request.form.getlist('both')
        if 'go' in request.values:
            #if 'go' in request.args:
            if 'show' in both:
                output_text, changes = Processor.process_text(input_text, 1, META['old_new_delimiters'][META['current_delimiters_text']])
            else:
                output_text, changes = Processor.process_text(input_text, 0, META['old_new_delimiters'][META['current_delimiters_text']])

        if 'clean' in request.values:
            input_text = ''
            output_text = ''

        if 'download_txt' in request.values:
            ftxt = request.files.getlist("f_txt")
            errors = []
            tmp_folder = str(time.time()) + '_ptc'
            META['tmp_folder'] = tmp_folder
            os.mkdir(tmp_folder)
            for el in ftxt:
                try:
                    META['filename'] = secure_filename(el.filename)
                    input_text = el.read().decode('utf-8')
                    if 'show' in both:
                        new_text, changes = Processor.process_text(input_text, 1, META['old_new_delimiters'][META['current_delimiters_text']])
                    else:
                        new_text, changes = Processor.process_text(input_text, 0, META['old_new_delimiters'][META['current_delimiters_text']])
                    with codecs.open('log', 'w', 'utf-8') as ou:
                        ou.write(changes)
                    print changes, 'THIS'
                    name = os.path.splitext(META['filename'])[0]
                    suffix = os.path.splitext(META['filename'])[1]
                    print 'GET NAME'
                    if suffix == '':
                        suffix = '.txt'
                    new_filename = name + "_transliterated" + suffix
                    log_filename = name + '_log.txt'
                    fnpath = tmp_folder + '/' + new_filename
                    lpath = tmp_folder + '/' + log_filename
                    print 'GET PATH'
                    with codecs.open(fnpath, 'w', 'utf-8') as ou1:
                            ou1.write(new_text)
                            print 'WRITE DATA'
                    with codecs.open(lpath, 'w', 'utf-8') as ou2:
                            ou2.write(changes)
                            print changes, 'WTF??'
                except:
                    m = 'Error: file ' + secure_filename(el.filename)
                    errors.append(m)
            if errors:
                errors = u'\n'.join(errors)
                fer = tmp_folder + '/' + 'errors.txt'
                with codecs.open(fer, 'w', 'utf-8') as ou3:
                    ou3.write(errors)
            response = Response(generator(tmp_folder), mimetype='application/zip')
            response.headers['Content-Disposition'] = 'attachment; filename={}'.format('files.zip')
            return response

        if 'download_xml' in request.values:
            fxml = request.files.getlist("f_xml")
            errors = []
            tmp_folder = str(time.time()) + '_ptc'
            META['tmp_folder'] = tmp_folder
            os.mkdir(tmp_folder)
            for el in fxml:
                try:
                    META['filename'] = secure_filename(el.filename)
                    temp_filename = LoadData.get_temp_web(tmp_folder, el)
                    new_text, changes = LoadData.iterate_root_web(temp_filename)
                    os.remove(temp_filename)
                    name = os.path.splitext(META['filename'])[0]
                    suffix = os.path.splitext(META['filename'])[1]
                    if suffix == '':
                        suffix = '.txt'
                    new_filename = name + "_transliterated" + suffix
                    log_filename = name + '_log.txt'
                    fnpath = tmp_folder + '/' + new_filename
                    lpath = tmp_folder + '/' + log_filename
                    with codecs.open(fnpath, 'w') as ou1:
                        ou1.write(new_text)
                    if changes != u'':
                        with codecs.open(lpath, 'w', 'utf-8') as ou2:
                            ou2.write(changes)
                except:
                    m = 'Error: file ' + secure_filename(el.filename)
                    errors.append(m)
            if errors:
                errors = u'\n'.join(errors)
                fer = tmp_folder + '/' + 'errors.txt'
                with codecs.open(fer, 'w', 'utf-8') as ou3:
                    ou3.write(errors)
            response = Response(generator(tmp_folder), mimetype='application/zip')
            response.headers['Content-Disposition'] = 'attachment; filename={}'.format('files.zip')
            return response

        return render_template("prereform_to_contemporary.html", output_text=output_text, input_text=input_text)

    return render_template("prereform_to_contemporary.html", output_text=output_text, input_text=input_text)

def generator(tmp_folder):
        z = zipstream.ZipFile(mode='w', compression=ZIP_DEFLATED)
        files = os.listdir(tmp_folder)
        for f in files:
            if u'~' in f:
                continue
            p = tmp_folder + '/' + f
            z.write(p)
        for chunk in z:
            yield chunk


@app.route("/feedback", methods=['GET', 'POST'])
def send_mail():
    input_mail = ''
    alert = ''
    if recaptcha.verify():
        user = "sieleny.feedback@yandex.com"
        pwd = "**********"
        FROM = 'sieleny.feedback@yandex.com'
        TO = ['sieleny.feedback@yandex.com']
        SUBJECT = "Feedback from old2new converter"
        TEXT = request.values.get('mail')
        if TEXT.strip() != u'':
            msg = MIMEMultipart(encoding='utf-8')
            attachment = MIMEText(TEXT.encode('utf-8'), 'plain', _charset='utf-8')
            msg['Subject'] = SUBJECT
            msg['From'] = FROM
            msg['To'] = ', '.join(TO)
            msg.attach(attachment)

            server = smtplib.SMTP("smtp.yandex.com", 587)
            server.ehlo()
            server.starttls()
            server.login(user, pwd)
            server.sendmail(FROM, TO, msg.as_string().encode('utf-8'))
            alert = u'Сообщение отправлено.'
            server.close()
            return render_template("feedback.html", input_mail = input_mail, alert = alert)
    else:
        if request.method == 'POST':
            input_mail = request.values.get('mail')
            return render_template("feedback.html", input_mail = input_mail, alert = u'Кажется, вы робот. Попробуйте ещё раз!')
    return render_template("feedback.html", input_mail = input_mail, alert = alert)

@app.route("/settings", methods=['GET', 'POST'])
def get_settings():

    if META['current_delimiters_text'] == 'tei':
        check_txt = 'tei_txt'
        uncheck_txt1 = 's_txt'
        uncheck_txt2 = 'm_txt'
    elif META['current_delimiters_text'] == 'simple':
        check_txt = 's_txt'
        uncheck_txt1 = 's_txt'
        uncheck_txt2 = 'tei_txt'
    elif META['current_delimiters_text'] == 'manual_text':
        check_txt = 'm_txt'
        uncheck_txt1 = 's_txt'
        uncheck_txt2 = 'tei_txt'
    if META['current_delimiters_xml'] == 'tei':
        check_xml = 'tei_xml'
        uncheck_xml1 = 's_xml'
        uncheck_xml2 = 'm_xml'
    elif META['current_delimiters_xml'] == 'simple':
        check_xml = 's_xml'
        uncheck_xml1 = 'tei_xml'
        uncheck_xml2 = 'm_xml'
    elif META['current_delimiters_xml'] == 'manual_xml':
        check_xml = 'm_xml'
        uncheck_xml1 = 's_xml'
        uncheck_xml2 = 'tei_xml'
    # print 'CURRENT BEFORE', META['current_delimiters_text'], META['current_delimiters_xml']
    if request.method == 'POST':
        if 'save_settings' in request.values:
            checked_text = request.form['text_settings']
            META['current_delimiters_text'] = checked_text
            checked_xml = request.form['xml_settings']
            META['current_delimiters_xml'] = checked_xml
            if checked_text == 'tei':
                check_txt = 'tei_txt'
                uncheck_txt1 = 's_txt'
                uncheck_txt2 = 'm_txt'
            elif checked_text == 'simple':
                check_txt = 's_txt'
                uncheck_txt1 = 'tei_txt'
                uncheck_txt2 = 'm_txt'
            else:
                check_txt = 'm_txt'
                uncheck_txt1 = 's_txt'
                uncheck_txt2 = 'tei_txt'
                t1 = request.values.get('br_text20')
                t2 = request.values.get('br_text21')
                t3 = request.values.get('br_text22')
                META['old_new_delimiters']['manual_text'] = [t1, t2, t3]
            if checked_xml == 'tei':
                check_xml = 'tei_xml'
                uncheck_xml1 = 's_xml'
                uncheck_xml2 = 'm_xml'
            elif checked_xml == 'simple':
                check_xml = 's_xml'
                uncheck_xml1 = 'tei_xml'
                uncheck_xml2 = 'm_xml'
            else:
                check_xml = 'm_xml'
                uncheck_xml1 = 's_xml'
                uncheck_xml2 = 'tei_xml'
                x1 = request.values.get('br_xml20')
                x2 = request.values.get('br_xml21')
                x3 = request.values.get('br_xml22')
                META['old_new_delimiters']['manual_xml'] = [x1, x2, x3]
            return render_template("settings.html", check_txt=check_txt, uncheck_txt1=uncheck_txt1, uncheck_txt2=uncheck_txt2, check_xml=check_xml, uncheck_xml1=uncheck_xml1, uncheck_xml2=uncheck_xml2, v1_txt=META['old_new_delimiters']['manual_text'][0], v2_txt=META['old_new_delimiters']['manual_text'][1], v3_txt=META['old_new_delimiters']['manual_text'][2], v1_xml=META['old_new_delimiters']['manual_xml'][0], v2_xml=META['old_new_delimiters']['manual_xml'][1], v3_xml=META['old_new_delimiters']['manual_xml'][2])
    return render_template("settings.html", check_txt=check_txt, uncheck_txt1=uncheck_txt1, uncheck_txt2=uncheck_txt2, check_xml=check_xml, uncheck_xml1=uncheck_xml1, uncheck_xml2=uncheck_xml2, v1_txt=META['old_new_delimiters']['manual_text'][0], v2_txt=META['old_new_delimiters']['manual_text'][1], v3_txt=META['old_new_delimiters']['manual_text'][2], v1_xml=META['old_new_delimiters']['manual_xml'][0], v2_xml=META['old_new_delimiters']['manual_xml'][1], v3_xml=META['old_new_delimiters']['manual_xml'][2])

def save_log(m):
    with codecs.open('log', 'a', 'utf-8') as lf:
        lf.write(m)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2131, debug=True)
    # app.run(debug=True)

