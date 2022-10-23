from telegram.ext import Updater, CommandHandler
import requests

# Telegram Info.  Bot API code, Group ID.
telegram = ["11111111:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "-111111111"]

# Telegram initializers
updater = Updater(token=telegram[0], use_context=True)
job_queue = updater.job_queue
dp = updater.dispatcher

print("Telegram Bot has been started.")

def help(update, context):
    intro = "Telegram Bot, Version 1.0\n\n"
    text_hello = "/hello - Talk to the bot!\n"

    update.effective_message.reply_text(
        intro + text_hello
    )

def hello(update,context):
    update.effective_message.reply_text("Hello!!")

def healthCheckerPing(context):
    # HealthChecks.io is a great site for monitoring uptime.  Get a URL and then configure it here, and the
    # bot will use requests to get the URL and notify HealthChecks that it is still online.

    url = "https://hc-ping.com/fcf31670-623c-4d12-9daa-2f42f0accccc"
    requests.get(url)

def main():
    # Add command handlers that the bot will respond to
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("hello", hello))

    # Add recurring tasks
    job_queue.run_repeating(healthCheckerPing, 40)

    # Start looking for commands and wait
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()