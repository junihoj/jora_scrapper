from threading import Thread
import pathlib
import requests
from scrapper import BASE
# from helpers import us_cities, uk_cities, au_cities, ca_cities, nz_cities
from constants import job_tiles_with_categories
from get_jora_data2 import getData

BASE_DIR = pathlib.Path(__file__).parent.resolve()
print('BASE_DIR',BASE_DIR )
skip_status = []



# def write_file(new_data, filename):
    # filePath = pathlib.Path( f'{BASE_DIR}/{filename}.txt')
    # filePath = pathlib.Path("filename.txt")
    # filePath.touch(exist_ok=True)
    # with open(filePath, 'a') as file_write:
    #     file_write.write(f"\n{new_data}")
def write_file(new_data, filename):
    filename = f'{BASE_DIR}/{filename}.txt'
    with open(filename, 'a') as file_write:
        file_write.write(f"\n{new_data}")

# country_cities = {"us": us_cities, "uk": uk_cities, "au": au_cities, "ca": ca_cities, "nz": nz_cities}
#alternative https://us.jora.com/j?sp=search&trigger_source=serp&a=1&q={}&l=United+States
#https://us.jora.com/j?a=1&l=United+States&q=python+developer
#https://us.jora.com/j?sp=search&a=24h&&q={}&l=United+States
#https://us.jora.com/j?a=24h&l=United+States&q=python+developer
template_urls = {"us": "https://us.jora.com/j?a=24h&l=United+States&q={}",
                 "uk": "https://uk.jora.com/j?a=24h&l=United+Kingdom&q={}",
                 "au": "https://au.jora.com/j?a=24h&l=Australia&q={}",
                 "ca": "https://ca.jora.com/j?a=24h&l=Canada&q={}",
                 "nz": "https://nz.jora.com/j?a=24h&l=New+Zealand&q={}"
                 }
# read_file("keywords")
if __name__== "__main__":
    base_obj = BASE("requests")
    session = requests.Session()
    session.trust_env=False
    base_obj.db_open_connection()
    dt_string = base_obj.fetch_date("%d-%m-%Y")
    countries = ["United States", "Canada", "Australia", "United Kingdom", "New Zealand"]
    country_index = 0
    for country in template_urls:
        scrape_country=countries[country_index]
        country_index += 1
        for catgry in job_tiles_with_categories:
            cat_keywords = job_tiles_with_categories[catgry]
            for keyword in cat_keywords:
                if f"{catgry} : {keyword}\n" in skip_status:
                    continue
                write_file(f"{catgry} : {keyword}", "keywords")
                url = template_urls[country].format(keyword.replace(' ', '+'))
                proxy_in = base_obj.get_proxy()
                # getData(url, catgry, keyword, scrape_country, base_obj)
                thread = Thread(target=getData, args=(url, catgry, keyword, scrape_country, base_obj))
                thread.start()
                thread.join()