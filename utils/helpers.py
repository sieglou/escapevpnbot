"""
Вспомогательные функции
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def format_subscription_info(username: str, subscription_info: Dict[str, Any]) -> str:
    """
    Форматирует информацию о подписке пользователя для отображения
    """
    try:
        # Базовая информация
        header = f"Аккаунт: {username}\n\n"
        
        if subscription_info.get("is_active"):
            # Активная подписка
            expire_date = subscription_info.get("expire_at")
            days_left = subscription_info.get("days_left", 0)
            
            if expire_date:
                formatted_date = expire_date.strftime("%d.%m.%Y %H:%M")
            else:
                formatted_date = "Неизвестно"
            
            status_text = f"""Статус: Активен
Подписка до: {formatted_date}
Осталось дней: {days_left}
Тариф: Премиум"""
            
            # Дополнительная информация в зависимости от количества дней
            if days_left <= 1:
                status_text += "\n\nВНИМАНИЕ: Подписка истекает завтра! Продлите сейчас."
            elif days_left <= 3:
                status_text += f"\n\nВНИМАНИЕ: Подписка истекает через {days_left} дня. Рекомендуем продлить."
            
        else:
            # Неактивная подписка
            status_text = """Статус: Неактивен
Осталось дней: 0
Тариф: Нет активной подписки

Оформите подписку для доступа к VPN."""
        
        # Дополнительная информация
        footer = """

Выберите действие:

💎 <b>Получай 100₽ за каждого приглашенного друга. Подробнее по кнопке "Пригласить"</b>

❓ <b>Наша поддержка работает 24/7. Если у Вас возникнут вопросы, переходите по кнопке "Помощь"</b>"""
        
        return header + status_text + footer
        
    except Exception as e:
        logger.error(f"Ошибка при форматировании информации о подписке: {e}")
        return f"👑 <b>{username}, Ваш аккаунт:</b>\n\n❌ Ошибка загрузки данных"


def format_currency(amount: float, currency: str = "₽") -> str:
    """
    Форматирует сумму с валютой
    """
    return f"{amount:.0f}{currency}"


def calculate_subscription_savings(base_monthly_price: float, total_price: float, months: int) -> float:
    """
    Вычисляет размер скидки при покупке длительной подписки
    """
    full_price = base_monthly_price * months
    savings = full_price - total_price
    return max(0, savings)


def calculate_discount_percentage(original_price: float, discounted_price: float) -> int:
    """
    Вычисляет процент скидки
    """
    if original_price <= 0:
        return 0
    
    discount = (original_price - discounted_price) / original_price * 100
    return max(0, int(discount))


def format_datetime(dt: datetime, format_string: str = "%d.%m.%Y %H:%M") -> str:
    """
    Форматирует дату и время
    """
    try:
        return dt.strftime(format_string)
    except Exception as e:
        logger.error(f"Ошибка при форматировании даты {dt}: {e}")
        return "Неизвестно"


def validate_user_input(text: str, max_length: int = 100) -> bool:
    """
    Валидирует пользовательский ввод
    """
    if not text or not isinstance(text, str):
        return False
    
    if len(text.strip()) == 0 or len(text) > max_length:
        return False
    
    return True


def extract_referral_code(start_param: Optional[str]) -> Optional[int]:
    """
    Извлекает ID реферера из параметра start команды
    """
    try:
        if not start_param or not start_param.startswith("ref_"):
            return None
        
        referrer_id = int(start_param.replace("ref_", ""))
        return referrer_id if referrer_id > 0 else None
        
    except (ValueError, AttributeError):
        return None


def sanitize_text(text: str) -> str:
    """
    Очищает текст от потенциально опасных символов
    """
    if not text:
        return ""
    
    # Удаляем HTML теги для безопасности
    import re
    clean_text = re.sub(r'<[^>]+>', '', text)
    
    # Ограничиваем длину
    return clean_text[:1000] if clean_text else ""


def is_valid_chat_id(chat_id: Any) -> bool:
    """
    Проверяет валидность chat_id
    """
    try:
        chat_id_int = int(chat_id)
        # Telegram chat_id для пользователей обычно положительные числа
        return chat_id_int > 0
    except (ValueError, TypeError):
        return False


def format_user_mention(first_name: Optional[str], username: Optional[str] = None) -> str:
    """
    Форматирует упоминание пользователя
    """
    if first_name:
        name = first_name.strip()
        if len(name) > 20:
            name = name[:20] + "..."
        return name
    elif username:
        return f"@{username}"
    else:
        return "Пользователь"
