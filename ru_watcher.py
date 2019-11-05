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
    :returns: Web content as a BeautifulSoup object
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

def get_daily_menu(soup, date):
    """
    Given a BeautifulSoup instance and a date, get the date's menu
    :returns: Menu in a string format
    """
    pattern = re.compile(date)
    tds = soup.find("td", text=pattern)
    if tds:
        menu = tds.parent.text
        return menu
    print(f"Data invalida({date}).")
    return None

def get_week_menu(soup):
    """TODO: Docstring for get_week_menu.
    :returns: TODO
    """
    trs = soup.findAll("tr")[1:8]
    menu = [x.text for x in trs]
    return '\n'.join(menu)

def help_text():
    """
    Prints argument help text
    """
    print("Uso: ru_watcher [Arg]")
    print("Arg pode ser:\n - help: mostra este texto\n - Data:")
    print("\t- hoje/today\n\t- amanha/tomorrow\n\t- formato %d.%m.%Y\n\t- dia (%d) \
            \n\t- semana/week")

def handle_date(soup, date):
    """
    Formats date correctly and returns menu accordingly
    :returns: Menu from given date
    """
    if date in ["hoje", "today"]:
        return get_daily_menu(soup, time.strftime("%d.%m.%Y"))
    if date in ["amanha", "tomorrow"]:
        tomorrow = datetime.date.today() + datetime.timedelta(hours=24)
        return get_daily_menu(soup, tomorrow.strftime("%d.%m.%Y"))
    if date.isdigit():
        return get_daily_menu(soup, str(date)+time.strftime(".%m.%Y"))
    if date.lower() in ["semana", "week"]:
        return get_week_menu(soup)
    help_text()
    return False

def main():
    """
    Main function. Defines url, calls handle_date and get_contents and prints the result of get_menu
    """
    if len(argv) != 2 or argv[1] in ["help", "ajuda"]:
        help_text()
        quit()

    date = argv[1].lower()

    url = "https://ru.ufsc.br/ru/"
    soup = get_contents(url)
    menu = handle_date(soup, date)

    if menu:
        print(menu)

if __name__ == "__main__":
    main()
