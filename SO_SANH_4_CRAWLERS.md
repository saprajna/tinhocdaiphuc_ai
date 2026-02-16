# 📊 SO SÁNH 4 CRAWLERS: RAM - CPU - MAINBOARD - VGA

## 📅 Ngày: 15/02/2026

---

## 🔍 BẢNG SO SÁNH TỔNG QUAN

| Tính năng | RAM | CPU | Mainboard | VGA |
|-----------|-----|-----|-----------|-----|
| **File** | `crawler_ram.py` | `crawler_cpu.py` | `crawler_mainboard.py` | `crawler_vga.py` |
| **URL** | `/bo-nho-ram/` | `/cpu-bo-vi-xu-ly` | `/bo-mach-chu` | `/card-man-hinh` |
| **Selector** | `.product-item` | `.product-item` | `.product-item` | `.product-item` |
| **Category** | `'RAM'` | `'CPU'` | `'Mainboard'` | `'VGA'` |
| **Số sản phẩm** | ~219 | ~120 | ~180 | ~142 |
| **File riêng** | `ram_data.csv` | `cpu_data.csv` | `mainboard_data.csv` | `vga_data.csv` |
| **Mode ghi data.csv** | **'w'** (tạo mới) | **'a'** (append) | **'a'** (append) | **'a'** (append) |
| **Thứ tự chạy** | **1. Đầu tiên** | **2. Thứ hai** | **3. Thứ ba** | **4. Thứ tư** |
| **JS Click** | ✅ Có | ✅ Có | ✅ Có | ✅ Có |
| **Kiểm tra URL** | ✅ Có | ✅ Có | ✅ Có | ✅ Có |
| **WebDriverWait** | ≥ 20 | ≥ 20 | ≥ 20 | ≥ 20 |
| **Brand Detection** | DDR4/DDR5 | Intel/AMD | ASUS/MSI/GB | **Smart** (Chipset > Mfr) |

---

## 📊 CẤU TRÚC DỮ LIỆU

### **RAM:**
```python
ram_info = {
    'ten_ram': 'RAM Kingston Fury Beast 8GB DDR4 3200MHz',
    'loai_ram': 'DDR4',
    'dung_luong': '8GB',
    'thong_so': '8GB 3200MHz',
    'gia_vnd': 490000,
    'link_hinh_anh': 'https://...',
    'category': 'RAM'
}
```

### **CPU:**
```python
cpu_info = {
    'ten_cpu': 'Intel Core i5-12400F',
    'hang': 'Intel',
    'thong_so': 'Intel Core i5-12400F',
    'gia_vnd': 4290000,
    'link_hinh_anh': 'https://...',
    'category': 'CPU'
}
```

### **Mainboard:**
```python
mainboard_info = {
    'ten_mainboard': 'ASUS TUF GAMING B550M-PLUS',
    'hang': 'ASUS',
    'thong_so': 'ASUS TUF GAMING B550M-PLUS',
    'gia_vnd': 2790000,
    'link_hinh_anh': 'https://...',
    'category': 'Mainboard'
}
```

### **VGA:**
```python
vga_info = {
    'ten_vga': 'ASUS ROG Strix GeForce RTX 4070 Ti',
    'hang': 'NVIDIA',  # ← Smart Detection: Chipset, không phải ASUS
    'thong_so': 'ASUS ROG Strix GeForce RTX 4070 Ti',
    'gia_vnd': 21990000,
    'link_hinh_anh': 'https://...',
    'category': 'VGA'
}
```

---

## 🎯 PHÂN LOẠI HÃNG

### **RAM:**
- DDR4 (~60%)
- DDR5 (~35%)
- DDR3 (~5%)

### **CPU:**
- Intel (~55%): Core i3/i5/i7/i9, Pentium, Celeron
- AMD (~45%): Ryzen 3/5/7/9

### **Mainboard:**
- ASUS (~35%): ROG, TUF, Prime
- MSI (~25%)
- Gigabyte (~25%): Aorus
- Khác (~15%): ASRock, Biostar, EVGA, NZXT

### **VGA (Smart Detection):**

**Chipset (Ưu tiên cao):**
- NVIDIA (~60%): GeForce, RTX, GTX
- AMD (~35%): Radeon, RX
- Intel (~5%): Arc

**Manufacturer (Fallback):**
- ASUS, MSI, Gigabyte, EVGA, Zotac, Palit, Galax, Sapphire, PowerColor, XFX, ASRock

---

## 📈 THỐNG KÊ

| Loại | Số sản phẩm | % |
|------|-------------|---|
| **RAM** | 219 | 33.1% |
| **CPU** | 120 | 18.2% |
| **Mainboard** | 180 | 27.2% |
| **VGA** | 142 | 21.5% |
| **TỔNG** | **661** | **100%** |

