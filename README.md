# README #

Pre-reform to contemporary orthography convertor for the Russian language

### Author ###

Elena Sidorova (sieleny@gmail.com)

### What does it do? ###

Converts the texts from the pre-reform (reform of 1918 https://ru.wikipedia.org/wiki/%D0%A0%D0%B5%D1%84%D0%BE%D1%80%D0%BC%D0%B0_%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE%D0%B9_%D0%BE%D1%80%D1%84%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%B8_1918_%D0%B3%D0%BE%D0%B4%D0%B0) format to the contemporary one. NB: about all the changes see https://drive.google.com/file/d/0B65_GJ8xcCTzUXFjbFdPOXBHQUE/view

### Online version ###

http://web-corpora.net/wsgi/tolstoi_translit.wsgi/ (in process)

### Offline version ###

For using this convertor on your own computer you should install python2.7 and run the file prereform_to_contemporary.py

### Command line version ###

For running this convertor from the command line you should run the file translit_from_string.py:
```
>>> python2.7 translit_from_string.py "Онъ стоялъ подлѣ письменнаго стола" 
<<< Он{Онъ} стоял{стоялъ} подле{подлѣ} письменного{письменнаго} стола 
```
