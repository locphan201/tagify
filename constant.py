import os

VERSION = '20240821'

MODEL = 'en_core_web_sm'
DATA_FOLDER = 'data'
RAW_FILE = os.path.join(DATA_FOLDER, 'metadata.txt')

OUTPUT_DIR = os.path.join(DATA_FOLDER, VERSION)
os.makedirs(OUTPUT_DIR, exist_ok=True)
DATA_FILE = os.path.join(OUTPUT_DIR, 'metadata.json')
DATA_MIN_FILE = os.path.join(OUTPUT_DIR, 'metadata.min.json')
EXAMPLE_FILE = os.path.join(OUTPUT_DIR, 'example.json')
SYN_FILE = os.path.join(OUTPUT_DIR, 'synonyms.min.json')
ANT_FILE = os.path.join(OUTPUT_DIR, 'antonyms.min.json')