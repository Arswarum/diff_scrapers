from bs4 import BeautifulSoup
import lxml
from time import sleep
import requests
from random import randrange
import os
import json

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
}

def get_persons_urls(headers):
    count = 1
    person_urls = []
    for page in range(0, 740, 20):
        url = f"https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={page}"

        req = requests.get(url, headers=headers)
        src = req.text

        soup = BeautifulSoup(src, "lxml")
        urls = soup.find_all("a", class_="bt-open-in-overlay")
        for url in urls:
            person_urls.append(url.get("href"))
        print(f"page {count}")
        count += 1
        sleep(randrange(1, 4))

    with open("data/urls.txt", "a") as file:
        for url in person_urls:
            file.write(f"{url}\n")

def person_scraper(url, headers):
    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")
    person_name = " ".join(soup.find(class_="bt-biografie-name").find("h3").text.replace(",", "").split()[0:2])
    person_party = soup.find(class_="bt-biografie-name").find("h3").text.replace(",", "").split()[2]
    person_position = soup.find(class_="bt-biografie-beruf").find("p").text

    social_network_links = soup.find(class_="bt-linkliste").find_all("a")
    social_networks = {}
    for link in social_network_links:
        social_networks[link["title"]] = link["href"]
    
    biografie_paragraphs = soup.find(class_="bt-collapse-padding-bottom").find_all("p")
    person_biography =[]
    for p in biografie_paragraphs:
        person_biography.append(p.text.replace("\n", "").strip())

    votes_link = "https://www.bundestag.de" + soup.find("div", class_="bt-abstimmungen-show-more").find("button")["data-url"]
    
    person_votes = votes_scraper(votes_link, headers)
    
    person_info = {
        "Person_name": person_name,
        "Person_party": person_party,
        "Person_position": person_position,
        "Person_social_networks": social_networks,
        "Person_biography": person_biography,
        "Person_last_votes": person_votes,
    }
    return person_info

def votes_scraper(url, headers):
    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")

    all_paragraphs = soup.find_all("p")

    all_votes = []
    vote = []
    answers = ['Ja', "Nein","Nicht abg."]
    for p in all_paragraphs:
        p = p.text.replace("\n", "").strip()
        
        if p in answers:
            vote.append(p)
            all_votes.append(vote)
            vote = []
        else:
            vote.append(p)
            
    return all_votes

def main():
    if not os.path.isfile("data/urls.txt"):
        print("Scraping urls from Web pages")
        get_persons_urls(headers)
    else:
        print("File with urls already exist")        

        with open("data/urls.txt", "r") as file:
            urls = [line.strip() for line in file.readlines()]
    
    print("Scraping persons data")
    count = 1
    persons_left = int(len(urls))
    persons_info = []
    for url in urls:
        print(f"Scraping {count} - person data, {persons_left} - left")
        persons_info.append(person_scraper(url, headers))
        count += 1
        persons_left -= 1
        sleep(randrange(1, 4))

    print("Scraping finished")
    with open("data/persons_info.json", "w", encoding="utf-8") as file:
        json.dump(persons_info, file, indent=4, ensure_ascii=False)

    print('Data saved to "data/persons_info.json"')
    person_scraper(urls[0], headers)

if __name__ == "__main__":
    main()