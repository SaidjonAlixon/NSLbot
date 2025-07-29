import os
from dotenv import load_dotenv

# Faqat lokal da .env faylini yuklash
if os.path.exists('.env'):
    load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Google Sheets ID
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')

# Google Sheets worksheet names - bu nomlar Google Sheets da mavjud bo'lishi kerak
# Agar worksheet nomlari boshqacha bo'lsa, ularni o'zgartiring
ORDERS_SHEET = 'List1'  # Buyurtmalar worksheet nomi
USERS_SHEET = 'List3'   # Foydalanuvchilar worksheet nomi 