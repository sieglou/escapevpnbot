"""
Telegram VPN Bot с платными подписками
Главная точка входа приложения
"""

import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config
from handlers import start, payments, menu, referral
from utils.database import init_database
from utils.notifications import start_notification_scheduler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """
    Основная функция для запуска бота
    """
    # Инициализация конфигурации
    config = Config()
    
    # Создание экземпляра бота
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Создание диспетчера с хранилищем состояний
    dp = Dispatcher(storage=MemoryStorage())
    
    # Инициализация базы данных
    await init_database()
    
    # Регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(payments.router)
    dp.include_router(menu.router)
    dp.include_router(referral.router)
    
    # Запуск планировщика уведомлений
    asyncio.create_task(start_notification_scheduler(bot))
    
    logger.info("Бот запущен успешно!")
    
    try:
        # Запуск бота
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
