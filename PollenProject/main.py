import logging
import time
import asyncio
from datetime import datetime

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from yapollenparser import get_forecast
import constants


def format_pollen_table(pollen_data):
    # Формируем клавиатуру-таблицу
    keyboard = []
    current_status = []

    header_row = [InlineKeyboardButton("📅", callback_data="ignore")]
    for day in pollen_data['day'][0:5]:
        header_row.append(
            InlineKeyboardButton(
                day.capitalize(), callback_data="ignore"
            )
        )
    keyboard.append(header_row)

    for allergen, levels in pollen_data['allergens'].items():
        if levels:
            row = [
                InlineKeyboardButton(
                    allergen.capitalize(),
                    callback_data="ignore"
                )
            ]
            current_status.append(f"{levels[0]} {allergen}")

            for level in levels[0:5]:

                emoji = constants.POLLEN_LEVEL[level]
                row.append(InlineKeyboardButton(emoji, callback_data="ignore"))

        keyboard.append(row)

    return keyboard


async def main():
    """Основная логика работы бота."""
    print('Начало выполнения')
    request = telegram.request.HTTPXRequest(
        connect_timeout=30, read_timeout=30
    )
    bot = telegram.Bot(token=constants.TELEGRAM_TOKEN, request=request)
    try:
        forecast = get_forecast()
        if not forecast:
            raise ValueError("Данные не получены")
        keyboard = format_pollen_table(forecast)

        new_message = await bot.send_message(
            chat_id=constants.TELEGRAM_CHAT_ID,
            text=forecast['message'],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        print('Отправлено')
    except Exception as e:
        logging.error(f"Ошибка в main: {str(e)}")
        raise

    try:
        if new_message.message_id-1:
            await bot.delete_message(
                constants.TELEGRAM_CHAT_ID,
                new_message.message_id-1
            )
            print('Старое сообщение удалено')
    except Exception:
        print('Старое сообщение не удалено')


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"{str(e)}")
