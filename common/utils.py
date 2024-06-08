import base64
import json
from rq.job import Job
import requests
from redis import Redis
from rq import Queue
from pyt2s.services import stream_elements
# from common.models import Quest, DialogList
import os
import random

r = Redis(host='localhost', port=6379, decode_responses=True)
q = Queue("generate", connection=r)
generate_endpoint = "http://localhost:11434/api/generate"
static_path = "/home/brandon/Projects/Python-projects/running-backend/static/"
static_hostname = "http://192.168.0.17:8000/static/"
song_intermissions = [f"{static_path}Irish_Tin_Whistle.mp3", f"{static_path}Evan_King-Titan_Striker.mp3", f"{static_path}Arthur_Vyncke-Breaking_the_siege.mp3"]



def build_final_fstack(dialog_fnames):
    res = []
    is_every_other = False
    for fname in dialog_fnames:
        # add a rando
        if not is_every_other:
            res.append(fname)
        else:
            res.append(song_intermissions[random.randint(0, (len(song_intermissions) - 1))])
            res.append(fname)
        is_every_other = not is_every_other
    return res


def queued_generate(stringified_data, uuid):
    res = requests.post(generate_endpoint, data=stringified_data)
    res_json = res.json()
    obj = stream_elements.StreamElements()
    response_list = list(filter(lambda i: i, res_json["response"].split("\n")))
    tts_responses = {f"{static_path}{(base64.b64encode(dialog.encode('utf8')).decode('utf8')[:20]).replace("/", "")}.mp3" : dialog for dialog in response_list}
    
    for fname, dialog in tts_responses.items():
        # Custom Voice
        data = obj.requestTTS(dialog, 'Matthew')
        with open(fname, '+wb') as file:
            file.write(data)
    final_file_stack = build_final_fstack(tts_responses.keys())
    r.set(uuid.encode("utf8"), json.dumps(final_file_stack))


class Prompt:

    templates = []
    motivation_multiplier = ["None", "low", "medium", "high"]
    
    def __init__(self, setting: str, story_length: int, motivation_freq: str):
        self.perspective = "first person point of view"
        self.motivation = self.motivation_multiplier.index(motivation_freq)
        self.setting = setting
        self.story_length = story_length
        
    def generate_prompt(self):
        motivation_times = "tbd"
        return f"Generate an {self.perspective} story, minimum if {self.story_length} words long in a exciting {self.setting} setting, the reader will be running while reading so please give occasional story motivations to run. Please ONLY generate the story."

    def queue_generation(self, uuid):
        data = {
            "model": "llama3",
            "prompt": self.generate_prompt(),
            "stream": False
        }
        q.enqueue(queued_generate, args=(json.dumps(data), uuid))
        return True

    
