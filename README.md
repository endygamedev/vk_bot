[![Python 3.8](https://img.shields.io/badge/python-3.8-green.svg)](https://www.python.org/downloads/release/python-380/)
![GitHub repo size](https://img.shields.io/github/repo-size/endygamedev/vk_bot)
![GitHub last commit](https://img.shields.io/github/last-commit/endygamedev/vk_bot)

# 🤖 Бот для сообщества ВК потока ПМ-19

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
1. Сервер для хостинга бота (оперативка — 1 Gb, SSD — 20 Gb)

## Реализация:
1. `vk_bot.py` - в этой программе запускается бот и создаётся текущая сессия с пользователем, хранятся все данные для общения с пользователем
1. `bot_actions.py` - самописный модуль в котором хранятся методы для ответа бота. Например метод отправки сообщения пользователем или метод для отправки фото.
1. `deadlines_data.py` - самописный модуль для работы с Google таблицей. <br/>


![GitHub Logo](data/vk_logo.png)

## Установка бота на сервере:
1. Клонируем репозиторий: `$ git clone https://github.com/endygamedev/vk_bot.git`
1. Заходим в каталог с репозиторием: `$ cd vk_bot`
1. Устанавливаем пакеты: `$ pip3 install -r requirements.txt`
1. Устанавливаем диспетчера служб: `$ apt-get install systemd`
1. Перейдём в каталог: `$ cd /etc/systemd/system`
1. Создадим новый файл `bot.service`:
```
[Unit]
Description=vk_bot
After=syslog.target
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/vk_bot
ExecStart=/usr/bin/python3 /root/vk_bot/vk_bot.py
RestartSec=10
Restart=always
 
[Install]
WantedBy=multi-user.target
```
7. Запускаем бота:
```bash
$ systemctl daemon-reload
$ systemctl enable bot
$ systemctl start bot
$ systemctl status bot
```
8. Для остановки бота нужно использовать: `$ systemctl stop bot`

Часть кода писала [**`Влада`**](https://github.com/VlPukhkalo)

<sub> Проект по ЯиМП: 1 курс (2 семестр) </sub>
<br>
<sub> Последнее обновление: 1.10.2020 </sub>

<br>
<p align="center">
  <sub> | <a href="https://endygamedev.github.io"> 👨‍💻 endygamdev </a> | </sub>
</p>
