from indeed import extract_indeed_pages, extract_indeed_jobs

last_indeed_page = extract_indeed_pages()
print(last_indeed_page)
a = extract_indeed_jobs(last_indeed_page)

for i in a:
    print(i) 