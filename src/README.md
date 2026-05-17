# File usage

- Wikiscraping.py is used to run the script that check if an user is real or not, get the link of all users and making the user link dict using zim file.
- Wikiselenium.py is used to run the script that check if an user is real or not, get the link of all users but this time using selenium so this file is used only to fetch data that failed under Wikiscraping.py run.
- Wikiscraping.py is used to run the script that check if an user is real or not using request instead of zim file or selenium.

First, we try to use the ZIM file. If it fails, we fall back to requests, and if that also fails, we use Selenium.

- Launch_script.py is used to run a file several time to make it go X time faster
- wikipeople.py is the file that handle the algorithm behind six-degrees-of-separation
