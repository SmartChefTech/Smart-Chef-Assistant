import enum
import logging
import requests
import os
import configparser
import openai
import hashlib
import uuid
import io

_TEMPERATURE = 1.0
_RATE_LIMIT_STATUS_CODE = 429
_GPT_NO_ANSWER = "Sorry, ChatGPT can't answer your question."

# Create a configparser object
config = configparser.ConfigParser()
# Read the configuration file from the same directory as this script
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)

if 'OPENAI' not in config:
    raise ValueError("Missing 'OPENAI' section in config.ini")

class ModelType(enum.Enum):
    basic_model = 0
    advance_model = 1


class RatelimitByProviderError(Exception):
    response: str
    status_code: int

    def __init__(self, response, status_code) -> None:
        self.response = response
        self.status_code = status_code


def request(statement: str, model_type: ModelType = ModelType.advance_model) -> str:
    # Set model.
    url = config['OPENAI'].get('url')
    api_key = config['OPENAI'].get('api_key')
    if not url or not api_key:
        raise ValueError("Missing 'url' or 'api_key' in 'OPENAI' section of config.ini")
    
    model = config['OPENAI'].get('advance_model')
    if model_type == ModelType.basic_model:
        model = config['OPENAI'].get('basic_model')
    
    headers = {
        'Authorization': f"Bearer {api_key}",
        'Content-Type': 'application/json'
    }

    request_payload = {
        'model': model,
        'temperature': _TEMPERATURE,
        'messages': [{'role': 'user', 'content': statement}],
        'response_format': {'type': 'json_object'},
    }
    response = requests.post(url, headers=headers, json=request_payload)
    logging.info(f"openai response: {response.json()}")
    if response.status_code == _RATE_LIMIT_STATUS_CODE:
        raise RatelimitByProviderError(str(response), response.status_code)
    if not response or not response.json() or not response.json().get('choices'):
        return _GPT_NO_ANSWER
    return response.json().get('choices')[0].get('message').get('content')


def _hash_string_to_uuid(input_string):
  # Create a SHA-1 hash object
  hasher = hashlib.sha1()
  # Update the hash object with the input string, encoded to bytes
  hasher.update(input_string.encode('utf-8'))
  # Get the SHA-1 hash of the string
  hash_bytes = hasher.digest()
  # Create a UUID based on the first 16 bytes of the SHA-1 hash
  return uuid.UUID(bytes=hash_bytes[:16])


def retrieve(question: str, knowledge: str, model_type: ModelType = ModelType.basic_model) -> str:
    if not knowledge:
        logging.warning(f"Knowledge is empty: question: {question}, knowledge: {knowledge}")
        return ""

    # Create a file-like object in memory
    file_content = io.BytesIO(knowledge.encode('utf-8'))
    file_content.name = f"{str(_hash_string_to_uuid(knowledge))}.txt"  # Give a name to the file-like object

    try:
        client = openai.OpenAI(api_key=config['OPENAI']['api_key'])

        # Upload the in-memory file to the assistant
        file_obj = client.files.create(file=file_content, purpose='assistants')

        # By default, use basic model for faster response and save money.
        model = config['OPENAI']['basic_model'] if model_type == ModelType.basic_model else config['OPENAI']['advance_model']

        # Add the file to the assistant
        assistant = client.beta.assistants.create(
            instructions="You are a knowledge retrieval expert.",
            model=model,
            response_format="json",
            tools=[{"type": "retrieval"}],
            file_ids=[file_obj.id]
        )

        thread = client.beta.threads.create(
            messages=[{
                "role": "user",
                "content": f"Use the uploaded document to best respond to user's query: {question}"
            }]
        )

        # Create and poll to ensure we received a response from the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        thread_messages = client.beta.threads.messages.list(thread_id=thread.id)
        if not thread_messages.data:
            logging.error(f"The retrieving returns no data, openai_retrieve({question} {file_content.name})")
            return ""

        response = thread_messages.data[0].content[0].text.value
        logging.info(f"Retrieved response: {response}")
        return response

    except Exception as e:
        logging.error(f"Error when retrieving, openai_retrieve({question} {file_content.name}): {e}")
        return ""

    finally:
        # If no assistant defined, skip.
        if assistant == None:
          return
        # Removes the file.
        client.files.delete(file_obj.id)
        logging.info(f"Deleted file {file_obj.id}")
        # Delete the assistant.
        client.beta.assistants.delete(assistant.id)
        logging.info(f"Deleted assistant {assistant.id}")