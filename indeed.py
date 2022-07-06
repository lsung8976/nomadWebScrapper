import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}'

def extract_indeed_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class" : "pagination"})
    links = pagination.find_all("a") 
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page

def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):  
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("td", {"class" : "resultContent"})
        for text in results:
            if(text.find("h2", {"class" : "jobTitle css-1h4a4n5 eu4oa1w0"}) == None):  
                continue
            title = text.find("h2", {"class" : "jobTitle css-1h4a4n5 eu4oa1w0"}).find("span").string
            company = text.find("span", {"class" : "companyName"}).string
            location = text.find("div", {"class" : "companyLocation"}).string
            jobs.append({"title" : title, "company" : company, "location" : location})
    return jobs