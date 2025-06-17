"""
Обработчик платежей и подписок
"""

import logging
from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, PreCheckoutQuery, LabeledPrice
from aiogram.fsm.context import FSMContext

from config import config
from keyboards.inline import get_subscription_keyboard, get_back_keyboard
from models.subscription import create_or_update_subscription, get_user_subscription
from models.payment import create_payment_record
from states.payment import PaymentStates
from utils.notifications import send_payment_success_notification

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "connect_vpn")
async def connect_vpn_handler(callback: CallbackQuery):
    """
    Обработчик подключения VPN
    """
    try:
        # Проверяем активную подписку пользователя
        subscription = await get_user_subscription(callback.from_user.id)
        
        if subscription and subscription.get('is_active'):
            # У пользователя есть активная подписка
            vpn_text = """
Подключение к VPN

У вас активная подписка.

Инструкция по подключению:

1. Скачайте приложение Escape!
2. Войдите в аккаунт используя ваш Telegram ID
3. Выберите сервер и нажмите "Подключиться"

Приложения:
• iOS: App Store → Escape!
• Android: Google Play → Escape!  
• Windows: escape.ct.ws/download
• macOS: escape.ct.ws/download

Настройки подключения:
• Ваш ID: <code>{user_id}</code>
• Протокол: WireGuard/OpenVPN
• Автоподключение: Включено

Нужна помощь? Обратитесь в поддержку: @sicsemperproteus
            """.format(user_id=callback.from_user.id)
        else:
            # У пользователя нет активной подписки - показываем выбор тарифов
            vpn_text = """
Подключение к VPN

У вас нет активной подписки.

Выберите тариф для получения доступа:

Что включено:
• Безлимитный трафик
• Высокая скорость
• Серверы в 50+ странах
• Круглосуточная поддержка

Выберите подходящий тариф:
            """
        
        keyboard = get_subscription_keyboard()
        
        await callback.message.edit_text(
            text=vpn_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в connect_vpn_handler: {e}")
        await callback.answer("❌ Произошла ошибка")


@router.callback_query(F.data == "extend")
async def extend_subscription_handler(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик продления подписки
    """
    try:
        extend_text = """
Покупка подписки

Выберите подходящий тариф:

Все тарифы включают:
• Безлимитный трафик
• Высокая скорость (до 1 Гбит/с)
• Серверы в 50+ странах мира
• Поддержка всех устройств
• Техническая поддержка 24/7
• Гарантия возврата средств

Рекомендуем: 12 месяцев - самая выгодная цена.
        """
        
        keyboard = get_subscription_keyboard()
        
        await callback.message.edit_text(
            text=extend_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в extend_subscription_handler: {e}")
        await callback.answer("❌ Произошла ошибка")


@router.callback_query(F.data.startswith("buy_"))
async def buy_subscription_handler(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик покупки подписки
    """
    try:
        # Извлекаем тип подписки из callback_data
        subscription_type = callback.data.replace("buy_", "")
        
        if subscription_type not in config.SUBSCRIPTION_PRICES:
            await callback.answer("❌ Неверный тип подписки")
            return
        
        # Получаем информацию о тарифе
        price_info = config.SUBSCRIPTION_PRICES[subscription_type]
        
        # Сохраняем тип подписки в состоянии
        await state.update_data(subscription_type=subscription_type)
        await state.set_state(PaymentStates.waiting_for_payment)
        
        if config.USE_TELEGRAM_STARS:
            # Для Telegram Stars используем другой подход
            await callback.message.answer_invoice(
                title=f"YouVPN - {price_info['title']}",
                description=f"Подписка YouVPN на {price_info['days']} дней\n"
                           f"Безлимитный трафик, высокая скорость, серверы в 50+ странах",
                payload=f"subscription_{subscription_type}_{callback.from_user.id}",
                currency="XTR",  # Telegram Stars
                prices=[LabeledPrice(label=price_info["title"], amount=price_info["price"])],
                start_parameter="subscription"
            )
        else:
            # Обычные платежи через провайдера
            prices = [
                LabeledPrice(
                    label=price_info["title"],
                    amount=price_info["price"] * 100  # Telegram требует сумму в копейках
                )
            ]
            
            await callback.message.answer_invoice(
                title=f"YouVPN - {price_info['title']}",
                description=f"Подписка YouVPN на {price_info['days']} дней\n"
                           f"Безлимитный трафик, высокая скорость, серверы в 50+ странах",
                provider_token=config.PAYMENT_TOKEN,
                currency=config.CURRENCY,
                prices=prices,
                start_parameter="subscription",
                payload=f"subscription_{subscription_type}_{callback.from_user.id}"
            )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в buy_subscription_handler: {e}")
        await callback.answer("❌ Произошла ошибка при создании счета")


@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    """
    Обработчик предварительной проверки платежа
    """
    try:
        # Валидируем payload
        payload = pre_checkout_query.invoice_payload
        if not payload.startswith("subscription_"):
            await pre_checkout_query.answer(ok=False, error_message="Неверный payload платежа")
            return
        
        # Извлекаем информацию из payload
        parts = payload.split("_")
        if len(parts) != 3:
            await pre_checkout_query.answer(ok=False, error_message="Неверный формат payload")
            return
        
        subscription_type = parts[1]
        user_id = int(parts[2])
        
        # Проверяем валидность типа подписки
        if subscription_type not in config.SUBSCRIPTION_PRICES:
            await pre_checkout_query.answer(ok=False, error_message="Неверный тип подписки")
            return
        
        # Проверяем соответствие суммы
        if config.USE_TELEGRAM_STARS:
            expected_amount = config.SUBSCRIPTION_PRICES[subscription_type]["price"]
        else:
            expected_amount = config.SUBSCRIPTION_PRICES[subscription_type]["price"] * 100
            
        if pre_checkout_query.total_amount != expected_amount:
            await pre_checkout_query.answer(ok=False, error_message="Неверная сумма платежа")
            return
        
        # Все проверки пройдены
        await pre_checkout_query.answer(ok=True)
        
        logger.info(f"Pre-checkout OK для пользователя {user_id}, тип: {subscription_type}")
        
    except Exception as e:
        logger.error(f"Ошибка в pre_checkout_handler: {e}")
        await pre_checkout_query.answer(ok=False, error_message="Внутренняя ошибка сервера")


@router.message(F.successful_payment)
async def successful_payment_handler(message: Message, state: FSMContext):
    """
    Обработчик успешного платежа
    """
    try:
        payment = message.successful_payment
        payload = payment.invoice_payload
        
        # Извлекаем информацию из payload
        parts = payload.split("_")
        subscription_type = parts[1]
        user_id = int(parts[2])
        
        # Получаем информацию о подписке
        price_info = config.SUBSCRIPTION_PRICES[subscription_type]
        
        # Вычисляем дату окончания подписки
        now = datetime.utcnow()
        expire_at = now + timedelta(days=price_info["days"])
        
        # Создаем или обновляем подписку
        await create_or_update_subscription(
            user_id=user_id,
            subscription_type="premium",
            expire_at=expire_at,
            is_active=True
        )
        
        # Записываем информацию о платеже
        if config.USE_TELEGRAM_STARS:
            amount = payment.total_amount  # Stars уже в правильном формате
        else:
            amount = payment.total_amount / 100  # Переводим из копеек в рубли
            
        await create_payment_record(
            user_id=user_id,
            amount=amount,
            currency=payment.currency,
            telegram_payment_charge_id=payment.telegram_payment_charge_id,
            provider_payment_charge_id=payment.provider_payment_charge_id or "",
            subscription_type=subscription_type
        )
        
        # Очищаем состояние
        await state.clear()
        
        # Отправляем уведомление об успешном платеже
        await send_payment_success_notification(
            bot=message.bot,
            user_id=user_id,
            subscription_type=subscription_type,
            expire_at=expire_at
        )
        
        logger.info(f"Успешный платеж: пользователь {user_id}, тип {subscription_type}, сумма {payment.total_amount/100}")
        
    except Exception as e:
        logger.error(f"Ошибка в successful_payment_handler: {e}")
        await message.answer("❌ Произошла ошибка при обработке платежа. Обратитесь в поддержку.")
