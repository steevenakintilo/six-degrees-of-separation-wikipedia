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

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re

import time
from global_variable import *
from urllib.parse import unquote

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
        path = rf"C:\Users\sakin\Desktop\code\six-degrees-of-separation-wikipedia\src\error_link_of_people_dir\error_link_of_people_page.txt"
        self.all_file = self.print_file_content(path).split("\n")
        xxx = 1
        
        self.size_of_batch_nb = xxx
        self.chunck_size = int(len(self.all_file)/self.size_of_batch_nb)
        
        self.all_real_people = self.print_file_content(rf"C:\Users\sakin\Desktop\code\six-degrees-of-separation-wikipedia\src\real_people_dir\list_of_real_people_diff.txt").split("\n")
        
        self.all_real_people_set = set(self.all_real_people)
     
        
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

    
    def get_all_link_of_a_page(self,page_name):
        # Example: get article by title
        #try:
        list_of_link = []
        # Read raw HTML
        # html = entry.get_item().content.tobytes().decode("utf-8", errors="replace")
        # #soup = BeautifulSoup(html, "html.parser")
        # #intro_text =  str(html[:10000])
        # intro_text = str(html)
        

        self.driver.get(f"https://fr.wikipedia.org/wiki/{page_name}")
        info_box = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body"))
        )
        text = self.driver.page_source

        #split_link = intro_text.split("<a href=")
        titles = re.findall(r'<a\s[^>]*title="([^"]+)"', text)

        #print(titles)
        for title in titles:
            if title in self.all_real_people_set and title not in list_of_link:
                list_of_link.append(title)
        # for link in split_link:
        #     if "title=" in link:
        #         split_link_ = link.split("title=")[1].split(">")
        #         link_name = split_link_[0].replace('"',"")
        #         if link_name in self.all_real_people_set and link_name not in list_of_link:
        #             list_of_link.append(link_name)
                
        #print(soup.get_text()[:1000])
        
        #print(list_of_link)
        return list_of_link
        #print(intro_text.split("<a href="))
        # except:
        #     return ["error","Nan","404"]
        #     traceback.print_exc()
        #     return ""

    def is_user_real(self, user_to_search, batch_nb=0):
        try:
            url = f"https://fr.wikipedia.org/wiki/{user_to_search}"
            self.driver.get(f"https://fr.wikipedia.org/wiki/{user_to_search}")
            info_box = WebDriverWait(self.driver, WAIT_TIME).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body"))
            )
            text = info_box.text
            text_normal = info_box.text
                            
            
            if "_en_" in user_to_search and "Biographies" in text_normal:
                return False,url
            skip = False
            for word in banned_word:
                if word in user_to_search:
                    #print("yooooo " , name)
                    skip = True
                    break
            


            if "Cet article présente les faits marquants de" in text_normal:
                return False, url    
            if "Cet article concerne des événements prévus ou attendus." in text_normal:
                return False, url    
            
            if "Le présent article donne différentes informations sur" in text_normal:
                return False , url
            
            if "Cette page concerne des événements d'actualité qui se sont produits" in text_normal:
                return False, url    
            if skip:
                return False, url
            
            # ---- FICTION ----
            if (
                "personnage de fiction apparaissant dans" in text or
                "personnage de fiction" in text or
                "personnage fictif" in text or
                "personnage de jeu vidéo" in text or
                "personnage de bande dessinée" in text or
                "personnage de cinéma" in text or
                "personnage de série télévisée" in text or
                "catégorie:personnage de fiction" in text
            ):
                return False, url

            # ---- VRAIE PERSONNE : infobox ----
            if ((
                    "nom de naissance" in text or
                    "date de naissance" in text or
                    "lieu de naissance" in text
                ) and (
                    "Biographie" in text_normal or
                    "informations générales" in text
                )
            ) or (
                
                ("naissance" in text and "activité principale" in text) or 
                ("Biographie" in text_normal and "naissance" in text) or 
                ("Biographie" in text_normal and "décès" in text)
            ):    return True, url

            # ---- VRAIE PERSONNE : catégories ----
            if (
                "catégorie:naissance en " in text or
                "catégorie:naissance à " in text or
                "catégorie:naissance dans " in text or
                "catégorie:décès en " in text or
                "catégorie:décès à " in text or
                "catégorie:personnalité" in text or
                "catégorie:chanteur" in text or
                "catégorie:chanteuse" in text or
                "catégorie:acteur" in text or
                "catégorie:actrice" in text or
                "catégorie:écrivain" in text or
                "catégorie:écrivaine" in text or
                "catégorie:musicien" in text or
                "catégorie:musicienne" in text or
                "catégorie:homme politique" in text or
                "catégorie:femme politique" in text or
                "catégorie:scientifique" in text or
                "catégorie:peintre" in text or
                "catégorie:réalisateur" in text or
                "catégorie:réalisatrice" in text
            ):
                return True, url

            return False, url

        except requests.RequestException:
            return None, url


    def clean_title(self,title):
        title = title.strip()

        # enlève seulement les guillemets extérieurs si présents
        if len(title) >= 2 and title[0] == '"' and title[-1] == '"':
            title = title[1:-1]

        title = unquote(title)
        title = title.replace("_", " ")
        
        return title.strip()

    
    def run_script(self,batch_nb):
        
        

        # split_list = self.split_list(self.all_file,self.chunck_size)
        # current_list = split_list[batch_nb]

        #already_done_page = self.print_file_content(rf"already_done_page_link{batch_nb}.txt").split("\n")
        for index , page in enumerate(self.all_file):
            
            if index % (len(self.all_file) / 10) == 0:
                print(f"{page} {index} {(index/int(len(self.all_file))) * 100}% done")

            try:
                is_real , page_link = self.is_user_real(page)
                # if page_link in already_done_page:
                #     continue

                #page_name = current_list[batch_nb]
                
                
                info_dict = str({"page_name":page,"link":page_link,"is_real":is_real})
                time.sleep(0.1)

                if is_real:
                    self.write_into_file(rf"{CODE_PATH}\real_people_dir\dict_of_real_people{batch_nb}.txt",info_dict+"\n")
                    self.write_into_file(rf"{CODE_PATH}\real_people_dir\list_of_real_people{batch_nb}.txt",page+"\n")
                    self.write_into_file(rf"{CODE_PATH}\real_people_dir\list_of_real_people_diff{batch_nb}.txt",self.clean_title(page)+"\n")

                    # self.write_into_file(rf"already_done_element{batch_nb}.txt",page_name+"\n")
                    # self.write_into_file(rf"already_done_page_link{batch_nb}.txt",page_link+"\n")

                elif is_real == False:
                    self.write_into_file(rf"{CODE_PATH}\non_real_people_dir\dict_of_non_real_people{batch_nb}.txt",info_dict+"\n")
                    self.write_into_file(rf"{CODE_PATH}\non_real_people_dir\list_of_non_real_people{batch_nb}.txt",page+"\n")
                    # self.write_into_file(rf"already_done_element{batch_nb}.txt",page_name+"\n")
                    # self.write_into_file(rf"already_done_page_link{batch_nb}.txt",page_link+"\n")
                    
                else:
                    self.write_into_file(rf"{CODE_PATH}\error_people_dir\dict_of_error_people{batch_nb}.txt",info_dict+"\n")
                    self.write_into_file(rf"{CODE_PATH}\error_people_dir\list_of_error_people{batch_nb}.txt",page+"\n")
                    # self.write_into_file(rf"already_done_element{batch_nb}.txt",page_name+"\n")
                    # self.write_into_file(rf"already_done_page_link{batch_nb}.txt",page_link+"\n")
            except:
                info_dict = str({})
                #traceback.print_exc()
                self.write_into_file(rf"{CODE_PATH}\error_people_dir\dict_of_error_people{batch_nb}.txt",info_dict+"\n")
                self.write_into_file(rf"{CODE_PATH}\error_people_dir\list_of_error_people{batch_nb}.txt",page+"\n")
                # self.write_into_file(rf"already_done_element{batch_nb}.txt",page_name+"\n")
                # self.write_into_file(rf"already_done_page_link{batch_nb}.txt",page_link+"\n")


    def run_link_script(self,batch_nb):
        
        #split_list = self.split_list(self.all_real_people,self.chunck_size)
        current_list = self.all_file
        
        #already_done_page = self.print_file_content(rf"already_done_page_link{batch_nb + 1}.txt").split("\n")

        for index , page in enumerate(current_list):
            if len(page) == 0 or len(page.replace(" ","")) == 0:
                continue
            if index % int(len(current_list) / 10) == 0 and batch_nb == 2:
                print(f"{page} {index} {batch_nb} {(index/int(len(current_list))) * 100}% done")
            
            try:
                list_of_link = self.get_all_link_of_a_page(page)
                time.sleep(0.1)
                self.write_into_file(rf"{CODE_PATH}\link_of_people_dir\link_of_people_link{batch_nb + 1}.txt",str({"page_name":page,"list_of_link":list_of_link})+"\n")

            except:
                self.write_into_file(rf"{CODE_PATH}\error_link_of_people_dir\error_link_of_people_link{batch_nb + 1}.txt",str({"page_name":page,"list_of_link":[]})+"\n")
                self.write_into_file(rf"{CODE_PATH}\error_link_of_people_dir\error_link_of_people_page{batch_nb + 1}.txt",page+"\n")
                


x = WikiSrapping(True)
x.run_link_script(int(sys.argv[1]))
