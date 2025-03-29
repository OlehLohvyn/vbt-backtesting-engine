# settings.py
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Отримуємо шлях з .env або за замовчуванням "data"
raw_store_dir = "data"

# Якщо шлях не абсолютний — робимо його відносним до BASE_DIR
if not os.path.isabs(raw_store_dir):
    STORE_DIRECTORY = os.path.join(BASE_DIR, raw_store_dir)
else:
    STORE_DIRECTORY = raw_store_dir
