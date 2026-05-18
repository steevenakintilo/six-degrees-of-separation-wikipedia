# pylint: disable=all
import ijson
import time
import json

import sys
try:
    MAX_NUMBER_OF_DEPTH = int(sys.argv[1])
except:
    MAX_NUMBER_OF_DEPTH = 2500

if MAX_NUMBER_OF_DEPTH < 100:
    MAX_NUMBER_OF_DEPTH = 500
sys.setrecursionlimit(MAX_NUMBER_OF_DEPTH)

#FILE_PATH = rf"C:\Users\sakin\Desktop\code\six-degrees-of-separation-wikipedia\src\list_of_link_of_all_users.json"
FILE_PATH = rf"C:\Users\sakin\Desktop\code\six-degrees-of-separation-wikipedia\src\list_of_link_of_all_users_sorted.json"

class WikiNode():
    """"""
    def __init__(self):
        #self.person1 = ""
        #self.person2 = ""
        self.list_of_people_link_dict = ijson.parse(open(FILE_PATH, 'r'))
        self.max_number_of_depth = MAX_NUMBER_OF_DEPTH
        self.path_of_people = []
        self.path_of_people_list_of_list = []
        self.path_of_people_list_of_list_len = []
        self.list_of_path_by_sub_user = []
        
        # self.all_real_people = self.print_file_content(rf"C:\Users\sakin\Desktop\code\six-degrees-of-separation-wikipedia\src\real_people_dir\real_people_diff_withouth_doublon.txt").split("\n")
        # self.all_real_people_set = set(self.all_real_people)

        
        self.final_path_list = []
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            self.people_links = json.load(file)
        
        pass


    def print_file_content(self,path):
        """A function that print the content of a file"""
        f = open(path, 'r',encoding="utf-8")    
        content = f.read()
        f.close()
        return(content)
    
    def get_person_links(self, name):
        name = name.replace("_"," ")
        return self.people_links.get(name, [])
        # with open(FILE_PATH, "r", encoding="utf-8") as file:
        #     for person, links in ijson.kvitems(file, ""):
        #         #if person.startswith("Jean-Pierre Ber"):
        #         #    print(person)
        #         if person == name:
        #             return links

        return []
    


    #def sort_list_by_popularity():
    
    def loop_through_people(self,page_name,base_person="",target_person="",nb_max=0):
        
        link_of_user = self.get_person_links(page_name)
        self.path_of_people.append(page_name)
        self.list_of_path_by_sub_user.append(link_of_user)
        if nb_max > self.max_number_of_depth:
            #print("oooooh")
            #time.sleep(10000)
            return
        
        #print(page_name,link_of_user,nb_max)
        
        if target_person in link_of_user:
            #print("yeeeaaaaah")
            
            self.path_of_people.append(target_person)
            if self.path_of_people.count(target_person) == 1:
                self.final_path_list = [base_person] + self.path_of_people
                #print(self.final_path_list,len(self.final_path_list))
                self.path_of_people_list_of_list.append(self.final_path_list)
                self.path_of_people_list_of_list_len.append(len(self.final_path_list))
                
            return
            #time.sleep(100000)
        
        if nb_max <= self.max_number_of_depth and target_person not in link_of_user:
            for user in link_of_user:
                if user == "Autobiographie":
                    continue
                link_of_next_user = self.get_person_links(user)
                
                #if user not in self.path_of_people and link_of_user != link_of_next_user and len(link_of_next_user) != 0 and user != base_person and link_of_next_user not in self.list_of_path_by_sub_user:

                if user not in self.path_of_people and link_of_user != link_of_next_user and len(link_of_next_user) != 0 and user != base_person:
                    self.loop_through_people(user,base_person,target_person,nb_max+1)
        pass
    

    def fix_list(self):
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            self.people_top = json.load(file)
        
        index = 0
        list_of_occurence = []
        list_of_user = []
        dict_link_sorted = {}
        skip = False
        for user,user_links in self.people_links.items():
            skip = False
            list_of_occurence = []
            list_of_user = []
            for u in user_links:
                
                try:
                    list_of_user.append(u)
                    list_of_occurence.append(self.people_top[u.replace("_"," ")])
                    # else:
                    #     print("not in set " , u)
                except:
                    skip = True   

            if skip:
                dict_link_sorted[user] = user_links
                continue
            if len(list_of_user) != 0:
                #print(list_of_user, list_of_occurence)
                paired = list(zip(list_of_user, list_of_occurence))

                paired.sort(key=lambda x: x[1], reverse=True)

                list_of_element, occurence_of_element_list = zip(*paired)
                list_of_element = list(list_of_element)
                occurence_of_element_list = list(occurence_of_element_list)
                dict_link_sorted[user] = list_of_element 
                if index % 90000 == 0:
                    print(user,user_links)
                    print(list_of_element,occurence_of_element_list)
                    print("\n\n\n\n")
                
                
            else:
                dict_link_sorted[user] = user_links    
                #pass    
            if index % 90000 == 0:
                pass
                #print(user,user_links,self.people_top.get(user.replace("_"," "), int))
            index+=1
            
                
        
        #print(dict_link_sorted)

        with open("list_of_link_of_all_users_sorted.json", "w",encoding="utf-8") as f:
            json.dump(dict_link_sorted, f,ensure_ascii=False,indent=4)
    
    def start(self):
        
        # self.fix_list()
        # return
        
        
        start = time.time()
        person1 = "Jean-Pierre_Bertrand_(pianiste)"
        person2 = "Ray Charles"
        
        person2 = "Jules César"
        person2 = "Mahomet"
        person2 = "Jésus de Nazareth"
        person2 = "Wolfgang Amadeus Mozart"
        person1 = "Emmanuel Macron"
        person2 = "Linus Torvalds"
        #person2 = "Billie Eilish"
        #person2 = "Mao Zedong"
        
        #person2 = "David Belle"
        
        #person2 = "Billie Eilish"
        #person1 = "Eugène Devéria"
        #person1 = "Emmanuel Macron"
        
        #person2 = "Mao Zedong"
        
        self.path_of_people.append(person1)
        link_of_person1 = self.get_person_links(person1)
        link_of_person2 = self.get_person_links(person2)
        
        print(link_of_person1)
        #print(link_of_person2)
        
        
        if len(link_of_person1) == 0:
            print(f"{person1} has no links on it's wikipedia page")
            return
        if person2 in link_of_person1:
            print(f"{person2} is inside the wikipedia of {person1}")
            return
        #print(self.get_person_links(person2))
        print("\n\n\n")
        for user in link_of_person1:
            #print(user , " copekfpoezkfzekf")
            if user == "Autobiographie":
                continue
            self.path_of_people = []
            self.list_of_path_by_sub_user = []
            try:
                self.loop_through_people(user,person1,person2)
            except RecursionError:
                #print(self.path_of_people)
                continue
           
        
        if len(self.path_of_people_list_of_list) == 0:
            print(f"No link found between {person1} and {person2}")
        else:
            
            paired = list(zip(self.path_of_people_list_of_list, self.path_of_people_list_of_list_len))

            paired.sort(key=lambda x: x[1], reverse=False)

            list_of_element, occurence_of_element_list = zip(*paired)
            list_of_element = list(list_of_element)
            occurence_of_element_list = list(occurence_of_element_list)
            
            smallest_people_list = list_of_element[0]
            print(f"Number of path found {len(self.path_of_people_list_of_list)}")
            print(f"All path size {occurence_of_element_list}")
            print(f"Smallest path size {len(smallest_people_list)}")
            print(smallest_people_list)
            print(f"Smallest path size {len(smallest_people_list)}")
            
        
        end = time.time()

        print(f"Total runtime of the program is {end - start} seconds")

        
        pass
