# KarelMobile
Modile application - dictionary of the Karelian language.

Мобильное приложение Карельский словарь, написанное при помощи инструментов проекта BeeWare на языке Python.

Для запуска и проверки программы должны быть установлены необходимые пакеты Toga и Briefcase (для удобства в виртуальном окружении). Подробнее см:

https://beeware.org/project/projects/libraries/toga/

https://beeware.org/project/projects/tools/briefcase/

Для работы программы необходимо добавить файл БД SQLite: karel_sqlite_compact.db, в папку src/vepkarmobile. Скачать его можно по ссылке:

https://drive.google.com/drive/u/0/folders/1OQCIa8fQrtdwDkmp408o9DbKXD3sRBH5

Для запуска программы на эмуляторе (мобильном телефоне) необходимо выполнить следующие команды в консоли (находясь в папке приложения):

$ briefcase create android 

$ briefcase build android

$ briefcase run android
