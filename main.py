import string
import requests
import time
import re
import locale
import logging
import logging.config
import os
import sys
from logging import Logger
from openpyxl import Workbook
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


locale.setlocale(category=locale.LC_ALL, locale="Russian")

all_urls = ["https://www.avito.ru/user/4feb3f1fabf745064a9cba93a1810815/profile?src=sharing", "https://www.avito.ru/user/17332ea6de374567e1c6d45dc1286ae8/profile?src=sharing", "https://www.avito.ru/brands/i76266501/items/all?sellerId=6cf3462bc4a0f32769533edaf6c56262", "https://www.avito.ru/user/688c03cef05552e140144a708a3059f2/profile?src=sharing", "https://www.avito.ru/user/25952e85c0225d8d904ccbdbcec6ccc2/profile?src=sharing", "https://www.avito.ru/user/eb8578a5cb2ff126e6270650b1c3c849/profile?src=sharing", "https://www.avito.ru/user/a107a1adb7520995594907d2e0b21d2b/profile?src=sharing", "https://www.avito.ru/brands/i193648154/items/all?sellerId=0a0b0f60120f0bcc3b26b78a3618cd32", "https://www.avito.ru/brands/i188370795/items/all?sellerId=4d9de7fc6308845565e7413b51a57785", "https://www.avito.ru/brands/i212554388/items/all?sellerId=d25ef0c0d8764d95c6e71e4bac3b2b18", "https://www.avito.ru/user/52e44510c7e83d9fc9af6190908c1f4b/profile?src=sharing", "https://www.avito.ru/user/f139b3aaa8d09a95227bf08496c20be7/profile?src=sharing", "https://www.avito.ru/user/2e75b88f23d62d190b869c84aba18b8c/profile?src=sharing", "https://www.avito.ru/brands/i314263183/items/all?sellerId=4b25ee39e208e512d438b959485f1b59", "https://www.avito.ru/brands/i169669317/items/all?sellerId=9dbc1b84f756dd9e455925323edbbd80", "https://www.avito.ru/brands/avtomax77/items/all?sellerId=e35e5566f6b442cc6392b0193889e530", "https://www.avito.ru/brands/i278007666/items/all?sellerId=3c83ad33c9cbb5ffe2745397a346be69", "https://www.avito.ru/user/d483d3ea61bbb85080e3624527d47dd0/profile?src=sharing", "https://www.avito.ru/user/2cb938e0dabd4a4baabd9e1d459906f2/profile?src=sharing", "https://www.avito.ru/brands/i168585898/items/all?sellerId=1d47ed0742f4c6b5484b485682761525", "https://www.avito.ru/user/bfee74dfc076127c9f597d0dc7d73c04/profile?src=sharing", "https://www.avito.ru/brands/i307004126/items/all?sellerId=5ce479ca4c6d1c5cfbe066b8c9fc1d48", "https://www.avito.ru/user/356fec245b17b070e662243a31c20624/profile?src=sharing", "https://www.avito.ru/user/c1948bd68e4c499aa6d474330e6a7c5a/profile?src=sharing", "https://www.avito.ru/user/cf1ca78cb8ff88adc1a675af112429a0/profile?src=sharing", "https://www.avito.ru/brands/i286456076/items/all?sellerId=59a7b39e9a97393cd8d96f82ab49eb76", "https://www.avito.ru/brands/i6298575/items/all?sellerId=45fca46ab29b0b5f859b17e766416dfd", "https://www.avito.ru/user/2c8ab1def09746b98e436ad86286ef06/profile?src=sharing", "https://www.avito.ru/brands/i206694595/items/all?sellerId=d69c729810a894123a207e64fcdaeb32", "https://www.avito.ru/brands/i171758815/items/all?sellerId=a0621acf286d7f997dea8b7e3fd73e82", "https://www.avito.ru/user/f3007a48cb0ba016dc3cde07a2131e60/profile/items/all?sellerId=f3007a48cb0ba016dc3cde07a2131e60", 'https://www.avito.ru/user/f3007a48cb0ba016dc3cde07a2131e60/profile?src=sharing', 'https://www.avito.ru/user/3dc3b5c375eb6b621ee03d264051d8c3/profile?src=sharing', 'https://www.avito.ru/user/667babf1d8f06eab9ecf4e5f81bafe64/profile?src=sharing', 'https://www.avito.ru/user/83911ef59ad83596e84fe80baed6e9d8/profile?src=sharing', 'https://www.avito.ru/user/4b6bf9c638355cfa741f2f86c4f1569d/profile?src=sharing', 'https://www.avito.ru/user/2b151266adecb2d44bb132583d535cf2/profile?src=sharing', 'https://www.avito.ru/user/f258ae84db2895c7425976f1c3a5ffe4/profile?src=sharing', 'https://www.avito.ru/user/c7d77b93806296be350d6007e4e56a7f/profile?src=sharing', 'https://www.avito.ru/user/53024d1a73e5876289ec68263d7030af/profile?src=sharing', 'https://www.avito.ru/user/a9f74d04939561e01970aab794f28f6e/profile?src=sharing', 'https://www.avito.ru/brands/i313080882/items/all?sellerId=88538d105f38ffbffa0bde426d3115b1', 'https://www.avito.ru/user/8bd6af698f36db9e1e46f1f5e0f0f37c/profile?src=sharing', 'https://www.avito.ru/user/8a8174b5eb206efdce21f9021af08a01/profile?src=sharing', 'https://www.avito.ru/brands/akb24/items/all?sellerId=98c7522cbc02cb4e2ae8fe6823226357', 'https://www.avito.ru/user/1150f9175fe2dba49bc6b77e60906e65/profile?src=sharing', 'https://www.avito.ru/user/983d73a4d075b8acf4019c149f265f43/profile?src=sharing', 'https://www.avito.ru/user/8b570ec77361275c5489c4f1e07524dd/profile?src=sharing', 'https://www.avito.ru/brands/i135678238/items/all?sellerId=5b03a606e391b704cccac0fa9eea743c', 'https://www.avito.ru/user/0a71b4379cf4e6176d0e150b0e0855e7/profile?src=sharing', 'https://www.avito.ru/user/6f512dd92bd02823866d82ee9bc7c223/profile?src=sharing', 'https://www.avito.ru/brands/i366872042/items/all?sellerId=b7024775658c6d3e4756f3d2f1cf1534', 'https://www.avito.ru/user/87126c67d1d6eb04002deb87dc706221/profile?src=sharing', 'https://www.avito.ru/user/a56e4267fca89803252957e454b4561b/profile?src=sharing', 'https://www.avito.ru/user/73db299f790bf165ffc23bd075938b48/profile?src=sharing', 'https://www.avito.ru/user/7172bd083072eeff018a049fadfa0cfc/profile?src=sharing', 'https://www.avito.ru/user/6f84b0cc98679880fef286838f801189/profile?src=sharing', 'https://www.avito.ru/user/d230ed5b0bb1e4fbbd52eaa2f18ae666/profile?src=sharing', 'https://www.avito.ru/brands/i299324446/items/all?sellerId=53024d1a73e5876289ec68263d7030af', 'https://www.avito.ru/user/8d3a483ed4af8be63f37e970a1886ae0/profile?src=sharing', 'https://www.avito.ru/user/ce0ad33662f67aec4f4bb4a7524dbcea/profile?src=sharing', 'https://www.avito.ru/user/bee3e532ba66133ee398f3e91a1366f0/profile?src=sharing', 'https://www.avito.ru/brands/soloauto/items/all?sellerId=b6f2a889267dcda0d61b37119555f133', 'https://www.avito.ru/user/88538d105f38ffbffa0bde426d3115b1/profile?src=sharing', 'https://www.avito.ru/user/04c0e12e2c1d00ab35c8a39fea3f7b7e/profile?src=sharing', 'https://www.avito.ru/user/59f0906b157fcb9e0421c8d521c22bf1/profile?src=sharing', 'https://www.avito.ru/brands/i212145235/items/all?sellerId=7d4982861b2b2f94bef7193c8ef6759e', 'https://www.avito.ru/user/18d06f8f72a7a0dd49ebf0413151fcef/profile?src=sharing']
test_url = 'https://www.avito.ru/brands/i171758815/items/all?sellerId=a0621acf286d7f997dea8b7e3fd73e82'
# url_404 = 'https://www.avito.ru/user/4feb3f1fabf745064a9cba93a1810815/profile?src=sharing'
# test_urls = (
#     'https://www.avito.ru/user/4feb3f1fabf745064a9cba93a1810815/profile?src=sharing',
#     'https://www.avito.ru/user/4feb3f1fabf745064a9cba93a1810815/profile?src=sharing',
#     'https://www.avito.ru/brands/i76266501/items/all?sellerId=6cf3462bc4a0f32769533edaf6c56262'
# )
# test_url = 'https://www.avito.ru/brands/i76266501/items/all?sellerId=6cf3462bc4a0f32769533edaf6c56262'
# bad_url = 'https://www.avito.ru/user/4feb3f1fabf745064a9cba93a1810815/profile?src=sharing'

