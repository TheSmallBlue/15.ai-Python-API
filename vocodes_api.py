import re
import time
import json
import logging
from base64 import b64decode

import requests
from requests.exceptions import ConnectionError

#Test!

class VocodesAPI:

    logger = logging.getLogger('VoCoAPI')
    logger.addHandler(logging.StreamHandler())

    max_text_len = 500

    tts_headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'User-Agent': 'python-requests uberduck.ai-Python-API(https://github.com/TheSmallBlue/Uberduck.ai-Python-API)',
        'Content-Type': 'application/json',
        'Origin': 'https://vo.codes',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://vo.codes/',
        'Accept-Language': 'en-US,en;q=0.9,es-AR;q=0.8,es;q=0.7'
    }

    tts_url = "https://mumble.stream/speak_spectrogram"


    def __init__(self, show_debug = False):
        if show_debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.WARNING)
        self.logger.info("VocodesAPI initialization")


    def get_tts_raw(self, character, text):

        resp = {"status": "NOT SET", "data": None}

        text_len = len(text)
        if text_len > self.max_text_len:
            self.logger.warning(f'Text too long ({text_len} > {self.max_text_len}), trimming to {self.max_text_len} symbols')
            text = text[:self.max_text_len - 1]

        if not text.endswith(".") and not text.endswith("!") and not text.endswith("?"):
            if len(text) < 140:
                text += '.'
            else:
                text = text[:-1] + '.'

        self.logger.info(f'Target text: [{text}]')
        self.logger.info(f'Character: [{character}]')

        data = json.dumps({"text": text, "speaker": character})

        self.logger.info('Waiting for vo.codes response...')

        try:
            response = requests.post(self.tts_url, data=data, headers=self.tts_headers)
        except requests.exceptions.ConnectionError as e:
            resp["status"] = f"ConnectionError ({e})"
            self.logger.error(f"ConnectionError ({e})")
            return resp

        if response.status_code == 200:
            resp["status"] = "OK"
            resp["data"] = b64decode(json.loads(response.content)['audio_base64'])
            self.logger.info(f"vo.codes API response success")
            return resp
        else:
            self.logger.error(f'vo.codes API request error, Status code: {response.status_code}')
            resp["status"] = f'vo.codes API request error, Status code: {response.status_code}'
        return resp
        
    def save_to_file(self, character, text, filename=None):
        tts = self.get_tts_raw(character, text)
        if tts["status"] == "OK" and tts["data"] is not None:
            if filename is None:
                char_filename_part = "".join(x for x in character[:10] if x.isalnum())
                text_filename_part = "".join(x for x in text[:16] if x.isalnum())
                filename = f"vocodes-{char_filename_part}-{text_filename_part}-{round(time.time())}.wav"
            if not filename.endswith(".wav"):
                filename += ".wav"
            f = open(filename, 'wb')
            f.write(tts["data"])
            f.close()
            self.logger.info(f"File saved: {filename}")
            return {"status": tts["status"], "filename": filename}
        else:
            return {"status": tts["status"], "filename": None}
        


if __name__ == "__main__":
    vocodes = VocodesAPI(show_debug = True)

    print("Visit https://vo.codes to find available characters and their emotions.")

    input_str = None
    while input_str != "quit":
        print("Input character (Case sensitive!):")
        character = input()
        print("Input text:")
        text = input()
        print("Processing...")
        vocodes.save_to_file(character, text)
