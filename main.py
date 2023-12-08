import openai
import os
import requests
import json
import logging
import argparse
from typing import Dict


from constant import Const
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.getenv("ORG_KEY")
openai.api_key = os.getenv("SECRET_KEY")
const_obj = Const()
logging.basicConfig(filename=const_obj.LOGGER_FILENAME, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def concatenate_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Concatenate two dictionaries, combining values for common keys.

    Args:
        dict1 (dict): The first dictionary.
        dict2 (dict): The second dictionary.

    Returns:
        dict: A new dictionary containing the combined key-value pairs from both input dictionaries.

    Example:
        dict1 = {'key1': 'value1', 'key2': 'xyz', 'key3': ['a', 'b']}
        dict2 = {'key2': abc, 'key3': 'c', 'key4': 'new_value'}
        result_dict = concatenate_dicts(dict1, dict2)
        # Output: {'key1': 'value1', 'key2': [xyz, abc], 'key3': ['a', 'b', 'c'], 'key4': 'new_value'}
    """

    result = dict1.copy()

    for key, value in dict2.items():
        if key in result:
            if isinstance(result[key], list) and isinstance(value, list):
                result[key].extend(value)
            elif isinstance(result[key], list):
                result[key].append(value)
            else:
                result[key] = [result[key], value]
        else:
            result[key] = value

    return result


def post_process(dictionary: Dict) -> Dict:
    """
    Filter a dictionary to remove entries with values equal to "NOT FOUND" or empty lists.

    Parameters:
        dictionary (dict): The input dictionary to be filtered.

    Args:
        dict: A dictionary containing scraped content

    Example:
        input_dict = {'key1': 'value1', 'key2': 'NOT FOUND', 'key3': [1, 2, 'NOT FOUND']}
        filtered_dict = filter_dict(input_dict)
        # Output: {'key1': 'value1', 'key3': [1, 2]}
    """

    return {key: value for key, value in dictionary.items() if value != "NOT FOUND" and (not isinstance(value, list) or any(item != "NOT FOUND" for item in value))}


def scrapper(url: str) -> None:
    """
    Extract relevant data from HTML content using the OpenAI Chat API and save it to a JSON file.

    Args:
        url (str): The URL of the HTML site to be scraped.

    Returns:
        None: The scraped data saved to a JSON file.

    Raises:
        json.JSONDecodeError: If there is an error decoding the JSON response from the OpenAI API.
    """
    prompt_template = const_obj.PROMPT_TEMPLATE_TEXT
    response = requests.get(url)
    html_content = response.text
   
    CHUNK_SIZE =2000
    prompt_chunks = [html_content[i:i + CHUNK_SIZE] for i in range(0, len(html_content), CHUNK_SIZE)]
    scraped_data = {}

    for chunk in prompt_chunks:
        chunk = f"Prompt Template: {prompt_template}\n ```Html Content: {chunk}```"
        data = [{"role": "user", "content": chunk}]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=data,
            temperature=0,
        )
        response_message = response["choices"][0]["message"]["content"]

        try:
            response_message_dict = json.loads(response_message)
        except json.JSONDecodeError as e:
            logging.error(f'{const_obj.JSON_ERROR} {e}', exc_info=True)
            continue
       
        filtered_dict = post_process(response_message_dict)

        scraped_data = concatenate_dicts(scraped_data, filtered_dict)
    filename = const_obj.JSON_FILENAME
    with open(filename, 'w') as json_file:
        json.dump(scraped_data, json_file)

   
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help="The URL of the HTML site.", required=True)
    args = parser.parse_args()

    scrapper(args.url)
    