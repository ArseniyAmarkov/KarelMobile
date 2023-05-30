# VepKarMobile
Modile application - dictionary of the Karelian language.

Мобильное приложение Карельский словарь, написанное при помощи инструментов проекта BeeWare на языке Python.

Для запуска и проверки программы должны быть установлены необходимые пакеты Toga и Briefcase (для удобства в виртуальном окружении). Подробнее см. 
https://beeware.org/project/projects/libraries/toga/
https://beeware.org/project/projects/tools/briefcase/

Для работы программы необходимо добавить файл БД SQLite: vepkar_sqlite_compact, в папку src/vepkarmobile

Для запуска программы на эмуляторе (мобильном телефоне) необходимо выполнить следующие команды в консоли (находясь в папке приложения):
briefcase create android \n
briefcase build android \n
briefcase run android \n