---

## ⏱️ THỜI GIAN DỰ KIẾN

| Crawler | Thời gian | Click "Xem thêm" |
|---------|-----------|-------------------|
| **RAM** | ~60-90s | ~5 lần |
| **CPU** | ~45-60s | ~3 lần |
| **Mainboard** | ~60-80s | ~6 lần |
| **VGA** | ~60-80s | ~5 lần |
| **TỔNG** | **~4-5 phút** | ~19 lần |

---

## 🚀 WORKFLOW HOÀN CHỈNH

```
START
  ↓
┌────────────────────────┐
│ 1. CRAWLER RAM         │
│ - Tạo mới data.csv     │
│ - 219 sản phẩm         │
│ - Mode: 'w'            │
└────────────────────────┘
  ↓
┌────────────────────────┐
│ 2. CRAWLER CPU         │
│ - Append vào data.csv  │
│ - 120 sản phẩm         │
│ - Mode: 'a'            │
└────────────────────────┘
  ↓
┌────────────────────────┐
│ 3. CRAWLER MAINBOARD   │
│ - Append vào data.csv  │
│ - 180 sản phẩm         │
│ - Mode: 'a'            │
└────────────────────────┘
  ↓
┌────────────────────────┐
│ 4. CRAWLER VGA         │
│ - Append vào data.csv  │
│ - 142 sản phẩm         │
│ - Mode: 'a'            │
└────────────────────────┘
  ↓
┌────────────────────────┐
│ KẾT QUẢ               │
│ data.csv: 661 dòng    │
│ (All 4 components)    │
└────────────────────────┘
  ↓
END
```

---

## 🔧 LOGIC CLICK "XEM THÊM" (GIỐNG NHAU)

Cả 4 crawler đều dùng **CÙNG LOGIC:**

```python
while click_count < max_clicks:
    # 1. Đếm sản phẩm hiện tại
    current_count = len(driver.find_elements(..., ".product-item"))
    
    # 2. Tìm nút "Xem thêm"
    button = find_load_more_button()
    if not button:
        break
    
    # 3. Lưu URL trước khi click
    original_url = driver.current_url
    
    # 4. Click bằng JavaScript (tránh overlay)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)
    
    # 5. Kiểm tra URL sau khi click
    current_url = driver.current_url
    if 'collections' not in current_url:
        # Click nhầm overlay!
        driver.back()
        click_count -= 1
        continue
    
    # 6. Chờ sản phẩm mới load
    time.sleep(3)
    
    # 7. Đếm lại và kiểm tra tăng
    new_count = len(driver.find_elements(..., ".product-item"))
    if new_count <= current_count:
        no_change_count += 1
        if no_change_count >= 2:
            break
    else:
        print(f"✅ Tăng thêm {new_count - current_count} sản phẩm")
```

---

## 🎯 ĐIỂM ĐẶC BIỆT: VGA SMART BRAND DETECTION

### **Tại sao cần Smart Detection?**

VGA khác với các linh kiện khác vì có **2 lớp thương hiệu:**
1. **Chipset** (quan trọng nhất): NVIDIA, AMD, Intel
2. **Manufacturer** (ít quan trọng hơn): ASUS, MSI, Gigabyte...

### **Logic:**

```python
def extract_brand(name):
    name_upper = name.upper()
    
    # Bước 1: Tìm Chipset (ưu tiên cao)
    chipset_brands = {
        'NVIDIA': ['NVIDIA', 'GEFORCE', 'RTX', 'GTX'],
        'AMD': ['AMD', 'RADEON', 'RX'],
        'Intel': ['INTEL', 'ARC']
    }
    
    for brand, keywords in chipset_brands.items():
        for keyword in keywords:
            if keyword in name_upper:
                return brand  # ← Trả về ngay khi tìm thấy chipset
    
    # Bước 2: Fallback Manufacturer (nếu không tìm thấy chipset)
    manufacturer_brands = {
        'ASUS': ['ASUS', 'ROG', 'TUF', 'STRIX'],
        'MSI': ['MSI', 'GAMING X', 'VENTUS'],
        'Gigabyte': ['GIGABYTE', 'AORUS', 'EAGLE'],
        # ...
    }
    
    for brand, keywords in manufacturer_brands.items():
        for keyword in keywords:
            if keyword in name_upper:
                return brand
    
    return 'Unknown'
```

### **Ví dụ:**

