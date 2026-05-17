"""File that handle wikepedia scrapping"""

# pylint: disable=all

import os

from random import randint

import time
import traceback
import yaml

import sys

# from selenium.webdriver.common.by import By
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains

from libzim.reader import Archive
from urllib.parse import unquote

#from bs4 import BeautifulSoup


import time
from global_variable import *
import re
import ast 
import json

from collections import Counter

class Scrapdata():
    def __init__(self,headless=False):
        # self.headless = headless
        # self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--log-level=1')
        # self.options.add_argument("--log-level=3")
        # if self.headless:
        #     self.options.add_argument('headless')

        # self.options.add_experimental_option("useAutomationExtension", False)
        # self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # self.options.add_argument("--start-maximized")
        # self.options.add_argument("--disable-gpu")
        # self.options.add_argument("--disable-dev-shm-usage")
        # self.driver = webdriver.Chrome(options=self.options)
        # self.driver.set_page_load_timeout(15)
        pass

class WikiSrapping(Scrapdata):
    def __init__(self,headless=False):
        #self.driver = Scrapdata(headless).driver
        self.all_file = self.print_file_content("../all_wikipedia_page_fr.txt").split("\n")
        #self.all_real_people = self.print_file_content(rf"{CODE_PATH}\real_people_dir\list_of_real_people_diff.txt").split("\n")
        self.all_real_people = self.print_file_content(rf"C:\Users\sakin\Desktop\code\six-degrees-of-separation-wikipedia\src\real_people_dir\real_people_diff_withouth_doublon.txt").split("\n")
        
        self.all_real_people_set = set(self.all_real_people)
        
        self.size_of_batch_nb = 100
        self.chunck_size = int(len(self.all_real_people_set)/self.size_of_batch_nb)
        #self.chunck_size = 10
        #self.zim = Archive("../wikipedia_fr_all_maxi_2026-02.zim")
        self.zim = Archive(rf"C:\Users\sakin\Desktop\code\six-degrees-of-separation-wikipedia\wikipedia_fr_all_maxi_2026-02.zim")
        

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
    

    def is_reaal(self, page_name):
        try:
            entry = self.zim.get_entry_by_title(self.clean_title(page_name))

            html = entry.get_item().content.tobytes().decode("utf-8", errors="replace")
            text = html[:10000].lower()
            text_normal = html[:10000]
            
            if "fonctions" in text:
                text = html[:100000].lower()    
                text_normal = html[:100000]
            
                
            url = f"https://fr.wikipedia.org/wiki/{page_name}"

            if "_en_" in page_name and "Biographies" in text_normal:
                return False,url
            skip = False
            for word in banned_word:
                if word in page_name:
                    #print("yooooo " , name)
                    skip = True
                    break
            


            if "Cet article présente les faits marquants de" in text_normal:
                return False, url    
            if "Cet article concerne des événements prévus ou attendus." in text_normal:
                return False, url    
                
            if "Cette page concerne des événements d'actualité qui se sont produits" in text_normal:
                return False, url    
            if "Le présent article donne différentes informations sur" in text_normal:
                return False , url
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

        except:
            return None, f"https://fr.wikipedia.org/wiki/{page_name}"

    def get_all_link_of_a_page(self,page_name):
        # Example: get article by title
        #try:
        entry = self.zim.get_entry_by_title(self.clean_title(page_name))
        list_of_link = []
        # Read raw HTML
        html = entry.get_item().content.tobytes().decode("utf-8", errors="replace")
        #soup = BeautifulSoup(html, "html.parser")
        #intro_text =  str(html[:10000])
        intro_text = str(html)
        #split_link = intro_text.split("<a href=")
        titles = re.findall(r'<a\s[^>]*title="([^"]+)"', html)

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
        
    def merge_file(self,batch_nb):
        dict_of_real_people = []
        list_of_real_people = []
        list_of_real_people_diff = []
        
        dict_of_non_real_people = []
        list_of_non_real_people = []
        
        dict_of_error_people = []
        list_of_error_people = []
        
        for i in range(1 , batch_nb + 1):
            print(i)
            dict_of_real_people+=self.print_file_content(rf"{CODE_PATH}\real_people_dir\dict_of_real_people{i}.txt").split("\n")
            list_of_real_people+=self.print_file_content(rf"{CODE_PATH}\real_people_dir\list_of_real_people{i}.txt").split("\n")
            list_of_real_people_diff+=self.print_file_content(rf"{CODE_PATH}\real_people_dir\list_of_real_people_diff{i}.txt").split("\n")

            dict_of_non_real_people+=self.print_file_content(rf"{CODE_PATH}\non_real_people_dir\dict_of_non_real_people{i}.txt").split("\n")
            list_of_non_real_people+=self.print_file_content(rf"{CODE_PATH}\non_real_people_dir\list_of_non_real_people{i}.txt").split("\n")
            
            dict_of_error_people+=self.print_file_content(rf"{CODE_PATH}\error_people_dir\dict_of_error_people{i}.txt").split("\n")
            list_of_error_people+=self.print_file_content(rf"{CODE_PATH}\error_people_dir\list_of_error_people{i}.txt").split("\n")
            
        print("REAL PEOPLE")
        for elem in dict_of_real_people:
            if len(elem) == 0:
                continue
                
            self.write_into_file(rf"{CODE_PATH}\real_people_dir\dict_of_real_people.txt",elem+"\n")
        for elem in list_of_real_people:
            if len(elem) == 0:
                continue
            
            self.write_into_file(rf"{CODE_PATH}\real_people_dir\list_of_real_people.txt",elem+"\n")
        for elem in list_of_real_people_diff:
            if len(elem) == 0:
                continue
            
            self.write_into_file(rf"{CODE_PATH}\real_people_dir\list_of_real_people_diff.txt",elem+"\n")
        
        print(len(dict_of_real_people))
        print(len(list_of_real_people))
        print(len(list_of_real_people_diff))
        print("\n")

        print("NON REAL PEOPLE")

        for elem in dict_of_non_real_people:
            if len(elem) == 0:
                continue
            
            self.write_into_file(rf"{CODE_PATH}\non_real_people_dir\dict_of_non_real_people.txt",elem+"\n")
        for elem in list_of_non_real_people:
            if len(elem) == 0:
                continue
            
            self.write_into_file(rf"{CODE_PATH}\non_real_people_dir\list_of_non_real_people.txt",elem+"\n")
        
        print(len(dict_of_non_real_people))
        print(len(list_of_non_real_people))
        print("\n")
        
        print("ERROR PEOPLE")

        for elem in dict_of_error_people:
            if len(elem) == 0:
                continue
            
            self.write_into_file(rf"{CODE_PATH}\error_people_dir\dict_of_error_people.txt",elem+"\n")
        for elem in list_of_error_people:
            if len(elem) == 0:
                continue
            
            self.write_into_file(rf"{CODE_PATH}\error_people_dir\list_of_error_people.txt",elem+"\n")
        

        print(len(dict_of_error_people))
        print(len(list_of_error_people))
        print("\n")



    def merge_file2(self,batch_nb):
        dict_of_real_people = []
        
        for i in range(1 , batch_nb + 1):
            print(i)
            try:
                dict_of_real_people+=self.print_file_content(rf"{CODE_PATH}\link_of_people_dir\link_of_people_link{i}.txt").split("\n")
            except:
                pass
        
        print("REAL PEOPLE")
        for elem in dict_of_real_people:
            if len(elem) == 0:
                continue
                
            self.write_into_file(rf"{CODE_PATH}\link_of_people_dir\link_of_people_link.txt",elem+"\n")
        
        print(len(dict_of_real_people))
        print("\n")

        
    def run_script(self,batch_nb):
        
        split_list = self.split_list(self.all_file,self.chunck_size)
        current_list = split_list[batch_nb]

        #already_done_page = self.print_file_content(rf"already_done_page_link{batch_nb + 1}.txt").split("\n")
        
        for index , page in enumerate(current_list):
            if index % int(len(current_list) / 10) == 0 and batch_nb == 1:
            
                print(f"{page} {index} {(index/int(len(current_list))) * 100}% done")
            
            try:
                is_real , page_link = self.is_reaal(page)
                page_name = page
                
                
                info_dict = str({"page_name":page_name,"link":page_link,"is_real":is_real})
                #print("goooood " , page) 
                if is_real:
                    self.write_into_file(rf"{CODE_PATH}\real_people_dir\dict_of_real_people{batch_nb + 1}.txt",info_dict+"\n")
                    self.write_into_file(rf"{CODE_PATH}\real_people_dir\list_of_real_people{batch_nb + 1}.txt",page_name+"\n")
                    self.write_into_file(rf"{CODE_PATH}\real_people_dir\list_of_real_people_diff{batch_nb + 1}.txt",self.clean_title(page_name)+"\n")
                
                elif is_real == False:
                    self.write_into_file(rf"{CODE_PATH}\non_real_people_dir\dict_of_non_real_people{batch_nb + 1}.txt",info_dict+"\n")
                    self.write_into_file(rf"{CODE_PATH}\non_real_people_dir\list_of_non_real_people{batch_nb + 1}.txt",page_name+"\n")

                elif is_real == "Maybe":
                    self.write_into_file(rf"{CODE_PATH}\maybe_real_people_dir\dict_of_maybe_real_people{batch_nb + 1}.txt",info_dict+"\n")
                    self.write_into_file(rf"{CODE_PATH}\maybe_real_people_dir\list_of_maybe_real_people{batch_nb + 1}.txt",page_name+"\n")
                  
                else:
                    self.write_into_file(rf"{CODE_PATH}\error_people_dir\dict_of_error_people{batch_nb + 1}.txt",info_dict+"\n")
                    self.write_into_file(rf"{CODE_PATH}\error_people_dir\list_of_error_people{batch_nb + 1}.txt",page_name+"\n")
            except:
                info_dict = str({})
                self.write_into_file(rf"{CODE_PATH}\error_people_dir\dict_of_error_people{batch_nb + 1}.txt",info_dict+"\n")
                self.write_into_file(rf"{CODE_PATH}\error_people_dir\list_of_error_people{batch_nb + 1}.txt",page_name+"\n")



    def run_link_script(self,batch_nb):
        split_list = self.split_list(self.all_real_people,self.chunck_size)
        current_list = split_list[batch_nb]
        
        #already_done_page = self.print_file_content(rf"already_done_page_link{batch_nb + 1}.txt").split("\n")

        for index , page in enumerate(current_list):
            if len(page) == 0 or len(page.replace(" ","")) == 0:
                continue
            
            if index % int(len(current_list) / 10) == 0 and batch_nb == 2:
                print(f"{page} {index} {batch_nb} {(index/int(len(current_list))) * 100}% done")
            
            try:
                list_of_link = self.get_all_link_of_a_page(page)
                self.write_into_file(rf"{CODE_PATH}\link_of_people_dir\link_of_people_link{batch_nb + 1}.txt",str({"page_name":page,"list_of_link":list_of_link})+"\n")

            except:
                self.write_into_file(rf"{CODE_PATH}\error_link_of_people_dir\error_link_of_people_link{batch_nb + 1}.txt",str({"page_name":page,"list_of_link":[]})+"\n")
                self.write_into_file(rf"{CODE_PATH}\error_link_of_people_dir\error_link_of_people_page{batch_nb + 1}.txt",page+"\n")
    
    def remove_page_name_from_link(self,page_name,list_of_link):
        new_list_of_link = []
        
        if page_name not in list_of_link:
            return list_of_link
        
        for link in list_of_link:
            skip = False
            for word in banned_word:
                if word in link:
                    skip = True
                    break
            if page_name != link and skip == False:
                new_list_of_link.append(link)
        
        return new_list_of_link
    
    def merge_dict(self):
        list_of_dict_link = self.print_file_content(rf"{CODE_PATH}\link_of_people_dir\link_of_people_link.txt").split("\n")
        dict_of_link = {}
        

        for i , link in enumerate(list_of_dict_link):
            if i % 93000 == 0:
                print(link , int(i/93000) * 10 , "blobloa merge_dict")
            
            try:
                current_dict = ast.literal_eval(link)
                name = current_dict["page_name"]
                skip = False
                for word in banned_word:
                    if word in name:
                        #print("yooooo " , name)
                        skip = True
                        break
                
                if skip:
                    continue
                # print(type(current_dict["list_of_name"]))
                # print(current_dict["list_of_name"])
                
                if skip is False:
                    list_of_link = self.remove_page_name_from_link(current_dict["page_name"],current_dict["list_of_link"])
                    dict_of_link[name] = list_of_link
                    
            except:
                dict_of_link[name] = []
        
        with open("list_of_link_of_all_users.json", "w",encoding="utf-8") as f:
            json.dump(dict_of_link, f,ensure_ascii=False,indent=4)
    
    def calc_stat(self):
        list_of_dict_link = self.print_file_content(rf"{CODE_PATH}\link_of_people_dir\link_of_people_link.txt").split("\n")
        nb_total = 0
        nb_total_with_link = 0
        nb_of_people_withouth_link = 0
        nb_of_people_with_link = 0
        list_of_link_nb = []
        list_of_link_name = []
        
        list_of_link_name2 = []
        list_of_link_name_ = []
        
        dict_of_number_of_link_per_page_sorted = {}
        dict_of_people_who_are_the_most_linked_sorted = {}
        
        list_of_link_name_occurence = []
        for i , link in enumerate(list_of_dict_link):
            if i % 93000 == 0:
                print(link , int(i/93000) * 10)
            
            try:
                current_dict = ast.literal_eval(link)
                name = current_dict["page_name"]
                skip = False
                for word in banned_word:
                    if word in name:
                        #print("yooooo " , name)
                        skip = True
                        break
                
                if skip:
                    continue
                
                # print(type(current_dict["list_of_name"]))
                # print(current_dict["list_of_name"])

                list_of_link = self.remove_page_name_from_link(current_dict["page_name"],current_dict["list_of_link"])
                nb_total+=len(list_of_link)
                list_of_link_nb.append(len(list_of_link))
                list_of_link_name.append(name)
                list_of_link_name_.append(name)
                for elem in list_of_link:
                    list_of_link_name2.append(elem)

                if len(list_of_link) == 0:
                    nb_of_people_withouth_link+=1
                else:
                    nb_of_people_with_link+=1
                    nb_total_with_link+=len(list_of_link)
                
                
            except:
                list_of_link_nb.append(0)
                list_of_link_name.append(name)
                
                pass
        

        # for name in list_of_link_name:
        #     list_of_link_name_occurence.append(list_of_link_name2.count(name))
        
        counts = Counter(list_of_link_name2)

        list_of_link_name_occurence = [
            counts.get(name, 0)
            for name in list_of_link_name
        ]
        print(f"Number of page on the whole wikipedia fr {len(self.all_file)}")
        print(f"% of real human page on the whole wikipedia fr {int((len(list_of_dict_link) / len(self.all_file)) * 100)}")
        print(f"% of non real human page on the whole wikipedia fr {100 - int((len(list_of_dict_link) / len(self.all_file)) * 100)}")
        print(f"Number of people on the whole wikipedia fr {len(list_of_dict_link)}")
        print(f"Number of total link of the whole wikipedia fr {nb_total}")
        print(f"Average number of link per person on the whole wikipedia fr {round(len(list_of_dict_link)/nb_total,2)}")
        print(f"Number of people withouth a link on the whole wikipedia fr {nb_of_people_withouth_link}")
        print(f"% of people withouth a link on the whole wikipedia fr {int((nb_of_people_withouth_link/len(list_of_dict_link)) * 100)}")
        print(f"Number of people with a link on the whole wikipedia fr {len(list_of_dict_link) - nb_of_people_withouth_link}")
        print(f"% of people with a link on the whole wikipedia fr {100 - int((nb_of_people_withouth_link/len(list_of_dict_link)) * 100)}")
        print(f"Average number of link per person who have atleast 1 link on the whole wikipedia fr {round((nb_of_people_with_link - nb_of_people_withouth_link)/nb_total_with_link,2)}")
        
        paired = list(zip(list_of_link_name, list_of_link_nb))

        paired.sort(key=lambda x: x[1], reverse=True)

        try:
            list_of_element, occurence_of_element_list = zip(*paired)
        except:
            return [] , []
        list_of_element = list(list_of_element)
        occurence_of_element_list = list(occurence_of_element_list)
        
        for i in range(10):
            print("Most Link on this page: " ,list_of_element[i],occurence_of_element_list[i])
        
        for i in range(len(list_of_element)):
            dict_of_number_of_link_per_page_sorted[list_of_element[i]] = occurence_of_element_list[i]
        
        
        #print(list_of_element[0:9])
        
        
        paired = list(zip(list_of_link_name_, list_of_link_name_occurence))

        paired.sort(key=lambda x: x[1], reverse=True)

        try:
            list_of_element, occurence_of_element_list = zip(*paired)
        except:
            return [] , []
        list_of_element = list(list_of_element)
        occurence_of_element_list = list(occurence_of_element_list)
        print("\n\n\n\n")
        
        for i in range(len(list_of_element)):
            dict_of_people_who_are_the_most_linked_sorted[list_of_element[i]] = occurence_of_element_list[i]
        
        for i in range(10):
            print("Most Linked user: " , list_of_element[i],occurence_of_element_list[i])
        

        
        
        with open("list_of_page_with_the_most_link.json", "w",encoding="utf-8") as f:
            json.dump(dict_of_number_of_link_per_page_sorted, f,ensure_ascii=False,indent=4)
        
        with open("list_of_most_linked_user.json", "w",encoding="utf-8") as f:
            json.dump(dict_of_people_who_are_the_most_linked_sorted, f,ensure_ascii=False,indent=4)
        
        

