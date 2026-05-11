"""File that handle global variable"""
import os

# pylint: disable=all

WIKIPEDIA_URL = "https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal"
SEARCH_BAR_INPUT_ID = "searchform"
SEARCH_BAR_BUTTON_XPATH = "/html/body/div[2]/header/div[2]/div/div/div/div/form/div/button"
INFO_BOX_XPATH = "/html/body/div[3]/div/div[3]/main/div[3]/div[3]/div[1]/table[1]"
WAIT_TIME = 5

CODE_PATH = os.getcwd().replace("","")
