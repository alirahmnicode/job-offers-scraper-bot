from telegram import Update
from telegram.ext import ContextTypes

from crawler.scrape import JobinjaScraper
from crawler.constant import JOBINJA

base_url = "{0}?&filters%5Bkeywords%5D%5B0%5D={1}&preferred_before=1721747069&sort_by=published_at_desc"

def handle_response(text: str) -> str:
    global user_job_title

    if text not in ["no", "yes"]:
        user_job_title = text
    return text


user_job_title = ""


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text.lower()

    print(f"user {update.message.chat.id} in {user_job_title}: {text} ")

    response = handle_response(text)
    django_url = base_url.format(JOBINJA, text)
    print(django_url)
    jobinja_scraper = JobinjaScraper(django_url, text)
    print("pages founded")
    l = await jobinja_scraper.scrape_job_offers()
    print(l)
    # if text == "yes" and user_job_title != "":
    #     await update.message.reply_text(
    #         f"looking for {user_job_title} job offers for you."
    #     )
    #     results = await find_all_jobinja_pages(django_url)
    #     for page in results:
    #         for job in page:
    #             await update.message.reply_text(
    #                 f"{job.title}, {job.city}, {job.passed_days}"
    #             )
    # elif text == "no":
    #     handle_response("")
    #     await update.message.reply_text(f"type your job title again.")
    # else:
    #     response_text = f"Are you looking for {user_job_title} jobs? answer yes or no."
    #     await update.message.reply_text(response_text)
