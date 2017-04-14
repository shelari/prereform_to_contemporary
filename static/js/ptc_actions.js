function rename_span(real_id, field_id) {
	var arr = [];
	fs = document.getElementById(real_id).files;
	for (var i=0, len=fs.length; i<len; i++) {
    arr.push(fs[i].name);
	};
	var newd=arr.join();
	if (newd.length > 12) {
		newd = newd.substr(0, 12) + '...'
	};
	document.getElementById(field_id).innerHTML = newd;
};

function go_to_settings() {
	location.href = "{{url_for('get_settings')}}";
};

function specificate() {
	var br = window.navigator.userAgent;
	if (br.indexOf("Chrome")==-1) {
			document.getElementById("ch1").style.fontSize="11px";
			document.getElementById("ch2").style.fontSize="11px";
			document.getElementById("show-file").style.fontSize="12px";
			document.getElementById("show-file-xml").style.fontSize="12px";
			document.getElementById("ru_button").style.backgroundColor="#E4ECF4";
	};
	var data = sessionStorage.getItem('lang');
	if (data == 'en') {
		change_language("en")
	}
	else {
		document.getElementById("ru_button").style.backgroundColor="#E4ECF4";
	}
};

function change_language(current) {
	if (current == 'ru') {
		document.getElementById("en_button").style.backgroundColor="white";
		document.getElementById("ru_button").style.backgroundColor="#E4ECF4";
		document.getElementById("translit").value="Транслитерировать";
		document.getElementById("clean").value="Очистить";
		document.getElementById("title").innerHTML="Транслитератор из дореформенной русской орфографии в современную";
		document.getElementById("sh0").innerHTML=" Показывать оригинальное написание";
		document.getElementById("settings_button").value="Настройки";
		document.getElementById("load_txt").innerHTML="Загрузить файл(ы) .txt:";
		document.getElementById("load_tml").innerHTML="Загрузить файл(ы) xml (.html, .xhtml):";
		document.getElementById("text_ch1").innerHTML="Выбрать файлы";
		document.getElementById("text_ch2").innerHTML="Выбрать файлы";
		document.getElementById("example_title").innerHTML="Для примера:";
		document.getElementById("feed").innerHTML="Форма обратной связи";
		document.getElementById("school").innerHTML="Школа лингвистики";
		document.getElementById("auth").innerHTML="Елена Сидорова 2017";
		sessionStorage.setItem('lang', 'ru');

		document.getElementById("hse_logo").src="{{url_for('static', filename='logo_hse_cmyk.png')}}";
		document.getElementById("ling_logo").src="{{url_for('static', filename='logo_ling.jpg')}}";

		if (document.getElementById("show-file").innerHTML == "Nothing selected") {
			document.getElementById("show-file").innerHTML="Файл не выбран";
		};
		if (document.getElementById("show-file-xml").innerHTML == "Nothing selected") {
			document.getElementById("show-file-xml").innerHTML="Файл не выбран";
		};
	}
	else {

		document.getElementById("ru_button").style.backgroundColor="white";
		document.getElementById("en_button").style.backgroundColor="#E4ECF4";
		document.getElementById("translit").value="Transliterate";
		document.getElementById("clean").value="Clean";
		document.getElementById("title").innerHTML="Pre-reform to contemporary converter";
		document.getElementById("sh0").innerHTML=" Show the original spelling";
		document.getElementById("settings_button").value="Settings";
		document.getElementById("load_txt").innerHTML="Upload file(s) .txt:";
		document.getElementById("load_tml").innerHTML="Upload file(s) xml (.html, .xhtml):";
		document.getElementById("text_ch1").innerHTML="Choose files";
		document.getElementById("text_ch2").innerHTML="Choose files";
		document.getElementById("example_title").innerHTML="Example:";
		document.getElementById("feed").innerHTML="Feedback form";
		document.getElementById("school").innerHTML="School of linguistics";
		document.getElementById("auth").innerHTML="Elena Sidorova 2017";
		sessionStorage.setItem('lang', 'en');

		document.getElementById("hse_logo").src="{{url_for('static', filename='logo_hse_en.png')}}";
		document.getElementById("ling_logo").src="{{url_for('static', filename='logo_eng.png')}}";

		if (document.getElementById("show-file").innerHTML == "Файл не выбран") {
			document.getElementById("show-file").innerHTML="Nothing selected";
		};
		if (document.getElementById("show-file-xml").innerHTML == "Файл не выбран") {
			document.getElementById("show-file-xml").innerHTML="Nothing selected";
		};
	};
};

