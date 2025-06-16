# Быстрая настройка базы данных

## Шаг 1: Откройте Supabase Dashboard
1. Перейдите на https://dashboard.supabase.com/project/rsvzwcbhvgjaarweifub
2. Войдите в свой аккаунт

## Шаг 2: Создайте таблицы через SQL Editor
1. В левом меню нажмите "SQL Editor"
2. Нажмите "New query"
3. Вставьте этот SQL код:

```sql
-- Таблица пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    referral_balance DECIMAL(10,2) DEFAULT 0,
    invited_count INTEGER DEFAULT 0,
    referred_by BIGINT,
    is_blocked BOOLEAN DEFAULT FALSE
);

-- Таблица подписок
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(chat_id),
    subscription_type TEXT NOT NULL,
    expire_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица платежей
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(chat_id),
    amount DECIMAL(10,2) NOT NULL,
    currency TEXT NOT NULL,
    telegram_payment_charge_id TEXT UNIQUE NOT NULL,
    provider_payment_charge_id TEXT,
    subscription_type TEXT NOT NULL,
    status TEXT DEFAULT 'completed',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица рефералов
CREATE TABLE referrals (
    id SERIAL PRIMARY KEY,
    referrer_id BIGINT NOT NULL REFERENCES users(chat_id),
    referred_id BIGINT NOT NULL REFERENCES users(chat_id),
    reward_amount DECIMAL(10,2) DEFAULT 0,
    is_paid BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(referrer_id, referred_id)
);
```

4. Нажмите "Run" (зеленая кнопка)

## Шаг 3: Проверьте результат
После выполнения SQL:
- В левом меню перейдите в "Table Editor"
- Вы должны увидеть 4 таблицы: users, subscriptions, payments, referrals

## Готово!
После создания таблиц бот будет полностью функциональным.

### Что работает сейчас:
- Команда /start
- Главное меню с кнопками
- Платежи через Telegram Stars
- Реферальная система
- Управление подписками