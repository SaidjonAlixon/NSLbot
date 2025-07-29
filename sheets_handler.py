import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from config import GOOGLE_SHEETS_ID, ORDERS_SHEET, USERS_SHEET
import json
import os

class SheetsHandler:
    def __init__(self):
        # Google Sheets API uchun ruxsatlar
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Service account credentials - Railway uchun
        if os.environ.get('GOOGLE_CREDENTIALS'):
            # Railway da environment variable dan o'qish
            creds_dict = json.loads(os.environ.get('GOOGLE_CREDENTIALS'))
            creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        else:
            # Lokal da fayldan o'qish
            creds = Credentials.from_service_account_file('config.json', scopes=scope)
        
        self.client = gspread.authorize(creds)
        
        # Spreadsheet ochish
        self.spreadsheet = self.client.open_by_key(GOOGLE_SHEETS_ID)
        
        # Worksheet nomlarini tekshirish
        self._check_worksheets()
        
    def _check_worksheets(self):
        """Worksheet nomlarini tekshirish va mavjud worksheetlarni ko'rsatish"""
        try:
            worksheets = self.spreadsheet.worksheets()
            print(f"Mavjud worksheetlar:")
            for ws in worksheets:
                print(f"- {ws.title}")
            
            # Worksheet nomlarini to'g'rilash
            self.orders_sheet_name = None
            self.users_sheet_name = None
            
            # Avval aniq nomlar bilan qidiramiz
            for ws in worksheets:
                if ws.title == ORDERS_SHEET or ws.title == "List1 - buyurtmalar":
                    self.orders_sheet_name = ws.title
                elif ws.title == USERS_SHEET or ws.title == "List3 - ro'yxatdan o'tganlar":
                    self.users_sheet_name = ws.title
            
            # Agar topilmasa, qismiy nomlar bilan qidiramiz
            if not self.orders_sheet_name:
                for ws in worksheets:
                    if "list1" in ws.title.lower() or "buyurtmalar" in ws.title.lower():
                        self.orders_sheet_name = ws.title
                        break
            
            if not self.users_sheet_name:
                for ws in worksheets:
                    if "list3" in ws.title.lower() or "ro'yxatdan" in ws.title.lower():
                        self.users_sheet_name = ws.title
                        break
            
            # Agar hali ham topilmasa, birinchi worksheetlarni olamiz
            if not self.orders_sheet_name and len(worksheets) >= 1:
                self.orders_sheet_name = worksheets[0].title
                print(f"Buyurtmalar uchun birinchi worksheet ishlatiladi: {self.orders_sheet_name}")
            
            if not self.users_sheet_name and len(worksheets) >= 2:
                self.users_sheet_name = worksheets[1].title
                print(f"Foydalanuvchilar uchun ikkinchi worksheet ishlatiladi: {self.users_sheet_name}")
            
            print(f"Buyurtmalar worksheet: {self.orders_sheet_name}")
            print(f"Foydalanuvchilar worksheet: {self.users_sheet_name}")
            
        except Exception as e:
            print(f"Worksheet nomlarini tekshirishda xatolik: {e}")
        
    def add_user(self, name, phone, business):
        """Yangi foydalanuvchini qo'shish"""
        try:
            if not self.users_sheet_name:
                print("Foydalanuvchilar worksheet topilmadi!")
                return False
                
            worksheet = self.spreadsheet.worksheet(self.users_sheet_name)
            today = datetime.now().strftime('%d.%m.%Y')
            
            # Yangi qator qo'shish
            row = [name, phone, business, today]
            worksheet.append_row(row)
            print(f"Foydalanuvchi muvaffaqiyatli qo'shildi: {name}")
            return True
        except Exception as e:
            print(f"Foydalanuvchi qo'shishda xatolik: {e}")
            return False
    
    def find_order_by_id(self, client_id):
        """Client ID bo'yicha buyurtmani topish"""
        try:
            if not self.orders_sheet_name:
                print("Buyurtmalar worksheet topilmadi!")
                return None
                
            worksheet = self.spreadsheet.worksheet(self.orders_sheet_name)
            all_values = worksheet.get_all_values()
            
            print(f"Jadvalda {len(all_values)} qator mavjud")
            
            # E ustun (Client ID) - 4-indeks
            for i, row in enumerate(all_values[4:], start=5):  # 5-qatordan boshlanadi
                if len(row) > 4 and row[4] == client_id:  # E ustun
                    print(f"Buyurtma topildi: {client_id}")
                    return {
                        'row': i,
                        'order_number': row[0] if len(row) > 0 else '',
                        'start_date': row[1] if len(row) > 1 else '',
                        'project_name': row[2] if len(row) > 2 else '',
                        'client_name': row[3] if len(row) > 3 else '',
                        'client_id': row[4] if len(row) > 4 else '',
                        'designer': row[5] if len(row) > 5 else '',
                        'laser_cutting': row[6] if len(row) > 6 else '',
                        'cutting': row[7] if len(row) > 7 else '',
                        'sponge': row[8] if len(row) > 8 else '',
                        'status': row[9] if len(row) > 9 else '',
                        'sent_checkbox': row[10] if len(row) > 10 else '',
                        'sent_date': row[11] if len(row) > 11 else ''
                    }
            
            print(f"Buyurtma topilmadi: {client_id}")
            return None
        except Exception as e:
            print(f"Buyurtma qidirishda xatolik: {e}")
            return None
    
    def find_orders_by_name(self, client_name):
        """Client nomi bo'yicha barcha buyurtmalarni topish"""
        try:
            if not self.orders_sheet_name:
                print("Buyurtmalar worksheet topilmadi!")
                return []
                
            worksheet = self.spreadsheet.worksheet(self.orders_sheet_name)
            all_values = worksheet.get_all_values()
            
            orders = []
            # D ustun (Client Name) - 3-indeks
            for i, row in enumerate(all_values[4:], start=5):  # 5-qatordan boshlanadi
                if len(row) > 3 and row[3] == client_name:  # D ustun
                    order = {
                        'row': i,
                        'order_number': row[0] if len(row) > 0 else '',
                        'start_date': row[1] if len(row) > 1 else '',
                        'project_name': row[2] if len(row) > 2 else '',
                        'client_name': row[3] if len(row) > 3 else '',
                        'client_id': row[4] if len(row) > 4 else '',
                        'designer': row[5] if len(row) > 5 else '',
                        'laser_cutting': row[6] if len(row) > 6 else '',
                        'cutting': row[7] if len(row) > 7 else '',
                        'status': row[9] if len(row) > 9 else '',
                        'sent_date': row[11] if len(row) > 11 else ''
                    }
                    orders.append(order)
            
            print(f"{client_name} uchun {len(orders)} ta buyurtma topildi")
            return orders
        except Exception as e:
            print(f"Buyurtmalar qidirishda xatolik: {e}")
            return [] 