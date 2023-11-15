# Yelp Web Crawler

## Overview
The Yelp Web Crawler is a python script developed using Scrapy library to scrape data from Yelpbusiness listings for SG.

***
## Usage
To use this crawler, follow next steps:
1. Run the crawler passing the necessary args, like `location` and `category`:  
```shell
scrapy crawl yelp_crawl yelp_crawler -a location="Your Location" -a category="Your Category"
```
2. The crawler will scrape data from Yelp business listings and stream it into a JSON file.
