import json
import re
import pandas as pd

KNOWN_BRANDS = [
    "asus",
    "digma",
    "xiaomi",
    "redmi",
    "huawei",
    "honor",
    "thunderobot",
    "apple",
    "macbook",
    "acer",
    "hp",
    "lenovo",
    "msi",
    "rikor",
    "chuwi",
    "maibenben",
    "ninkear",
    "tecno",
    "machcreator",
    "veltron",
    "pwr",
    "vectron",
    "echips"
]

with open("laptops_data.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

df = pd.DataFrame(raw_data)

def extract_ram(title):
    match = re.search(r'RAM\s+(\d+)\s*ГБ', title, re.IGNORECASE)
    return int(match.group(1)) if match else None

def extract_ssd(title):
    match = re.search(r'SSD\s+(\d+)\s*ГБ', title, re.IGNORECASE)
    return int(match.group(1)) if match else None

def extract_screen(title):
    match = re.search(r'(\d+[.,]?\d*)\s*\\?"',title)
    return float(match.group(1).replace(',','.')) if match else None

def check_discrete_gpu(title):
    pattern = r'(rtx|gtx|geforce|nvidia|radeon rx)'
    return 1 if re.search(pattern, title, re.IGNORECASE) else 0

def clean_brand(title):
    text = str(title).lower()
    for brand in KNOWN_BRANDS:
        if re.search(r"\b" + brand + r"\b", text):
            if brand == "macbook":
                return "Apple"
            return brand.capitalize()
    return "Other"

df['brand'] = df['title'].apply(clean_brand)
df['ram_gb'] = df['title'].apply(extract_ram)
df['ssd_gb'] = df['title'].apply(extract_ssd)
df['screen_size'] = df['title'].apply(extract_screen)
df['is_discrete_gpu'] = df['title'].apply(check_discrete_gpu)

top_brands = df['brand'].value_counts()[lambda x: x >= 2].index
df['brand'] = df['brand'].where(df['brand'].isin(top_brands),"Other")

print(f"Загружено записей из JSON: {len(df)}")

df_clean = df.dropna(subset=['ram_gb', 'ssd_gb','price_byn']).copy()
df_clean = df_clean[df_clean['price_byn'] <= 9000]

df_clean['ram_gb'] = df_clean['ram_gb'].astype(int)
df_clean['ssd_gb'] = df_clean['ssd_gb'].astype(int)

print(f"Принято в итоговый датасет после очистки: {len(df_clean)}")

print("\n Распределение брендов:")
print(df_clean['brand'].value_counts())

print("\n Дискретные видеокарты (0 = Встроенная, 1 = Дискретная):")
print(df_clean['is_discrete_gpu'].value_counts())

print("\n Примеры обработанных данных:")
print(df_clean[['brand','ram_gb','ssd_gb','screen_size','is_discrete_gpu','price_byn',]].head())

df_clean.to_csv("laptops_cleaned.csv",index=False, encoding='utf-8-sig')
print("\n Чистая таблица сохранена в 'laptops_cleaned.csv'")

