#!/usr/bin/env python
"""
File: ru_watcher.py
Author: Henrique da Cunha Buss
Email: henrique.buss@hotmail.com
Github: https://github.com/NeoVier
Description: ru_watcher is a script to get the menu for a given day in UFSC's ru
"""

from sys import argv            # Command line arguments
from pathlib import Path        # Handle directory and file locations
from os import remove           # Clear cache file
import datetime                 # Handle dates
import time                     # Handle dates
import pickle                   # Write and read contents from file
import requests                 # Get HTML Content from web page
from bs4 import BeautifulSoup   # Parse HTML


def dump_week(week, location):
    """
    :week: Content to be dumped
    :location: Location of file to be written
    """
    with open(location, 'wb') as cache_file:
        pickle.dump(week, cache_file)

def read_file(location):
    """
    :location: Path to file
    :returns: Contents of file if it exists. Else, None
    """
    try:
        with open(location, 'rb') as cache_file:
            contents = pickle.load(cache_file)
        return contents
    except FileNotFoundError:
        return None

def get_contents(url):
    """
    Returns web content from a given URL
    :returns: Web content as a BeautifulSoup object
    """
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.text, features="html.parser")
        return soup
    except ConnectionError:
        print("Erro na rede. Verifique sua conexão.")
        quit()
    except TimeoutError:
        print("Time out na requisição.")
        quit()

def get_daily_menu(menu, date):
    """
    Given a list and a date, get the date's menu
    :menu: week's menu
    :date: target date
    :returns: Menu in a string format
    """
    for index, line in enumerate(menu):
        if date in line:
            start = index
            return menu[start]
    return None

def get_week_menu(soup):
    """
    :soup:
    :returns: TODO
    """
    trs = soup.findAll("tr")[1:8]
    return [x.text for x in trs]

def handle_date(week, date):
    """
    Formats date correctly and returns menu accordingly
    :returns: Menu from given date
    """
    if date in ["hoje", "today"]:
        return get_daily_menu(week, time.strftime("%d.%m.%Y"))
    if date in ["amanha", "tomorrow"]:
        tomorrow = datetime.date.today() + datetime.timedelta(hours=24)
        return get_daily_menu(week, tomorrow.strftime("%d.%m.%Y"))
    if date.isdigit():
        return get_daily_menu(week, str(date)+time.strftime(".%m.%Y"))
    if date.lower() in ["semana", "week"]:
        return '\n'.join(week)
    help_text()
    return None

def week_file(week):
    """
    :file_contents: A list containing the week's menu
    :returns: Bool saying if the file is from the same week as today
    """
    # Get first and last days of file and today's date, all as ints
    first_date = week[0].split(' ')[0][1:]
    last_date = week[-1].split(' ')[0][1:]
    first_day = int(first_date[:2])
    last_day = int(last_date[:2])
    today = int(time.strftime("%d"))

    # Check if today is between the first and last days in file
    return first_day < today < last_day

# def clear_cache(location):

def help_text():
    """
    Prints argument help text
    """
    print("Uso: ru_watcher COMANDO")
    print("COMANDO pode ser:\n - help: mostra este texto\n - limpar/clear: remove arquivo de cache \
            \n - Data:")
    print("\t- hoje/today\n\t- amanha/tomorrow\n\t- formato %d.%m.%Y\n\t- dia (%d) \
            \n\t- semana/week")

def main():
    """
    Main function. Defines URL, calls handle_date and get_contents and prints the result of get_menu
    """
    # Parse arguments
    if len(argv) != 2 or argv[1] in ["help", "ajuda"]:
        help_text()
        return
    command = argv[1].lower()

    # Handle .cache dir and cache file
    cache_dir = Path(f'{Path.home()}/.cache')
    if not cache_dir.exists():
        cache_dir.mkdir()

    cache_location = f'{Path.home()}/.cache/ru_watcher'

    if command in ["clear", "limpar"]:
        remove(cache_location)
        return

    file_contents = read_file(cache_location)

    # If cache file already exists and is this week's menu
    if file_contents and week_file(file_contents):
        # Get the data from the file
        menu = handle_date(file_contents, command)
        if menu:
            print(menu)
    # Cache file doesn't help us, so get the data online and save it to the file for future use
    else:
        # Get online content
        url = "https://ru.ufsc.br/ru/"
        soup = get_contents(url)

        # Get week content and save it to cache file
        week_menu = get_week_menu(soup)
        dump_week(week_menu, cache_location)

        # Handle date
        menu = handle_date(week_menu, command)
        if menu:
            print(menu)

if __name__ == "__main__":
    main()
