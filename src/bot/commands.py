from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "https://docs.python-telegram-bot.org/en/v21.4/telegram.ext.application.html"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = "دنبال چه شغلی میگردی؟ فقط عنوان شغل را تایپ کنید."
    await update.message.reply_text(help_text)


async def get_job_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("send me your target job title")
