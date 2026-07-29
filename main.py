import hashlib
import string
import secrets
from multiprocessing import Pool, cpu_count
import requests
import yaml

CONFIG = {}
DEFAULT_URL = 'https://158.220.119.11:6798/write'
DEFAULT_NICKNAME = ''
DEFAULT_WORD_LENGTH = 32
DEFAULT_MIN_REPETITIONS = 25
DEFAULT_SAVE_FILE = './save.txt'

# Precomputed lookup table for leading zeros in a single byte (0-255)
CLZ_TABLE = [8] + [7]*1 + [6]*2 + [5]*4 + [4]*8 + [3]*16 + [2]*32 + [1]*64 + [0]*128

def default_settings(*args):
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
        elif arg == 'save_file':  # FIX: Corrected typo from 'min_repetitions'
            print(f"Set default value for 'save_file'. ({DEFAULT_SAVE_FILE})")
            CONFIG['save_file'] = DEFAULT_SAVE_FILE

def count_repeated_bits(hash_bytes: bytes) -> int:
    # FIX: Isolate the very first bit to see if we are counting 0s or 1s
    first_bit = (hash_bytes[0] & 0x80) >> 7
    count = 0

    for byte in hash_bytes:
        # FIX: If the target bit is 1, invert the byte so we can look up zeros
        if first_bit == 1:
            byte = ~byte & 0xFF
            
        lz = CLZ_TABLE[byte]
        count += lz
        if lz < 8:
            break
            
    return count

def mining_worker(min_repetitions, word_length, url, nickname, save_file):
    all_signs = (string.ascii_letters + string.digits + string.punctuation).encode()

    while True:
        text_bytes = bytearray(secrets.token_bytes(word_length))

        for i in range(word_length):
            text_bytes[i] = all_signs[text_bytes[i] % len(all_signs)]

        hash_bytes = hashlib.sha256(text_bytes).digest()

        if count_repeated_bits(hash_bytes) >= min_repetitions:
            text = text_bytes.decode()
            # Pass connection details directly into the function
            send_data(text, url, nickname, save_file)
        
def send_data(word, url, nickname, save_file, with_save=True) -> int:
    data = {
            "word": word,
            "hashType": "sha256",
            "user": nickname
        }
    
    try:
        # Note: verify=False will give a warning, but keeps your original setup
        response = requests.post(url, json=data, verify=False)
        print(f"{response.json()} ({response.status_code})\n")
        return 0
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
        if with_save:
            print(f"This word has locally saved in file: {save_file}")
            with open(save_file, 'a') as file:
                file.write(f"{word}\n")
    
    return -1

def start_parallel_mining():
    cores = cpu_count()
    print(f"Spawning mining workers across {cores} CPU cores...")

    # FIX: Explicitly pass configuration values to the worker pool threads
    worker_args = [
        (
            CONFIG['min_repetitions'], 
            CONFIG['word_length'], 
            CONFIG['url'], 
            CONFIG['nickname'], 
            CONFIG['save_file']
        ) 
        for _ in range(cores)
    ]

    with Pool(cores) as pool:
        pool.starmap(mining_worker, worker_args)


if __name__ == "__main__":
    print("Loading configuration...")
    try:
        with open('./config.yml', 'r') as stream:
            try:
                CONFIG = yaml.safe_load(stream)
                if not CONFIG:
                    CONFIG = {}
            except yaml.YAMLError as exc:
                print(f"Error: {exc}")

        if 'url' not in CONFIG:
            print("The property 'url' do not exists.")
            default_settings('url')

        if 'nickname' in CONFIG:
            if len(CONFIG['nickname']) >= 32:
                print("The length of property 'nickname' should be lower than 32 signs.")
                default_settings('nickname')
        else:
            print("The property 'nickname' do not exists.")
            default_settings('nickname')

        if 'word_length' in CONFIG:
            if CONFIG['word_length'] <= 0:
                print("The property 'word_length' should be more than 0.")
                default_settings('word_length')
        else:
            print("The property 'word_length' do not exists.")
            default_settings('word_length')

        if 'min_repetitions' in CONFIG:
            if CONFIG['min_repetitions'] <= 0:
                print("The property 'min_repetitions' should be more than 0.")
                default_settings('min_repetitions')
        else:
            print("The property 'min_repetitions' do not exists.")
            default_settings('min_repetitions')

        if 'save_file' not in CONFIG:
            CONFIG['save_file'] = './save.txt'
            
    except FileNotFoundError as e:
        print("File 'config.yml' is not found. Loading default settings...")
        default_settings('url', 'nickname', 'word_length', 'min_repetitions', 'save_file')

    print("Configuration successfully loaded.")
    print("Loading local saves...")

    result = 0
    try:
        with open(CONFIG['save_file'], 'r') as file:
            for line in file:
                # Use main thread's configurations for startup upload
                result = send_data(line.strip(), CONFIG['url'], CONFIG['nickname'], CONFIG['save_file'], with_save=False)
                if result == -1:
                    print("This data could not be uploaded to the server.")
                    break

            if result == 0:
                print("This data has successfully uploaded")

        if result == 0:
            with open(CONFIG['save_file'], "w") as file:
                pass
    except FileNotFoundError:
        print("Saves do not exist.")

    print("Searching...")
    start_parallel_mining()