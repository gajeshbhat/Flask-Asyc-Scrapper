import crochet

crochet.setup()  # initialize crochet

import json
from flask import Flask
from scrapy.crawler import CrawlerRunner
from scraper.tweets_spider import QuoteSpider

app = Flask('Scrape With Flask')
crawl_runner = CrawlerRunner()  # requires the Twisted reactor to run
quotes_list = []  # store quotes
scrape_in_progress = False
scrape_complete = False


@app.route('/crawl')
def crawl_for_quotes():
    """
    Scrape for quotes
    """
    global scrape_in_progress
    global scrape_complete

    if not scrape_in_progress:
        scrape_in_progress = True
        global quotes_list
        # start the crawler and execute a callback when complete
        scrape_with_crochet(quotes_list)
        return 'SCRAPING'
    elif scrape_complete:
        scrape_in_progress = False
        scrape_complete = False
        return 'SCRAPE COMPLETE'
    return 'SCRAPE IN PROGRESS'


@app.route('/results')
def get_results():
    """
    Get the results only if a spider has results
    """
    global scrape_complete
    if scrape_complete:
        return json.dumps(quotes_list)
    return 'Scrape Still Progress'


@crochet.run_in_reactor
def scrape_with_crochet(_list):
    eventual = crawl_runner.crawl(QuoteSpider, quotes_list=_list)
    eventual.addCallback(finished_scrape)


def finished_scrape(null):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global scrape_complete
    scrape_complete = True


if __name__ == '__main__':
    app.run('0.0.0.0', 9000)
