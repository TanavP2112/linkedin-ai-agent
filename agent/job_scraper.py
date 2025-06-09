import urllib.parse
import requests
from bs4 import BeautifulSoup

def linkedin_search(query, location="United States", num_results=10):
    query = urllib.parse.quote_plus(query)
    url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={urllib.parse.quote(location)}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    jobs = []
    for job_card in soup.select("li.jobs-search-results__list-item")[:num_results]:
        title_elem = job_card.select_one("h3")
        company_elem = job_card.select_one("h4")
        link_elem = job_card.find("a", href=True)
        if title_elem and company_elem and link_elem:
            jobs.append({
                "title": title_elem.get_text(strip=True),
                "company": company_elem.get_text(strip=True),
                "link": "https://www.linkedin.com" + link_elem["href"]
            })
    return jobs