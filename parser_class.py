import time
import selenium
import os
import random
from PIL import Image , ImageEnhance
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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
        elements = self.driver.find_elements(By.CLASS_NAME, "product-thumb")
        for element in elements:
            link = element.find_element(By.CSS_SELECTOR, "h4 a")
            print('найден')
            self.links_list.append(link.get_attribute("href"))

    def go_to_the_next_page(self):
        clickable_element = WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[4]/div[1]/ul/li[10]/a"))
        )
        self.driver.execute_script("arguments[0].click();", clickable_element)

    def get_info(self):
        for link in self.links_list:
            self.driver.get(link)
            try:
                time.sleep(2)
                tabble_list = self.driver.find_elements(By.CSS_SELECTOR, "table.table.table-bordered tbody tr td")
                for table in tabble_list:
                    text = table.get_attribute("textContent").strip()
                    if text:
                        self.info_list.append(text)
                    else:
                        self.info_list.append('-')

            except Exception as e:
                print(f"Ошибка при обработке страницы {link}: {e}")

    def creating_csv_file(self):
       
        for i in range(0 , len(self.info_list)-1):
            if (i % 2 == 0):
                self.date_dict.update({self.info_list[i] : [self.info_list[i + 1]]})
                if self.info_list[i] == 'Моноблок':

                    df_1 = pd.DataFrame(self.date_dict)
                    print(df_1)
                    df_1.to_csv("var.csv", index=False,  mode="a", sep=",", header=not os.path.isfile("var.csv"))
        print(self.date_dict)    

      
    def __del__ (self):
        print("Конец")
