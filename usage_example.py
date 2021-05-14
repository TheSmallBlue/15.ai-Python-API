import os
from vocodes_api import VocodesAPI

#Vocodes

# initialization
tts_api = VocodesAPI(show_debug=True)

# be aware that there is a serverside max text length. If text is too long, it will be trimmed.
print(tts_api.max_text_len)
### valid usage examples

# get tts raw bytes 
response = tts_api.get_tts_raw("homer-simpson", "This is a test")
assert response["status"] == "OK"
assert len(response["data"]) > 100000  # those are .wav audiofile bytes

# save tts to file with generated filename
response = tts_api.save_to_file("homer-simpson", "This is another test")
assert response["status"] == "OK"
assert response["filename"] != None  # this is a generated filename of TTS file
print(response)
os.remove(response["filename"])

# save tts to file with target filename.
response = tts_api.save_to_file("homer-simpson", "One more test", "tts.wav")
assert response["status"] == "OK"
assert response["filename"] == "tts.wav"
print(response)
os.remove("tts.wav")

# if filename doesn't end with '.wav', it will be added automatically
response = tts_api.save_to_file("homer-simpson", "Last one valid test", "randomfilename")
assert response["status"] == "OK"
assert response["filename"] == "randomfilename.wav"
print(response)
os.remove("randomfilename.wav")


### invalid usage examples

# unavailable character
response = tts_api.save_to_file("random character or an incorrect name", "Test?", "tts.wav")
assert response["status"] != "OK"
assert response["filename"] == None
print(response)