def get_dict_config(cur_url) -> dict:
    path_logs = os.path.abspath(
        os.path.join('.', 'loggers', 'logs.txt')
    )
    path_errors_logs = os.path.abspath(
        os.path.join('.', 'loggers', 'error_logs.txt')
    )
    path_url_logs = os.path.abspath(
        os.path.join('.', 'loggers', 'not_workers_urls.txt')
    )
    path_dir_logs = os.path.abspath(os.path.join('.', 'loggers'))
    if not os.path.isdir(path_dir_logs):
        os.makedirs(path_dir_logs)

    dict_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "simple": {
                "format": f"%(levelname)s | %(asctime)s | %(lineno)s | %(funcName)s | ({cur_url}) | %(message)s",
            },
            "collect_url": {
                "format": f"%(asctime)s | ({cur_url}) | %(message)s",
            },
            'work_script': {
                "format": f"Идет сбор информации с сайта: {cur_url} | %(asctime)s | %(message)s",
            }
        },
        "handlers": {
            "base_handler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "when": "h",
                "interval": 10,
                "backupCount": 5,
                "level": "DEBUG",
                "formatter": "simple",
                "filename": path_logs,
                "encoding": "utf-8",
            },
            "error_handler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "when": "h",
                "interval": 10,
                "backupCount": 5,
                "level": "ERROR",
                "formatter": "simple",
                "filename": path_errors_logs,
                "encoding": "utf-8",
            },
            "collect_error_url": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "when": "h",
                "interval": 10,
                "backupCount": 5,
                "level": "ERROR",
                "formatter": "collect_url",
                "filename": path_url_logs,
                "encoding": "utf-8",
            },
            "check_work": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "work_script",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            'base_logger': {
                "level": "DEBUG",
                "handlers": ["base_handler", 'error_handler', 'check_work']
            },
            'url_logger': {
                "level": "ERROR",
                "handlers": ['collect_error_url']
            },
        },
    }
    return dict_config

