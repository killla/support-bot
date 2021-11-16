import logging.config
import random

from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow_tools import detect_intent_texts

logger = logging.getLogger('telegramLogger')


def reply_message(event, vk_api, google_project_id):
    language_code = 'ru-RU'
    reply_text, recognized = detect_intent_texts(google_project_id,
                                                 event.user_id,
                                                 [event.text],
                                                 language_code)
    if recognized:
        vk_api.messages.send(
            user_id=event.user_id,
            message=reply_text,
            random_id=random.randint(1, 1000)
        )


def listen_vk_events(vk_token, google_project_id):
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply_message(event, vk_api, google_project_id)


if __name__ == "__main__":
    env = Env()
    env.read_env()
    log_bot_token = env.str('TG_LOG_BOT_TOKEN')
    tg_chat_id = env.str("TG_LOG_CHAT_ID")
    logging.config.fileConfig('logging.conf', defaults={
                    'token': env.str('TG_LOG_BOT_TOKEN'),
                    'chat_id': env.str("TG_LOG_CHAT_ID")})
    logger.info('VK бот запущен')

    vk_token = env.str('VK_TOKEN')
    google_project_id = env.str('GOOGLE_PROJECT_ID')
    listen_vk_events(vk_token, google_project_id)
