#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

driver = webdriver.Firefox()

students = {}

contest = "https://www.hackerrank.com/contests/ap-0"
leaderboard = "/leaderboard/"

contest_link = "https://www.hackerrank.com/contests/pp-term/leaderboard"

def call_link(link):
    driver.get(link)

    while True:
        tmp_divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'span-flex-2')]")
        if len(tmp_divs) > 0:
            break
        driver.get(link)

    divs = driver.find_elements(By.XPATH, "//div [contains(@class, 'leaderboard-list-view')]")

    for d in divs:
        html_doc = d.get_attribute('innerHTML')
        soup = BeautifulSoup(html_doc, 'html.parser')
        key = soup.find('div', 'span-flex-2').p.text
        value = len(soup.find_all('div', 'correct'))
        
        if key in students:
            f, s = students[key]
            students[key] = (f + value, s)
        else:
            students[key] = (value, 0) 

def call_additional_contest(link):
    driver.get(link)

    while True:
        tmp_divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'span-flex-2')]")
        if len(tmp_divs) > 0:
            break
        driver.get(link)

    divs = driver.find_elements(By.XPATH, "//div [contains(@class, 'leaderboard-list-view')]")

    for d in divs:
        html_doc = d.get_attribute('innerHTML')
        soup = BeautifulSoup(html_doc, 'html.parser')
        key = soup.find('div', 'span-flex-2').p.text
        value = len(soup.find_all('div', 'correct'))
        
        if key in students:
            f, s = students[key]
            students[key] = (f, s + value)
        else:
            students[key] = (0, value) 

for i in range(1, 6):
    for j in range(1, 3):
        link = contest + str(i) + leaderboard + str(j)
        
        call_link(link)

call_additional_contest(contest_link)

for student in sorted(students.items(), key=lambda x: (x[1][0], x[1][1], x[0]), reverse=True):
    print("<tr>")
    print("\t<td>" + str(student[0]) + "</td>")
    print("\t<td>" + str(student[1][0]) + "</td>")
    print("\t<td>" + str(student[1][1]) + "</td>")
    print("</tr>")