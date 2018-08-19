import os
import json


def create_folders():
    list_path = ['output',
                 'output/video',
                 'output/frames',
                 'output/gif']
    for f in list_path:
        if not os.path.isdir(f):
            os.mkdir(f)

def create_credential_file():
    if not os.path.isfile("bot_config.json"):
        dic = {"token": "",
            "authorized_ids": []}
        with open("bot_config.json", "w") as f:
            json.dump(dic, f)


create_credential_file()
create_folders()
