from bs4 import BeautifulSoup
import requests
regulation='(R20)'
html_text = requests.get("https://mits.ac.in/ugc-autonomous-exam-portal#ugc-pro3").text
soup = BeautifulSoup(html_text, 'lxml')
def exam_timetable():
    n=0
    table=soup.find('div', id='ugc-pro3')
    exam=table.find('div',class_='container')
    exam_data=exam.find("div",class_="publication-list mb-4")
    exam1=exam.find_all("li")
    for index,exam2 in enumerate(exam1):
        if n==1:
            break
        a=exam2.text.strip()
        downlink=exam2.find("a")['href']
        if regulation in a:
            print(a)
            print(downlink)
            n=n+1
exam_timetable()