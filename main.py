from utils.file_util import ensure_directories
from scrapers.historical_scraper import fetch_historical
from scrapers.realtime_scraper import scrape_realtime

def main():
    ensure_directories()
    fetch_historical('worldnews', total=5000)
    scrape_realtime('worldnews', limit=2000, keyword='AI')

if __name__ == "__main__":
    main()    