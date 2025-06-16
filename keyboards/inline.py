"""
Инлайн-клавиатуры для бота
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import config


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Главное меню бота (соответствует дизайну из скриншота)
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⚙️ Подключить VPN",
                callback_data="connect_vpn"
            )
        ],
        [
            InlineKeyboardButton(
                text="💥 Продлить",
                callback_data="extend"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Пригласить",
                callback_data="invite"
            )
        ],
        [
            InlineKeyboardButton(
                text="🚀 о YouVPN",
                callback_data="about"
            )
        ],
        [
            InlineKeyboardButton(
                text="❓ Помощь",
                callback_data="help"
            )
        ],
        [
            InlineKeyboardButton(
                text="⭐ Отзывы",
                callback_data="reviews"
            )
        ],
        [
            InlineKeyboardButton(
                text="💻 Наш сайт",
                callback_data="website"
            )
        ]
    ])
    return keyboard


def get_subscription_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура выбора подписки
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"💎 1 месяц - {config.SUBSCRIPTION_PRICES['1_month']['price']}₽",
                callback_data="buy_1_month"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"💎 3 месяца - {config.SUBSCRIPTION_PRICES['3_months']['price']}₽ (скидка 20%)",
                callback_data="buy_3_months"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"💎 6 месяцев - {config.SUBSCRIPTION_PRICES['6_months']['price']}₽ (скидка 33%)",
                callback_data="buy_6_months"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"💎 12 месяцев - {config.SUBSCRIPTION_PRICES['12_months']['price']}₽ (скидка 42%)",
                callback_data="buy_12_months"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="back"
            )
        ]
    ])
    return keyboard


def get_back_keyboard() -> InlineKeyboardMarkup:
    """
    Простая клавиатура с кнопкой "Назад"
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="main_menu"
            )
        ]
    ])
    return keyboard


def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой отмены
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="❌ Отменить",
                callback_data="cancel"
            )
        ]
    ])
    return keyboard


def get_payment_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для платежей
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💳 Оплатить",
                pay=True
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Отменить",
                callback_data="cancel"
            )
        ]
    ])
    return keyboard
