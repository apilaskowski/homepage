#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import time
import sys

students = {}

contest = "https://www.hackerrank.com/contests/wda-"
leaderboard = "/leaderboard/"

contest_link = "https://www.hackerrank.com/contests/pp-winter-term/leaderboard/"

def retrieve_leaderboard_info(driver, link):
    driver.get(link)

    while True:
        tmp_divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'span-flex-2')]")
        if len(tmp_divs) > 0:
            break
        driver.get(link)
        time.sleep(1)

    return driver.find_elements(By.XPATH, "//div [contains(@class, 'leaderboard-list-view')]")

def retrieve_statistics(div):
    html_doc = div.get_attribute('innerHTML')
    soup = BeautifulSoup(html_doc, 'html.parser')
    key = soup.find('div', 'span-flex-2').p.text
    value = len(soup.find_all('div', 'correct'))
    return key, value

def get_leaderboard_data(driver, link, additional=False):
    divs = retrieve_leaderboard_info(driver, link)

    for div in divs:
        key, value = retrieve_statistics(div)
        
        f, s = 0, 0
        if key in students:
            f, s = students[key]

        if additional:
            s += value
        else:
            f += value

        students[key] = (f, s)

def print_html_table():
    print("document.write('\\")
    for student in sorted(students.items(), key=lambda x: (x[1][0], x[1][1], x[0]), reverse=True):
        print("<tr>\\")
        print("\t<td>" + str(student[0]) + "</td>\\")
        print("\t<td>" + str(student[1][0]) + "</td>\\")
        print("\t<td>" + str(student[1][1]) + "</td>\\")
        print("</tr>\\a")
    print("');")

def main():
    debug = bool(sys.argv[1])
    if debug:
        print('Starting Safari')
    driver = webdriver.Safari()
    if debug:
        print('Safari started')

    if debug:
        print('Crawling')
    for i in range(1, 10):
        if debug:
            print('Page' + str(i))
        for j in range(1, 6):
            if debug:
                print('Tab' + str(j))
            if i < 10:
                link = contest + '0' + str(i) + leaderboard + str(j)
            elif i == 10:
                link = contest + str(i) + 'b' + leaderboard + str(j)
            else:
                link = contest + str(i) + leaderboard + str(j)            

            if debug:
                print('Retrieving leaderboard data')
            get_leaderboard_data(driver, link)

    for j in range(1, 5):
        link = contest_link + str(j)
        get_leaderboard_data(driver, link, True)

    print_html_table()

if __name__ == "__main__":
    main()
