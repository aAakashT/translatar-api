import requests, uuid, json
import dotenv
import os
from django.core.cache import cache
import hashlib

env = dotenv.load_dotenv()

class TranslationCache:
    """will save latest translations to cache and first try to retrive exixting
    cache """
    @staticmethod
    # generate key for cache dict
    def generate_cache_key(source_text, source_lang, target_lang):
        key_string = f"{source_text}_{source_lang}_{target_lang}"
        cache_key = hashlib.md5(key_string.encode()).hexdigest()
        return cache_key

    @staticmethod
    # fetch exixting translation
    def get_translation(source_text, source_lang, target_lang):
        cache_key = TranslationCache.generate_cache_key(source_text, source_lang, target_lang)
        cache_translation = cache.get(cache_key)
        return cache_translation

    @staticmethod
    # store latest translation
    def set_translation(source_text, source_lang, target_lang, translated_text):
        cache_key = TranslationCache.generate_cache_key(source_text, source_lang, target_lang)
        cache.set(cache_key, translated_text, timeout=3600)

# api of azure is consumed for usage of translation 
def translator_function(source_lang, source_text, target_lang):
    """ Api of azure is consumed"""
    endpoint = "https://api.cognitive.microsofttranslator.com"
    key = os.getenv("AZURE_KEY")
    location = os.getenv("LOCATION")
    path = '/translate'
    constructed_url = endpoint + path
    # target language should be list
    params = {
        'api-version': '3.0',
        'from': source_lang,
        'to': target_lang
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    request = requests.post(constructed_url, params=params, headers=headers, json=source_text)
    response = request.json()
    return response

if __name__ == "__main__":
    source_text = [{
        'text': 'I would really like to drive your car around the block a few times!'}]
    source_lang = "EN"
    target_lang = ['fr', 'hi', 'mr']
    k = translator_function(source_lang=source_lang, source_text=source_text, target_lang=target_lang)
    print(k)