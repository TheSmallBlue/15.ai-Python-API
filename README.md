# Voice Synthesizer API - Uberduck.ai and Vo.codes Python API

Unofficial Python3 API for https://vo.codes/

## Installation
Requires `python >= 3.6`


Note: on Windows, in this and the following commands instead of `python3`, you may want to use `python`

Install dependencies

    python3 -m pip install requests
Grab the `vocodes_api.py` and throw it where you want to use it.

## Usage
### As command line tool:
You can use `vocodes_api.py` as executable in terminal. Launch it with
    python3 vocodes_api.py
 Visit https://uberduck.ai/ or https://vo.codes/, find the character's name through inspect element, and use them right there to get your text-to-speech dreams come true as .wav files. (**WARNING**: Character's names case sensitive! You'll get a server error if you type them in incorrectly.)
### As imported module in python code:

Suppose you put `vocodes_api.py` next to the file in which you want to use it:

#### Import class:

    from vocodes_api import VocodesAPI

#### Initialize API:

    tts_api = VocodesAPI()
Alternatively, to get verbose output:

    tts_api = VocodesAPI(show_debug=True)

#### Save TTS to file:

    tts_api.save_to_file("homer-simpson", "This is a test text", "my_tts_file.wav")
Alternatively, to automatically generate a unique file name

    tts_api.save_to_file("homer-simpson", "This is a test text")
Example output on successful request: 


    {'status': 'OK', 'filename': 'uberduck-homer-simpson-Thisisatestte-1588057995.wav'}
Example output on failed request: 

     {'status': 'Reason_why_it_failed', 'filename': None}
#### Get TTS as bytes:

    response = tts_api.get_tts_raw("homer-simpson", "This is a test text")
Example output on successful request: 


    {'status': 'OK', 'data': b'th3r3g03sy0urbyt3s'}
Example output on failed request: 

     {'status': 'Reason_why_it_failed', 'data': None}