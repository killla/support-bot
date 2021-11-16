#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging.config

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env

from dialog_flow_tools import detect_intent_texts


logger = logging.getLogger('telegramLogger')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    project_id = env.str('GOOGLE_PROJECT_ID')
    session_id = update.effective_chat.id
    language_code = 'ru-RU'
    reply_text, _ = detect_intent_texts(project_id, session_id, [update.message.text], language_code)
    update.message.reply_text(reply_text)


def main(token) -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    log_bot_token = env.str('TG_LOG_BOT_TOKEN')
    tg_chat_id = env.str("TG_LOG_CHAT_ID")
    logging.config.fileConfig('logging.conf', defaults={
                    'token': env.str('TG_LOG_BOT_TOKEN'),
                    'chat_id': env.str("TG_LOG_CHAT_ID")})

    logger.info('start tg_bot')

    tg_bot_token = env.str('TG_BOT_TOKEN')
    project_id = env.str('GOOGLE_PROJECT_ID')
    language_code = 'ru-RU'

    main(tg_bot_token)
