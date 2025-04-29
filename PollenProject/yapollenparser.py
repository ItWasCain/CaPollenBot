from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

import time

from config import create_driver
import constants

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_data_new(buttons, driver):
    result = {
        'day': [],
        'allergens': {},
    }

    days_collected = False

    for button in buttons:
        # Кликаем на кнопку

        button.click()
        time.sleep(constants.TIME_SLEEP)
        # Извлекаем название аллергена
        allergen_name = button.find_element(
            By.TAG_NAME, 'span'
        ).text.strip().lower()
        # Получаем блок с прогнозом
        try:
            forecast_div = driver.find_element(
                By.CLASS_NAME, constants.FORECAST_CLASS
            )
        except Exception as e:
            print(f"Прогноз не найден для {allergen_name}: {e}")
            continue

        # Получаем все бары прогноза
        pie_bars = forecast_div.find_elements(
            By.CLASS_NAME,
            constants.BAR_CLASS
        )

        allergens = []
        # Собираем данные только для первых 3 дней
        for i, bar in enumerate(pie_bars):
            try:
                day = bar.find_element(
                    By.CLASS_NAME, constants.DAY_CLASS
                ).text.strip()

                # Заполняем дни только один раз
                if not days_collected:
                    result['day'].append(day)

                tooltip = bar.find_element(
                    By.CLASS_NAME, constants.TOOLTIP_CLASS
                )
                level_div = tooltip.find_element(
                    By.CLASS_NAME, constants.LEVEL_CLASS
                )
                level_classes = level_div.get_attribute("class").split()

                if constants.STRONG_CLASS in level_classes:
                    level = 'STRONG'
                elif constants.NORMAL_CLASS in level_classes:
                    level = 'NORMAL'
                elif constants.WEAK_CLASS in level_classes:
                    level = 'WEAK'
                elif constants.CLEAR_CLASS in level_classes:
                    level = 'CLEAR'
                else:
                    level = 'UNKNOWN'

                allergens.append(level)

            except Exception as e:
                print(f"Ошибка при обработке бара для {allergen_name}: {e}")
                allergens.append('нет данных')
            if allergens:
                result['allergens'][allergen_name] = allergens
        # Помечаем, что дни уже собраны
        days_collected = True

    return result


def get_forecast():
    driver = create_driver()
    if not driver:
        raise RuntimeError("Не удалось инициализировать WebDriver")

    try:
        driver.get(constants.MAIN_URL)

        # Ждем загрузки страницы
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, constants.BUTTON_CLASS)
            )
        )

        # Находим все кнопки аллергенов
        buttons = driver.find_elements(
            By.CLASS_NAME, constants.BUTTON_CLASS
        )
        message = driver.find_element(
            By.CLASS_NAME,
            constants.WARNING_MESSAGE_CLASS
        ).text
        result = get_data_new(buttons, driver)
        result['message'] = message
        return result

    finally:
        try:
            driver.quit()
        except Exception as e:
            logging.warning(f"Ошибка при закрытии драйвера: {str(e)}")


# @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
# def get_forecast():
#     driver = None
#     try:
#         driver = create_driver()
#         driver.set_page_load_timeout(30)
#         driver.set_script_timeout(30)
        
#         logger.info("Загрузка страницы...")
#         driver.get(constants.MAIN_URL)
        
#         WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located((By.CLASS_NAME, constants.BUTTON_CLASS))
#         )
        
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CLASS_NAME, constants.BUTTON_CLASS))
#         )
        
#         # Ваша основная логика парсинга...
#         buttons = driver.find_elements(
#             By.CLASS_NAME, constants.BUTTON_CLASS
#         )
#         message = driver.find_element(
#             By.CLASS_NAME,
#             constants.WARNING_MESSAGE_CLASS
#         ).text
#         result = get_data_new(buttons, driver)
#         result['message'] = message
#         return result
        
#     except Exception as e:
#         logger.error(f"Ошибка парсинга: {str(e)[:200]}")  # Ограничиваем длину лога
#         raise
#     finally:
#         if driver:
#             try:
#                 driver.quit()
#             except:
#                 pass


if __name__ == '__main__':
    print(get_forecast())
