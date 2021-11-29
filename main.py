from time import sleep
import requests
from bs4 import BeautifulSoup
import csv
import json

# Create index.html

# URL = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Mobile Safari/537.36',
    'Accept': '*/*'
}
# req = requests.get(URL, headers=HEADERS)
# src = req.text
# with open('index.html', 'w', encoding="utf-8") as file:
#     file.write(src)

# Then I will work offline with index.html
# Create all_categories_dict.json

# with open('index.html', encoding="utf-8") as file:
#     src = file.read()
# soup = BeautifulSoup(src, 'lxml')
# all_products_hrefs = soup.find_all(class_ = 'mzr-tc-group-item-href')
#
# all_categories_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = 'https://health-diet.ru' + item.get('href')
#     all_categories_dict[item_text] = item_href
#
# with open('all_categories_dict.json', 'w', encoding='utf-8') as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

# Then I will work offline with all_categories_dict.json

with open('all_categories_dict.json', encoding="utf-8") as file:
    all_categories = json.load(file)
iteration_count = int(len(all_categories)) - 1
count = 0
print(f'Всего итераций: {iteration_count}')
# Replace unnecessary characters with "_"
for category_name, category_href in all_categories.items():
    rep = [' ', ',']
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")

    req = requests.get(url=category_href, headers=HEADERS)
    src = req.text
    # Writing the code to the html file
    with open(f'data/{count}_{category_name}.html', 'w', encoding='utf-8') as file:
        file.write(src)
    # Read the written code and create the soup object
    with open(f'data/{count}_{category_name}.html', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    # 'uk-alert-danger' is empty, so we create a condition for catching this class so that there is no error
    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue
    # Filling in the title
    table_head = soup.find(class_='uk-table mzr-tc-group-table uk-table-hover '
                                  'uk-table-striped uk-table-condensed').find('tr').find_all('th')
    product = table_head[0].text
    calorie = table_head[1].text
    squirrels = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calorie,
                squirrels,
                fats,
                carbohydrates
            )
        )
    # Filling in product data
    product_data = soup.find(class_='uk-table mzr-tc-group-table uk-table-hover '
                                    'uk-table-striped uk-table-condensed').find('tbody').find_all('tr')

    product_info = []

    for item in product_data:
        product_tds = item.find_all('td')

        title = product_tds[0].find('a').text
        calorie = product_tds[1].text
        squirrels = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        product_info.append(
            {
                'Title': title,
                'Calories': calorie,
                'Squirrels': squirrels,
                'Fats': fats,
                'Carbohydrates': carbohydrates
            }
        )
        # Loading data into csv file
        with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calorie,
                    squirrels,
                    fats,
                    carbohydrates
                )
            )
    # Loading data into json file
    with open(f'data/{count}_{category_name}.json', 'a', encoding='utf-8') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f'# Итераций {count}. {category_name} записан...')
    iteration_count = iteration_count - 1
    if iteration_count == 0:
        print('Работа завершена')
        break
    print(f'Осталось итераций: {iteration_count}')
    sleep(2)
