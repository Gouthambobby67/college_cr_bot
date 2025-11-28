from urllib.parse import quote, urljoin
import requests
from email.mime import text
from bs4 import BeautifulSoup
def safe_url(u):
    if " " not in u:
        return u
    parts=u.split('/',3)
    if len(parts) < 4:
        return u
    prefix ='/'.join(parts[:3])
    path =  quote(parts[3])
    return f"{prefix}/{path}"
def exam_timetable(regulation):
    html_text = requests.get("https://mits.ac.in/ugc-autonomous-exam-portal#ugc-pro3").text
    soup = BeautifulSoup(html_text, 'lxml')
    n=0
    b=[]
    table=soup.find('div', id='ugc-pro3')
    exam=table.find('div',class_='container')
    exam_data=exam.find("div",class_="publication-list mb-4")
    exam1=exam.find_all("li")
    for index,exam2 in enumerate(exam1):
        if n==5:
            break
        a=exam2.text.strip()
        downlink=exam2.find("a")['href']
        downloadlink=safe_url(downlink)
        if regulation in a:
            b.append(a)
            b.append(downloadlink)
            n=n+1
    return b
def notification_timetable(regulation):
    html_text = requests.get("https://mits.ac.in/ugc-autonomous-exam-portal#ugc-pro1").text
    soup = BeautifulSoup(html_text, 'lxml')
    n=0
    b=[]
    table=soup.find('div', id='ugc-pro1')
    exam=table.find('div',class_='container')
    exam_data=exam.find("div",class_="publication-list mb-4")
    exam1=exam.find_all("li")
    for index,exam2 in enumerate(exam1):
        if n==5:
            break
        a=exam2.text.strip()
        downlink=exam2.find("a")['href']
        downloadlink=safe_url(downlink)
        if regulation in a:
            b.append(a)
            b.append(downloadlink)
            n=n+1
    return b
class results_checking:
    def get_results_link(self,all_data_collected):
        html_text="http://125.16.54.154/mitsresults/resultug"
        soup=BeautifulSoup(requests.get(html_text).text,'lxml')
        table=soup.find('div',class_='wrapper')
        table1=table.find_all('a')
        data=[]
        self.results_link=[]
        self.new_text=[]
        ROMAN = {
            "I": 1,
            "II": 2,
            "III": 3,
            "IV": 4,
        }
        for index,x in enumerate(table1):
            link=x["href"]
            name=x.get_text(strip=True)      
            full_link = urljoin(html_text, link)
            data.append(name)
            parts = name.split("-")        # ['B.Tech', 'IV', 'II', 'R20', 'Regular', 'May', '2024']
            parts[1] = str(ROMAN[parts[1].upper()])   # IV  -> 4
            parts[2] = str(ROMAN[parts[2].upper()])   # II  -> 2
            text = "-".join(parts)
            if all_data_collected[0] in text and all_data_collected[1] in text[7] and all_data_collected[2] in text[9]:
                self.new_text.append(text)
                self.results_link.append(full_link)
        return self.new_text
    def print_options(self,all_data_collected):
        data1=[]
        for index,x in enumerate(self.new_text):
            data1.append((f"{index}: {x}"))
        #print("\n".join(data1))
        #idx = int(input("Enter number: "))
        result_link = self.results_link[all_data_collected[3]]
        return result_link    
if __name__=="__main__":
    pass
