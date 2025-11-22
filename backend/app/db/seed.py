import os
import mysql.connector
from backend.app.config import settings

# Klasör Yolları
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CREATE_DIR = os.path.join(BASE_DIR, "database", "create")
TABLES_DIR = os.path.join(BASE_DIR, "database", "table_creation")

# SQL Dosyalarının Yüklenme Sırası (Bağımlılıklara Göre)
TABLE_FILES = [
    # Bağımsız Tablolar
    "table_users.sql",
    "table_regions.sql",
    "table_languages.sql",
    "table_title_types.sql",
    "table_genres.sql",
    "table_jobs.sql",
    "table_categories.sql",
    "table_professions.sql",
    "table_award_ceremonies.sql",
    "table_award_categories.sql",
    "table_people.sql",
    
    # Bağımlı Tablolar (Önce yukarıdakiler oluşmalı)
    "table_productions.sql",        # title_types'a bağlı
    "table_episodes.sql",           # productions'a bağlı
    "table_ratings.sql",            # productions'a bağlı
    "table_alt_titles.sql",         # productions, regions, languages'e bağlı
    "table_production_genres.sql",  # productions, genres'e bağlı
    "table_person_professions.sql", # people, professions'a bağlı
    "table_cast_members.sql",       # productions, people, jobs, categories'e bağlı
    "table_directors.sql",          # productions, people'a bağlı
    "table_writers.sql",            # productions, people'a bağlı
    "table_awards.sql",             # ceremonies, award_categories, productions'a bağlı
    "table_award_nominees.sql"      # awards, people'a bağlı
]

def get_server_connection():
    """Veritabanı ismi belirtmeden MySQL sunucusuna bağlanır (DB oluşturmak için)."""
    try:
        conn = mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            autocommit=True
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Sunucu Bağlantı Hatası: {err}")
        return None

def get_db_connection():
    """Belirli veritabanına bağlanır (Tabloları oluşturmak için)."""
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

def run_sql_file(cursor, file_path):
    """Verilen SQL dosyasını çalıştırır."""
    if not os.path.exists(file_path):
        print(f"[UYARI] Dosya bulunamadı: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Çoklu komutları (multi=True) destekler
    for result in cursor.execute(sql_content, multi=True):
        pass
    print(f"✓ Çalıştırıldı: {os.path.basename(file_path)}")

def apply_seed():
    print("--- Veritabanı Kurulumu Başlatılıyor ---")

    # 1. ADIM: Veritabanını Oluştur (Create DB)
    server_conn = get_server_connection()
    if server_conn:
        cursor = server_conn.cursor()
        creator_path = os.path.join(CREATE_DIR, "database_creator.sql")
        print(f"Veritabanı oluşturuluyor ({settings.DB_NAME})...")
        try:
            run_sql_file(cursor, creator_path)
        except mysql.connector.Error as err:
            print(f"Veritabanı oluşturma hatası: {err}")
        finally:
            cursor.close()
            server_conn.close()
    else:
        print("Sunucuya bağlanılamadı, işlem durduruluyor.")
        return

    # 2. ADIM: Tabloları Oluştur (Create Tables)
    db_conn = get_db_connection()
    if not db_conn:
        print(f"Veritabanına ({settings.DB_NAME}) bağlanılamadı. Oluşturulduğundan emin misiniz?")
        return

    cursor = db_conn.cursor()
    try:
        # Foreign Key kontrollerini geçici kapat
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        
        for file_name in TABLE_FILES:
            file_path = os.path.join(TABLES_DIR, file_name)
            try:
                run_sql_file(cursor, file_path)
            except mysql.connector.Error as err:
                print(f"HATA ({file_name}): {err}")
        
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        print("\n--- Tüm işlemler başarıyla tamamlandı! ---")

    finally:
        cursor.close()
        db_conn.close()

if __name__ == "__main__":
    apply_seed()