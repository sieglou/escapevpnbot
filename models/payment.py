"""
Модель платежей
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any
from utils.database import get_supabase_client

logger = logging.getLogger(__name__)


async def create_payment_record(user_id: int, amount: float, currency: str,
                               telegram_payment_charge_id: str, 
                               provider_payment_charge_id: str,
                               subscription_type: str) -> Dict[str, Any]:
    """
    Создает запись о платеже в базе данных
    """
    try:
        supabase = get_supabase_client()
        
        payment_data = {
            "user_id": user_id,
            "amount": amount,
            "currency": currency,
            "telegram_payment_charge_id": telegram_payment_charge_id,
            "provider_payment_charge_id": provider_payment_charge_id,
            "subscription_type": subscription_type,
            "status": "completed",
            "created_at": datetime.utcnow().isoformat()
        }
        
        result = supabase.table("payments").insert(payment_data).execute()
        
        if result.data:
            logger.info(f"Создана запись о платеже: пользователь {user_id}, сумма {amount} {currency}")
            return result.data[0]
        else:
            raise Exception("Не удалось создать запись о платеже")
            
    except Exception as e:
        logger.error(f"Ошибка при создании записи о платеже для {user_id}: {e}")
        raise


async def get_user_payments(user_id: int, limit: int = 10) -> list:
    """
    Получает историю платежей пользователя
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("payments").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()
        
        return result.data if result.data else []
        
    except Exception as e:
        logger.error(f"Ошибка при получении платежей пользователя {user_id}: {e}")
        return []


async def get_payment_by_charge_id(telegram_payment_charge_id: str) -> Optional[Dict[str, Any]]:
    """
    Получает платеж по Telegram charge ID
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("payments").select("*").eq("telegram_payment_charge_id", telegram_payment_charge_id).execute()
        
        return result.data[0] if result.data else None
        
    except Exception as e:
        logger.error(f"Ошибка при получении платежа по charge_id {telegram_payment_charge_id}: {e}")
        return None


async def get_total_revenue() -> float:
    """
    Получает общую выручку
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("payments").select("amount").eq("status", "completed").execute()
        
        total = sum(payment["amount"] for payment in result.data) if result.data else 0
        return total
        
    except Exception as e:
        logger.error(f"Ошибка при получении общей выручки: {e}")
        return 0


async def get_payments_by_period(start_date: datetime, end_date: datetime) -> list:
    """
    Получает платежи за определенный период
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("payments").select("*").gte("created_at", start_date.isoformat()).lte("created_at", end_date.isoformat()).eq("status", "completed").execute()
        
        return result.data if result.data else []
        
    except Exception as e:
        logger.error(f"Ошибка при получении платежей за период {start_date} - {end_date}: {e}")
        return []
