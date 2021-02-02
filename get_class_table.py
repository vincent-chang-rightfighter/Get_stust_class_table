from bs4 import BeautifulSoup
import pandas as pd
import requests
import os

with requests.Session() as s:
    page = s.get('https://course.stust.edu.tw/CourSel/Login.aspx?ReturnUrl=%2fCourSel%2fboard.aspx')
    soup = BeautifulSoup(page.content, 'lxml')

    payload_loginPage = {
        'Login1$UserName': 'sutdent_id',
        'Login1$Password': 'student_password',
        'Login1$LoginButton': '登入'
    }

    payload_loginPage["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
    payload_loginPage["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
    payload_loginPage["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]
    s.post('https://course.stust.edu.tw/CourSel/Login.aspx?ReturnUrl=%2fCourSel%2fboard.aspx', data=payload_loginPage)

page = s.get('https://course.stust.edu.tw/CourSel/Pages/MyTimeTable.aspx?role=S')
soup = BeautifulSoup(page.content, 'html.parser')
table = pd.read_html(page.text, encoding='utf-8',keep_default_na=False)[31]
table=table.drop([9])
table.to_csv('Class_table.csv',index=0,encoding='utf-8-sig')
print("finish check file")