//var xml = "{{check_xml}}";
//var txt = "{{check_txt}}";
function submits(){
    //document.getElementById(txt).checked = true;
    //document.getElementById(xml).checked = true;
    specificate_settings();
};
function click(){
    if (document.getElementById("tei_txt").checked){
        txt = "tei_txt"
    };
    if (document.getElementById("s_txt").checked){
        txt = "s_txt"
    };
    if (document.getElementById("m_txt").checked){
        txt = "m_txt"
    };
    if (document.getElementById("tei_xml").checked){
        xml = "tei_xml"
    };
    if (document.getElementById("s_xml").checked){
        xml = "s_xml"
    };
    if (document.getElementById("m_xml").checked){
        xml = "m_xml"
    };
};
function change_language_settings(current) {
  if (current == 'ru') {
    document.getElementById("en_button").style.backgroundColor="white";
    document.getElementById("ru_button").style.backgroundColor="#E4ECF4";
    document.getElementById("back").innerHTML="Вернуться к транслитератору";
    document.getElementById("title_set").innerHTML="Настройки вывода";
    document.getElementById("txt_set").innerHTML="Для данных в формате .txt (загружаемые файлы и вводимые вручную тексты)";
    document.getElementById("xml_set").innerHTML="Для данных в формате xml/html";
    document.getElementById("simple_txt").innerHTML=" Простой";
    document.getElementById("manual_txt").innerHTML=" Задать вручную";
    document.getElementById("simple_xml").innerHTML=" Простой";
    document.getElementById("manual_xml").innerHTML=" Задать вручную";
    document.getElementById("save_button").value="Сохранить настройки";
    sessionStorage.setItem('lang', 'ru');
  }
  else {
    document.getElementById("ru_button").style.backgroundColor="white";
    document.getElementById("en_button").style.backgroundColor="#E4ECF4";
    document.getElementById("back").innerHTML="Go back to the converter";
    document.getElementById("title_set").innerHTML="Output settings";
    document.getElementById("txt_set").innerHTML="For .txt data (for uploaded files and entered text)";
    document.getElementById("xml_set").innerHTML="For xml/html data";
    document.getElementById("simple_txt").innerHTML=" Simple";
    document.getElementById("manual_txt").innerHTML=" Set manually";
    document.getElementById("simple_xml").innerHTML=" Simple";
    document.getElementById("manual_xml").innerHTML=" Set manually";
    document.getElementById("save_button").value="Save the settings";
    sessionStorage.setItem('lang', 'en');
  };
};

function specificate_settings() {
  var data = sessionStorage.getItem('lang');
  if (data == 'en') {
    change_language_settings("en")
  }
  else {
    document.getElementById("ru_button").style.backgroundColor="#E4ECF4";
  };
};

function change_language_feedback(current) {
  if (current == 'ru') {
    document.getElementById("en_button").style.backgroundColor="white";
    document.getElementById("ru_button").style.backgroundColor="#E4ECF4";
    document.getElementById("back").innerHTML="Вернуться к транслитератору";
    document.getElementById("title_feed").innerHTML="Форма обратной связи";
    document.getElementById("res_message").innerHTML="Если у вас возникли какие-то коментарии, вопросы, связанные с работой транслитератора, или же вы нашли ошибку, пожалуйста, свяжитесь с нами. Не забудьте оставить контактные данные, если вы хотите получить ответ.";
    document.getElementById("send_mes").value="Отправить";
    sessionStorage.setItem('lang', 'ru');
  }
  else {
    document.getElementById("ru_button").style.backgroundColor="white";
    document.getElementById("en_button").style.backgroundColor="#E4ECF4";
    document.getElementById("back").innerHTML="Go back to the converter";
    document.getElementById("title_feed").innerHTML="Feedback form";
    document.getElementById("res_message").innerHTML="If you have a comment, or questions about the converter, or you have find a fault, please, write us a message. Don't forget to leave your contacts if you want to get an answer.";
    document.getElementById("send_mes").value="Send";
    sessionStorage.setItem('lang', 'en');
  };
};

function specificate_feedback() {
  var data = sessionStorage.getItem('lang');
  if (data == 'en') {
    change_language_feedback("en")
  }
  else {
    document.getElementById("ru_button").style.backgroundColor="#E4ECF4";
  };
};
