
from datetime import datetime
import json
import time

from bs4 import BeautifulSoup
import requests


def open_file(file_path):
    '''Gets the data from a JSON file and copies it into a return object'''
    try:
        with open(file_path, 'r', encoding='UTF-8') as outfile:
            outfile.flush()
            data = json.load(outfile)
            outfile.close()
            return data
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        raise

def save_file(file_path, data):
    '''Writes the given data to the given file path, and converts the data into a JSON format'''
    try:
        with open(file_path, 'w', encoding='UTF-8') as outfile:
            outfile.flush()
            json.dump(data, outfile, indent=4, separators=(',', ': '))
            outfile.close()
    except (FileNotFoundError, TypeError):
        raise

series_temp = open_file('./series.json')
volumes_temp = open_file('./volumes.json')
shops_temp = open_file('./shop.json')

# vols_need_enrich = [isbn for isbn in volumes_temp if volumes_temp[isbn]['release_date'] is None and shops_temp[isbn]['shops'][0]['stock_status'] == 'Pre-Order']
# vols_need_enrich = [isbn for isbn in volumes_temp if volumes_temp[isbn]['name'] is None]
# print(len(vols_need_enrich), 'volumes need to be enriched')
# print()

completed = 0
invalid = []

for isbn in series_temp:
    # vol = volumes_temp[isbn]
    series_temp[isbn]['volumes'] = sorted(
        series_temp[isbn]['volumes'],
        key = lambda x: (
            x['category'],
            -1
            if x['volume'] is None
            else (
                int(x['volume'].split('-')[0])
                if '-' in x['volume']
                else int(x['volume'])
            )
        )
    )
    # # print('parsing ' + vol['isbn'])
    # sp = BeautifulSoup(
    #     requests.get(vol['url'], timeout=30).text,
    #     'html.parser'
    # )
    # # get the description
    # descriptions = sp.find('div', {'class': 'product-description'}) \
    #     .find('div', {'class': 'short-description'}) \
    #         .find_all('p')
    # vol['description'] = '\n'.join([desc.text for desc in descriptions])
    # # get the thumbnail carousel images
    # carousel = sp.find_all('div', {'class': 'slick-paging-image-container'})
    # all_images = [
    #     img.find('img', {'class': 'img-fluid'}).attrs['src'] for img in carousel
    # ]
    # # print('All images: %s for %s', json.dumps(all_images), vol['name'])
    # vol['cover_images'].extend(
    #     [
    #         { 'name': 'thumbnail', 'url': img } for img in all_images
    #     ]
    # )
    # # print(isbn)
    # # print(vol['url'])
    # # print(sp.find('div', {'class': 'pre-order-street-date'}).text)
    # preorder_soup = sp.find('div', {'class': 'pre-order-street-date'})
    # if preorder_soup is not None:
    #     preorder_text = sp.find('div', {'class': 'pre-order-street-date'}).text
    #     if 'Release date:' in preorder_text:
    #         parsed_preorder_date = preorder_text.replace('Release date:', '').strip()
    #         vol['release_date'] = str(datetime.strptime(parsed_preorder_date, '%m/%d/%Y').date())
    #     else:
    #         parsed_preorder_date = preorder_text.replace('ESTIMATED TO SHIP', '') \
    #             .replace('Ship date is an estimate and not guaranteed', '') \
    #                 .replace('Pre-order FAQ', '') \
    #                     .strip()
    #         vol['release_date'] = str(datetime.strptime(parsed_preorder_date, '%B %d, %Y').date())
    # else:
    #     invalid.append(isbn)

    # # print(vol['release_date'])
    # # print()

    completed += 1
    progress = round((completed / len(series_temp)) * 50)
    remaining = 50 - progress
    percentage = round((completed / len(series_temp)) * 100, ndigits=2)
    print('progress: |' + ''.join(['=' for _ in range(progress)]) + ''.join(['-' for _ in range(remaining)]) + '| ' + str(percentage) + '%', end='\r')
    # # print()
    # save_file('./volumes.json', volumes_temp)
    # # save_file('./shop.json', shops_temp)

    # time.sleep(3)


print('Saving all files...')
save_file('./series.json', series_temp)
# save_file('./volumes.json', volumes_temp)
# save_file('./shop.json', shops_temp)
# print(invalid)