def get_logger(cur_url: str, name_logger: str) -> Logger:
    logging.config.dictConfig(get_dict_config(cur_url))
    logger: Logger = logging.getLogger(name_logger)
    return logger

def get_count_adc(element: str) -> int:
    pattern = r'Найдено\s(.*)\s.*'
    count_adc = re.findall(pattern, element)
    return int(count_adc[0])

def get_webdriver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--proxy-server=94.127.136.248:8000')
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    user_agent = f'user_agent={ua}'
    options.add_argument(user_agent)
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)
    # driver.add_cookie(cookies)
    return driver

def check_404_page(driver_obj: WebDriver) -> bool:
    h1_elem = driver_obj.find_element(By.TAG_NAME, 'h1').text
    if 'Такой страницы нe существует' in h1_elem:
        return False
    return True

def get_article_product(soup_object: BeautifulSoup, logger_obj: Logger) -> str:
    try:
        all_elements = soup_object.find('ul', 'params-paramsList-_awNW').find_all('li')
        for elem in all_elements:
            if 'Номер запчасти' in elem.text:
                article = elem.text.replace('Номер запчасти: ', '')
                return article
    except Exception as exc:
        logger_obj.debug('Артикль не был найден')
    return 'Артикль товара не найден'

def get_data_adc(soup_obj: BeautifulSoup) -> str:
    data_adc = soup_obj.find('div', 'style-item-socials-container-_aa1d style-new-style-eTWEE').find_all('span')[1].text[3:]
    if 'сегодня' in data_adc:
        date_today = str(datetime.now().strftime('%d %b'))
        data_adc = data_adc.replace('сегодня', date_today)
    elif 'вчера' in data_adc:
        data_tommorow = datetime.now() - timedelta(days=1)
        data_tommorow = str(data_tommorow.strftime('%d %b'))
        data_adc = data_adc.replace('вчера', data_tommorow)
    return data_adc

