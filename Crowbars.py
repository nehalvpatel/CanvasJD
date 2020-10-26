import requests
import re

from bs4 import BeautifulSoup
from os import environ, makedirs, path
from datetime import datetime

def log(msg):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + msg, flush=True)

def get_saved_entry_ids():
    entry_ids_path = "./saved_entry_ids.txt"

    if path.exists(entry_ids_path):
        with open(entry_ids_path, 'r') as file:
            txt = file.read()
            return txt.splitlines()
    else:
        return []

def save_entry_id(entry_id):
    entry_ids_path = "./saved_entry_ids.txt"
    with open(entry_ids_path, 'a') as file:
        entry_id = entry_id.strip()
        entry_id = "\n" + entry_id
        file.write(entry_id)

def download_entry(session, entry):
    splat = entry.title.split(": ")
    class_name = splat[0]
    file_name = splat[1]

    download_link = entry.link
    download_folder = environ["CANVASSYNC_INBOX_FOLDER"] + "/" + class_name
    download_path = download_folder + "/" + file_name

    if not path.exists(download_folder):
        log("Making " + class_name + " folder.")
        makedirs(download_folder)

    log("Downloading new file [" + entry.title + "] to [" + download_path + "].")

    r = session.get(download_link, stream=True)
    with open(download_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size = 8192):
            fd.write(chunk)

def fetch_sso_execution(session, sso_url):
    sso_response = session.get(sso_url)
    soup = BeautifulSoup(sso_response.text, 'html.parser')

    execution_input = soup.find(attrs={"name": "execution"})
    return execution_input["value"]

def perform_sso_login(username, password, sso_url):
    session = requests.session()
    session.post(sso_url, {
        "username": username,
        "password": password,
        "execution": fetch_sso_execution(session, sso_url),
        "_eventId": "submit",
        "geolocation": ""
    })
    return session