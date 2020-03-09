from threading import Thread

from utils.download import download
from utils import get_logger
# from scraper import scraper
import scraper as sc
import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        super().__init__(daemon=True)

    def run(self):
        # count = 0
        while True:

            tbd_url = self.frontier.get_tbd_url()
            # print("nexturl", tbd_url)
            # if count > 0:
            #     tbd_url = False
            # count += 1
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                sc.print_data()
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = sc.scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
