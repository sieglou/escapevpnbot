"""
Система уведомлений
"""

import logging
import asyncio
from datetime import datetime, timedelta
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from keyboards.inline import get_main_menu_keyboard
from models.subscription import get_expiring_subscriptions
from models.user import add_referral_reward
from config import config

logger = logging.getLogger(__name__)


async def send_payment_success_notification(bot: Bot, user_id: int, 
                                          subscription_type: str, expire_at: datetime):
    """
    Отправляет уведомление об успешной оплате
    """
    try:
        days = config.SUBSCRIPTION_PRICES[subscription_type]["days"]
        price = config.SUBSCRIPTION_PRICES[subscription_type]["price"]
        
        success_text = f"""
✅ <b>Платеж успешно обработан!</b>

💎 <b>Подписка активирована:</b>
• Тариф: {config.SUBSCRIPTION_PRICES[subscription_type]["title"]}
• Сумма: {price}₽
• Действует до: {expire_at.strftime("%d.%m.%Y %H:%M")}
• Дней: {days}

🚀 <b>Что дальше?</b>
• Нажмите "Подключить VPN" для получения инструкций
• Скачайте приложение YouVPN
• Войдите используя ваш Telegram ID: <code>{user_id}</code>

Спасибо за выбор YouVPN! 🎉
        """
        
        keyboard = get_main_menu_keyboard()
        
        await bot.send_message(
            chat_id=user_id,
            text=success_text,
            reply_markup=keyboard
        )
        
        logger.info(f"Отправлено уведомление об успешной оплате пользователю {user_id}")
        
    except TelegramForbiddenError:
        logger.warning(f"Пользователь {user_id} заблокировал бота")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления об оплате пользователю {user_id}: {e}")


async def send_subscription_expiry_warning(bot: Bot, user_id: int, days_left: int):
    """
    Отправляет предупреждение об истечении подписки
    """
    try:
        if days_left == 1:
            warning_text = """
⚠️ <b>Внимание! Подписка истекает завтра!</b>

Ваша подписка YouVPN истекает завтра. 

Чтобы не потерять доступ к VPN:
• Нажмите "Продлить" в меню
• Выберите подходящий тариф
• Оплатите подписку

💡 <b>Совет:</b> Выберите годовую подписку и сэкономьте до 42%!
            """
        elif days_left <= 3:
            warning_text = f"""
⚠️ <b>Подписка истекает через {days_left} дня!</b>

Ваша подписка YouVPN скоро истечет.

Продлите подписку заранее, чтобы избежать перерывов в работе VPN.

💰 <b>Специальное предложение:</b> При продлении на год скидка до 42%!
            """
        else:
            return  # Не отправляем уведомления за более чем 3 дня
        
        keyboard = get_main_menu_keyboard()
        
        await bot.send_message(
            chat_id=user_id,
            text=warning_text,
            reply_markup=keyboard
        )
        
        logger.info(f"Отправлено предупреждение об истечении подписки пользователю {user_id}")
        
    except TelegramForbiddenError:
        logger.warning(f"Пользователь {user_id} заблокировал бота")
    except Exception as e:
        logger.error(f"Ошибка при отправке предупреждения пользователю {user_id}: {e}")


async def send_referral_reward_notification(bot: Bot, user_id: int, 
                                          referred_user_name: str, reward_amount: float):
    """
    Отправляет уведомление о реферальной награде
    """
    try:
        # Добавляем награду на баланс
        success = await add_referral_reward(user_id, reward_amount)
        
        if success:
            reward_text = f"""
🎉 <b>Поздравляем! Вы получили реферальную награду!</b>

👤 <b>Приглашенный пользователь:</b> {referred_user_name}
💰 <b>Ваша награда:</b> {reward_amount}₽

Награда добавлена на ваш реферальный баланс.

💡 <b>Продолжайте приглашать друзей и зарабатывать!</b>
Каждый приглашенный друг = {config.REFERRAL_REWARD_RUBLES}₽ на ваш счет.

Нажмите "Пригласить" чтобы получить вашу реферальную ссылку.
            """
            
            keyboard = get_main_menu_keyboard()
            
            await bot.send_message(
                chat_id=user_id,
                text=reward_text,
                reply_markup=keyboard
            )
            
            logger.info(f"Отправлено уведомление о реферальной награде пользователю {user_id}")
        
    except TelegramForbiddenError:
        logger.warning(f"Пользователь {user_id} заблокировал бота")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления о награде пользователю {user_id}: {e}")


async def check_expiring_subscriptions_task(bot: Bot):
    """
    Периодическая задача проверки истекающих подписок
    """
    try:
        # Получаем подписки, истекающие в ближайшие 3 дня
        expiring_subscriptions = await get_expiring_subscriptions(days_before=3)
        
        for subscription in expiring_subscriptions:
            user_id = subscription["users"]["chat_id"]
            expire_at = datetime.fromisoformat(subscription["expire_at"].replace("Z", "+00:00"))
            now = datetime.utcnow().replace(tzinfo=expire_at.tzinfo)
            
            days_left = (expire_at - now).days
            
            if days_left <= 3 and days_left > 0:
                await send_subscription_expiry_warning(bot, user_id, days_left)
                
                # Ждем немного между отправками, чтобы не перегружать API
                await asyncio.sleep(0.1)
        
        logger.info(f"Проверка истекающих подписок завершена. Найдено: {len(expiring_subscriptions)}")
        
    except Exception as e:
        logger.error(f"Ошибка при проверке истекающих подписок: {e}")


async def start_notification_scheduler(bot: Bot):
    """
    Запускает планировщик уведомлений
    """
    logger.info("Запуск планировщика уведомлений")
    
    while True:
        try:
            # Проверяем истекающие подписки каждые 12 часов
            await check_expiring_subscriptions_task(bot)
            
            # Ждем 12 часов до следующей проверки
            await asyncio.sleep(12 * 60 * 60)  # 12 часов в секундах
            
        except Exception as e:
            logger.error(f"Ошибка в планировщике уведомлений: {e}")
            # Если произошла ошибка, ждем 1 час и пробуем снова
            await asyncio.sleep(60 * 60)
