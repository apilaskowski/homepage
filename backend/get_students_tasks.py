#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

driver = webdriver.Firefox()

students = {}

contest = "https://www.hackerrank.com/contests/ap-0"
leaderboard = "/leaderboard/"

for i in range(1, 6):
    for j in range(1, 3):
        link = contest + str(i) + leaderboard + str(j)
        
        driver.get(link)

        while True:
            tmp_divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'span-flex-2')]")
            if len(tmp_divs) > 0:
                break
            driver.get(link)

        divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'leaderboard-list-view')]")

        for d in divs:
            html_doc = d.get_attribute('innerHTML')
            soup = BeautifulSoup(html_doc, 'html.parser')
            key = soup.find('div', 'span-flex-2').p.text
            value = len(soup.find_all('div', 'correct'))
            
            if key in students:
                students[key] += value
            else:
                students[key] = value

for student in sorted(students.items(), key=lambda x: (x[1], x[0]), reverse=True):
    print("<tr>")
    print("\t<td>" + str(student[0]) + "</td>")
    print("\t<td>" + str(student[1]) + "</td>")
    print("</tr>")