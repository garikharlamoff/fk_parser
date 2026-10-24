import time
import selenium
import os
import random
from PIL import Image , ImageEnhance
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import pandas as pd

class Parser:
    def __init__(self, link):
        self.link = link
        self.driver = webdriver.Chrome()
        self.driver.get(self.link)
        self.info_list = []
        self.links_list = [] 
        self.date_dict = {}

    def get_links_on_page(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'product-thumb')
        for element in elements:
            link = element.find_element(By.CSS_SELECTOR, 'h4 a')
            print('найден')
            self.links_list.append(link.get_attribute('href'))

    def go_to_the_next_page(self):
        clickable_element = WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div[4]/div[1]/ul/li[10]/a"))
        )
        self.driver.execute_script("arguments[0].click();", clickable_element)

    # def accept_cookie(self):
    #     clickable_element = WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.CLASS_NAME, "popup-cookie__confirm"))
    #     )
    #     clickable_element.click()

    def get_info(self):
        # Список, где будем хранить словари с характеристиками каждого товара
        self.all_products_data = []

        for link in self.links_list:
            self.driver.get(link)
            # Небольшая пауза для гарантированной загрузки DOM-дерева
            time.sleep(2) 
            
            # Находим все строки таблиц с характеристиками на странице товара
            rows = self.driver.find_elements(By.XPATH, "//table//tr")
            
            # Создаем словарь под текущий товар и добавляем ссылку как уникальный идентификатор
            product_dict = {'Ссылка': link}
            
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                # Нам нужны только строки, где есть ровно две ячейки: Название и Значение
                if len(cells) == 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    
                    # Исключаем пустые строки, заголовки секций (например, "Процессор") и кнопку отзыва
                    if key and value and not key.startswith("Написать отзыв"):
                        product_dict[key] = value
            
            # Если собрали что-то помимо ссылки — сохраняем в общий список
            if len(product_dict) > 1:
                self.all_products_data.append(product_dict)
                print(f"Успешно собраны характеристики для: {link}")
            time.sleep(1)

    def creating_csv_file(self):
        if not hasattr(self, 'all_products_data') or not self.all_products_data:
            print("Нет данных для записи в CSV.")
            return

        # Pandas автоматически объединит разные наборы ключей/характеристик в единую таблицу.
        # Если у одного ПК есть 'Оптический привод', а у другого нет — Pandas сам проставит NaN (пустоту).
        df = pd.DataFrame(self.all_products_data)
        
        file_name = "products_specs.csv"
        
        # Проверяем существование файла, чтобы не дублировать заголовки колонок при дозаписи
        file_exists = os.path.isfile(file_name)
        
        # Сохраняем с поддержкой кириллицы (utf-8-sig решает проблему с кракозябрами в Excel)
        df.to_csv(file_name, index=False, mode="a", sep=",", header=not file_exists, encoding="utf-8-sig")
        print(f"Данные успешно сохранены в файл: {file_name}")


      


    def __del__ (self):
        print("zakoncheno")




        сыендук = "пр"

