import os
import mysql.connector
from backend.app.config import settings

# SQL Dosyalarının Yolu
# backend/app/db/seed.py -> database/table_creation/
SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "database", "table_creation"))

# TABLO OLUŞTURMA SIRASI (Dependency Order)
# Bağımlılığı olmayan tablolar en üstte, bağımlı olanlar altta olmalı.
SQL_FILES_ORDERED = [
    "table_regions.sql",
    "table_languages.sql",
    "table_title_types.sql",
    "table_genres.sql",
    "table_jobs.sql",
    "table_categories.sql",
    "table_award_ceremonies.sql",
    "table_professions.sql",
    "table_award_categories.sql",
    "table_users.sql",  # Kullanıcılar genelde bağımsızdır
    "table_people.sql", # Kişiler
    
    # Bu noktadan sonra Foreign Key içeren tablolar gelir
    "table_productions.sql",        # title_types'a bağlı
    "table_alt_titles.sql",         # productions, regions, languages'e bağlı
    "table_production_genres.sql",  # productions, genres'e bağlı
    "table_ratings.sql",            # productions'a bağlı
    "table_episodes.sql",           # productions'a bağlı
    "table_person_professions.sql", # people, professions'a bağlı
    "table_cast_members.sql",       # productions, people, jobs, categories'e bağlı
    "table_directors.sql",          # productions, people'a bağlı
    "table_writers.sql",            # productions, people'a bağlı
    "table_awards.sql",             # ceremonies, award_categories, productions'a bağlı
    "table_award_nominees.sql"      # awards, people'a bağlı
]

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=settings.DB_HOST,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            autocommit=True
        )
        return conn
    except mysql.connector.Error as err:
        print(f"DB Bağlantı Hatası: {err}")
        return None

def apply_seed():
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()
    print(f"--- Veritabanı Seed İşlemi Başlatılıyor ---")
    print(f"Hedef Klasör: {SQL_DIR}")

    try:
        # Foreign key kontrolünü geçici olarak kapatabiliriz (opsiyonel ama güvenli)
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        
        for file_name in SQL_FILES_ORDERED:
            file_path = os.path.join(SQL_DIR, file_name)
            
            if not os.path.exists(file_path):
                print(f"[UYARI] Dosya bulunamadı, atlanıyor: {file_name}")
                continue
                
            print(f"İşleniyor: {file_name}...")
            
            with open(file_path, "r", encoding="utf-8") as f:
                sql_content = f.read()
            
            # multi=True sayesinde tek dosyada birden fazla SQL komutu (INSERT vs) çalıştırabiliriz
            for result in cursor.execute(sql_content, multi=True):
                pass

        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        print("--- Tüm tablolar başarıyla oluşturuldu/güncellendi ---")

    except mysql.connector.Error as err:
        print(f"\n[HATA] SQL Çalıştırma Hatası ({file_name}):\n{err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    apply_seed()