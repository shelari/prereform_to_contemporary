# -*- coding: utf-8 -*-
__author__ = 'ElenaSidorova'

META = {
    'filename': 'filename',
    'result_name': 'result_name',
    'log_name': 'log_name',
    'flag': 0,
    'parent': None,
    'default_directory':u'',
    'old_new_delimiters': {
        'tei':[u'<choice><reg>', u'</reg><orig>', u'</orig></choice>'],
        'simple':[u'', u'{', u'}'],
        'manual_text':[u'', u'', u''],
        'manual_xml':[u'', u'', u'']
    },
    'current_delimiters_text':'simple',
    'current_delimiters_xml':'tei',
    'tmp_folder':''

}
