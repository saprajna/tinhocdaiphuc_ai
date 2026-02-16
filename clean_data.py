# -*- coding: utf-8 -*-
"""
Script lam sach du lieu tu data.csv (V3.0 - ULTRA ROBUST)
- Chuan hoa category cuc manh voi mapping cung
- Hop nhat cot ten va gia
- Bao cao chi tiet

Tac gia: Cursor AI Agent
Ngay: 15/02/2026
"""

import pandas as pd
import re
import os
from datetime import datetime


def clean_price(price):
    """
    Lam sach gia tien
    - Xoa ky tu dac biet (d, ., ,)
    - Chuyen thanh int
    - Xu ly 'Lien he' -> 0
    """
    if pd.isna(price):
        return 0
    
    price_str = str(price).strip()
    
    # Xu ly 'Lien he', 'Contact'
    if any(x in price_str.upper() for x in ['LIEN HE', 'CONTACT', 'N/A', 'CALL']):
        return 0
    
    # Xoa cac ky tu khong phai so
    price_clean = re.sub(r'[^\d]', '', price_str)
    
    if not price_clean:
        return 0
    
    try:
        price_int = int(price_clean)
        
        # Xu ly gia bat thuong
        if price_int < 50000:  # < 50k -> 0
            return 0
        
        if price_int > 100000000:  # > 100tr -> lay 7 chu so dau
            if len(price_clean) > 10:
                price_int = int(price_clean[:7])
        
        return price_int
    
    except (ValueError, OverflowError):
        return 0


def clean_text(text):
    """Lam sach text - xoa khoang trang thua, ky tu dac biet"""
    if pd.isna(text):
        return ''
    
    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text)  # Nhieu space -> 1 space
    text = text.strip('"').strip("'")  # Xoa dau ngoac
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def normalize_category_ultra_robust(category):
    """
    Chuan hoa category CUC MANH voi mapping cung
    
    Args:
        category: Ten category goc
    
    Returns:
        str: Ten category chuan (CPU, RAM, VGA, Mainboard, SSD, HDD, Case, PSU)
    """
    if pd.isna(category) or category == '':
        return ''
    
    # Chuyen ve lowercase va trim de bat tat ca truong hop
    cat_lower = str(category).lower().strip()
    
    # ===== BANG MAPPING CUNG - CUC MANH =====
    # Mapping tu tat ca bien the -> ten chuan Web App
    
    mapping = {
        # CPU
        'cpu': 'CPU',
        'cpus': 'CPU',
        'vi xu ly': 'CPU',
        'vi xử lý': 'CPU',
        'bộ vi xử lý': 'CPU',
        'bo vi xu ly': 'CPU',
        'processor': 'CPU',
        'processors': 'CPU',
        
        # RAM
        'ram': 'RAM',
        'rams': 'RAM',
        'bo nho': 'RAM',
        'bộ nhớ': 'RAM',
        'memory': 'RAM',
        'bộ nhớ ram': 'RAM',
        'bo nho ram': 'RAM',
        
        # VGA
        'vga': 'VGA',
        'vgas': 'VGA',
        'gpu': 'VGA',
        'gpus': 'VGA',
        'card': 'VGA',
        'card man hinh': 'VGA',
        'card màn hình': 'VGA',
        'card do hoa': 'VGA',
        'card đồ họa': 'VGA',
        'graphics card': 'VGA',
        'video card': 'VGA',
        'display card': 'VGA',
        
        # Mainboard
        'main': 'Mainboard',
        'mainboard': 'Mainboard',
        'mainboards': 'Mainboard',
        'main board': 'Mainboard',
        'bo mach chu': 'Mainboard',
        'bộ mạch chủ': 'Mainboard',
        'bo mạch chủ': 'Mainboard',
        'motherboard': 'Mainboard',
        'motherboards': 'Mainboard',
        'mobo': 'Mainboard',
        'mb': 'Mainboard',
        
        # SSD
        'ssd': 'SSD',
        'ssds': 'SSD',
        'o cung ssd': 'SSD',
        'ổ cứng ssd': 'SSD',
        'o ssd': 'SSD',
        'ổ ssd': 'SSD',
        'solid state': 'SSD',
        'solid state drive': 'SSD',
        
        # HDD
        'hdd': 'HDD',
        'hdds': 'HDD',
        'o cung hdd': 'HDD',
        'ổ cứng hdd': 'HDD',
        'o hdd': 'HDD',
        'ổ hdd': 'HDD',
        'o cung': 'HDD',
        'ổ cứng': 'HDD',
        'hard disk': 'HDD',
        'hard disk drive': 'HDD',
        
        # Case
        'case': 'Case',
        'cases': 'Case',
        'thung may': 'Case',
        'thùng máy': 'Case',
        'thung': 'Case',
        'thùng': 'Case',
        'vo case': 'Case',
        'vỏ case': 'Case',
        'vo may': 'Case',
        'vỏ máy': 'Case',
        'vo': 'Case',
        'vỏ': 'Case',
        'cabinet': 'Case',
        'thung pc': 'Case',
        'thùng pc': 'Case',
        
        # PSU
        'psu': 'PSU',
        'psus': 'PSU',
        'nguon': 'PSU',
        'nguồn': 'PSU',
        'nguon may tinh': 'PSU',
        'nguồn máy tính': 'PSU',
        'nguon pc': 'PSU',
        'nguồn pc': 'PSU',
        'power supply': 'PSU',
        'power': 'PSU',
        'bo nguon': 'PSU',
        'bộ nguồn': 'PSU',
    }
    
    # Tim trong mapping
    if cat_lower in mapping:
        return mapping[cat_lower]
    
    # Neu khong tim thay, thu tim partial match
    for key, value in mapping.items():
        if key in cat_lower or cat_lower in key:
            return value
    
    # Neu van khong tim thay, return title case
    return category.strip().title()


