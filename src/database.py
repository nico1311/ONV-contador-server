from databases import Database
from decouple import config

url = config('DB_URL')
db = Database(url)