| Tên sản phẩm | Kết quả | Giải thích |
|--------------|---------|------------|
| "ASUS ROG Strix GeForce RTX 4070 Ti" | **NVIDIA** | Có "GEFORCE" và "RTX" → Chipset |
| "MSI GeForce RTX 4060 Ti Gaming X" | **NVIDIA** | Có "GEFORCE" và "RTX" → Chipset |
| "Gigabyte Radeon RX 7800 XT Gaming OC" | **AMD** | Có "RADEON" và "RX" → Chipset |
| "Intel Arc A770 Limited Edition" | **Intel** | Có "ARC" → Chipset |
| "ASUS TUF Gaming A1" | **ASUS** | Không có chipset → Manufacturer |

---

## 📁 FILE OUTPUT

### **Files riêng:**
```
├── ram_data.csv        (219 dòng)
├── cpu_data.csv        (120 dòng)
├── mainboard_data.csv  (180 dòng)
└── vga_data.csv        (142 dòng)
```

### **File chung:**
```
└── data.csv            (661 dòng)
    ├── 219 dòng RAM
    ├── 120 dòng CPU
    ├── 180 dòng Mainboard
    └── 142 dòng VGA
```

---

## 📸 DEBUG FILES

### **RAM:**
- `debug_initial_load.png`
- `debug_after_load_all.png`

### **CPU:**
- `debug_cpu_initial_load.png`
- `debug_cpu_after_load_all.png`

### **Mainboard:**
- `debug_mainboard_initial_load.png`
- `debug_mainboard_after_load_all.png`

### **VGA:**
- `debug_vga_initial_load.png`
- `debug_vga_after_load_all.png`

---

## ✅ CHECKLIST SO SÁNH

| Tính năng | RAM | CPU | Mainboard | VGA |
|-----------|-----|-----|-----------|-----|
| **Selector chính** | ✅ `.product-item` | ✅ `.product-item` | ✅ `.product-item` | ✅ `.product-item` |
| **Tên** | ✅ `h3.pdLoopName a` | ✅ `h3.pdLoopName a` | ✅ `h3.pdLoopName a` | ✅ `h3.pdLoopName a` |
| **Giá** | ✅ `p.pdPrice span` | ✅ `p.pdPrice span` | ✅ `p.pdPrice span` | ✅ `p.pdPrice span` |
| **JS Click** | ✅ Có | ✅ Có | ✅ Có | ✅ Có |
| **Kiểm tra URL** | ✅ Có | ✅ Có | ✅ Có | ✅ Có |
| **WebDriverWait** | ✅ ≥ 20 | ✅ ≥ 20 | ✅ ≥ 20 | ✅ ≥ 20 |
| **Debug screenshots** | ✅ Có | ✅ Có | ✅ Có | ✅ Có |
| **Auto-detect Brand** | ✅ DDR4/DDR5 | ✅ Intel/AMD | ✅ ASUS/MSI... | ✅ **Smart** |

---

## ⚠️ ĐIỂM KHÁC BIỆT QUAN TRỌNG

### **1. Mode ghi data.csv:**
- ✅ RAM: `mode='w'` - **TẠO MỚI**
- ✅ CPU: `mode='a'` - **APPEND**
- ✅ Mainboard: `mode='a'` - **APPEND**
- ✅ VGA: `mode='a'` - **APPEND**

### **2. Thứ tự chạy:**
- ✅ RAM **phải chạy đầu tiên**
- ✅ CPU, Mainboard, VGA **phải chạy sau RAM**
- ❌ **KHÔNG** chạy ngược lại!

### **3. Cột Category:**
- RAM: `'category': 'RAM'`
- CPU: `'category': 'CPU'`
- Mainboard: `'category': 'Mainboard'`
- VGA: `'category': 'VGA'`

### **4. Brand Detection Logic:**
- RAM: Đơn giản (DDR4/DDR5/DDR3)
- CPU: Đơn giản (Intel/AMD)
- Mainboard: Đơn giản (ASUS/MSI/Gigabyte...)
- VGA: **SMART** (Chipset > Manufacturer) ← **Đặc biệt!**

---

## 🎉 KẾT LUẬN

Cả 4 crawler đều:
1. ✅ Dùng **CÙNG CẤU TRÚC CODE**
2. ✅ Dùng **CÙNG SELECTOR**
3. ✅ Dùng **CÙNG LOGIC CLICK**
4. ✅ Dùng **CÙNG CƠ CHẾ BẢO VỆ** (JS Click + URL Check)
5. ✅ Có **DEBUG SCREENSHOTS**
6. ✅ Có **TÀI LIỆU ĐẦY ĐỦ**

**Điểm đặc biệt:**
- ✨ VGA có **Smart Brand Detection** (Chipset > Manufacturer)
- ✨ RAM duy nhất có cột `dung_luong`
- ✨ RAM duy nhất dùng mode='w' (tạo mới)

**Tổng:** 661 sản phẩm từ 4 crawler! 🎉

---

**Version:** 9.0 (4 Crawlers)  
**Status:** ✅ Production Ready  
**Date:** 15/02/2026
