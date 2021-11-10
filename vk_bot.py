import random

from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow_tools import detect_intent_texts


def echo(event, vk_api):
    project_id = env.str('GOOGLE_PROJECT_ID')
    session_id = event.user_id
    language_code = 'ru-RU'
    reply_text = detect_intent_texts(project_id, session_id, [event.text], language_code)

    vk_api.messages.send(
        user_id=event.user_id,
        message=reply_text,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    vk_token = env.str('VK_TOKEN')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)