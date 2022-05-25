


FOLDERS_NAME = ["log","db"]



SUPPORTED_DOMAIN = ['www.amazon.com.tr','www.amazon.com']

BIRIMLER = ['$','TL', "PLN"]

CREATETABLE_USERS = f"""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    is_bot INTEGER,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    language_code TEXT,
    created_at INTEGER
);"""

CREATETABLE_URLS = f"""CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT
);"""

CREATETABLE_PRODUCT = """CREATE TABLE IF NOT EXISTS products (
    id	INTEGER PRIMARY KEY,
    owner_telegram_id INTEGER,
    isim TEXT NOT NULL,
    link TEXT NOT NULL,
    fiyat_takip TEXT NOT NULL, 
    stok_takip TEXT NOT NULL,
    fiyat REAL NOT NULL,
    stok TEXT NOT NULL,
    son_kontrol_zamani REAL NOT NULL,
    created_at REAL NOT NULL,
    birim_id INTEGER NOT NULL
);"""

CREATETABLE_PRICES = """CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    fiyat REAL NOT NULL,
    time REAL NOT NULL
);"""

CREATETABLE_BIRIM = """CREATE TABLE IF NOT EXISTS birimler (
    id INTEGER PRIMARY KEY,
    birim TEXT NOT NULL,
    simge TEXT NOT NULL
);"""