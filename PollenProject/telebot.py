
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
    # while True:
    forecast = get_forecast()
    keyboard = format_pollen_table(forecast)

    new_message = await bot.send_message(
        chat_id=constants.TELEGRAM_CHAT_ID,
        text=forecast['message'],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    if new_message.message_id-1:
        await bot.delete_message(
            constants.TELEGRAM_CHAT_ID,
            new_message.message_id-1
        )
    print('Отправлено')


async def scheduler():
    while True:
        now = datetime.now()
        if now.hour == constants.HOURS and now.minute == constants.MINUTES:
            print('Время наступило')
            await main()
            time.sleep(60)
        else:
            time.sleep(10)

if __name__ == "__main__":
    asyncio.run(scheduler())