def merge_name_columns(df):
    """Hop nhat tat ca cac cot ten (ten_*) thanh cot 'ten' duy nhat"""
    print("\n" + "=" * 80)
    print("BUOC 1: HOP NHAT CAC COT TEN")
    print("=" * 80)
    
    # Tim tat ca cac cot bat dau voi 'ten_'
    name_columns = [col for col in df.columns if col.startswith('ten_')]
    
    if not name_columns:
        print("Khong tim thay cot ten (ten_*)")
        df['ten'] = ''
        return df
    
    print("Tim thay {} cot ten:".format(len(name_columns)))
    for col in name_columns:
        non_null = df[col].notna().sum()
        print("   - {} ({} gia tri)".format(col, non_null))
    
    # Hop nhat: Lay gia tri khong null dau tien
    print("\nDang hop nhat {} cot -> 'ten'...".format(len(name_columns)))
    
    df['ten'] = df[name_columns[0]]
    for col in name_columns[1:]:
        df['ten'] = df['ten'].fillna(df[col])
    
    df['ten'] = df['ten'].fillna('')
    df['ten'] = df['ten'].apply(clean_text)
    
    # Thong ke
    non_empty = (df['ten'] != '').sum()
    print("Hoan thanh!")
    print("   - Cot moi: 'ten' (1 cot duy nhat)")
    print("   - San pham co ten: {}/{}".format(non_empty, len(df)))
    
    return df


