"""
Состояния FSM для платежей
"""

from aiogram.fsm.state import State, StatesGroup


class PaymentStates(StatesGroup):
    """
    Состояния для процесса оплаты
    """
    waiting_for_payment = State()  # Ожидание оплаты
    processing_payment = State()   # Обработка платежа
    payment_completed = State()    # Платеж завершен
    payment_failed = State()       # Платеж неуспешен


class ReferralStates(StatesGroup):
    """
    Состояния для реферальной системы
    """
    sharing_referral_link = State()    # Отправка реферальной ссылки
    processing_referral = State()      # Обработка реферала
    referral_completed = State()       # Реферал обработан


class SupportStates(StatesGroup):
    """
    Состояния для системы поддержки
    """
    waiting_for_message = State()      # Ожидание сообщения
    message_sent = State()             # Сообщение отправлено
