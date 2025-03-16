import hashlib
import random
import string
import requests
import yaml

CONFIG = {}
with open('config.yml', 'r') as stream:
    try:
        CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(f"Error: {exc}")
if CONFIG['word_length'] <= 0:
    raise Exception("The property 'word_length' should be more than 0")
if CONFIG['min_repetitions'] <= 0:
    raise Exception("The property 'min_repetitions' should be more than 0")

def count_repeated_pattern_from_start(hash: str) -> int:
    sign: str = hash[0]
    for i in range(1, len(hash)):
        if hash[i] != sign:
            return i

coder = hashlib.sha256()
while True:
    text = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=CONFIG['word_length']))
    hash_in_hex = hashlib.sha256(text.encode()).hexdigest()
    hash_in_binary = format(int(hash_in_hex, 16), '0>42b')
    hash_in_binary = f"{"0" * (256-len(hash_in_binary))}{hash_in_binary}"
    count_from_start = count_repeated_pattern_from_start(hash_in_binary)
    max_count = count_from_start
    if max_count >= CONFIG['min_repetitions']:
        print(f"COUNT FROM START: {max_count};\n Text: {text};\n Hash (hex): {hash_in_hex};\n Hash (bin): {hash_in_binary}")

        data = {
            "word": text,
            "hashType": "sha256",
            "user": "pythonHomeBot"
        }

        response = requests.post(CONFIG['url'], json=data)
        print(f"{response.json()} ({response.status_code})\n")