def merge_price_columns(df):
    """Hop nhat tat ca cac cot gia thanh cot 'gia' duy nhat"""
    print("\n" + "=" * 80)
    print("BUOC 2: HOP NHAT CAC COT GIA")
    print("=" * 80)
    
    # Tim cac cot gia
    price_columns = [col for col in df.columns if any(x in col.lower() for x in ['gia', 'price', 'cost'])]
    
    if not price_columns:
        print("Khong tim thay cot gia")
        df['gia'] = 0
        return df
    
    print("Tim thay {} cot gia:".format(len(price_columns)))
    for col in price_columns:
        non_null = df[col].notna().sum()
        print("   - {} ({} gia tri)".format(col, non_null))
    
    # Hop nhat
    print("\nDang hop nhat {} cot -> 'gia'...".format(len(price_columns)))
    
    df['gia'] = df[price_columns[0]]
    for col in price_columns[1:]:
        df['gia'] = df['gia'].fillna(df[col])
    
    df['gia'] = df['gia'].apply(clean_price)
    
    # Thong ke
    valid = (df['gia'] > 0).sum()
    zero = (df['gia'] == 0).sum()
    
    print("Hoan thanh!")
    print("   - Cot moi: 'gia' (1 cot duy nhat)")
    print("   - Gia hop le (>0): {}/{}".format(valid, len(df)))
    print("   - Gia = 0: {}".format(zero))
    if valid > 0:
        print("   - Gia TB: {:,.0f}d".format(df[df['gia'] > 0]['gia'].mean()))
        print("   - Gia min: {:,.0f}d".format(df[df['gia'] > 0]['gia'].min()))
        print("   - Gia max: {:,.0f}d".format(df['gia'].max()))
    
    return df


def normalize_category_column(df):
    """
    Chuan hoa cot category CUC MANH voi mapping cung
    """
    print("\n" + "=" * 80)
    print("BUOC 3: CHUAN HOA COT CATEGORY (QUAN TRONG NHAT!)")
    print("=" * 80)
    
    if 'category' not in df.columns:
        print("Khong tim thay cot 'category'!")
        return df
    
    # Thong ke truoc khi xu ly
    print("\nTruoc khi chuan hoa:")
    print("   - Tong dong: {}".format(len(df)))
    print("   - Category null: {}".format(df['category'].isna().sum()))
    
    unique_before = df['category'].dropna().unique()
    print("   - Category unique: {}".format(len(unique_before)))
    print("   - Danh sach: {}".format(', '.join([str(c) for c in unique_before[:15]])))
    
    # ===== MAPPING CUNG - CUC MANH =====
    print("\nAp dung MAPPING CUNG...")
    
    mapping = {
        # CPU
        'cpu': 'CPU', 'cpus': 'CPU', 'vi xu ly': 'CPU', 'vi xử lý': 'CPU',
        'bộ vi xử lý': 'CPU', 'bo vi xu ly': 'CPU', 'processor': 'CPU',
        
        # RAM
        'ram': 'RAM', 'rams': 'RAM', 'bo nho': 'RAM', 'bộ nhớ': 'RAM',
        'memory': 'RAM', 'bộ nhớ ram': 'RAM', 'bo nho ram': 'RAM',
        
        # VGA
        'vga': 'VGA', 'vgas': 'VGA', 'gpu': 'VGA', 'gpus': 'VGA',
        'card': 'VGA', 'card man hinh': 'VGA', 'card màn hình': 'VGA',
        'card do hoa': 'VGA', 'card đồ họa': 'VGA',
        'graphics card': 'VGA', 'video card': 'VGA',
        
        # Mainboard
        'main': 'Mainboard', 'mainboard': 'Mainboard', 'main board': 'Mainboard',
        'bo mach chu': 'Mainboard', 'bộ mạch chủ': 'Mainboard', 'bo mạch chủ': 'Mainboard',
        'motherboard': 'Mainboard', 'mobo': 'Mainboard', 'mb': 'Mainboard',
        
        # SSD
        'ssd': 'SSD', 'ssds': 'SSD', 'o cung ssd': 'SSD', 'ổ cứng ssd': 'SSD',
        'o ssd': 'SSD', 'ổ ssd': 'SSD', 'solid state': 'SSD',
        
        # HDD
        'hdd': 'HDD', 'hdds': 'HDD', 'o cung hdd': 'HDD', 'ổ cứng hdd': 'HDD',
        'o hdd': 'HDD', 'ổ hdd': 'HDD', 'o cung': 'HDD', 'ổ cứng': 'HDD',
        'hard disk': 'HDD',
        
        # Case
        'case': 'Case', 'cases': 'Case', 'thung may': 'Case', 'thùng máy': 'Case',
        'thung': 'Case', 'thùng': 'Case', 'vo case': 'Case', 'vỏ case': 'Case',
        'vo may': 'Case', 'vỏ máy': 'Case', 'vo': 'Case', 'vỏ': 'Case',
        'cabinet': 'Case',
        
        # PSU
        'psu': 'PSU', 'psus': 'PSU', 'nguon': 'PSU', 'nguồn': 'PSU',
        'nguon may tinh': 'PSU', 'nguồn máy tính': 'PSU',
        'nguon pc': 'PSU', 'nguồn pc': 'PSU',
        'power supply': 'PSU', 'power': 'PSU',
        'bo nguon': 'PSU', 'bộ nguồn': 'PSU',
    }
    
    # Ap dung mapping
    def apply_mapping(cat):
        if pd.isna(cat) or cat == '':
            return ''
        
        # Chuyen ve lowercase va strip
        cat_clean = str(cat).lower().strip()
        
        # Tim trong mapping
        if cat_clean in mapping:
            return mapping[cat_clean]
        
        # Neu khong co, return nguyen goc (title case)
        return str(cat).strip().title()
    
    df['category'] = df['category'].apply(apply_mapping)
    
    # Xoa dong co category rong
    before_drop = len(df)
    df = df[df['category'] != '']
    df = df.dropna(subset=['category'])
    after_drop = len(df)
    
    removed = before_drop - after_drop
    if removed > 0:
        print("   Da xoa {} dong co category rong".format(removed))
    
    # Thong ke sau khi xu ly
    print("\nSau khi chuan hoa:")
    print("   - Tong dong: {}".format(len(df)))
    
    unique_after = sorted(df['category'].unique())
    print("   - Category unique: {}".format(len(unique_after)))
    print("   - Danh sach: {}".format(', '.join(unique_after)))
    
    # Dem theo tung category
    print("\nPhan bo theo category:")
    for cat in unique_after:
        count = len(df[df['category'] == cat])
        print("      - {:<12} : {:>3} san pham".format(cat, count))
    
    print("\nCategory da chuan hoa HOAN TOAN!")
    
    return df


