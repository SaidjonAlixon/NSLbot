import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from sheets_handler import SheetsHandler
from pdf_generator import PDFGenerator
from config import TELEGRAM_BOT_TOKEN
import os
from flask import Flask, request

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask app yaratish
app = Flask(__name__)

# Conversation states
NAME, PHONE, BUSINESS, MAIN_MENU, CHECK_ORDER, ORDER_HISTORY = range(6)

class NematLaserBot:
    def __init__(self):
        self.sheets_handler = SheetsHandler()
        self.pdf_generator = PDFGenerator()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start komandasi"""
        user = update.effective_user
        
        # Foydalanuvchi ma'lumotlarini saqlash
        context.user_data['user_id'] = user.id
        context.user_data['username'] = user.username
        
        await update.message.reply_text(
            "Assalomu alaykum! NEMAT LASER SERVICE botiga xush kelibsiz!\n\n"
            "Botdan foydalanish uchun avval ro'yxatdan o'tishingiz kerak.\n\n"
            "Iltimos, ism va familiyangizni kiriting:"
        )
        return NAME
    
    async def get_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Foydalanuvchi ismini olish"""
        context.user_data['name'] = update.message.text
        
        # Telefon raqamini so'rash
        keyboard = [[KeyboardButton("📞 Telefon raqamini ulash", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            "Iltimos, telefon raqamingizni ulashing:",
            reply_markup=reply_markup
        )
        return PHONE
    
    async def get_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Telefon raqamini olish"""
        if update.message.contact:
            context.user_data['phone'] = update.message.contact.phone_number
        else:
            context.user_data['phone'] = update.message.text
        
        await update.message.reply_text(
            "Iltimos, biznes nomingizni kiriting:",
            reply_markup=ReplyKeyboardRemove()
        )
        return BUSINESS
    
    async def get_business(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Biznes nomini olish va ma'lumotlarni saqlash"""
        context.user_data['business'] = update.message.text
        
        # Ma'lumotlarni Google Sheets ga saqlash
        success = self.sheets_handler.add_user(
            context.user_data['name'],
            context.user_data['phone'],
            context.user_data['business']
        )
        
        if success:
            await update.message.reply_text(
                "✅ Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!\n\n"
                "Assalomu alaykum, xush kelibsiz!\n"
                "NEMAT LASER SERVICE botiga!"
            )
        else:
            await update.message.reply_text(
                "❌ Ro'yxatdan o'tishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
            )
        
        return await self.show_main_menu(update, context)
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Asosiy menyuni ko'rsatish"""
        keyboard = [
            ["📌 Biz haqimizda"],
            ["🔍 Zakazni tekshirish"],
            ["📦 Umumiy zakazlar tarixi"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "Asosiy menyu:",
            reply_markup=reply_markup
        )
        return MAIN_MENU
    
    async def handle_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Asosiy menyu tanlovlarini boshqarish"""
        text = update.message.text
        
        if text == "📌 Biz haqimizda":
            await update.message.reply_text(
                "🏢 NEMAT LASER SERVICE\n\n"
                "Biz lazerli kesish, dizayn va boshqa xizmatlar ko'rsatamiz.\n\n"
                "📞 Aloqa: +998 XX XXX XX XX\n"
                "📍 Manzil: Toshkent shahri\n"
                "🌐 Veb-sayt: www.nematlaser.uz\n\n"
                "Ish vaqti: Dushanba - Shanba, 9:00 - 18:00"
            )
            return await self.show_main_menu(update, context)
        
        elif text == "🔍 Zakazni tekshirish":
            await update.message.reply_text(
                "Iltimos, buyurtma ID raqamini kiriting:\n\n"
                "Masalan: 12345"
            )
            return CHECK_ORDER
        
        elif text == "📦 Umumiy zakazlar tarixi":
            await update.message.reply_text(
                "Iltimos, ism va familiyangizni kiriting:\n\n"
                "Masalan: Aziz Azizov"
            )
            return ORDER_HISTORY
        
        else:
            await update.message.reply_text(
                "Iltimos, menyudan biror tanlovni bosing."
            )
            return MAIN_MENU
    
    async def check_order(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Buyurtmani tekshirish"""
        client_id = update.message.text.strip()
        
        # Buyurtmani topish
        order = self.sheets_handler.find_order_by_id(client_id)
        
        if not order:
            await update.message.reply_text(
                "❌ Bu ID bilan hech qanday buyurtma topilmadi!\n\n"
                "Iltimos, to'g'ri buyurtma ID raqamini kiriting."
            )
            return CHECK_ORDER
        
        # Buyurtma ma'lumotlarini tayyorlash
        message = f"""📋 Buyurtma ma'lumotlari

🆔 Buyurtma ID: {order['client_id']}
📅 Boshlangan sana: {order['start_date']}
📝 Buyurtma: {order['project_name']}
👤 Mijoz: {order['client_name']}

🔧 Ishlab chiqarish holati:
• Dizayn: {'✅ Tayyor' if order['designer'] == 'TRUE' else '⏳ Tayyorlanmoqda'}
• Lazerli kesish: {'✅ Tayyor' if order['laser_cutting'] == 'TRUE' else '⏳ Tayyorlanmoqda'}
• Kesish: {'✅ Tayyor' if order['cutting'] == 'TRUE' else '⏳ Tayyorlanmoqda'}
• Gubka: {'✅ Tayyor' if order['sponge'] == 'TRUE' else '⏳ Tayyorlanmoqda'}

📊 Umumiy holat: {order['status']}% tayyor

"""
        
        if order['sent_date']:
            message += f"📦 Yuborilgan sana: {order['sent_date']}"
        else:
            message += "📦 Yuborilgan sana: tez fursatda tayyor bo'ladi"
        
        await update.message.reply_text(message)
        
        # PDF faylini yaratish va yuborish
        pdf_filename = self.pdf_generator.generate_order_pdf(order)
        if pdf_filename and os.path.exists(pdf_filename):
            with open(pdf_filename, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename=f"buyurtma_{order['client_id']}.pdf",
                    caption="📄 Buyurtma ma'lumotlari PDF fayli"
                )
            # PDF faylini o'chirish
            os.remove(pdf_filename)
        
        return await self.show_main_menu(update, context)
    
    async def order_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Buyurtmalar tarixini ko'rsatish"""
        client_name = update.message.text.strip()
        
        # Buyurtmalarni topish
        orders = self.sheets_handler.find_orders_by_name(client_name)
        
        if not orders:
            await update.message.reply_text(
                "❌ Bu ism bilan hech qanday buyurtma topilmadi!\n\n"
                "Iltimos, to'g'ri ism va familiyangizni kiriting."
            )
            return ORDER_HISTORY
        
        # Buyurtmalar tarixini tayyorlash
        message = f"""👤 Ism: {client_name}
📦 Zakazlar soni: {len(orders)} ta

"""
        
        for i, order in enumerate(orders, 1):
            message += f"""{i}️⃣
🆔: {order['client_id']}
📅 Sana: {order['start_date']}
📝 Mahsulot: {order['project_name']}
📊 Status: {order['status']}% tayyor

"""
        
        await update.message.reply_text(message)
        
        # PDF faylini yaratish va yuborish
        pdf_filename = self.pdf_generator.generate_orders_history_pdf(client_name, orders)
        if pdf_filename and os.path.exists(pdf_filename):
            with open(pdf_filename, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename=f"buyurtmalar_tarixi_{client_name}.pdf",
                    caption="📄 Buyurtmalar tarixi PDF fayli"
                )
            # PDF faylini o'chirish
            os.remove(pdf_filename)
        
        return await self.show_main_menu(update, context)
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Conversation ni bekor qilish"""
        await update.message.reply_text(
            "Bot ishlatish bekor qilindi.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

# Global application o'zgaruvchisi
application = None

def create_app():
    """Flask app yaratish"""
    global application
    
    # Bot yaratish
    bot = NematLaserBot()
    
    # Application yaratish
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", bot.start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_name)],
            PHONE: [MessageHandler(filters.CONTACT | filters.TEXT & ~filters.COMMAND, bot.get_phone)],
            BUSINESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_business)],
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_main_menu)],
            CHECK_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.check_order)],
            ORDER_HISTORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.order_history)],
        },
        fallbacks=[CommandHandler("cancel", bot.cancel)],
    )
    
    application.add_handler(conv_handler)
    
    return app

# Flask route yaratish
@app.route('/')
def home():
    return "NEMAT LASER SERVICE Bot ishlayapti!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Telegram webhook"""
    if request.method == 'POST':
        update = Update.de_json(request.get_json(), application.bot)
        application.process_update(update)
        return 'OK'
    return 'OK'

def main():
    """Asosiy funksiya"""
    # Botni ishga tushirish
    print("Bot ishga tushdi...")
    
    # Railway da webhook ishlatish
    if os.environ.get('RAILWAY_ENVIRONMENT'):
        # Railway da webhook ishlatish
        webhook_url = f"https://{os.environ.get('RAILWAY_STATIC_URL', 'your-app-name')}.railway.app/webhook"
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get('PORT', 8080)),
            webhook_url=webhook_url,
            allowed_updates=Update.ALL_TYPES
        )
    else:
        # Lokal da polling ishlatish
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    # Botni ishga tushirish
    create_app()
    main() 