"""File that handle wikepedia scrapping"""

# pylint: disable=all

import os

from random import randint

import time
import traceback
import yaml

import sys

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from libzim.reader import Archive
from urllib.parse import unquote


import time
from global_variable import *

class Scrapdata():
    def __init__(self,headless=False):
        self.headless = headless
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--log-level=1')
        self.options.add_argument("--log-level=3")
        if self.headless:
            self.options.add_argument('headless')

        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.set_page_load_timeout(15)

class WikiSrapping(Scrapdata):
    def __init__(self,headless=False):
        self.driver = Scrapdata(headless).driver
        self.all_file = self.print_file_content("../all_wikipedia_page_fr.txt").split("\n")
        self.size_of_batch_nb = 200
        self.chunck_size = int(len(self.all_file)/self.size_of_batch_nb)
        self.zim = Archive("../wikipedia_fr_all_maxi_2026-02.zim")

        #self.wikipedia_url = "https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal"
    
    # def search_page(self, user_to_search):
    #     try:
    #         self.driver.get(WIKIPEDIA_URL)
            
    #         # Wait for page to stabilize
    #         WebDriverWait(self.driver, WAIT_TIME).until(
    #             EC.presence_of_element_located((By.TAG_NAME, "body"))
    #         )

    #         # Robust element acquisition with explicit clickable wait
    #         search_bar_input = WebDriverWait(self.driver, WAIT_TIME).until(
    #             EC.element_to_be_clickable((By.ID, SEARCH_BAR_INPUT_ID))
    #         )

    #         # Method 1: JavaScript injection (most reliable for stubborn elements)
    #         self.driver.execute_script("arguments[0].value = '';", search_bar_input)
    #         self.driver.execute_script("arguments[0].focus();", search_bar_input)
            
    #         # Method 2: ActionChains fallback if JS fails
    #         try:
    #             ActionChains(self.driver).move_to_element(search_bar_input).click().pause(0.5).send_keys(user_to_search).perform()
    #         except:
    #             # Direct send_keys as last resort
    #             search_bar_input.send_keys(user_to_search)

    #         print("Searching for:", user_to_search)

    #         # Find button with clickable check
    #         search_bar_button = WebDriverWait(self.driver, WAIT_TIME).until(
    #             EC.element_to_be_clickable((By.XPATH, SEARCH_BAR_BUTTON_XPATH))
    #         )
            
    #         # Click with JavaScript fallback (handles overlay issues)
    #         try:
    #             search_bar_button.click()
    #         except:
    #             self.driver.execute_script("arguments[0].click();", search_bar_button)
    #     except Exception as e:
    #         traceback.print_exc()


    def split_list(self,lst, chunk_size):
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

    def print_file_content(self,path):
        """A function that print the content of a file"""
        f = open(path, 'r',encoding="utf-8")    
        content = f.read()
        f.close()
        return(content)

    def write_into_file(self,path, x):
        """A function that write into a file"""
        try:
            with open(path, "ab") as f:
                f.write(str(x).encode("utf-8"))
        except FileNotFoundError:
            pass

    def is_user_real2(self,user_to_search,batch_nb=0):
        try:
            self.driver.get(f"https://fr.wikipedia.org/wiki/{user_to_search}")
            info_box = WebDriverWait(self.driver, WAIT_TIME).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body"))
                )
            whole_page_text = info_box.text

            if "Personnage de fiction apparaissant dans" in whole_page_text:
                return False , f"https://fr.wikipedia.org/wiki/{user_to_search}"
            
            elif "Biographie" in whole_page_text and "Naissance" in whole_page_text:
                return True , f"https://fr.wikipedia.org/wiki/{user_to_search}"
            else:
                return False , f"https://fr.wikipedia.org/wiki/{user_to_search}"
            

        except:
            return None , f"https://fr.wikipedia.org/wiki/{user_to_search}"


    
    def clean_title(self,title):
        title = title.strip()

        # enlève seulement les guillemets extérieurs si présents
        if len(title) >= 2 and title[0] == '"' and title[-1] == '"':
            title = title[1:-1]

        title = unquote(title)
        title = title.replace("_", " ")
        
        return title.strip()
    

    def is_reaal(self,page_name):
        # Example: get article by title
        try:
            entry = self.zim.get_entry_by_title(self.clean_title(page_name))

            # Read raw HTML
            html = entry.get_item().content.tobytes().decode("utf-8", errors="replace")
            intro_text =  str(html[:10000])
            if "Personnage de fiction apparaissant dans".lower() in intro_text.lower():
                return False , f"https://fr.wikipedia.org/wiki/{page_name}"
            
            elif "biographie".lower() in intro_text.lower() and "naissance".lower() in intro_text.lower():
                return True , f"https://fr.wikipedia.org/wiki/{page_name}"
            else:
                return False , f"https://fr.wikipedia.org/wiki/{page_name}"
        except:
            #print("baaaaaad " , "titlee   " , page_name , " cleaaaned title " , self.clean_title(page_name))
            #traceback.print_exc()
            return None, f"https://fr.wikipedia.org/wiki/{page_name}"

    def run_script(self):
        
        

        split_list = self.split_list(self.all_file,self.chunck_size)
        #current_list = split_list[batch_nb]

        #already_done_page = self.print_file_content(rf"already_done_page_link{batch_nb}.txt").split("\n")

        for index , page in enumerate(self.all_file):
            if index % 100000 == 0 and index > 0:
                print(f"{page} {index}")

            try:
                is_real , page_link = self.is_reaal(page)
                page_name = page
                
                
                info_dict = str({"page_name":page_name,"link":page_link,"is_real":is_real})
                #print("goooood " , page) 
                if is_real:
                    self.write_into_file(rf"{CODE_PATH}\real_people_dir\dict_of_real_people.txt",info_dict+"\n")
                    self.write_into_file(rf"{CODE_PATH}\real_people_dir\list_of_real_people.txt",page_name+"\n")
                    self.write_into_file(rf"{CODE_PATH}\real_people_dir\list_of_real_people_diff.txt",self.clean_title(page_name)+"\n")
                
                elif is_real == False:
                    self.write_into_file(rf"{CODE_PATH}\non_real_people_dir\dict_of_non_real_people.txt",info_dict+"\n")
                    self.write_into_file(rf"{CODE_PATH}\non_real_people_dir\list_of_non_real_people.txt",page_name+"\n")
                    
                else:
                    self.write_into_file(rf"{CODE_PATH}\error_people_dir\dict_of_error_people.txt",info_dict+"\n")
                    self.write_into_file(rf"{CODE_PATH}\error_people_dir\list_of_error_people.txt",page_name+"\n")
            except:
                info_dict = str({})
                self.write_into_file(rf"{CODE_PATH}\error_people_dir\dict_of_error_people.txt",info_dict+"\n")
                self.write_into_file(rf"{CODE_PATH}\error_people_dir\list_of_error_people.txt",page_name+"\n")
            
x = WikiSrapping(True)
x.run_script()