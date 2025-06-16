#!/usr/bin/env python3
"""
Скрипт для создания таблиц в Supabase
"""

from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

def setup_database():
    """Создает таблицы в Supabase"""
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    supabase = create_client(supabase_url, supabase_key)
    
    # SQL для создания всех таблиц
    sql_script = """
    -- Создаем таблицу пользователей
    CREATE TABLE IF NOT EXISTS users (
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

    -- Создаем таблицу подписок
    CREATE TABLE IF NOT EXISTS subscriptions (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        subscription_type TEXT NOT NULL,
        expire_at TIMESTAMP WITH TIME ZONE NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Создаем таблицу платежей
    CREATE TABLE IF NOT EXISTS payments (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        currency TEXT NOT NULL,
        telegram_payment_charge_id TEXT UNIQUE NOT NULL,
        provider_payment_charge_id TEXT,
        subscription_type TEXT NOT NULL,
        status TEXT DEFAULT 'completed',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Создаем таблицу рефералов
    CREATE TABLE IF NOT EXISTS referrals (
        id SERIAL PRIMARY KEY,
        referrer_id BIGINT NOT NULL,
        referred_id BIGINT NOT NULL,
        reward_amount DECIMAL(10,2) DEFAULT 0,
        is_paid BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        UNIQUE(referrer_id, referred_id)
    );

    -- Создаем индексы
    CREATE INDEX IF NOT EXISTS idx_users_chat_id ON users(chat_id);
    CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
    CREATE INDEX IF NOT EXISTS idx_subscriptions_active ON subscriptions(is_active, expire_at);
    CREATE INDEX IF NOT EXISTS idx_payments_user_id ON payments(user_id);
    CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_id);
    """
    
    try:
        # Попробуем выполнить SQL через rpc
        result = supabase.rpc('exec_sql', {'sql': sql_script}).execute()
        print("Таблицы созданы успешно!")
        
    except Exception as e:
        print(f"Ошибка при создании таблиц через RPC: {e}")
        
        # Альтернативный способ - создаем таблицы по одной через отдельные операции
        print("Пробуем создать таблицы по одной...")
        
        try:
            # Проверяем есть ли уже таблица users
            result = supabase.table("users").select("*").limit(1).execute()
            print("Таблица users уже существует")
            
        except Exception:
            print("Создаем таблицы через вставку данных...")
            
            # Создаем тестового пользователя для инициализации таблицы
            try:
                # Создаем таблицы через SQL Editor в веб-интерфейсе
                print("\nНужно создать таблицы вручную в Supabase Dashboard:")
                print("1. Откройте https://dashboard.supabase.com")
                print("2. Выберите ваш проект")
                print("3. Перейдите в Table Editor")
                print("4. Создайте таблицы users, subscriptions, payments, referrals")
                print("\nИли выполните SQL из файла database_setup.sql в SQL Editor")
                
                return False
                
            except Exception as e2:
                print(f"Ошибка: {e2}")
                return False
    
    return True

if __name__ == "__main__":
    setup_database()