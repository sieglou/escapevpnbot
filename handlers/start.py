"""
Обработчик команды /start и главного меню
"""

import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import get_main_menu_keyboard, get_back_keyboard
from models.user import create_or_get_user, get_user_subscription_info
from utils.helpers import format_subscription_info

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    """
    Обработчик команды /start
    Создает пользователя в БД и показывает главное меню
    """
    try:
        # Очищаем состояние FSM
        await state.clear()
        
        # Получаем или создаем пользователя
        user = await create_or_get_user(
            chat_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        
        # Получаем информацию о подписке
        subscription_info = await get_user_subscription_info(message.from_user.id)
        
        # Форматируем информацию о пользователе
        user_info = format_subscription_info(
            username=message.from_user.first_name or "Пользователь",
            subscription_info=subscription_info
        )
        
        # Получаем главное меню
        keyboard = get_main_menu_keyboard()
        
        await message.answer(
            text=user_info,
            reply_markup=keyboard
        )
        
        logger.info(f"Пользователь {message.from_user.id} запустил бота")
        
    except Exception as e:
        logger.error(f"Ошибка в start_command: {e}")
        await message.answer(
            "❌ Произошла ошибка при запуске бота. Попробуйте позже.",
            reply_markup=get_back_keyboard()
        )


@router.callback_query(F.data == "main_menu")
async def show_main_menu(callback: CallbackQuery, state: FSMContext):
    """
    Возврат к главному меню
    """
    try:
        # Очищаем состояние FSM
        await state.clear()
        
        # Получаем информацию о подписке
        subscription_info = await get_user_subscription_info(callback.from_user.id)
        
        # Форматируем информацию о пользователе
        user_info = format_subscription_info(
            username=callback.from_user.first_name or "Пользователь",
            subscription_info=subscription_info
        )
        
        # Получаем главное меню
        keyboard = get_main_menu_keyboard()
        
        await callback.message.edit_text(
            text=user_info,
            reply_markup=keyboard
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в show_main_menu: {e}")
        await callback.answer("❌ Произошла ошибка")


@router.callback_query(F.data == "about")
async def about_handler(callback: CallbackQuery):
    """
    Информация о YouVPN
    """
    try:
        about_text = """
🚀 <b>Об Escape!</b>

Escape! - это современный VPN-сервис, обеспечивающий:

🔒 <b>Безопасность</b>
• Шифрование военного уровня
• Защита от утечек DNS
• Kill Switch для максимальной безопасности

🌍 <b>Глобальное покрытие</b>
• Серверы в 50+ странах
• Высокая скорость соединения
• Без ограничений трафика

⚡ <b>Простота использования</b>
• Подключение в один клик
• Поддержка всех устройств
• 24/7 техническая поддержка

💎 <b>Премиум качество</b>
• Стабильная работа
• Регулярные обновления
• Гарантия возврата средств
        """
        
        keyboard = get_back_keyboard()
        
        await callback.message.edit_text(
            text=about_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в about_handler: {e}")
        await callback.answer("❌ Произошла ошибка")


@router.callback_query(F.data == "help")
async def help_handler(callback: CallbackQuery):
    """
    Помощь пользователю
    """
    try:
        help_text = """
❓ <b>Помощь</b>

<b>Часто задаваемые вопросы:</b>

<b>Q: Как подключиться к VPN?</b>
A: Нажмите кнопку "⚙️ Подключить VPN" и следуйте инструкциям.

<b>Q: Как продлить подписку?</b>
A: Используйте кнопку "💥 Продлить" в главном меню.

<b>Q: Как получить награду за приглашения?</b>
A: Пригласите друзей через кнопку "👥 Пригласить" и получите 100₽ за каждого.

<b>Q: Что делать если VPN не работает?</b>
A: Обратитесь в техподдержку через кнопку "❓ Помощь".

<b>Q: Есть ли ограничения по трафику?</b>
A: Нет, все тарифы предоставляют безлимитный трафик.

<b>💬 Техподдержка:</b>
Если у вас остались вопросы, обратитесь к нашей службе поддержки: @sicsemperproteus

Мы работаем 24/7 и всегда готовы помочь!
        """
        
        keyboard = get_back_keyboard()
        
        await callback.message.edit_text(
            text=help_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в help_handler: {e}")
        await callback.answer("❌ Произошла ошибка")


@router.callback_query(F.data == "reviews")
async def reviews_handler(callback: CallbackQuery):
    """
    Отзывы о сервисе
    """
    try:
        reviews_text = """
⭐ <b>Отзывы наших клиентов</b>

Мы ценим мнение каждого пользователя и постоянно работаем над улучшением сервиса.

📝 <b>Оставить отзыв:</b>
Поделитесь своим опытом использования YouVPN в нашем канале отзывов или напишите в поддержку.

🌟 <b>Ваше мнение важно!</b>
Все отзывы помогают нам становиться лучше и предоставлять еще более качественный сервис.

📞 <b>Связаться с нами:</b>
• Техподдержка: @youvpn_support
• Канал новостей: @youvpn_news
• Отзывы: @youvpn_reviews

Спасибо за выбор YouVPN! 🚀
        """
        
        keyboard = get_back_keyboard()
        
        await callback.message.edit_text(
            text=reviews_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в reviews_handler: {e}")
        await callback.answer("❌ Произошла ошибка")


@router.callback_query(F.data == "website")
async def website_handler(callback: CallbackQuery):
    """
    Информация о сайте
    """
    try:
        from config import config
        
        website_text = f"""
🌐 <b>Наш сайт</b>

Посетите наш официальный сайт для получения дополнительной информации:

🔗 <b>Сайт:</b> {config.WEBSITE_URL}

На сайте вы найдете:
• Подробную информацию о тарифах
• Инструкции по настройке
• Последние новости и обновления
• Техническую документацию

💻 <b>Веб-панель управления</b>
Через сайт также доступна веб-панель для управления вашей подпиской и настройками VPN.

📱 <b>Мобильные приложения</b>
Скачайте наши приложения для удобного использования VPN на всех ваших устройствах.
        """
        
        keyboard = get_back_keyboard()
        
        await callback.message.edit_text(
            text=website_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в website_handler: {e}")
        await callback.answer("❌ Произошла ошибка")
