import pandas as pd
import logging
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup


pokemon_list = []
filename = 'pokemons.csv'
logging.basicConfig(filename='errors.txt',filemode='w', format='%(asctime)s - %(message)s', level=logging.ERROR)

def html_clear(html_doc):
  return " ".join(str(html_doc).split()).replace('> <','><')

def get_pages(soup):
  return list(set(soup.find_all('a')))

def crawl_page(html_doc):   
  soup = BeautifulSoup(html_doc, 'html.parser')
  table_list = soup.find_all('table')

  ix = 0
  for table in table_list:
    ix = ix + 1
    try:
      keys = []
      tags = table.find_all('td', {"bgcolor": ["#96B8FB", "#ADC7FB"]})
      for tag in tags:
        keys.append(tag.get_text())

      values = []
      tags = table.find_all('td', {"bgcolor": ["#CADAF9","#cadaf9","#DEE9FF"], "align": ["left","middle"]})
      tags.pop(0)

      for tag in tags:
        values.append(tag.get_text())

      values[1], values[2] = values[2], values[1]
      values[1] = table.find('td', {"bgcolor": ["#CADAF9","#DEE9FF"], "align": ["middle"]}).img.get('src')

      pokemon = {}
      pokemon = dict(zip(keys, values))
      pokemon['image'] = table.td.img.get('src')

      pokemon_list.append(pokemon)
    except Exception as e:
      logging.error('Error url={} ix={}'.format(soup.url, ix), exc_info=True)
      continue

if __name__=='__main__':
  try:
    url_source = "https://pokemythology.net/conteudo/pokemon/lista01.htm"
    headers = {'User-Agent': 'Custom user agent'}

    request = Request(url=url_source, headers=headers)
    response = urlopen(request)    
    html_doc = response.read()
    html_doc = html_doc.decode('latin1')
    html_doc = html_clear(html_doc)

    crawl_page(html_doc)

    soup = BeautifulSoup(html_doc, 'html.parser')
    url_list = get_pages(soup)

    for url in url_list:
      url = "https://pokemythology.net" + url.get('href')
      request = Request(url=url, headers=headers)
      response = urlopen(request)
      html_doc = response.read()
      html_doc = html_doc.decode('latin1')
      html_doc = html_clear(html_doc)
      crawl_page(html_doc)

    df = pd.DataFrame.from_dict(pokemon_list)
    df.drop_duplicates(inplace=True)
    df.sort_values(df.columns[2], ascending=True, inplace=True)
    df.to_csv(filename, sep=',', index=False, encoding='utf-8')

  except HTTPError as e:
    print(e.status, e.reason)
  except URLError as e:
    print(e.reason)