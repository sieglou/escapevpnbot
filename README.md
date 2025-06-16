# YouVPN Telegram Bot

Telegram-бот для VPN-сервиса с платными подписками, реферальной системой и интеграцией с Telegram Payments.

## Функциональность

- 🚀 Авторизация пользователей по chat_id
- 💳 Платные подписки через Telegram Payments
- 👥 Реферальная система с наградами
- 📊 Управление подписками в Supabase
- 🔔 Уведомления о платежах и истечении подписок
- ⚙️ Инструкции по подключению VPN
- 🎯 Красивый интерфейс с inline-клавиатурами

## Технологии

- **Python 3.8+**
- **aiogram 3.x** - фреймворк для Telegram ботов
- **Supabase** - база данных PostgreSQL в облаке
- **Telegram Payments** - встроенная система платежей

## Установка на Replit

### 1. Создание проекта

1. Откройте [Replit](https://replit.com)
2. Нажмите "Create Repl"
3. Выберите "Import from GitHub" или "Upload files"
4. Загрузите все файлы проекта

### 2. Настройка переменных окружения

В Replit перейдите в раздел "Secrets" (🔒) и добавьте следующие переменные:

```bash
BOT_TOKEN=ваш_токен_бота_от_BotFather
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=ваш_anon_key_от_supabase
PAYMENT_TOKEN=ваш_payment_token_от_BotFather
WEBSITE_URL=https://youvpn.com
SUPPORT_USERNAME=@youvpn_support
