import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}'

def extract_indeed_pages():
    max_page = 0
    temp = URL
    pages = []
    while(1):
        result = requests.get(temp+f'&start={max_page*LIMIT}')
        soup = BeautifulSoup(result.text, "html.parser")
        pagination = soup.find("div", {"class" : "pagination"})
        links = pagination.find_all("span", { "class" : "pn" }) 
        for link in links:
            if link.string is not None:
                pages.append(int(link.string))
        if(max_page == max(pages)):
            break
        max_page = max(pages)
        print(pages)
        print(max_page)
    return max_page

def extract_job(html):
    if(html.find("h2", {"class" : "jobTitle css-1h4a4n5 eu4oa1w0"}) != None):  
        title = html.find("h2", {"class" : "jobTitle css-1h4a4n5 eu4oa1w0"}).find("span").string
        company = html.find("span", {"class" : "companyName"}).string
        location = html.find("div", {"class" : "companyLocation"}).string
        return {"title" : title, "company" : company, "location" : location}

def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):  
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("td", {"class" : "resultContent"})
        for html in results:
            dic = extract_job(html)
            if dic != None:
                jobs.append(dic)
    return jobs