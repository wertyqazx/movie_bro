# 🎬 MovieMate — Telegram-бот для поиска фильмов

**Автор:** Олег Яковлев 413120

---

## 📌 О проекте

MovieMate — это Telegram-бот, который помогает быстро находить и сохранять фильмы.  
Основные функции:

- Поиск фильмов по названию  
- Просмотр краткой карточки с постером, рейтингом и описанием  
- Добавление в избранное  
- Просмотр списка избранных фильмов  
- Случайная рекомендация  
- Фильтрация по жанрам  
- Рейтинг TMDb Top-250  

Бот работает с TMDb API и сохраняет пользовательские данные в SQLite.

---

## 🚀 Быстрый старт

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/wertyqazx/movie_bro.git
cd moviemate-bot
```

2. **Создайте виртуальное окружение и установите зависимости:**
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
---

3. **🔑 Получение API ключей**

Для работы бота необходимы два токена: Telegram Bot Token и TMDb API Key. Ниже описано, как их получить.

---

**📬 1. Получить Telegram Bot Token**

1. Открой Telegram и найди [@BotFather](https://t.me/BotFather).
2. Напиши команду `/newbot`.
3. Укажи имя и юзернейм для бота (например, `MovieMateBot`).
4. BotFather отправит тебе токен — **скопируй его**.

---

**🎥 2. Получить TMDb API Key**

1. Перейди на сайт: [https://www.themoviedb.org/subscription](https://www.themoviedb.org/subscription)
2. Войди или зарегистрируйся.
3. Выбери **"Developer" (бесплатный)** план.
4. После активации аккаунта зайди в [API Settings](https://www.themoviedb.org/settings/api).
5. Заполни форму (можно указать, что делаешь Telegram-бота).
6. После одобрения ты получишь **API Key v3** — **это и есть нужный токен**.

> ⚠️ **Важно:** если ты запускаешь бота из России, TMDb API может быть недоступен без VPN.  
> Убедись, что у тебя включён VPN, иначе запросы к `api.themoviedb.org` не будут работать.

---

**⚙️ Создание `.env`**

Создай файл `.env` в корне проекта и добавь туда:

```
BOT_TOKEN=сюда_вставь_токен_от_BotFather
TMDB_TOKEN=сюда_вставь_API_key_v3_от_TMDb
```

> ❗️ **Никогда не публикуй этот файл в интернете или на GitHub.**

---

## 📁 Структура проекта

```
moviemate-bot/

├── bot.py                  # Точка входа
├── .env                    # Токены и API ключи
├── README.md               # Документация

├── config/                 # Настройки через pydantic
│   └── settings.py

├── routers/                # Обработчики команд
│   ├── commands.py         # /start и /help
│   ├── favorites.py        # /favorites
│   ├── genre.py            # /setgenre и фильтрация
│   ├── random.py           # /random
│   ├── search.py           # /find + FSM
│   └── top250.py           # /top250

├── services/               # Внешние API и БД
│   ├── db.py               # SQLite (add/remove/list)
│   └── tmdb.py             # TMDb API

├── states/                 # FSM состояния
│   └── search.py           # Поиск по названию

├── utils/                  # Вспомогательные утилиты
│   └── preferences.py      # Выбранные жанры пользователей

├── storage/                # Хранилище данных
│   ├── .keep               # Пустышка для git
│   └── movies.db           # SQLite база
```

---

## 🛠 Технологии

- Python 3.11+  
- Aiogram 3.x  
- TMDb API (The Movie Database)  
- SQLite + aiosqlite  
- FSM (Finite State Machine)  
- Pydantic Settings для конфигурации  
