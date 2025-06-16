"""
Конфигурация бота
Содержит все настройки и переменные окружения
"""

import os
from typing import Optional


class Config:
    """
    Класс конфигурации для бота
    """
    
    def __init__(self):
        # Токен бота Telegram
        self.BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не найден в переменных окружения")
        
        # Настройки Supabase
        self.SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
        self.SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
        if not self.SUPABASE_URL or not self.SUPABASE_KEY:
            raise ValueError("SUPABASE_URL или SUPABASE_KEY не найдены в переменных окружения")
        
        # Токен для Telegram Payments
        self.PAYMENT_TOKEN: str = os.getenv("PAYMENT_TOKEN", "")
        if not self.PAYMENT_TOKEN:
            raise ValueError("PAYMENT_TOKEN не найден в переменных окружения")
        
        # Настройки подписок
        self.SUBSCRIPTION_PRICES = {
            "1_month": {"price": 500, "title": "1 месяц (Премиум)", "days": 30},
            "3_months": {"price": 1200, "title": "3 месяца (Премиум)", "days": 90},
            "6_months": {"price": 2000, "title": "6 месяцев (Премиум)", "days": 180},
            "12_months": {"price": 3500, "title": "12 месяцев (Премиум)", "days": 365}
        }
        
        # Реферальные награды
        self.REFERRAL_REWARD_RUBLES = 100  # 100 рублей за каждого приглашенного
        
        # URL сайта
        self.WEBSITE_URL: str = os.getenv("WEBSITE_URL", "https://youvpn.com")
        
        # Информация о поддержке
        self.SUPPORT_USERNAME: str = os.getenv("SUPPORT_USERNAME", "@youvpn_support")
        
        # Валюта для платежей (рубли)
        self.CURRENCY = "RUB"


# Глобальный экземпляр конфигурации
config = Config()
