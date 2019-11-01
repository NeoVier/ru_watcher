#!/usr/bin/env python
"""
File: ru_watcher.py
Author: Henrique da Cunha Buss
Email: henrique.buss@hotmail.com
Github: https://github.com/NeoVier
Description: ru_watcher is a script to get the menu for a given day in UFSC's ru
"""

from sys import argv
import datetime
import time
import re
import requests
from bs4 import BeautifulSoup

def get_contents(url):
    """
    Returns web content from a given url
    :returns: web content in form of BeautifulSoup
    """
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.text, features="html.parser")
        return soup
    except ConnectionError:
        print("Erro na rede. Verifique sua conexao.")
        quit()
    except TimeoutError:
        print("Time out na requisicao.")
        quit()

def get_menu(soup, date):
    """
    Given a BeautifulSoup instance and a date, get the date's menu
    :returns: the menu in a string format
    """
    pattern = re.compile(date)
    tds = soup.find("td", text=pattern)
    if tds:
        menu = tds.parent.text
        return menu
    print(f"Data invalida({date}).")
    return None

def handle_args():
    """
    Handles all arguments
    :returns: Date as string
    """
    if len(argv) != 2 or argv[1] == "help":
        print("Uso: ru_watcher {Data}")
        print("Data pode ser:\n- hoje/today\n- amanha/tomorrow\n- formato %d.%m.%Y\n- dia (%d)")
        quit()
    date = argv[1].lower()
    if date in ["hoje", "today"]:
        return time.strftime("%d.%m.%Y")
    if date in ["amanha", "tomorrow"]:
        tomorrow = datetime.date.today() + datetime.timedelta(hours=24)
        return tomorrow.strftime("%d.%m.%Y")
    if date.isdigit():
        return str(date) + time.strftime(".%m.%Y")
    return date

def main():
    """
    Main function. Defines url, calls handle_args and get_contents and prints the result of get_menu
    """
    url = "https://ru.ufsc.br/ru/"
    date = handle_args()
    soup = get_contents(url)

    menu = get_menu(soup, date)
    if menu:
        print(menu)

if __name__ == "__main__":
    main()
