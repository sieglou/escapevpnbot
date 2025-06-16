"""
Модель пользователя
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any
from utils.database import get_supabase_client

logger = logging.getLogger(__name__)


async def create_or_get_user(chat_id: int, username: Optional[str] = None, 
                           first_name: Optional[str] = None, 
                           last_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Создает нового пользователя или возвращает существующего
    """
    try:
        supabase = get_supabase_client()
        
        # Проверяем, существует ли пользователь
        result = supabase.table("users").select("*").eq("chat_id", chat_id).execute()
        
        if result.data:
            # Пользователь существует, обновляем информацию
            user_data = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "last_activity": datetime.utcnow().isoformat()
            }
            
            updated_result = supabase.table("users").update(user_data).eq("chat_id", chat_id).execute()
            return updated_result.data[0] if updated_result.data else result.data[0]
        else:
            # Создаем нового пользователя
            user_data = {
                "chat_id": chat_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "created_at": datetime.utcnow().isoformat(),
                "last_activity": datetime.utcnow().isoformat(),
                "referral_balance": 0,
                "invited_count": 0
            }
            
            new_result = supabase.table("users").insert(user_data).execute()
            return new_result.data[0] if new_result.data else user_data
            
    except Exception as e:
        logger.error(f"Ошибка при создании/получении пользователя {chat_id}: {e}")
        raise


async def get_user_subscription_info(chat_id: int) -> Optional[Dict[str, Any]]:
    """
    Получает информацию о подписке пользователя
    """
    try:
        supabase = get_supabase_client()
        
        # Получаем активную подписку пользователя
        result = supabase.table("subscriptions").select("*").eq("user_id", chat_id).eq("is_active", True).execute()
        
        if result.data:
            subscription = result.data[0]
            
            # Проверяем, не истекла ли подписка
            expire_at = datetime.fromisoformat(subscription["expire_at"].replace("Z", "+00:00"))
            now = datetime.utcnow().replace(tzinfo=expire_at.tzinfo)
            
            if expire_at > now:
                # Подписка активна
                days_left = (expire_at - now).days
                return {
                    "is_active": True,
                    "subscription_type": subscription["subscription_type"],
                    "expire_at": expire_at,
                    "days_left": days_left
                }
            else:
                # Подписка истекла, деактивируем
                supabase.table("subscriptions").update({"is_active": False}).eq("id", subscription["id"]).execute()
                return {
                    "is_active": False,
                    "subscription_type": None,
                    "expire_at": None,
                    "days_left": 0
                }
        else:
            # Нет активной подписки
            return {
                "is_active": False,
                "subscription_type": None,
                "expire_at": None,
                "days_left": 0
            }
            
    except Exception as e:
        logger.error(f"Ошибка при получении информации о подписке для {chat_id}: {e}")
        return {
            "is_active": False,
            "subscription_type": None,
            "expire_at": None,
            "days_left": 0
        }


async def get_user_referral_stats(chat_id: int) -> Dict[str, Any]:
    """
    Получает статистику рефералов пользователя
    """
    try:
        supabase = get_supabase_client()
        
        # Получаем пользователя
        result = supabase.table("users").select("referral_balance, invited_count").eq("chat_id", chat_id).execute()
        
        if result.data:
            user_data = result.data[0]
            return {
                "invited_count": user_data.get("invited_count", 0),
                "earned_amount": user_data.get("referral_balance", 0),
                "available_balance": user_data.get("referral_balance", 0)
            }
        else:
            return {
                "invited_count": 0,
                "earned_amount": 0,
                "available_balance": 0
            }
            
    except Exception as e:
        logger.error(f"Ошибка при получении статистики рефералов для {chat_id}: {e}")
        return {
            "invited_count": 0,
            "earned_amount": 0,
            "available_balance": 0
        }


async def process_referral(referred_user_id: int, referrer_user_id: int) -> bool:
    """
    Обрабатывает реферальное приглашение
    """
    try:
        from config import config
        supabase = get_supabase_client()
        
        # Проверяем, что пользователь не приглашал сам себя
        if referred_user_id == referrer_user_id:
            return False
        
        # Проверяем, что пользователь еще не был приглашен
        result = supabase.table("users").select("referred_by").eq("chat_id", referred_user_id).execute()
        
        if result.data and result.data[0].get("referred_by"):
            # Пользователь уже был приглашен
            return False
        
        # Обновляем информацию о реферале
        supabase.table("users").update({"referred_by": referrer_user_id}).eq("chat_id", referred_user_id).execute()
        
        # Увеличиваем счетчик приглашений у реферера
        supabase.table("users").update({
            "invited_count": supabase.rpc("increment_invited_count", {"user_chat_id": referrer_user_id})
        }).eq("chat_id", referrer_user_id).execute()
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при обработке реферала {referred_user_id} -> {referrer_user_id}: {e}")
        return False


async def add_referral_reward(user_id: int, amount: float) -> bool:
    """
    Добавляет реферальную награду пользователю
    """
    try:
        supabase = get_supabase_client()
        
        # Получаем текущий баланс
        result = supabase.table("users").select("referral_balance").eq("chat_id", user_id).execute()
        
        if result.data:
            current_balance = result.data[0].get("referral_balance", 0)
            new_balance = current_balance + amount
            
            # Обновляем баланс
            supabase.table("users").update({"referral_balance": new_balance}).eq("chat_id", user_id).execute()
            
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"Ошибка при добавлении реферальной награды пользователю {user_id}: {e}")
        return False
