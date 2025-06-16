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
        # Импортируем здесь для избежания циклических импортов
        from handlers.start import show_main_menu
        await show_main_menu(callback, None)
        
    except Exception as e:
        logger.error(f"Ошибка в back_handler: {e}")
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
