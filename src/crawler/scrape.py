import asyncio
from collections import namedtuple

import aiohttp
from bs4 import BeautifulSoup

Job = namedtuple("Job", ("title", "city", "passed_days"))
django_url = "https://jobinja.ir/jobs?&filters%5Bkeywords%5D%5B0%5D=django&preferred_before=1721747069&sort_by=published_at_desc"


async def find_all_jobinja_pages(base_url):
    print("start")
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url) as res:
            html = await res.text()
            soup = BeautifulSoup(html, features="html.parser")
            paginator = soup.find("div", attrs={"class": "paginator"})
            pages = paginator.find_all("li")

            last_page_number = int(pages[-2].find("a").get("href").split("=")[-1])
            founded_pages = pages[:-1]
            all_pages = [
                page.find("a").get("href") for page in founded_pages if page.find("a")
            ]
            all_pages.insert(0, base_url)
            if last_page_number == len(founded_pages):
                return await find_jobinja_jobs(all_pages)
            else:
                # generate all pages
                ...


async def find_jobinja_jobs(pages: list):
    print("jobs")
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[find_jobs_in_page(session, page) for page in pages]
        )
        return results


async def find_jobs_in_page(session, url) -> list[Job]:
    async with session.get(url) as res:
        html = await res.text()
        soup = BeautifulSoup(html, features="html.parser")
        jobs_box = soup.find_all("li", attrs={"class": "o-listView__item"})

        jobs = []
        for job in jobs_box:
            title = job.find(
                "a", attrs={"class": "c-jobListView__titleLink"}
            ).text.strip()
            passed_days = job.find("span", attrs={"class": "c-jobListView__passedDays"})
            city = job.find_all("li", attrs={"class": "c-jobListView__metaItem"})
            jobs.append(
                Job(
                    title=title,
                    city=city[-2].text.strip(),
                    passed_days=passed_days.text.strip(),
                )
            )
        return jobs
