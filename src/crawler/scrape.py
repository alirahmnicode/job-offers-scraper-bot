import asyncio
from collections import namedtuple

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from .job_scraper import JobsScraper
from .constant import JOBINJA_BASE_URL, JOBINJA_QUERY


Job = namedtuple("Job", ("title", "city", "passed_days"))


def pars_html(html):
    return BeautifulSoup(html, features="html.parser")


class JobinjaScraper(JobsScraper):

    async def scrape_job_offers(self) -> list[list[Job]]:
        async with ClientSession() as session:
            # find all pages
            pages = await self._find_all_pages(session)
            results = await asyncio.gather(
                *[self._scrape_page_jobs(session, page) for page in pages]
            )
            return results

    async def _find_all_pages(self, session: ClientSession) -> list[str]:
        first_page_url = await self._generate_pages_url()

        async with session.get(first_page_url) as res:
            soup = pars_html(await res.text())
            paginator = soup.find("div", attrs={"class": "paginator"})

            if paginator is not None:
                pages = paginator.find_all("li")

                last_page_number = int(pages[-2].find("a").get("href").split("=")[-1])
                founded_pages = pages[:-1]
                all_pages = []

                if last_page_number == len(founded_pages):
                    all_pages = [
                        page.find("a").get("href")
                        for page in founded_pages
                        if page.find("a")
                    ]
                    # add first page to list
                    all_pages.insert(0, first_page_url)
                else:
                    # generate all pages
                    all_pages = [
                        first_page_url + f"&page={page_number}"
                        for page_number in range(1, int(last_page_number) + 1)
                    ]
                return all_pages
            else:
                raise ValueError("the page dose not exist")

    async def _generate_pages_url(self):
        return JOBINJA_BASE_URL + JOBINJA_QUERY.format(skill=self.job_title)

    async def _scrape_page_jobs(self, session: ClientSession, url: str) -> list[Job]:
        async with session.get(url) as res:
            soup = pars_html(await res.text())
            jobs_box = soup.find_all("li", attrs={"class": "o-listView__item"})

            jobs = []
            for job in jobs_box:
                title = job.find(
                    "a", attrs={"class": "c-jobListView__titleLink"}
                ).text.strip()
                passed_days = job.find(
                    "span", attrs={"class": "c-jobListView__passedDays"}
                )
                city = job.find_all("li", attrs={"class": "c-jobListView__metaItem"})
                jobs.append(
                    Job(
                        title=title,
                        city=city[-2].text.strip(),
                        passed_days=passed_days.text.strip(),
                    )
                )
            return jobs
