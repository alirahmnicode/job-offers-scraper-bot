from abc import ABC, abstractmethod


class JobsScraper(ABC):
    def __init__(self, job_title: str) -> None:
        self.job_title = str(job_title)

    @abstractmethod
    async def scrape_job_offers(self):
        """This method returns a list of Job objects in a page"""
        pass

    @abstractmethod
    async def _find_all_pages(self):
        """This method returns a list of pages urls in paginator"""
        pass

    @abstractmethod
    async def _scrape_page_jobs(self):
        """This method use scrape_job_offers for scrape all job offers for all pages"""
        pass

    @abstractmethod
    async def _generate_pages_url(self):
        pass
