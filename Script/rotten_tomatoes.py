# -*- conding: utf-8 -*-
from pprint import pprint
import requests
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, ProcessPoolExecutor
from concurrent.futures import wait
from time import sleep
from config import config
from datetime import datetime
from bs4 import BeautifulSoup
from pymongo import UpdateOne
from handles.mongo import insert_bulk, get_db_items


# I cannot get the pagination so I just query a number that I know will get redirected to show all movies.


class ROTTENTOMATOES:
    def __init__(self, websites, operation, skip, created_at, ):
        _mongo = config()['mongo']
        self.db_crawlers = _mongo['crawlers']
        self.db_scraping = _mongo['scrapings']
        _config = config()['websites'][websites]
        self.platform = _config['platform_code']
        self.crawlers_url = _config['crawlers_url']
        self.base_url = _config['base_url']
        self.rating_url = _config['ratings_url']
        if created_at:
            self.created_at = created_at
        else:
            now = datetime.now()
            self.created_at = now.strftime("%Y-%m-%d")
        self.process(operation, skip)

    def process(self, operation, skip):
        if operation == 'scraping':
            if not skip:
                self.crawling()
            self.scraping()
        elif operation == 'crawlers':
            self.crawling()

    def crawling(self):
        """This function calls self.get_crawlers() and inserts the crawlers to MongoDB"""
        crawlers = self.get_crawlers()

        if len(crawlers) > 0:
            print(f'Por insertar a la DB...')
            insert_bulk(crawlers, self.db_crawlers)

    def get_crawlers(self):
        """Gets the crawlers from the popular movies section. Returns a list of n movies in that page"""
        tries = 2
        while tries > 0:
            try:
                response = requests.get(self.crawlers_url)
            except Exception as e:
                print(
                    f"Error de conexion - Durmiendo por 2 segundos... quedan {tries} intentos mas para el titulo {item['Title']}")
                sleep(2)
                tries -= 1
                if tries == 0:
                    print(f'{self.crawlers_url} de  no pudo ser crawleada')

                    page_error = {
                        "PlatformCode": self.platform,
                        "URL": self.crawlers_url,
                        "Error": "Connection error",
                        "Date": self.created_at
                    }

                    query = {
                        "PlatformCode": self.platform,
                        "ContentType":  "movies",
                        "CreatedAt":    self.created_at,
                    }
                    return UpdateOne(
                        query,
                        {
                            "$set": page_error
                        },
                        upsert=True
                    )
            else:
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    titles_div = soup.select(
                        'div[class*="discovery-tiles__wrap"]')[-1]
                    all_titles = titles_div.find_all('a')

                    crawlers = []

                    for title in all_titles:
                        url = self.base_url + title['href']
                        movie_slug = title['href']
                        clean_title = title.text.strip()
                        stats = title.select_one('score-pairs')

                        try:
                            audience_score = int(stats['audiencescore'])
                        except Exception as e:
                            audience_score = 0
                            pass

                        try:
                            audience_sentiment = stats['audiencesentiment']
                        except Exception as e:
                            audience_sentiment = "not available"
                            pass

                        try:
                            critics_score = int(stats['criticsscore'])
                        except Exception as e:
                            critics_score = 0
                            pass

                        try:
                            critics_sentiment = stats['criticssentiment']
                        except Exception as e:
                            critics_sentiment = "not available"
                            pass

                        item = {
                            'Title': clean_title,
                            'URL': url,
                            'Movie_slug': movie_slug,
                            'Audience_score': audience_score,
                            'Audience_sentiment': audience_sentiment,
                            'Critics_score': critics_score,
                            'Critics_sentiment': critics_sentiment

                        }
                        query = {
                            "ContentType":  "movies",
                            "URL":      url,
                            "Website":      self.platform,
                            "CreatedAt":    self.created_at
                        }
                        crawlers.append(
                            UpdateOne(query, {"$set": item}, upsert=True))
                    print(
                        f'Finalizados los crawlers del sitio.')

                    return crawlers

    def get_metadata(self, item_url):
        """Aux function that gets metadata from the main movie page. Returns a dictionary"""
        response = requests.get(item_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        metadata_lis = soup.select_one(
            'ul[class*="content-meta info"]').select('li')
        genre, producer, director, release_date = "not available", "not available", "not available", "not available"

        for li in metadata_lis:
            label = li.select_one(
                'div[class*="meta-label"]').text.replace(':', '')
            if 'Genre' in label:
                try:
                    genre = " ".join(li.select_one(
                        'div[class*="meta-value"]').text.split())
                except Exception as e:
                    pass

            elif 'Producer' in label:
                try:
                    producer = " ".join(li.select_one(
                        'div[class*="meta-value"]').text.split())
                except Exception as e:
                    pass

            elif 'Director' in label:
                try:
                    director = " ".join(li.select_one(
                        'div[class*="meta-value"]').text.split())
                except Exception as e:
                    pass

            elif 'Release Date' in label:
                try:
                    release_date = " ".join(li.select_one(
                        'div[class*="meta-value"]').text.split())
                except Exception as e:

                    pass

        _metadata = {
            'Director': director,
            'Producer': producer,
            'Genres': genre,
            'Release-date': release_date
        }
        return [_metadata]

    def get_reviews(self, movie_slug):
        "Aux function that gets existing reviews. Returns a list of reviews."
        response = requests.get(self.rating_url.format(movie_slug))
        soup = BeautifulSoup(response.text, 'html.parser')
        comments = []
        try:
            reviews_table = soup.select_one(
                'div[class*="review_table"]')
        except Exception as e:
            comments.append("No reviews yet.")
            return comments
        else:
            try:
                reviews_lis = reviews_table.select_one(
                    'ul[class*="audience-reviews"]').find_all('li')
            except Exception as e:
                pass
            try:
                for review in reviews_lis:
                    comment = review.select_one(
                        'p[class*="audience-reviews__review"]')
                    comments.append(comment.text)
            except Exception as e:
                pass
        return comments

    def get_scraping(self, item):
        """Gets the end product of scraping aux funcions and returns an UpdateOne object."""
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(self.get_metadata, item['URL']),
                       executor.submit(self.get_reviews, item['Movie_slug'])]
            wait(futures, return_when=ALL_COMPLETED)
            item['Metadata'] = futures[0].result()
            item['Comments'] = futures[1].result()
            print(f'Finalizado el titulo {item["Title"]}')
            query = {
                "Website": item['Website'],
                "CreatedAt": item["CreatedAt"],
                "ContentId": item["URL"]
            }
            return UpdateOne(
                query,
                {
                    "$set": item
                },
                upsert=True
            )

    def scraping(self):
        """This function queries the database for all the crawled items and scraps the items concurrently using get_movie_scraping()"""
        query = {
            "Website": self.platform,
            "CreatedAt": self.created_at,
            "ContentType":  "movies",
            "URL":      {"$exists": True}
        }

        items = list(get_db_items(query, self.db_crawlers, {"_id": 0}))
        print(f"Peliculas listas para scrapear: {len(items)}")

        with ThreadPoolExecutor(max_workers=12) as executor:
            movie_scraping = []
            results = {
                executor.submit(self.get_scraping, item):
                    item for item in items
            }
            wait(results, return_when=ALL_COMPLETED)
            for item in results:
                executor.submit(movie_scraping.append(item.result()))

        if len(movie_scraping) > 0:
            print(f'Por insertar a la DB...')
            insert_bulk(movie_scraping, self.db_scraping)