def get_numbers_views_today(soup_obj: BeautifulSoup) -> str:
    count_views = soup_obj.find(
        'div',
        'style-item-socials-container-_aa1d style-new-style-eTWEE'
    ).find_all('span')[2].find_all_next('span')[1].text
    return f'Количество просмотров: {datetime.now().strftime("%d %b")}' + count_views

def get_compatibility(driver_obj: WebDriver) -> str:
    try:
        div_with_buttons = driver_obj.find_element(By.CLASS_NAME, 'groupings-root-WjgeL')
        div_soup = BeautifulSoup(driver_obj.page_source, 'lxml').find('div', 'groupings-root-WjgeL')
        while div_soup.find('button'):
            all_buttons = div_with_buttons.find_elements(By.TAG_NAME, 'button')
            for but in all_buttons:
                but.click()
                time.sleep(0.8)
            div_soup = BeautifulSoup(driver_obj.page_source, 'lxml').find('div', 'groupings-root-WjgeL')
        list_elem_with_text = div_soup.find_all('p')
        compatibility = '\n'.join([elem_p.text for elem_p in list_elem_with_text])
        return compatibility
    except Exception as exc:
        return 'Нет информации о совместимости'

def check_content(driver_obj: WebDriver, logger_obj: Logger) -> bool:
    """
    Идет проверка контента на главной объявления.
    Если первым стоит видео, то переключаем на фото и идем дальше.
    Если первым стоит фото, то просто возвращаем True и идем дальше.
    """
    logger_obj.debug('Идет проверка контента (видео/фото)')
    try:
        logger_obj.debug('Находим кнопку запуска видео')
        driver_obj.find_element(
            By.TAG_NAME, 'video'
        )
        logger_obj.debug('Кнопка была найдена. Контент на главной видео')
        preview_images = driver_obj.find_element(
            By.XPATH, '/html/body/div[1]/div/div[5]/div[1]/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/div/div/ul'
        ).find_elements(By.TAG_NAME, 'li')[-1].click()
        logger_obj.debug('Переключаем на картинку, чтобы продолжить сбор фотографий')
        return True
    except Exception as exc:
        logger_obj.debug('Контент на главной фото')
        return False

