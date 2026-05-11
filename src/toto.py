import wikipediaapi

import random
import time

def print_file_content(path):
    """A function that print the content of a file"""
    f = open(path, 'r',encoding="utf-8")    
    content = f.read()
    f.close()
    return(content)

def write_into_file(path, x):
    """A function that write into a file"""
    try:
        with open(path, "ab") as f:
            f.write(str(x).encode("utf-8"))
    except FileNotFoundError:
        pass



start = time.time()

#test = "Section_des_Gobelins"
test = "cancer"


# all_file = print_file_content("../all_wikipedia_page_fr.txt").split("\n")
# random_page = random.choice(all_file)
# print(random_page)

wiki_wiki = wikipediaapi.Wikipedia(user_agent='MyProjectName (merlin@example.com)', language='fr')

page_py = wiki_wiki.page(test)
print(page_py.text)
write_into_file("toto.txt",page_py.text)

end = time.time()

print(f"Total runtime of the program is {end - start} seconds")

