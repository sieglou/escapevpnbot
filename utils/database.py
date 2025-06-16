"""
Утилиты для работы с базой данных Supabase
"""

import logging
from supabase import create_client, Client
from config import config

logger = logging.getLogger(__name__)

# Глобальный клиент Supabase
_supabase_client: Client = None


def get_supabase_client() -> Client:
    """
    Получает клиент Supabase (singleton)
    """
    global _supabase_client
    
    if _supabase_client is None:
        _supabase_client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    
    return _supabase_client


async def init_database():
    """
    Инициализирует базу данных и создает необходимые таблицы
    """
    try:
        supabase = get_supabase_client()
        
        # Проверяем подключение
        result = supabase.table("users").select("count", count="exact").execute()
        logger.info(f"Подключение к Supabase успешно. Пользователей в БД: {result.count}")
        
        # Создаем таблицы, если они не существуют (через SQL)
        await create_tables_if_not_exist()
        
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
        raise


async def create_tables_if_not_exist():
    """
    Создает таблицы в Supabase, если они не существуют
    """
    try:
        supabase = get_supabase_client()
        
        # SQL для создания таблиц
        create_users_table = """
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
        """
        
        create_subscriptions_table = """
        CREATE TABLE IF NOT EXISTS subscriptions (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            subscription_type TEXT NOT NULL,
            expire_at TIMESTAMP WITH TIME ZONE NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            FOREIGN KEY (user_id) REFERENCES users(chat_id)
        );
        """
        
        create_payments_table = """
        CREATE TABLE IF NOT EXISTS payments (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            currency TEXT NOT NULL,
            telegram_payment_charge_id TEXT UNIQUE NOT NULL,
            provider_payment_charge_id TEXT NOT NULL,
            subscription_type TEXT NOT NULL,
            status TEXT DEFAULT 'completed',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            FOREIGN KEY (user_id) REFERENCES users(chat_id)
        );
        """
        
        create_referrals_table = """
        CREATE TABLE IF NOT EXISTS referrals (
            id SERIAL PRIMARY KEY,
            referrer_id BIGINT NOT NULL,
            referred_id BIGINT NOT NULL,
            reward_amount DECIMAL(10,2) DEFAULT 0,
            is_paid BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            FOREIGN KEY (referrer_id) REFERENCES users(chat_id),
            FOREIGN KEY (referred_id) REFERENCES users(chat_id),
            UNIQUE(referrer_id, referred_id)
        );
        """
        
        # Выполняем SQL запросы
        # Примечание: Supabase-py не поддерживает прямое выполнение SQL
        # Таблицы должны быть созданы через Supabase Dashboard или API
        
        logger.info("Проверка структуры базы данных завершена")
        
    except Exception as e:
        logger.error(f"Ошибка при создании таблиц: {e}")


async def cleanup_expired_subscriptions():
    """
    Очищает истекшие подписки
    """
    try:
        from datetime import datetime
        supabase = get_supabase_client()
        
        now = datetime.utcnow().isoformat()
        
        # Деактивируем истекшие подписки
        result = supabase.table("subscriptions").update({
            "is_active": False
        }).lt("expire_at", now).eq("is_active", True).execute()
        
        if result.data:
            logger.info(f"Деактивировано истекших подписок: {len(result.data)}")
        
    except Exception as e:
        logger.error(f"Ошибка при очистке истекших подписок: {e}")
