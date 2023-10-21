from bs4 import BeautifulSoup
from interfaces.ivolume import IVolume

def create_blank_record(isbn):
    item = IVolume()
    item.isbn = isbn
    item.stock_status = 'Unavailable'
    return item

def create_new_record(record, item, soup):
    edition = ' ' + item.get('edition') if 'edition' in item.keys() and item.get('edition') != '' else ''
    mal_titles = soup.find_all('span', {'class': 'title-english'})
    record['series'] = soup.find_all('span', {'itemprop': 'name'})[0].text if len(mal_titles) == 0 else mal_titles[0].text
    record['name'] = record['series'] + edition
    mal_form = soup(text='Type:')[0].parent.parent.find_all('a')[0].text
    record['format'] = 'Novels' if 'Novel' in mal_form else mal_form
    record['volume'] = str(item.get('volume'))
    record['display_name'] = record['name'] + ' ' + record['format'] + edition + ' ' + record['volume']
    return record

def mal_enrich(record, mal_url, soup):
    if not isinstance(record['cover_images'], list):
        record['cover_images'] = []
    record['cover_images'] = record['cover_images'].append(soup.find('img', {'itemprop': 'image'})['data-src'])
    record['description'] = soup.find_all('span', {'itemprop': 'description'})[0].text if len(soup.find_all('span', {'itemprop': 'description'})) > 0 else ''

    if len(soup(text='Genre:')) > 0:
        record['genres'] = [genre.text.strip() for genre in soup(text='Genre:')[0].parent.parent.find_all('a')]
    elif len(soup(text='Genres:')) > 0:
        record['genres'] = [genre.text.strip() for genre in soup(text='Genres:')[0].parent.parent.find_all('a')]
    if len(soup(text='Theme:')) > 0:
        record['themes'] = [theme.text.strip() for theme in soup(text='Theme:')[0].parent.parent.find_all('a')]
    elif len(soup(text='Themes:')) > 0:
        record['themes'] = [theme.text.strip() for theme in soup(text='Themes:')[0].parent.parent.find_all('a')]

    record['authors'] = [text.text + ' ' + text.next_sibling.strip() for text in soup(text='Authors:')[0].parent.parent.findChildren('a' , recursive=False)]
    record['publishing_status'] = soup(text='Status:')[1].parent.next_sibling.strip()
    record['series_volumes'] = soup(text='Volumes:')[0].parent.next_sibling.strip() # TODO: get a list of japanese releases
    record['series_chapters'] = soup(text='Chapters:')[0].parent.next_sibling.strip() # TODO: get a list of japanese releases
    record['demographics'] = ''
    if len(soup(text='Demographic:')) > 0:
        record['demographics'] = [demo.text.strip() for demo in soup(text='Demographic:')[0].parent.parent.find_all('a')]
    elif len(soup(text='Demographics:')) > 0:
        record['demographics'] = [demo.text.strip() for demo in soup(text='Demographics:')[0].parent.parent.find_all('a')]
    if len(soup(text='Serialization:')) > 0:
        mal_serializations = soup(text='Serialization:')[0].parent.parent.find_all('a')
        if len(mal_serializations) > 1:
            print('multiple serializations found... chosing one', record['isbn'])
        record['jp_magazine'] = mal_serializations[0].text.strip() if len(mal_serializations) > 0 else soup(text='Serialization:')[0].parent.next_sibling.strip()
    record['rating'] = soup.find_all('span', {'itemprop': 'ratingValue'})[0].text if len(soup.find_all('span', {'itemprop': 'ratingValue'})) > 0 else ''
    record['popularity'] = soup(text='Members:')[0].parent.next_sibling.strip().replace(',','')
    mal_year = soup(text='Published:')[0].parent.next_sibling.strip().replace(' ', '')
    record['start_year'] = mal_year.split(',')[1][:4] if ',' in mal_year else mal_year[:4]
    record['end_year'] = '?' if mal_year[-1] == '?' else mal_year[-4:]
    record['alt_titles'] = [soup.find('span', {'class': 'h1-title'}).find('span', {'itemprop': 'name'}).text]
    if len(soup(text='Synonyms:')) > 0:
        new_title = soup(text='Synonyms:')[0].parent.next_sibling.strip()
        if new_title not in record['alt_titles']:
            record['alt_titles'].append(new_title)
    if len(soup(text='Japanese:')) > 0:
        new_title = soup(text='Japanese:')[0].parent.next_sibling.strip()
        if new_title not in record['alt_titles']:
            record['alt_titles'].append(new_title)
    if len(soup(text='English:')) > 0:
        new_title = soup(text='English:')[0].parent.next_sibling.strip()
        if new_title not in record['alt_titles']:
            record['alt_titles'].append(new_title)
    record['links'] = [{ 'MyAnimeList': mal_url }]
    if record.get('url_component') != None:
        record['links'].append({ 'RightStuf': 'https://www.rightstufanime.com/' + record.get('url_component') })

    return record
        

