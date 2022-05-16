from asyncio import sleep
from email import header
from bs4 import BeautifulSoup
import lxml
import json
import csv
import time
import requests
from random import randrange

url = "https://www.calories.info"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
}

req = requests.get(url, headers=headers)
src = req.text

with  open("index.html", "w") as file:
    file.write(src)

with  open("index.html") as file:
    src = file.read()


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

##################################################################################

with open("all_products.json", "w") as file:
    json.dump(all_products_dict, file, indent=4, ensure_ascii=False)

iteration_count = int(len(all_products))
print(f"Number of iterations: {iteration_count}")
count = 0
for prod_cat, href in all_products_dict.items():


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
    
    with  open(f"data/{count}_{prod_cat}.json", "a", encoding="utf-8") as file:
        json.dump(food_info, file, indent=4, ensure_ascii=False)


    count +=1
    print(f"# iteration {count}. {prod_cat} written...")
    iteration_count -= 1
    if iteration_count == 0:
        print("THE END!!!")
        break

    print(f"Iterations left: {iteration_count}")
    sleep(randrange(2, 4))