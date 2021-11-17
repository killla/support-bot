import logging.config

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env

from dialog_flow_tools import detect_intent_texts


logger = logging.getLogger('telegramLogger')


def reply_welcome(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте! Чем могу помочь?')


def reply_message(update: Update, context: CallbackContext) -> None:
    reply_text, _ = detect_intent_texts(context.bot_data['google_project_id'],
                                        f'tg-{update.effective_chat.id}',
                                        [update.message.text],
                                        context.bot_data['language_code'])
    update.message.reply_text(reply_text)


def start_tg_bot(token, google_project_id) -> None:
    updater = Updater(token)
    dispatcher = updater.dispatcher
    context = CallbackContext(dispatcher)
    context.bot_data['google_project_id'] = google_project_id
    context.bot_data['language_code'] = 'ru-RU'

    dispatcher.add_handler(CommandHandler("start", reply_welcome))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                          reply_message))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    log_bot_token = env.str('TG_LOG_BOT_TOKEN')
    tg_chat_id = env.str("TG_LOG_CHAT_ID")
    logging.config.fileConfig('logging.conf', defaults={
                    'token': env.str('TG_LOG_BOT_TOKEN'),
                    'chat_id': env.str("TG_LOG_CHAT_ID")})

    logger.info('Телеграм бот запущен')

    tg_bot_token = env.str('TG_BOT_TOKEN')
    google_project_id = env.str('GOOGLE_PROJECT_ID')

    start_tg_bot(tg_bot_token, google_project_id)