def clean_other_columns(df):
    """Lam sach cac cot text khac"""
    print("\n" + "=" * 80)
    print("BUOC 4: LAM SACH CAC COT KHAC")
    print("=" * 80)
    
    text_columns = ['hang', 'thong_so', 'loai_ram', 'dung_luong']
    
    cleaned = 0
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
            cleaned += 1
    
    print("Da lam sach {} cot text".format(cleaned))
    
    return df


def reorder_columns(df):
    """Sap xep lai cot theo thu tu logic"""
    print("\n" + "=" * 80)
    print("BUOC 5: SAP XEP LAI CAC COT")
    print("=" * 80)
    
    # Thu tu uu tien
    priority = ['ten', 'category', 'hang', 'gia', 'thong_so', 'link_hinh_anh']
    
    # Lay cot theo thu tu
    ordered = [col for col in priority if col in df.columns]
    remaining = [col for col in df.columns if col not in ordered]
    ordered.extend(remaining)
    
    df = df[ordered]
    
    print("Thu tu cot moi:")
    for i, col in enumerate(ordered[:8], 1):
        print("   {}. {}".format(i, col))
    
    return df


def main():
    """Ham main"""
    print("\n")
    print("=" * 80)
    print("     DATA CLEANING V3.0 - ULTRA ROBUST")
    print("     Chuan hoa Category cuc manh - Fix web app")
    print("=" * 80)
    print("")
    
    print("=" * 80)
    print("BAT DAU XU LY")
    print("=" * 80)
    print("Thoi gian: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print("Input: data.csv")
    print("Output: clean_data.csv")
    print("=" * 80)
    
    # Kiem tra file
    if not os.path.exists('data.csv'):
        print("\nKhong tim thay file data.csv!")
        print("Chay lenh: python run_all.py")
        return
    
    # Doc file
    print("\nDang doc file data.csv...")
    try:
        df = pd.read_csv('data.csv', encoding='utf-8-sig')
        print("Doc thanh cong!")
        print("   - Tong dong: {}".format(len(df)))
        print("   - Tong cot: {}".format(len(df.columns)))
    except Exception as e:
        print("Loi: {}".format(e))
        return
    
    # BUOC 1: Hop nhat cot ten
    df = merge_name_columns(df)
    
    # BUOC 2: Hop nhat cot gia
    df = merge_price_columns(df)
    
    # BUOC 3: Chuan hoa category (QUAN TRONG NHAT!)
    df = normalize_category_column(df)
    
    # BUOC 4: Lam sach cac cot khac
    df = clean_other_columns(df)
    
    # BUOC 5: Sap xep lai cot
    df = reorder_columns(df)
    
    # Luu file
    print("\n" + "=" * 80)
    print("BUOC 6: LUU FILE")
    print("=" * 80)
    
    try:
        print("Dang luu vao clean_data.csv...")
        df.to_csv('clean_data.csv', index=False, encoding='utf-8-sig')
        
        file_size = os.path.getsize('clean_data.csv')
        print("Da luu thanh cong!")
        print("   - File: clean_data.csv")
        print("   - Size: {:,} bytes ({:.1f} KB)".format(file_size, file_size/1024))
        print("   - Dong: {}".format(len(df)))
        print("   - Cot: {}".format(len(df.columns)))
        
    except Exception as e:
        print("Loi khi luu: {}".format(e))
        return
    
    # Bao cao cuoi cung
    print("\n" + "=" * 80)
    print("HOAN THANH!")
    print("=" * 80)
    
    print("\nTom tat:")
    print("   - Input: data.csv ({} dong)".format(len(df)))
    print("   - Output: clean_data.csv ({} dong)".format(len(df)))
    print("   - Cot 'ten': OK (hop nhat tu {} cot)".format(len([c for c in df.columns if c.startswith('ten_')])))
    print("   - Cot 'gia': OK (da clean)")
    print("   - Cot 'category': OK (da chuan hoa)")
    
    # ===== BAO CAO CATEGORY - QUAN TRONG =====
    print("\n" + "=" * 80)
    print("BAO CAO CATEGORY (De kiem tra Web App)")
    print("=" * 80)
    
    categories = sorted(df['category'].unique())
    print("\nCac loai linh kien tim thay: {}".format(categories))
    print("\nChi tiet:")
    
    for cat in categories:
        count = len(df[df['category'] == cat])
        percentage = count / len(df) * 100
        print("   - {:<12} : {:>3} san pham ({:>5.1f}%)".format(cat, count, percentage))
    
    # Kiem tra 8 loai chuan
    print("\nKiem tra 8 loai chuan Web App can:")
    standard_categories = ['CPU', 'Mainboard', 'RAM', 'VGA', 'SSD', 'HDD', 'Case', 'PSU']
    
    for std_cat in standard_categories:
        if std_cat in categories:
            count = len(df[df['category'] == std_cat])
            print("   OK {:<12} : {} san pham".format(std_cat, count))
        else:
            print("   XX {:<12} : KHONG CO!".format(std_cat))
    
    # Canh bao neu co category khong chuan
    non_standard = [c for c in categories if c not in standard_categories]
    if non_standard:
        print("\nCategory khong chuan (can kiem tra):")
        for cat in non_standard:
            count = len(df[df['category'] == cat])
            print("   - {} : {} san pham".format(cat, count))
    
    print("\n" + "=" * 80)
    print("HUONG DAN SU DUNG")
    print("=" * 80)
    print("1. Kiem tra bao cao category o tren")
    print("2. Dam bao co du 8 loai: CPU, Mainboard, RAM, VGA, SSD, HDD, Case, PSU")
    print("3. Chay web app:")
    print("   streamlit run app.py")
    print("4. Kiem tra sidebar co hien thi du 8 loai khong")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nNguoi dung dung chuong trinh!")
    except Exception as e:
        print("\n\nLoi khong mong doi: {}".format(e))
        import traceback
        traceback.print_exc()
