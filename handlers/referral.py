"""
Обработчик реферальной системы
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import config
from keyboards.inline import get_back_keyboard
from models.user import get_user_referral_stats

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "invite")
async def invite_handler(callback: CallbackQuery):
    """
    Обработчик реферальной системы
    """
    try:
        # Получаем статистику рефералов пользователя
        referral_stats = await get_user_referral_stats(callback.from_user.id)
        
        # Формируем реферальную ссылку
        bot_username = callback.bot.me.username if hasattr(callback.bot, 'me') else "youvpn_bot"
        referral_link = f"https://t.me/{bot_username}?start=ref_{callback.from_user.id}"
        
        invite_text = f"""
👥 <b>Пригласить друзей</b>

💰 <b>Получай 100₽ за каждого приглашенного друга!</b>

📊 <b>Ваша статистика:</b>
• Приглашено друзей: {referral_stats.get('invited_count', 0)}
• Заработано: {referral_stats.get('earned_amount', 0)}₽
• Доступно к выводу: {referral_stats.get('available_balance', 0)}₽

🔗 <b>Ваша реферальная ссылка:</b>
<code>{referral_link}</code>

📋 <b>Как это работает:</b>
1️⃣ Поделитесь ссылкой с друзьями
2️⃣ Друг переходит по ссылке и регистрируется
3️⃣ Друг покупает подписку
4️⃣ Вы получаете {config.REFERRAL_REWARD_RUBLES}₽ на баланс

Совет: Расскажите друзьям о преимуществах Escape!:
• Безлимитный трафик
• Высокая скорость
• Серверы в 50+ странах
• 24/7 поддержка

💬 <b>Поделиться:</b>
Скопируйте ссылку выше и отправьте друзьям в любом мессенджере!
        """
        
        keyboard = get_back_keyboard()
        
        await callback.message.edit_text(
            text=invite_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в invite_handler: {e}")
        await callback.answer("❌ Произошла ошибка")
