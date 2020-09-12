# 🌐 Бот для сообщества ВК потока ПМ-19

## Актуальность:
У нас имеется группа ВК, где находятся все ребята нашего потока и со 2 семестра нас стало меньше, поэтому у нас начала творится абсолютная вакханалия с расписанием. Сейчас вроде бы всё устаканилось, но расписание, которое находится в мобильном приложении или на сайте недействительно и поэтому некоторые студенты всё равно путаются. Также с начала дистанционного обучения вакханалия начала творится и с дедлайнами. Особенно с историей и английским, когда реальные дедлайны просто теряются в каше домашних заданий других групп.
Поэтому из всей этой кучи домашних заданий мы должны отфильтровывать наши (реальные). Бывали случаи, когда мы узнавали о существовании дедлайна за 5 минут до его конца.
**Поэтому наш бот должен облегчить головную боль студентов нашего потока.**

## Цель:
Cоздать бота, который по нескольким запросам будет формировать текстовое сообщение с дедлайнами по предметам или расписанием на неделю, список Дней рождений, список фильмов и олимпиадных задачек.

## Технологии:
1. Python
1. VK API
1. Google Drive API
1. Google Sheets API
1. Сервер для хостинга бота (520 Mb - оперативки, 10 Gb - SSD)

## Реализация:
1. vk_bot.py - в этой программе запускается бот и создаётся текущая сессия с пользователем, хранятся все данные для общения с пользователем
1. bot_actions.py - самописный модуль в котором хранятся методы для ответа бота. Например метод отправки сообщения пользователем или метод для отправки фото.
1. deadlines_data.py - самописный модуль для работы с Google таблицей.

![GitHub Logo](data/vk_logo.png)
