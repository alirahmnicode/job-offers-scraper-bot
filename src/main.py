from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    filters,
    MessageHandler,
)

from bot.commands import start_command, help_command
from bot.handlers import handle_message


def main() -> None:

    app = (
        ApplicationBuilder()
        .token("7455403292:AAEzM83LM9wJSUcMlMSjFQ_BL22hsTeWHF8")
        .build()
    )
    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