def save_image_from_page(driver_obj: WebDriver, name_product: str, name_shop: str, logger_obj: Logger) -> None:
    """
    Поиск и сохранение изображений товара в директорию name_shop/name_product
    name_shop: название магазина
    name_product: название товара
    """

    #  Поиск элемента с превью фотографий
    logger_obj.debug('Получаем объект с превью фото')
    try:
        time.sleep(1)
        ul_preview_all_image: list = driver_obj.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div[5]/div[1]/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/div/div/ul'
        ).find_elements(By.TAG_NAME, 'li')

        #  Получение кол-ва фотографий на странице
        logger_obj.debug('Считаем кол-во фото товара')
        count_image: int = int(len(ul_preview_all_image))

        #  Проверяем что стоит на главной фото или видео
        if check_content(driver_obj, logger_obj):
            count_image -= 1

        #  Открываем просмотр фото, чтобы скачать более качественные фотографии
        logger_obj.debug('Открываем, чтобы собрать фотографии')
        driver_obj.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div[5]/div[1]/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/div/div/div/div/div[3]/img'
        ).click()

        time.sleep(1.5)

        #  Поиск кнопки для переключения фотографий
        logger_obj.debug('Поиск кнопки для переключения фотографий')
        button = driver_obj.find_element(
            By.CLASS_NAME, 'styles-wrapper-_7Lvo'
        ).find_element(By.TAG_NAME, 'button')

        #  Определеяем директорию для сохранения фотографий
        logger_obj.debug('Опеределеяем директорию для сохранения фотографий')
        path_dir = os.path.abspath(
            os.path.join('.', name_shop, name_product)
        )
        if not os.path.isdir(path_dir):
            logger_obj.debug('Создаем директорию для сохранения фотографий')
            os.makedirs(path_dir)

        time.sleep(1)
        #  Проходимся по всем фотографиям и сохраняем их
        for i in range(1, count_image + 1):
            #  Ищем ссылку на фото
            src_photo = driver_obj.find_element(
                By.CLASS_NAME, 'styles-wrapper-_7Lvo'
            ).find_element(By.TAG_NAME, 'img').get_attribute('src')
            #  Скачиваем фото
            bytes_photo = requests.get(src_photo).content
            #  Определеям путь и имя фото
            path_to_photo_png = os.path.join(path_dir, f'{i}_image.png')
            #  Сохраняем фото
            save_image(bytes_photo, path_to_photo_png)
            #  Переходим к следующему фото
            button.click()
            time.sleep(1)

        #  Закрыть просмотр фото, чтобы вернуться к дальнешему сбору информации со страницы
        driver_obj.find_element(By.CLASS_NAME, 'styles-cross-jE1a2').click()

    except Exception as exc:
        logger_obj.debug('Объект с превью фото не найден. Значит на странице одно фото')
        count_image = 1

        #  Открываем просмотр фото, чтобы скачать более качественные фотографии
        logger_obj.debug('Открываем фото, чтобы скачать фотографию')
        driver_obj.find_element(
            By.CLASS_NAME,
            'style-item-view-main-tKI1S'
        ).find_element(By.TAG_NAME, 'img').click()

        time.sleep(1)

        #  Определеяем директорию для сохранения фотографий
        logger_obj.debug('Опеределеяем директорию для сохранения фотографии')
        path_dir = os.path.abspath(
            os.path.join('.', name_shop, name_product)
        )
        if not os.path.isdir(path_dir):
            logger_obj.debug('Создаем директорию для сохранения фотографий')
            os.makedirs(path_dir)

        #  Ищем ссылку на фото
        src_photo = driver_obj.find_element(
            By.CLASS_NAME, 'styles-wrapper-_7Lvo'
        ).find_element(By.TAG_NAME, 'img').get_attribute('src')
        #  Скачиваем фото
        bytes_photo = requests.get(src_photo).content
        #  Определеям путь и имя фото
        path_to_photo_png = os.path.join(path_dir, f'1_image.png')
        #  Сохраняем фото
        save_image(bytes_photo, path_to_photo_png)
        #  Переходим к следующему фото
        time.sleep(1)
        #  Закрыть просмотр фото, чтобы вернуться к дальнешему сбору информации со страницы
        driver_obj.find_element(By.CLASS_NAME, 'styles-cross-jE1a2').click()