a = 5


# Get all real user using zim

# x = WikiSrapping(True)
# x.run_script(int(sys.argv[1]))

# # Merging all the file of real people into a big one

# x = WikiSrapping(True)
# x.merge_file(x.size_of_batch_nb)

# # Get all real user link using zim

# x = WikiSrapping(True)
# x.run_link_script(int(sys.argv[1]))

# # Merging all the file of real people link into a big one
# x = WikiSrapping(True)
# x.merge_file2(x.size_of_batch_nb)

# # Merging all link stat into a dict and gettting some statistics
x = WikiSrapping(True)
# # r = x.get_all_link_of_a_page("Lili_Leignel")
# # print(r)
x.merge_dict()
x.calc_stat()


# if a == 1:
#     x = WikiSrapping(True)
#     # x.merge_file(x.size_of_batch_nb)
#     x.run_script(int(sys.argv[1]))
#     end = time.time()

#     print(f"Total runtime of the program is {end - start} seconds")

# if a == 2:
#     x = WikiSrapping(True)
#     x.merge_file(x.size_of_batch_nb)



# if a == 3:
#     x = WikiSrapping(True)
#     x.run_link_script(int(sys.argv[1]))

# if a == 4:
#     x = WikiSrapping(True)
#     x.merge_file2(300)

# if a == 5:
#     x = WikiSrapping(True)
#     #x.merge_dict()
#     x.calc_stat()

# x = WikiSrapping(True)
# # r = x.is_reaal("Emmanuel_Macron")
# print(r)
