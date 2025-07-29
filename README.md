# NEMAT LASER SERVICE Telegram Bot

Bu bot NEMAT LASER SERVICE kompaniyasi uchun yaratilgan Telegram bot bo'lib, mijozlarga buyurtmalar holatini ko'rish, ma'lumotlarni qabul qilish va PDF holatda buyurtmani yuborish imkonini beradi.

## 🚀 Xususiyatlar

### 1. Ro'yxatdan o'tish
- Foydalanuvchi ismi va familiyasi
- Telefon raqami (Contact share tugmasi orqali)
- Biznes nomi
- Ma'lumotlar Google Sheets ga saqlanadi

### 2. Asosiy menyu
- 📌 Biz haqimizda
- 🔍 Zakazni tekshirish
- 📦 Umumiy zakazlar tarixi

### 3. Buyurtma tekshirish
- Client ID bo'yicha qidirish
- Barcha ishlab chiqarish bosqichlari holati
- PDF fayl sifatida yuborish

### 4. Buyurtmalar tarixi
- Mijoz nomi bo'yicha qidirish
- Barcha buyurtmalar ro'yxati
- PDF fayl sifatida yuborish

## 📋 O'rnatish

### Lokal o'rnatish

#### 1. Kerakli kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

#### 2. Konfiguratsiya
1. `.env` faylini yarating va quyidagi ma'lumotlarni kiriting:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   GOOGLE_SHEETS_ID=your_google_sheets_id_here
   ```
2. `config.json` faylida Google Service Account ma'lumotlari mavjud

#### 3. Google Sheets sozlash
1. Google Sheets da ikkita worksheet yarating:
   - "List1 - buyurtmalar" - buyurtmalar ma'lumotlari
   - "List3 - ro'yxatdan o'tganlar" - foydalanuvchilar ma'lumotlari

2. Google Service Account ga ruxsat bering

#### 4. Botni ishga tushirish
```bash
python bot.py
```

### Railway da o'rnatish

#### 1. Railway da loyiha yarating
1. [Railway.app](https://railway.app) ga kiring
2. Yangi loyiha yarating
3. GitHub repository ni ulang

#### 2. Environment Variables sozlang
Railway da quyidagi environment variables larni qo'shing:
- `TELEGRAM_BOT_TOKEN` - Telegram bot tokeni
- `GOOGLE_SHEETS_ID` - Google Sheets ID
- `GOOGLE_CREDENTIALS` - Google Service Account JSON ma'lumotlari (to'liq JSON)
- `RAILWAY_ENVIRONMENT` - true
- `RAILWAY_STATIC_URL` - loyiha nomi (masalan: nemat-laser-bot)

#### 3. Google Service Account ma'lumotlarini qo'shing
`config.json` faylini ochib, uning ichidagi barcha ma'lumotlarni nusxalab, Railway da `GOOGLE_CREDENTIALS` environment variable ga yuklang.

#### 4. Deploy qiling
Railway avtomatik ravishda loyihani deploy qiladi. Deploy tugagandan so'ng, bot URL manzilini oling va Telegram da webhook sozlang.

## 📁 Fayl strukturasi

```
├── bot.py              # Asosiy bot fayli
├── sheets_handler.py   # Google Sheets bilan ishlash
├── pdf_generator.py    # PDF fayllarini yaratish
├── config.py           # Konfiguratsiya
├── config.json         # Google Service Account (lokal uchun)
├── requirements.txt    # Kerakli kutubxonalar
├── Procfile           # Railway deployment
├── runtime.txt        # Python versiyasi
├── app.json           # Railway konfiguratsiya
├── .gitignore         # Git ignore fayllar
└── README.md          # Loyiha ma'lumoti
```

## 🔧 Texnik ma'lumotlar

- **Til:** Python 3.11.7
- **Telegram Bot API:** python-telegram-bot 20.7
- **Google Sheets:** gspread 5.12.0
- **PDF:** fpdf2 2.7.6
- **Web Framework:** Flask 3.0.0
- **Deployment:** Railway

## 📊 Google Sheets strukturasi

### List1 - buyurtmalar
- A ustun: № (Buyurtma raqami)
- B ustun: Boshlangan kun
- C ustun: Proyektlar nomi
- D ustun: Mijoz I.F.Sh
- E ustun: Kilent ID
- F ustun: Dizayner (TRUE/FALSE)
- G ustun: Lazerli kesish (TRUE/FALSE)
- H ustun: Kesish (TRUE/FALSE)
- I ustun: Gubka (TRUE/FALSE)
- J ustun: Status (%)
- K ustun: Yuborilgan checkbox
- L ustun: Mijozga jo'natilgan sana

### List3 - ro'yxatdan o'tganlar
- A ustun: Ism
- B ustun: Telefon
- C ustun: Biznes
- D ustun: Sana

## 🎯 Bot ishlash tartibi

1. **Start** - Foydalanuvchi ro'yxatdan o'tadi
2. **Asosiy menyu** - Foydalanuvchi tanlov qiladi
3. **Buyurtma tekshirish** - Client ID bo'yicha qidiradi
4. **Buyurtmalar tarixi** - Mijoz nomi bo'yicha qidiradi
5. **PDF yuborish** - Natijalar PDF fayl sifatida yuboriladi

## ⚠️ Eslatma

- TRUE = Tayyor
- FALSE = Tayyorlanmoqda
- Bo'sh yuborilgan sana = "tez fursatda tayyor bo'ladi"
