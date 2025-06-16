"""
Обработчики меню и навигации
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline import get_back_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery):
    """
    Универсальный обработчик кнопки "Назад"
    Перенаправляет к главному меню
    """
    try:
        from models.user import get_user_subscription_info
        from utils.helpers import format_subscription_info
        from keyboards.inline import get_main_menu_keyboard
        
        # Получаем информацию о подписке
        subscription_info = await get_user_subscription_info(callback.from_user.id)
        
        # Форматируем информацию о пользователе
        user_info = format_subscription_info(
            username=callback.from_user.first_name or "Пользователь",
            subscription_info=subscription_info or {}
        )
        
        # Получаем главное меню
        keyboard = get_main_menu_keyboard()
        
        await callback.message.edit_text(
            text=user_info,
            reply_markup=keyboard
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в back_handler: {e}")
        await callback.answer("❌ Произошла ошибка")


@router.callback_query(F.data == "main_menu")
async def main_menu_handler(callback: CallbackQuery):
    """
    Обработчик возврата в главное меню (для get_back_keyboard)
    """
    try:
        from models.user import get_user_subscription_info
        from utils.helpers import format_subscription_info
        from keyboards.inline import get_main_menu_keyboard
        
        # Получаем информацию о подписке
        subscription_info = await get_user_subscription_info(callback.from_user.id)
        
        # Форматируем информацию о пользователе
        user_info = format_subscription_info(
            username=callback.from_user.first_name or "Пользователь",
            subscription_info=subscription_info or {}
        )
        
        # Получаем главное меню
        keyboard = get_main_menu_keyboard()
        
        await callback.message.edit_text(
            text=user_info,
            reply_markup=keyboard
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в main_menu_handler: {e}")
        await callback.answer("❌ Произошла ошибка")


@router.callback_query(F.data == "cancel")
async def cancel_handler(callback: CallbackQuery):
    """
    Обработчик отмены операции
    """
    try:
        await callback.message.edit_text(
            "❌ Операция отменена",
            reply_markup=get_back_keyboard()
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в cancel_handler: {e}")
        await callback.answer("❌ Произошла ошибка")
