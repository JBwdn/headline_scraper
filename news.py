#!/usr/bin/env python
# News headline scraper - Jake Bowden 2019:

# Reads website settings from "newsites.csv" at the path variable.
# Add websites to the settings file in the form: "Title,URL,html-class"

# Modules:
from requests import get
from bs4 import BeautifulSoup
from random import shuffle
from numpy import array
from pandas import read_csv
from os import system

path = "~/scripts/newsites.csv"


# Read websites and scraping directions from .csv file:
def load_settings(path):
    print("Loaded settings from:", path)
    settings = array(read_csv(path))
    titles = settings[:, 0]
    URLs = settings[:, 1]
    headline_class = settings[:, 2]
    return titles, URLs, headline_class


# Helper function to only accept valid options or quit command:
def _input(message, in_type=int):
    while True:
        selection = input(message)
        if selection == 'q' or selection == 'Q':
            quit()
        try:
            return in_type(selection)
        except:pass


# List available websites to the user and accept their choice:
def offer_options(title):
    max = len(title)
    for i in range(max):
        print(i, '>', title[i])
    choices = list(range(max))
    selection = 999
    while selection not in choices:
        selection = _input(f"Select website 0-{str(max-1)} or (q)uit:")
    return selection


# Scrape headlines from news site and return the top 10:
def print_headlines(option, Titles, URLs, headline_class):
    i = int(option)
    print("\n--- ", Titles[i], ": ---             ", URLs[i])
    r = get(str(URLs[i]))
    rraw = r.text
    soup = BeautifulSoup(rraw, 'html.parser')
    counter = 1
    for x in soup.find_all(class_=headline_class[i]):
        if counter == 10:
            if x.string != None:
                print(counter, ">   ", x.string, "\n")
                break
            else:
                print(counter, ">   ", x.get_text(), "\n")
                break
            break
        if x.string != None :
            print(counter, " >   ", x.string)
            counter += 1
        else:
            print(counter, " >   ", x.get_text())
            counter += 1


# Main function:
def main(settings_path):
    # Load settings:
    titles, URLs, headline_class = load_settings(settings_path)
    while True:
        # Show available source and accept choice:
        selection = offer_options(titles)
        # Clear terminal (cross platform portable):
        system("cls||clear")
        # Return headlines from selected site:
        print_headlines(selection, titles, URLs, headline_class)


if __name__ == "__main__":
    main(path)
