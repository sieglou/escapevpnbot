#!/usr/bin/env python3
"""
Скрипт для создания таблиц в Supabase через REST API
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Получаем настройки
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def create_tables():
    """Создает таблицы в Supabase через REST API"""
    
    # SQL запросы для создания таблиц
    sql_queries = [
        # Таблица пользователей
        """
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
        """,
        
        # Таблица подписок
        """
        CREATE TABLE IF NOT EXISTS subscriptions (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL REFERENCES users(chat_id),
            subscription_type TEXT NOT NULL,
            expire_at TIMESTAMP WITH TIME ZONE NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        # Таблица платежей
        """
        CREATE TABLE IF NOT EXISTS payments (
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
        """,
        
        # Таблица рефералов
        """
        CREATE TABLE IF NOT EXISTS referrals (
            id SERIAL PRIMARY KEY,
            referrer_id BIGINT NOT NULL REFERENCES users(chat_id),
            referred_id BIGINT NOT NULL REFERENCES users(chat_id),
            reward_amount DECIMAL(10,2) DEFAULT 0,
            is_paid BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            UNIQUE(referrer_id, referred_id)
        );
        """,
        
        # Индексы
        """
        CREATE INDEX IF NOT EXISTS idx_users_chat_id ON users(chat_id);
        CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
        CREATE INDEX IF NOT EXISTS idx_subscriptions_active ON subscriptions(is_active, expire_at);
        CREATE INDEX IF NOT EXISTS idx_payments_user_id ON payments(user_id);
        CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_id);
        """
    ]
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json'
    }
    
    print("Создание таблиц в Supabase...")
    
    for i, query in enumerate(sql_queries, 1):
        try:
            # Используем RPC функцию для выполнения SQL
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/rpc/sql_exec",
                headers=headers,
                json={"query": query.strip()}
            )
            
            if response.status_code == 200:
                print(f"✓ Запрос {i} выполнен успешно")
            else:
                print(f"✗ Ошибка в запросе {i}: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"✗ Ошибка при выполнении запроса {i}: {e}")
    
    print("Создание таблиц завершено!")

if __name__ == "__main__":
    create_tables()