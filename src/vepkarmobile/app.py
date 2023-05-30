#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Modile application - dictionary of the Karelian language.
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import sqlite3
from sqlite3 import Error

import os.path

import sys
#reload(sys)
#sys.setdefaultencoding('utf8')


class Vepkarmobile(toga.App):
    
    ###
    # Метод обработки нажатия кнопки (Поиск определений)
    ###
    def search_words(self, widget):
        self.count+=1
        print(self.count)
        print(format(self.name_input.value))
        #self.count_label.refresh()
        self.count_label.text = "Найдено " + str(self.count) + " записей"
        
        
        #data1 = [("word%s" % i) for i in range(1, self.count+1)]
        #self.container.data = data1
        
        ###
        # Составление Select запроса по выбранным параметрам
        ###
        # Выбранное наречие
        lang = self.selector_langs.value
        # Выбранный тип слов (леммы/словоформы)
        word = self.selector_words.value
        
        # Слово из поисковой строки
        search_word = self.name_input.value
        
        # id искомого наречия
        langs_id = ''
        
        if lang == 'всем наречиям' :
            langs_id = '(4, 5, 6)'
        elif lang == 'собственно карельскому наречию' :
            langs_id = '(4)'
            
        elif lang == 'ливвиковскому наречию' :
            langs_id = '(5)'
            
        elif lang == 'людиковскому наречию' :
            langs_id = '(6)'
          
        
        
        select_request = ''
        if word == 'всем словам':
            #
            #
            #
            pass
        elif word == 'леммам':
            # Запрос на леммы
            #select_request = f'''SELECT lemmas.lemma
            #FROM lemmas, langs
            #WHERE (lemmas.lang_id = langs.id) AND (lemmas.lemma like '{search_word}') AND (langs.id in {langs_id})'''
            
            select_request = f'''SELECT stems.stem || affixes_lemmas.lemma_affix AS stem_affix
            FROM stems, stem_affix__lemma, lang_stem, langs, affixes_lemmas
            WHERE stem_affix__lemma.stem_id = stems.id AND stem_affix__lemma.affix_lemma_id = affixes_lemmas.id
            AND lang_stem.stem_id = stems.id AND lang_stem.lang_id = langs.id
            AND langs.id in {langs_id} 
            AND stem_affix like '{search_word}'
            '''
            
            pass
        elif word == 'словоформам':
            # Запрос на словоформы
            #select_request = f'''SELECT wordforms.wordform
            #FROM wordforms, lemmas, lemma_wordform, langs
            #WHERE (wordforms.id = lemma_wordform.wordform_id) AND (lemma_wordform.lemma_id = lemmas.id) AND
            #(wordforms.wordform like '{search_word}') AND
            #(lemmas.lang_id = langs.id) AND (langs.id in {langs_id} )'''
            
            select_request = f'''SELECT stems.stem || affixes_changes.change_affix AS stem_affix
            FROM stems, stem_affix__lemma, lang_stem, langs, stem_affix__changes, affixes_changes
            WHERE stem_affix__lemma.stem_id = stems.id AND stem_affix__changes.lemma_id = stem_affix__lemma.id AND stem_affix__changes.change_affix_id = affixes_changes.id
            AND lang_stem.stem_id = stems.id AND lang_stem.lang_id = langs.id
            AND langs.id in {langs_id} 
            AND stem_affix like '{search_word}'
            '''
            
            pass
        
        
        ###
        # Соединение с БД и получение данных
        ###
    
        # Создание абстрактного пути к файлу БД
        package_dir = os.path.abspath(os.path.dirname(__file__))
        db_dir = os.path.join(package_dir, 'vepkar_sqlite_compact.db')
        # Соединение с БД
        connection = self.create_connection(db_dir)
        
        count = 0
        
        # Поиск в БД по Select запросу
        list_of_words = self.execute_read_query(connection, select_request)
        print(list_of_words)
        
        
        # Вывод на экран
        self.count_label.text = "Найдено " + str(len(list_of_words)) + " записей"
        self.container.data = list_of_words
        
        
        pass
    
    ######################################################################
    
    ###
    # Функция подключения к БД
    ###
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection
    
    ###
    # Функция чтения результата SELECT построчно
    ###
    def execute_read_query(self, connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        
        except Error as e:
            print(f"The error '{e}' occurred")

    
    ################################################
    #####
    ## startup - Модуль отрисовки виджетов на экране
    #####
    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(id='box', style=Pack(direction=COLUMN, padding_top=10))
        
        ###
        # Виджет - строка (рядом со списком выбора)
        ###
        label1 = toga.Label(
            text="Поиск по:",
            id="label1",
            style=Pack(padding=(4,2))
            )
        
        ###
        # Виджет - список выбора (карельского наречия)
        ###
        self.selector_langs = toga.Selection(
            id ="selector",
            items=['всем наречиям', 'собственно карельскому наречию', 'ливвиковскому наречию', 'людиковскому наречию']
            )

        ###
        # Виджет - бокс (для размещения в нём строки и списка выбора)
        ###
        lang_box = toga.Box(style=Pack(direction=ROW, padding=5))
        lang_box.add(label1)
        lang_box.add(self.selector_langs)
        
        
        ###
        # Виджет - список выбора (леммы и словоформы)
        ###
        self.selector_words = toga.Selection(
            id ="selector2",
            items=['всем словам', 'леммам', 'словоформам'],
            style=Pack(padding=(0,0,0,2))
            )

        ###
        # Виджет - бокс (для размещения в нём строки и списка выбора)
        ###
        #word_box = toga.Box(style=Pack(direction=ROW, padding=5))
        #word_box.add(label2)
        #word_box.add(self.selector_words)
        

        lang_box.add(self.selector_words)
        
        # Добавляем бокс на главный экран
        main_box.add(lang_box)
        
        ###
        # Виджет - поле ввода (для поиска определений)
        ###
        self.name_input = toga.TextInput(style=Pack(flex=1, padding=2))
        
        self.count = 0
        
        ###
        # Виджет - кнопка поиска (для поиска определений)
        ###
        btn = toga.Button(
            "Показать",
            on_press=self.search_words,
            style=Pack(padding=0)
            )
        
        ###
        # Виджет - бокс (для размещения в нём поля ввода и кнопки)
        ###
        search_box = toga.Box(style=Pack(direction=ROW, padding=5))
        search_box.add(self.name_input)
        search_box.add(btn)
        
        # Добавляем бокс на главный экран (добавлен ниже)
        main_box.add(search_box)
        
        ###
        # Виджет - строка (вывод количества записей)
        ###
        #count = 0
        self.count_label = toga.Label(
            text = "Найдено " + str(self.count) + " записей",
            style=Pack(padding_bottom=8)
            )
        
        
        main_box.add(self.count_label)
        
        
        ###
        # Создание контейнера в виде таблицы
        ###
        data = [("word%s" % i) for i in range(1, 100)]
        #data = []
        
        self.container = toga.Table(
            headings=["Searching:"], 
            data=data,
            style=Pack(padding_bottom=10, flex=1)
            )
        main_box.add(self.container)
        
        
 
       
        ############################################################
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


#####
## Модуль main
#####
def main():
    return Vepkarmobile()
