from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import ConfigParser
import os


class Main:

    def __init__(self):
        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        if not os.path.isfile("telegram.conf.ini"):
            config_file = open("telegram.conf.ini", "w")
            config = ConfigParser.ConfigParser()
            config.add_section("Telegram")
            user_message = """Configuration file was not found. Please enter the API token of your Telegram bot.
            API Token: """
            config.set("Telegram", "API_Token", raw_input(user_message))
            config.write(config_file)
            config_file.close()

        # Create the EventHandler and pass it your bot's token.
        self.updater = Updater(Main.get_token())

        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher

    @staticmethod
    def get_token():
        telegram_configuration = ConfigParser.ConfigParser()
        telegram_configuration.read("telegram.conf.ini")
        token = telegram_configuration.get("Telegram", "API_Token")
        return token

    def initialize(self):
        """Start the bot."""

        # on different commands - answer in Telegram
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("help", self.help))

        # to get technical details of the chat
        self.dp.add_handler(CommandHandler("techdetails", self.technical_details))

        # on noncommand i.e message - echo the message on Telegram
        self.dp.add_handler(MessageHandler(Filters.text, self.echo))

        # log all errors
        self.dp.add_error_handler(self.error)

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.
    @staticmethod
    def start(bot, update):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    @staticmethod
    def help(bot, update):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    @staticmethod
    def technical_details(bot, update):
        reply = "Here, you would receive technical details about this chat."
        update.message.reply_text(reply)

    @staticmethod
    def echo(bot, update):
        """Echo the user message. If the user message has URLs, it shortens them."""
        message_received = update.message.text
        reply_text = message_received
        import re
        links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',\
                           message_received)
        ctr = 1
        for link in links:
            sl = str(ctr)
            reply_text = reply_text.replace(link, sl)
            ctr += 1
        update.message.reply_text(reply_text)

    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, error)


class Link:
    def __init__(self):
        self.long_url = str()

    def __call__(self, *args, **kwargs):
        print args
        ret_val = args[0].groups()
        print ret_val
        return str(ret_val)

if __name__ == '__main__':
    app = Main()
    app.initialize()
