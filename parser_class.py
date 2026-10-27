import time
import selenium
import os
import random
import logging
import functools
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("parser.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def measure_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"Функция:{func.__name__} - время выполнения:{duration:.4f} сек")
        return result
    return wrapper

class Parser:
    @measure_time
    def __init__(self, link):
        self.link = link
        
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/62.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        ]
        
        proxy_servers = [
            "http://159.195.53.110:3128",
            "http://20.205.61.145:80",
            "http://51.158.110.216:8811",
            "http://138.68.60.151:3128",
            "http://161.35.176.166:3128"
        ]
        
        chosen_user_agent = random.choice(user_agents)
        chosen_proxy = random.choice(proxy_servers) 
        
        setting = ChromeOptions()
        setting.add_argument(f"--proxy-server={chosen_proxy}")
        setting.add_argument("--ignore-certificate-errors")
        setting.add_argument(f"user-agent={chosen_user_agent}")
        setting.page_load_strategy = 'normal'
        
        print(f"Используемый User-Agent: {chosen_user_agent}")
        print(f"Используемый Proxy: {chosen_proxy}")
        
        self.driver = webdriver.Chrome(options = setting)
        self.driver.get(self.link)
        self.info_list = []
        self.links_list = [] 
        self.date_dict = {}

    @measure_time
    def get_links_on_page(self):
        elements = self.driver.find_elements(By.CLASS_NAME, "product-thumb")
        for element in elements:
            link = element.find_element(By.CSS_SELECTOR, "h4 a")
            print('найден')
            self.links_list.append(link.get_attribute("href"))

    @measure_time
    def go_to_the_next_page(self):
        clickable_element = WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div[4]/div[1]/ul/li[11]/a"))
        )
        self.driver.execute_script("arguments[0].click();", clickable_element)

    @measure_time
    def get_info(self):
        for link in self.links_list:
            self.driver.get(link)
            try:
                try:
                    text_1 = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div[2]/div/div[6]/ul/li/p/span/b").text.strip()
                except Exception:
                    text_1 = "-"
                
                try:
                    text_2 = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div[2]/div/div[6]/ul/li/p/span/span[2]/b").text.strip()
                except Exception:
                    text_2 = "-"
                
                self.info_list.append(text_1 if text_1 else '-')
                self.info_list.append(text_2 if text_2 else '-')
                time.sleep(2)
                tabble_list = self.driver.find_elements(By.CSS_SELECTOR, "table.table.table-bordered tbody tr td")
                for table in tabble_list:
                    text = table.get_attribute("textContent").strip()
                    if text:
                        self.info_list.append(text)
                    else:
                        self.info_list.append('-')

            except Exception as e:
                logging.error(f"Ошибка при обработке страницы {link}: {e}")

    @measure_time
    def creating_csv_file(self):
        for i in range(0, len(self.info_list)-1):
            if (i % 2 == 0):
                self.date_dict.update({self.info_list[i] : [self.info_list[i + 1]]})
                if self.info_list[i] == 'Моноблок':
                    df_1 = pd.DataFrame(self.date_dict)
                    print(df_1)
                    df_1.to_csv("var.csv", index=False, mode="a", sep=",", header=not os.path.isfile("var.csv"))
        print(self.date_dict)    

    def __del__(self):
        print("Конец")