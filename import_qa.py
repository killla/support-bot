#!/usr/bin/env python

import argparse
import json
from pathlib import Path

from environs import Env
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Импорт вопросов=ответов в DialogFlow')
    parser.add_argument('filename', help='имя json файла')
    args = parser.parse_args()
    env = Env()
    env.read_env()
    project_id = env.str('GOOGLE_PROJECT_ID')
    filename = Path(args.filename)
    with open(filename, "r") as file:
        entries = json.load(file)

    for entry, entry_data in entries.items():
        training_phrases_parts = entry_data['questions']
        message_texts = entry_data['answer']
        create_intent(project_id, entry, training_phrases_parts, [message_texts])
