from bs4 import BeautifulSoup
from requests import get
import sqlite3
from sys import argv

URL = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/q-kawalerka/?search%5Bfilter_float_price%3Ato%5D=2000'

def parce_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', '.'))

db = sqlite3.connect('dane.db')
cursor =db.cursor()

if len(argv) > 1 and argv[1] == 'setup':
    cursor.execute('''CREATE TABLE offers (name TEXT, price REAL, city TEXT)''')
    quit()


def parce_page(number):
    print(f'Pracuje nad stroną numer {number}.')
    page = get(f'{URL}&page={number}')
    bs = BeautifulSoup(page.content, 'html.parser')
    for offer in bs.find_all('div', class_='offer-wrapper'):
        footer = offer.find('td', class_='bottom-cell')
        location = footer.find('small', class_='breadcrumb').get_text().strip().split(',')
        title = offer.find('strong').get_text().strip()
        price = parce_price(offer.find('p', class_='price').get_text().strip())
        link = offer.find('a')['href']
        print(link,'\n',title,'\n',location,'\n',price)
        bs_inner = BeautifulSoup(get(link).content, 'html.parser')
        offer_content_block = bs_inner.find('div', class_='offerdescription')
        offer_from = offer_content_block.find('strong', class_='offer-details__value').get_text()
        floor = bs_inner.find('strong', class_='offer-details__value').get_text()
        furnished = ''
        building_type = ''
        area = ''
        rental = ''
        for value in offer_content_block.find_all('strong', class_='offer-details__value'):
            print(value.get_text())
        deskription = offer_content_block.find('div', class_ ='clr lheight20 large').get_text()
        print('__________________________________________________')
        print(deskription)
        #print(offer_from)
        break


    #     cursor.execute('INSERT INTO offers VALUES (?,?,?)', (title, price, location))
    #
    # db.commit()

# for page in range(1, 31):
#     parce_page(page)

parce_page(1)
db.close()