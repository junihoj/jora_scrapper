import pathlib
import requests
from scrapper import BASE
from helpers import us_cities, uk_cities, au_cities, ca_cities, nz_cities
from constants import job_tiles_with_categories

BASE_DIR = pathlib.Path(__file__).parent.resolve()
print('BASE_DIR',BASE_DIR )
skip_status = []



def write_file(new_data, filename):

    # filePath = pathlib.Path( f'{BASE_DIR}/{filename}.txt')
    filePath = pathlib.Path("filename.txt")
    filePath.touch(exist_ok=True)
    with open(filePath, 'a') as file_write:
        file_write.write(f"\n{new_data}")

country_cities = {"us": us_cities, "uk": uk_cities, "au": au_cities, "ca": ca_cities, "nz": nz_cities}
template_urls = {"us": "https://us.jora.com/j?sp=search&trigger_source=serp&q={}&l={}",
                 "uk": "https://gb.bebee.com/jobs?term={}&location={}",
                 "au": "https://au.bebee.com/jobs?term={}&location={}",
                 "ca": "https://ca.bebee.com/jobs?term={}&location={}",
                 "nz": "https://nz.bebee.com/jobs?term={}&location={}"
                 }
# read_file("keywords")
if __name__== "__main__":
    BASE_DIR = pathlib.Path(__file__).parent.resolve()
    print('BASE_DIR',BASE_DIR )
    base_obj = BASE("requests")
    session = requests.Session()
    session.trust_env=False
    base_obj.db_open_connection()
    dt_string = base_obj.fetch_date("%d-%m-%Y")
   
    for country in country_cities:
        for city in country_cities[country]:
            for catgry in job_tiles_with_categories:
                cat_keywords = job_tiles_with_categories[catgry]
                for keyword in cat_keywords:
                    if f"{city} : {catgry} : {keyword}\n" in skip_status:
                        continue
                    write_file(f"{city} : {catgry} : {keyword}", "keywords")
                    url = template_urls[country].format(keyword.replace(' ', '%20'), city.replace(' ', '%20'))
                    proxy_in = base_obj.get_proxy()
