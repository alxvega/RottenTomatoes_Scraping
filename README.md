# ROTTENTOMATOES SCRAPING

## Getting started:

This is a web scrapping tool that can help us retrieve movie reviews and info from https://www.rottentomatoes.com/

It connects to MongoDB's default LocalHost and saves both the crawling and scraping of the site.

## Libraries used:

- BeautifulSoup
- Requests
- Pymongo
- concurrent.futures
- Conda environment (ideally)

## Running commands:

- Execute crawlers: python3 main.py ROTTENTOMATOES -o crawlers
- Execute scraping: python3 main.py ROTTENTOMATOES -o scraping --skip true
- Execute everything: python3 main.py ROTTENTOMATOES -o scraping

## Notes:

Very fun and simple project to scrape data from the web. This info can be further used for dataframes, exporting as json or even to get the latest and best rated movies.
I will be leaving a data.json file for it to be able to view easily.

### Crawlers:

```json
eg_crawling = {
    "ContentType" : "movies",
    "CreatedAt" : "2022-05-26",
    "URL" : "https://www.rottentomatoes.com/m/facing_nolan",
    "Website" : "ROTTENTOMATOES",
    "Audience_score" : NumberInt(100),
    "Audience_sentiment" : "positive",
    "Critics_score" : NumberInt(96),
    "Critics_sentiment" : "positive",
    "Movie_slug" : "/m/facing_nolan",
    "Title" : "Facing Nolan"
}
```

### Scraping:

```json
eg_scraping = {
            "ContentType" : "movies",
            "CreatedAt" : "2022-05-26",
            "URL" : "https://www.rottentomatoes.com/m/facing_nolan",
            "Website" : "ROTTENTOMATOES",
            "Audience_score" : NumberInt(100),
            "Audience_sentiment" : "positive",
            "Critics_score" : NumberInt(96),
            "Critics_sentiment" : "positive",
            "Movie_slug" : "/m/facing_nolan",
            "Title" : "Facing Nolan",
            "Metadata" : [
                {
                    "Director" : "Bradley Jackson",
                    "Producer" : "Russell Wayne Groves",
                    "Genres" : "Documentary, Biography",
                    "Release-date" : "May 24, 2022 limited"
                }
            ]
            "Comments" : [
                "If you are any sort of baseball fan, you will love this in depth documentary. Being a Houston native I already thought Nolan Ryan was amazing, but this just opened my eyes so much more. I couldn't recommend this more. I'm so glad I had the chance to see it!",
                "This was the best documentary I have ever seen!\nI already was a huge Nolan Ryan as a baseball player fan but I am a bigger fan of him as a regular human and family man now.  This was an incredibly made documentary with so many baseball legends.  I can't wait until it comes out on DVD.",
                "Very well done!  Great clips from the past!",
                "It was a well made documentary on the outstanding career of Nolan Ryan! You dont have to be a baseball fan to enjoy this film.",
                "If you are a baseball fan, this is a great story about one of the greatest pitchers off all time.  It covers his flaws, his dominance, and his family.  It's great story.",
                "Excellent movie of family values, friends and baseball life.",
                "Loved this movie!  Huge fan and this movie was spot on!",
                "An absolute MUST-WATCH movie for everyone in the family. Baseball fans. Fans of Americana. Just a great great movie.",
                "This film does a great job telling the Nolan Ryan story. I would recommend this documentary to any baseball fan!",
                "Excellent look at how and why Nolan became The Express!"
            ]

}
```

---

### This repository is only for educational purposes only. All rights to their respective owners.
