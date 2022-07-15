import requests
from bs4 import BeautifulSoup

LIMIT = 40
URL = f'https://search.incruit.com/list/search.asp?col=job&kw=python'
#startno=0&psize=60
def extract_pages():
    max_page = 0
    temp = URL
    pages = []
    while(1):
        if(max_page > 0):
            result = requests.get(temp+f'&startno={( max_page - 1 )*LIMIT}&psize={LIMIT}')
        else:
            result = requests.get(temp+f'&startno={( max_page )*LIMIT}&psize={LIMIT}')
        soup = BeautifulSoup(result.text, "html.parser")
        pagination = soup.find("p", {"class" : "sqr_paging sqr_pg_mid"})
        links = pagination.find_all("span")
        for link in links:
            if link.string is not None:
                pages.append(int(link.string))
        if(max_page == max(pages)):
            break
        max_page = max(pages)
    return max_page

def extract_job(html):
    if(html.find("ul", {"class" : "c_row"}) != None):  
        title = html.find("div", {"class" : "cell_mid"}).find("div", {"class" : "cl_top"}).find("a")
        print(title)
        #company = html.find("span", {"class" : "companyName"}).string
        #location = html.find("div", {"class" : "companyLocation"}).string
        #job_id = html.find("a")["data-jk"]
        #return { "title" : title, "company" : company, "location" : location, "apply_link" : f"https://kr.indeed.com/applystart?jk={job_id}" }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):  
        print(f"Scrapping Page {page}")#startno=0&psize=60
        result = requests.get(f"{URL}&startno={page*LIMIT}&size={LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class" : "cBbslist_contenst"})
        for html in results:
            dic = extract_job(html)
            if dic != None:
                jobs.append(dic)
    return jobs

#a = extract_pages()
extract_jobs(3)