# def create_record(self):
#     if is_editing():
#         return 503

#     adding = request.json
#     isbn_to_enrich = []

#     editing_in_progress(True)
#     try:
#         all_items = get_file(items_dir).get('items')

#         if isinstance(adding, list) and len(adding) > 0:
#             for a in adding:
#                 if a not in all_items.keys():
#                     isbn_to_enrich.append(a)

#         if len(isbn_to_enrich) == 0:
#             print('incorrect format: ' + json.dumps(adding))
#             editing_in_progress(False)
#             return 400
            
#         r = []
#         for isbn in isbn_to_enrich:
#             record = create_blank_record(isbn)
#             all_items[record['isbn']] = record
#             r.append(all_items[record['isbn']])
#             update_items_file(all_items)
#         editing_in_progress(False)
#         return jsonify(r)
#     except Exception as ex:
#         editing_in_progress(False)
#         return 500
        

# def enrich_from_mal(self):
#     if is_editing():
#         return 503

#     enriching = request.json
#     items_to_enrich = []

#     editing_in_progress(True)
#     try:
#         all_items = get_file(items_dir).get('items')

#         if isinstance(enriching, list) and len(enriching) > 0:
#             for a in enriching:
#                 if 'isbn' in a and 'mal_url' in a and a.get('isbn') in all_items.keys():
#                     items_to_enrich.append(a)

#         if len(items_to_enrich) == 0:
#             print('incorrect format: ' + json.dumps(enriching))
#             editing_in_progress(False)
#             return 400

#         r = []
#         for item in items_to_enrich:
#             record = all_items[item.get('isbn')]                
#             if item.get('mal_url') != '':
#                 soup = BeautifulSoup(requests.get(item.get('mal_url')).text, 'html.parser')
#                 record = mal_enrich(create_new_record(record, item, soup), item.get('mal_url'), soup)

#             all_items[record['isbn']] = record
#             r.append(all_items[record['isbn']])

#             update_items_file(all_items)
#         editing_in_progress(False)
#         return jsonify(r)
#     except Exception as ex:
#         editing_in_progress(False)
#         return 500
        

# def override_record(self):
#     if is_editing():
#         return 503

#     records = request.json
#     items_to_enrich = []
#     if isinstance(records, list) and len(records) > 0:
#         for a in records:
#             if 'isbn' in a:
#                 items_to_enrich.append(a)

#     if len(items_to_enrich) == 0:
#         print('incorrect format: ' + json.dumps(records))
#         return 400

#     editing_in_progress(True)
#     try:
#         all_items = get_file(items_dir).get('items')
#         r = []
#         for item in items_to_enrich:
#             all_items[item['isbn']] = item
#             r.append(all_items[item['isbn']])
#             update_items_file(all_items)
#         editing_in_progress(False)
#         return jsonify(r)
#     except Exception as ex:
#         editing_in_progress(False)
#         return 500