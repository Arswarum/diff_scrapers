from email import header
from bs4 import BeautifulSoup
import lxml
import json
import csv
import time
import os
import requests
from random import randrange

url = "https://www.calories.info"
#url  = "https://stackoverflow.com/questions/14896046/python-os-remove-is-not-working"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
}

# req = requests.get(url, headers=headers)
# src = req.text

# with  open("index.html", "w") as file:
#     file.write(src)

# with  open("index.html") as file:
#     src = file.read()

def get_html(url, headers):
    print("Getting HTML from web")
    req = requests.get(url, headers)
    src = req.text
    return src

def chek_and_save_html():
    decision = ""
    if os.path.isfile("index.html"):
        decision = input('File "index.html" already exist, type "yes" to rewright or press Enter to skip:')
    elif decision.lower() == "yes" or os.path.isfile("index.html") == False:
        try:
            os.remove("index.html")
        except:
            pass
        time.sleep(4)
        src = get_html(url, headers)
        with open("index.html", "w") as file:
            print('Saving HTML source to "index.html"')
            file.write(src)
            file.close()

def get_category_name_and_links(src):
    soup = BeautifulSoup(src, "lxml")
    all_products = soup.find_all("li", class_="menu-item-object-calorietables")


    all_products_dict ={}
    rep = [",", " ", "-", "`", "."]
    for item in all_products:
    
        item = item.find("a")
        item_href = item.get("href")

        item_text = item.text
        
        for item in rep:
            if item in item_text:
                item_text = item_text.replace(item, "_")
    

        all_products_dict[item_text] = item_href
    return all_products_dict

def save_all_categoryes_and_links_to_json(all_category_name_and_links):
    with open("all_products.json", "w") as file:
        json.dump(all_category_name_and_links, file, indent=4, ensure_ascii=False)

def get_categori_data(category, link):
    req = requests.get(href, headers=headers)
        src = req.text

        soup = BeautifulSoup(src, "lxml")

        # collect table headers
        table_head = soup.find("thead").find("tr").find_all("td")
        food = table_head[0].text
        serving = table_head[1].text
        calories = table_head[4].text
        kilojoules = table_head[5].text
        
        with open(f"data/{count}_{prod_cat}.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    food,
                    serving,
                    calories,
                    kilojoules
                )
            )

        # Collect table data
        food_data = soup.find("tbody").find_all("tr")

        food_info = []
        for item in food_data:
            food_tds = item.find_all("td")
            food = food_tds[0].text
            serving = food_tds[1].text
            calories = food_tds[4].text
            kilojoules = food_tds[5].text
            print(food,serving,calories,kilojoules)

            food_info.append(
                {
                    "food": food,
                    "serving": serving,
                    "calories": calories,
                    "kilojoules": kilojoules
                }
            )
        
        with  open(f"data/{count}_{prod_cat}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    food,
                    serving,
                    calories,
                    kilojoules
                )
            )
    pass











chek_and_save_html()

with  open("index.html","r") as file:
    src = file.read()

all_category_name_and_links = get_category_name_and_links(src)

save_all_categoryes_and_links_to_json(all_category_name_and_links)

for product, href in all_category_name_and_links.items():
    print(product, href)

# with  open("index.html","r") as file:
    