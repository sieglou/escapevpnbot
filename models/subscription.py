"""
Модель подписки
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any
from utils.database import get_supabase_client

logger = logging.getLogger(__name__)


async def create_or_update_subscription(user_id: int, subscription_type: str, 
                                      expire_at: datetime, is_active: bool = True) -> Dict[str, Any]:
    """
    Создает новую подписку или обновляет существующую
    """
    try:
        supabase = get_supabase_client()
        
        # Деактивируем все предыдущие подписки пользователя
        supabase.table("subscriptions").update({"is_active": False}).eq("user_id", user_id).execute()
        
        # Создаем новую подписку
        subscription_data = {
            "user_id": user_id,
            "subscription_type": subscription_type,
            "expire_at": expire_at.isoformat(),
            "is_active": is_active,
            "created_at": datetime.utcnow().isoformat()
        }
        
        result = supabase.table("subscriptions").insert(subscription_data).execute()
        
        if result.data:
            logger.info(f"Создана подписка для пользователя {user_id}: {subscription_type} до {expire_at}")
            return result.data[0]
        else:
            raise Exception("Не удалось создать подписку")
            
    except Exception as e:
        logger.error(f"Ошибка при создании/обновлении подписки для {user_id}: {e}")
        raise


async def get_user_subscription(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Получает активную подписку пользователя
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("subscriptions").select("*").eq("user_id", user_id).eq("is_active", True).execute()
        
        if result.data:
            subscription = result.data[0]
            
            # Проверяем, не истекла ли подписка
            expire_at = datetime.fromisoformat(subscription["expire_at"].replace("Z", "+00:00"))
            now = datetime.utcnow().replace(tzinfo=expire_at.tzinfo)
            
            if expire_at > now:
                return subscription
            else:
                # Подписка истекла, деактивируем
                await deactivate_subscription(subscription["id"])
                return None
        
        return None
        
    except Exception as e:
        logger.error(f"Ошибка при получении подписки для {user_id}: {e}")
        return None


async def deactivate_subscription(subscription_id: int) -> bool:
    """
    Деактивирует подписку
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("subscriptions").update({"is_active": False}).eq("id", subscription_id).execute()
        
        return bool(result.data)
        
    except Exception as e:
        logger.error(f"Ошибка при деактивации подписки {subscription_id}: {e}")
        return False


async def get_expiring_subscriptions(days_before: int = 3) -> list:
    """
    Получает подписки, которые истекают в ближайшие дни
    """
    try:
        supabase = get_supabase_client()
        
        # Вычисляем дату, до которой ищем истекающие подписки
        from datetime import timedelta
        target_date = datetime.utcnow() + timedelta(days=days_before)
        
        result = supabase.table("subscriptions").select("*, users(chat_id, first_name)").eq("is_active", True).lt("expire_at", target_date.isoformat()).execute()
        
        return result.data if result.data else []
        
    except Exception as e:
        logger.error(f"Ошибка при получении истекающих подписок: {e}")
        return []


async def extend_subscription(user_id: int, days: int) -> bool:
    """
    Продлевает существующую подписку на указанное количество дней
    """
    try:
        supabase = get_supabase_client()
        
        # Получаем активную подписку
        subscription = await get_user_subscription(user_id)
        
        if subscription:
            # Продлеваем существующую подписку
            expire_at = datetime.fromisoformat(subscription["expire_at"].replace("Z", "+00:00"))
            new_expire_at = expire_at + timedelta(days=days)
            
            supabase.table("subscriptions").update({
                "expire_at": new_expire_at.isoformat()
            }).eq("id", subscription["id"]).execute()
            
            return True
        else:
            # Нет активной подписки, создаем новую
            from datetime import timedelta
            expire_at = datetime.utcnow() + timedelta(days=days)
            
            await create_or_update_subscription(
                user_id=user_id,
                subscription_type="premium",
                expire_at=expire_at
            )
            
            return True
        
    except Exception as e:
        logger.error(f"Ошибка при продлении подписки для {user_id}: {e}")
        return False
