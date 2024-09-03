from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv('DB_URL')
tg_token = os.getenv('BOT_TOKEN')
config_directory = 'ovpns/'