def remove_invalid_chars(filename):
    """Убирает все не печатаемые символы"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters + "".join(map(chr, range(ord("а"), ord("я")+1))) + "".join(map(chr, range(ord("А"), ord("Я")+1))), string.digits)
    return ''.join(c for c in filename if c in valid_chars)

def save_image(bytes_file: bytes, path_dir: str) -> None:
    with open(path_dir, 'wb') as file:
        file.write(bytes_file)

def check_job_vacancy(driver_obj: WebDriver, logger_obj: Logger) -> bool:
    logger_obj.debug('Проверка объявления (товар/вакансия)')
    try:
        logger_obj.debug('Поиск первого заголовка h2')
        text_h2 = driver_obj.find_element(
            By.TAG_NAME, 'h2'
        ).text
        logger_obj.debug('Сравнение текста с заголовком')
        if 'Условия' in text_h2:
            return True
        return False
    except Exception as exc:
        logger_obj.error('При проверке заголовка произошла ошибка')
        logger_obj.error(exc)

def collecting_info_from_page(objects: list[WebElement], driver: WebDriver, logger_obj: Logger, name_shop: str) -> dict:
    """Функция для сбора информации со всех объявлений продавца"""
    logger_obj.debug('Начало сбора информации со страницы продавца')
    date_today = str(datetime.now().strftime('%d %b'))
    dict_with_info = [
        (
            'Товар', 'ID объявления', 'Описание объявления', 'Адресс собъявления',
         'Ссылка на объявление', 'Стоимость', 'Дата объявленя', 'Кол-во просмотров',
         f'Кол-во просмотров сегодня ({date_today})', 'Артикуль товара', 'Совместимости',
        )
    ]
    for adc_product in objects:
        try:
            logger_obj.debug('Начало проходки по объявлению')
            adc_product.click()
            time.sleep(2.5)
            driver.switch_to.window(driver.window_handles[-1])
            logger_obj.debug(f'Переход на страницу объявления. URL: {driver.current_url}')

            #  Проверяем является ли страница вакансией
            if check_job_vacancy(driver, logger_obj):
                raise Exception('Страница оказалась вакансией')

            #  Создаем объект супа, для более удобного и быстрого парсинга информации со страницы
            src = driver.page_source
            soup = BeautifulSoup(src, 'lxml')
            logger_obj.debug('Парсинг страницы с помощью bs4')

            #  Получаем имя товара (заголовок объявления)
            name_product = remove_invalid_chars(soup.find('h1').text)
            logger_obj.debug(f'Название товара: {name_product}')
            logger_obj.info(f'Сбор информации о товаре: {name_product}')
            logger_obj.info(f'URL на товар: {driver.current_url}')

            #  Собираем все фотографии и сохраняем в директорию name_shop/name_product
            logger_obj.debug('Сбор всех фото товара и сохранения в папку с названием товара')
            save_image_from_page(driver, name_product, name_shop, logger_obj)

            #  Получаем ID объявления
            id_adc = soup.find(
                'div',
                'style-item-socials-container-_aa1d style-new-style-eTWEE'
            ).find_all('span')[0].text.replace('№ ', '')
            logger_obj.debug(f'ID объявления: {id_adc}')
            #  Получаем описание объявление
            description_list = [
                elem.text + '\n' for elem in soup.find('div', 'style-item-description-html-qCwUL').find_all('p')
            ]
            description = '\n'.join(description_list)
            logger_obj.debug(f'Описание объявления: {description}')
            #  Получаем адрес с объявления
            address = soup.find('span', 'style-item-address__string-wt61A').text
            logger_obj.debug(f'Адрес объявления: {address}')
            #  Получаем URL объявления
            url_adc = driver.current_url
            logger_obj.debug(f'URL объявления: {url_adc}')
            #  Получаем цену объявления
            price = soup.find_all('span', 'style-price-value-string-rWMtx')[-1].text
            logger_obj.debug(f'Цена объявления: {price}')
            #  Получаем дату объявления
            data_adc = get_data_adc(soup)
            logger_obj.debug(f'Дата объявления: {data_adc}')
            #  Получаем количество просмотров
            numbers_views = soup.find(
                'div',
                'style-item-socials-container-_aa1d style-new-style-eTWEE'
            ).find_all('span')[2].find_all_next('span')[0].text
            logger_obj.debug(f'Кол-во просмотров объявления: {numbers_views}')
            #  Получаем количество просмотров сегодня
            numbers_views_today = get_numbers_views_today(soup)
            logger_obj.debug(f'Кол-во просмотров объявления сегодня: {numbers_views_today}')
            #  Получаем артикуль товара
            article_product = get_article_product(soup, logger_obj)
            logger_obj.debug(f'Артикуль товара: {article_product}')
            #  Получаем совместимости товара (если они есть)
            compatibility = get_compatibility(driver)
            logger_obj.debug(f'Совместимости товара: {article_product}')

            dict_with_info.append(
                (
                    name_product,
                    id_adc,
                    description,
                    address,
                    url_adc,
                    price,
                    data_adc,
                    numbers_views,
                    numbers_views_today,
                    article_product,
                    compatibility,
                )
            )
            logger_obj.debug('Сбор информации в список кортежей')
        except Exception as exc:
            logger_obj.error(exc)
        finally:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    logger_obj.debug('Возвращаем информацию об объявлениях продавца')
    logger_obj.info(f'Сбор информации закончен')
    return dict_with_info

def recording_info_to_file(info_about_adc: list[tuple[str]], name_shop: str) -> None:
    """Получает лист с кортежами в которых находится информация об объявлении (товаре) и записывает в Excel"""
    wb = Workbook()
    wb['Sheet'].title = 'Информая о товаре продавца'
    ws: Worksheet = wb.active

    for info in info_about_adc:
        ws.append(info)

    wb.save(f'{name_shop}.xlsx')


def get_elem_count_adc(driver_obj: WebDriver, logger_obj: Logger):
    logger_obj.debug('Начало поверки наличия элемента с кол-вом объявлений')
    try:
        result = driver_obj.find_element(By.TAG_NAME, 'h5').text
        logger_obj.debug('Элемент с кол-вом объявлений найден')
        return result
    except Exception as exc:
        logger_obj.debug('Элемент с кол-вом объявлений не найден')
        driver_obj.find_element(
            By.XPATH, '/html/body/div[1]/div/div[6]/div[2]/div/div/div[2]/section[1]/div[3]/div[2]/div[2]/div/div[2]/a/span'
        ).click()
        logger_obj.debug('Страница была перелючена (нажата кнопка "Показать все")')
        time.sleep(1)
        result = driver_obj.find_element(By.TAG_NAME, 'h5').text
        return result


def main(url):
    driver = get_webdriver()
    driver.maximize_window()
    logger = get_logger(url, 'base_logger')
    url_logger = get_logger(url, 'url_logger')
    try:
        # Делаем запрос на url и получаем количество объявление на странице
        logger.debug('Запрос к URL')
        logger.info('Начало сбора информации со страницы продавца')
        driver.get(url=url)
        time.sleep(2)
        # Проверяем рабочий ли URL или нет
        if check_404_page(driver):
            # Получаем информацию об общем кол-ве объявлений у продавца
            logger.debug('Начало сбора информации со страницы')
            elem_with_count_adc = get_elem_count_adc(driver, logger)
            count_adc = get_count_adc(elem_with_count_adc)
            name_shop = driver.find_element(By.TAG_NAME, 'h1').text
            trans_table = str.maketrans('', '', string.punctuation)
            name_shop = name_shop.translate(trans_table)
            logger.debug(f'Продавец: {name_shop}, кол-во объявлений: {count_adc}')
        else:
            # Если нет, то собираем информацию со страницы и вызываем исключение
            logger.info('Продавец не найден. Сбор информации об ошибке')
            h1_elem = driver.find_element(By.TAG_NAME, 'h1').text
            p_elem = driver.find_elements(By.TAG_NAME, 'p')[-1].text
            raise Exception(f'{h1_elem}, {p_elem}')
    except Exception as exc:
        logger.error(exc)
        logger.info('Произошла ошибка сбора данных с сайта')
    else:
        try:
            # Собираем все объявления со страницы
            div_products = list()
            logger.debug('Начало скрола страницы продавца')
            while count_adc != len(div_products):
                div_products = driver.find_elements(By.CLASS_NAME, 'photo-slider-root-Exoie')
                # Скрипт прокрутки страницы
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Пауза, пока загрузится страница.
                time.sleep(0.8)
            logger.debug('Скрол страницы продавца закончен\n\n')
            info_about_products = collecting_info_from_page(div_products, driver, logger, name_shop)
            recording_info_to_file(info_about_products, name_shop)
            logger.info(
                f'Сбор информации о товарах прошел успешно. '
                f'Информация сохранена в файл. '
                f'Можете брать файл с названием {name_shop}\n\n'
            )
        except Exception as exc:
            url_logger.error(exc)
    finally:
        logger.info('Конец сбора информации. Переход к следующему продавцу')
        driver.close()
        driver.quit()


if __name__ == "__main__":
    url = input('Вставьте ссылку на продавца для сбора информации: ')
    main(url)
    # main(test_url)
    print('Работа скрипта закончена, нажмите Enter', file=sys.stdout)
    input()
