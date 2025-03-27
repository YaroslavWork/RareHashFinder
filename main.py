import hashlib
import random
import string
import requests
import yaml
import os


CONFIG = {}
DEFAULT_URL = 'http://158.220.119.11:6798/write'
DEFAULT_NICKNAME = ''
DEFAULT_WORD_LENGTH = 32
DEFAULT_MIN_REPETITIONS = 25
DEFAULT_SAVE_FILE = './/save.txt'


def defautl_settings(*args):
    global CONFIG
    for arg in args:
        if arg == 'url':
            print(f"Set default value for 'url'. ({DEFAULT_URL})")
            CONFIG['url'] = DEFAULT_URL
        elif arg == 'nickname':
            print(f"Set default value for 'nickname'. ({DEFAULT_NICKNAME})")
            CONFIG['nickname'] = DEFAULT_NICKNAME
        elif arg == 'word_length':
            print(f"Set default value for 'word_length'. ({DEFAULT_WORD_LENGTH})")
            CONFIG['word_length'] = DEFAULT_WORD_LENGTH
        elif arg == 'min_repetitions':
            print(f"Set default value for 'min_repetitions'. ({DEFAULT_MIN_REPETITIONS})")
            CONFIG['min_repetitions'] = DEFAULT_MIN_REPETITIONS
        elif arg == 'min_repetitions':
            print(f"Set default value for 'save_file'. ({DEFAULT_SAVE_FILE})")
            CONFIG['save_file'] = DEFAULT_SAVE_FILE


def count_repeated_pattern_from_start(hash: str) -> int:
    sign: str = hash[0]
    for i in range(1, len(hash)):
        if hash[i] != sign:
            return i
        
def send_data(word, with_save=True) -> int:
    global CONFIG
    data = {
            "word": word,
            "hashType": "sha256",
            "user": CONFIG['nickname']
        }
    
    try:
        response = requests.post(CONFIG['url'], json=data, verify=False)
        print(f"{response.json()} ({response.status_code})\n")
        return 0
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
        if with_save:
            print(f"This word has locally saved in file: {CONFIG['save_file']}")
            with open(CONFIG['save_file'], 'a') as file:
                file.write(f"{word}\n")
    
    return -1


print("Loading configuration...")
try:
    with open('./config.yml', 'r') as stream:
        try:
            CONFIG = yaml.safe_load(stream)
            if not CONFIG:
                CONFIG = {}
        except yaml.YAMLError as exc:
            print(f"Error: {exc}")

    if not 'url' in CONFIG.keys():
        print("The property 'url' do not exists.")
        defautl_settings('url')

    if 'nickname' in CONFIG.keys():
        if len(CONFIG['nickname']) >= 32:
            print("The length of property 'nickname' should be lower than 32 signs.")
            defautl_settings('nickname')
    else:
        print("The property 'nickname' do not exists.")
        defautl_settings('nickname')

    if 'word_length' in CONFIG.keys():
        if CONFIG['word_length'] <= 0:
            print("The property 'word_length' should be more than 0.")
            defautl_settings('word_length')
    else:
        print("The property 'word_length' do not exists.")
        defautl_settings('word_length')

    if 'min_repetitions' in CONFIG.keys():
        if CONFIG['min_repetitions'] <= 0:
            print("The property 'min_repetitions' should be more than 0.")
            defautl_settings('min_repetitions')
    else:
        print("The property 'min_repetitions' do not exists.")
        defautl_settings('min_repetitions')

    if 'save_file' not in CONFIG.keys():
        CONFIG['save_file'] = './/save.txt'
    
except FileNotFoundError as e:
    print("File 'config.yml' is not founded. Loading default settings...")
    defautl_settings('url', 'nickname', 'word_length', 'min_repetitions', 'save_file')

print("Configuration successfully loaded.")
print("Loading local saves...")

result = 0
try:
    with open(CONFIG['save_file'], 'r') as file:
        for line in file:
            result = send_data(line.strip(), with_save=False)
            if result == -1:
                print("This data could not be uploaded to the server.")
                break

        if result == 0:
            print("This data has successfully uploaded")

    if result == 0:
        with open(CONFIG['save_file'], "w") as file:
            pass
except FileNotFoundError:
    print("Saves do not exists.")

print("Searching...")
coder = hashlib.sha256()
while True:
    text = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=CONFIG['word_length']))
    hash_in_hex = hashlib.sha256(text.encode()).hexdigest()
    hash_in_binary = format(int(hash_in_hex, 16), '0>42b')
    padding = "0" * (256-len(hash_in_binary))
    hash_in_binary = f"{padding}{hash_in_binary}"
    count_from_start = count_repeated_pattern_from_start(hash_in_binary)
    max_count = count_from_start
    if max_count >= CONFIG['min_repetitions']:
        print(f"COUNT FROM START: {max_count};\nText: ----- {text} -----\nHash (hex): {hash_in_hex};\nHash (bin): {hash_in_binary}")

        send_data(text)