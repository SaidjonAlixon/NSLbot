from fpdf import FPDF
from datetime import datetime

class PDFGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
    
    def generate_order_pdf(self, order_data):
        """Buyurtma ma'lumotlari uchun PDF yaratish"""
        try:
            self.pdf = FPDF()
            self.pdf.add_page()
            self.pdf.set_font("Arial", 'B', 16)
            
            # Sarlavha
            self.pdf.cell(200, 10, txt="NEMAT LASER SERVICE", ln=True, align='C')
            self.pdf.cell(200, 10, txt="Buyurtma ma'lumotlari", ln=True, align='C')
            self.pdf.ln(10)
            
            # Ma'lumotlar
            self.pdf.set_font("Arial", 'B', 12)
            self.pdf.cell(200, 10, txt=f"Buyurtma ID: {order_data['client_id']}", ln=True)
            self.pdf.cell(200, 10, txt=f"Boshlangan sana: {order_data['start_date']}", ln=True)
            
            # Buyurtma nomini qisqartirish
            project_name = order_data['project_name']
            if len(project_name) > 50:
                project_name = project_name[:50] + "..."
            self.pdf.cell(200, 10, txt=f"Buyurtma: {project_name}", ln=True)
            self.pdf.cell(200, 10, txt=f"Mijoz Ism familiyasi: {order_data['client_name']}", ln=True)
            self.pdf.ln(5)
            
            # Status ma'lumotlari
            self.pdf.set_font("Arial", 'B', 12)
            self.pdf.cell(200, 10, txt="Ishlab chiqarish holati:", ln=True)
            self.pdf.set_font("Arial", size=12)
            
            # Dizayn statusi
            designer_status = "Tayyor" if order_data['designer'] == 'TRUE' else "Tayyorlanmoqda"
            self.pdf.cell(200, 10, txt=f"Dizayn: {designer_status}", ln=True)
            
            # Lazerli kesish statusi
            laser_status = "Tayyor" if order_data['laser_cutting'] == 'TRUE' else "Tayyorlanmoqda"
            self.pdf.cell(200, 10, txt=f"Lazerli kesish: {laser_status}", ln=True)
            
            # Kesish statusi
            cutting_status = "Tayyor" if order_data['cutting'] == 'TRUE' else "Tayyorlanmoqda"
            self.pdf.cell(200, 10, txt=f"Kesish: {cutting_status}", ln=True)
            
            # Gubka statusi
            sponge_status = "Tayyor" if order_data['sponge'] == 'TRUE' else "Tayyorlanmoqda"
            self.pdf.cell(200, 10, txt=f"Gubka: {sponge_status}", ln=True)
            
            self.pdf.ln(5)
            
            # Umumiy holat
            self.pdf.set_font("Arial", 'B', 12)
            self.pdf.cell(200, 10, txt=f"Holat: {order_data['status']}% tayyor", ln=True)
            
            # Yuborilgan sana
            if order_data['sent_date']:
                self.pdf.cell(200, 10, txt=f"Zakaz tugash muddati: {order_data['sent_date']}", ln=True)
            else:
                self.pdf.cell(200, 10, txt="Zakaz tugash muddati: tez fursatda tayyor bo'ladi", ln=True)
            
            # PDF faylini saqlash
            filename = f"order_{order_data['client_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            self.pdf.output(filename)
            return filename
            
        except Exception as e:
            print(f"PDF yaratishda xatolik: {e}")
            return None
    
    def generate_orders_history_pdf(self, client_name, orders):
        """Buyurtmalar tarixi uchun PDF yaratish"""
        try:
            self.pdf = FPDF()
            self.pdf.add_page()
            self.pdf.set_font("Arial", 'B', 16)
            
            # Sarlavha
            self.pdf.cell(200, 10, txt="NEMAT LASER SERVICE", ln=True, align='C')
            self.pdf.cell(200, 10, txt="Buyurtmalar tarixi", ln=True, align='C')
            self.pdf.ln(10)
            
            # Mijoz ma'lumotlari
            self.pdf.set_font("Arial", 'B', 14)
            self.pdf.cell(200, 10, txt=f"Ism: {client_name}", ln=True)
            self.pdf.cell(200, 10, txt=f"Zakazlar soni: {len(orders)} ta", ln=True)
            self.pdf.ln(10)
            
            # Buyurtmalar ro'yxati
            for i, order in enumerate(orders, 1):
                self.pdf.set_font("Arial", 'B', 12)
                self.pdf.cell(200, 10, txt=f"{i}.", ln=True)
                
                self.pdf.set_font("Arial", size=12)
                self.pdf.cell(200, 10, txt=f"ID: {order['client_id']}", ln=True)
                self.pdf.cell(200, 10, txt=f"Sana: {order['start_date']}", ln=True)
                
                # Mahsulot nomini qisqartirish
                project_name = order['project_name']
                if len(project_name) > 50:
                    project_name = project_name[:50] + "..."
                self.pdf.cell(200, 10, txt=f"Mahsulot: {project_name}", ln=True)
                self.pdf.cell(200, 10, txt=f"Status: {order['status']}% tayyor", ln=True)
                self.pdf.ln(5)
            
            # PDF faylini saqlash
            filename = f"history_{client_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            self.pdf.output(filename)
            return filename
            
        except Exception as e:
            print(f"PDF yaratishda xatolik: {e}")
            return None 