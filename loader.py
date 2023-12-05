from aiogram import Bot, Dispatcher, Router
from aiogram.enums.parse_mode import ParseMode
from utils.db.sqlite import Database
from data.config import BOT_TOKEN

dp = Dispatcher()
router = Router()
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
db = Database(path_to_db="data/main.db")
