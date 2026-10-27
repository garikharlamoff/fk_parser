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
        elements = self.driver.find_elements(By.CLASS_NAME, 'anons-name')
        for element in elements:
            link = element.find_element(By.TAG_NAME, 'a')
            self.links_list.append(link.get_attribute('href'))

    def go_to_the_next_page(self):
        clickable_element = WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div/div[1]/div[3]/div[3]/a"))
        )
        self.driver.execute_script("arguments[0].click();", clickable_element)

    # def accept_cookie(self):
    #     clickable_element = WebDriverWait(self.driver, 50).until(
    #         EC.element_to_be_clickable((By.CLASS_NAME, "mile-cookie__btn mile-cookie__accept"))
    #     )
    #     clickable_element.click()

    def get_info(self):
        for link in self.links_list:
            self.driver.get(link)
            time.sleep(1)
            # wait = WebDriverWait(self.driver, 10)
            # wait.until(EC.any_of((By.CLASS_NAME, "prod-tab-specifications__table")))
            tabble_list = self.driver.find_elements(By.CLASS_NAME, 'characteristic-name')
            print(tabble_list)
            for table in tabble_list:
                self.info_list.append(table.text)
            print(self.info_list)
            time.sleep(1)

        for link in self.links_list:
            self.driver.get(link)
            time.sleep(1)
            tabble_list = self.driver.find_elements(By.CSS_SELECTOR, 'div.characteristic-value span')
            print(tabble_list)
            for table in tabble_list:
                self.info_list.append(table.text)
            print(self.info_list)
            time.sleep(1)
            

    def creating_csv_file(self):
       
        for i in range(0 , len(self.info_list)-1):
            if (i < (len(self.info_list)/2)):
                print(i)
                print(int(len(self.info_list)/2))
                self.date_dict.update({self.info_list[i] : [self.info_list[i+(int(len(self.info_list)/2))]]})
                if self.info_list[i] == 'Высота, мм:':
                    df_1 = pd.DataFrame(self.date_dict)
                    print(df_1)
                    df_1.to_csv("var.csv", index=False,  mode="a", sep=",", header=not os.path.isfile("var.csv"))
        print(self.date_dict)    

        
       

      


    def __del__ (self):
        print("zakoncheno")

