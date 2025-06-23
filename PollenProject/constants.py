import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
HOURS = int(os.getenv('HOURS'))
MINUTES = int(os.getenv('MINUTES'))
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')
MAIN_URL = (
    'https://yandex.ru/pogoda/ru/allergies?lat={lat}&lon={lon}'.format(
        lat=LATITUDE, lon=LONGITUDE
    )
)
TIME_SLEEP = 2
DAYS = 5

BUTTON_CLASS = 'AppAllergyForecast_allergensList__button____VIX'
STRONG_CLASS = 'AppAllergyForecast_pie__level_strong__H7IA2'
NORMAL_CLASS = 'AppAllergyForecast_pie__level_normal__Y6Ytt'
WEAK_CLASS = 'AppAllergyForecast_pie__level_weak__0_jqA'
CLEAR_CLASS = 'AppAllergyForecast_pie__level_clear__uqh7t'
LEVEL_DIV_CLASS = 'AppAllergyForecast_level__VQJG7'
LEVEL_CLASS = 'AppAllergyForecast_pie__level__uWQeg'
FORECAST_CLASS = 'AppAllergyForecast_forecast__mfnOz'
BAR_CLASS = 'AppAllergyForecast_pie__bar__hRvdk'
DAY_CLASS = 'AppAllergyForecast_pie__date__a1DrM'
TOOLTIP_CLASS = 'AppTooltip_tooltip__O2eKf'
WARNING_MESSAGE_CLASS = 'AppAllergyWarning_message__A0lQw'

# 🟥🟧🟨🟩⬜🔴🟠🟡🟢
POLLEN_LEVEL = {
    'STRONG': '🟥',
    'NORMAL': '🟧',
    'WEAK': '🟨',
    'CLEAR': '🟩',
    'UNKNOWN': '⬜',
}
