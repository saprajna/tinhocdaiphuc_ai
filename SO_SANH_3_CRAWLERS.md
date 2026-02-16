# 📊 SO SÁNH 3 CRAWLERS: RAM - CPU - MAINBOARD

## 📅 Ngày: 15/02/2026

---

## 🔍 BẢNG SO SÁNH TỔNG QUAN

| Tính năng | RAM | CPU | Mainboard |
|-----------|-----|-----|-----------|
| **File** | `crawler_ram.py` | `crawler_cpu.py` | `crawler_mainboard.py` |
| **URL** | `/bo-nho-ram/` | `/cpu-bo-vi-xu-ly` | `/bo-mach-chu` |
| **Selector** | `.product-item` | `.product-item` | `.product-item` |
| **Category** | `'RAM'` | `'CPU'` | `'Mainboard'` |
| **Số sản phẩm** | ~219 | ~120 | ~118 |
| **File riêng** | `ram_data.csv` | `cpu_data.csv` | `mainboard_data.csv` |
| **Mode ghi data.csv** | **'w'** (tạo mới) | **'a'** (append) | **'a'** (append) |
| **Thứ tự chạy** | **1. Đầu tiên** | **2. Thứ hai** | **3. Thứ ba** |
| **JS Click** | ✅ Có | ✅ Có | ✅ Có |
| **Kiểm tra URL** | ✅ Có | ✅ Có | ✅ Có |
| **WebDriverWait** | ≥ 20 sản phẩm | ≥ 20 sản phẩm | ≥ 20 sản phẩm |

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

---

## 🔄 LOGIC GHI FILE

### **RAM (mode='w'):**
```python
# Bước 1: Lưu ram_data.csv (mode='w')
with open('ram_data.csv', 'w', ...) as f:
    writer.writeheader()
    writer.writerows(ram_data)

# Bước 2: Tạo MỚI data.csv (mode='w')
with open('data.csv', 'w', ...) as f:
    writer.writeheader()
    writer.writerows(ram_data)
```

**Kết quả:** `data.csv` = 219 dòng RAM (mới tạo)

---

### **CPU (mode='a'):**
```python
# Bước 1: Lưu cpu_data.csv (mode='w')
with open('cpu_data.csv', 'w', ...) as f:
    writer.writeheader()
    writer.writerows(cpu_data)

# Bước 2: APPEND vào data.csv (mode='a')
with open('data.csv', 'a', ...) as f:
    if not file_exists:
        writer.writeheader()
    writer.writerows(cpu_data)
```

**Kết quả:** `data.csv` = 219 RAM + 120 CPU = 339 dòng

---

### **Mainboard (mode='a'):**
```python
# Bước 1: Lưu mainboard_data.csv (mode='w')
with open('mainboard_data.csv', 'w', ...) as f:
    writer.writeheader()
    writer.writerows(mainboard_data)

# Bước 2: APPEND vào data.csv (mode='a')
with open('data.csv', 'a', ...) as f:
    if not file_exists:
        writer.writeheader()
    writer.writerows(mainboard_data)
```

**Kết quả:** `data.csv` = 219 RAM + 120 CPU + 118 Mainboard = **457 dòng**

---

## 🎯 PHÂN LOẠI HÃNG

### **RAM:**
- DDR4
- DDR5
- DDR3

### **CPU:**
- Intel (Core i3/i5/i7/i9, Pentium, Celeron)
- AMD (Ryzen 3/5/7/9)

### **Mainboard:**
- ASUS (ROG, TUF, Prime)
- MSI
- Gigabyte (Aorus)
- ASRock
- Biostar
- EVGA
- NZXT

---

## 📈 THỐNG KÊ

| Loại | Số sản phẩm | % |
|------|-------------|---|
| **RAM** | 219 | 47.9% |
| **CPU** | 120 | 26.3% |
| **Mainboard** | 118 | 25.8% |
| **TỔNG** | **457** | **100%** |

---

## ⏱️ THỜI GIAN DỰ KIẾN

| Crawler | Thời gian | Click "Xem thêm" |
|---------|-----------|-------------------|
| **RAM** | ~60-90 giây | ~5 lần |
| **CPU** | ~45-60 giây | ~3 lần |
| **Mainboard** | ~50-70 giây | ~4 lần |
| **TỔNG** | **~3-4 phút** | ~12 lần |

---

## 🔧 LOGIC CLICK "XEM THÊM" (GIỐNG NHAU)

Cả 3 crawler đều dùng **CÙNG LOGIC:**

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

## 🚀 WORKFLOW HOÀN CHỈNH

```
┌─────────────────┐
│   1. RAM        │ → mode='w' (tạo mới data.csv)
│   219 sản phẩm  │    Thời gian: ~60-90s
└─────────────────┘
         ↓
┌─────────────────┐
│   2. CPU        │ → mode='a' (append vào data.csv)
│   120 sản phẩm  │    Thời gian: ~45-60s
└─────────────────┘
         ↓
┌─────────────────┐
│ 3. MAINBOARD    │ → mode='a' (append vào data.csv)
│   118 sản phẩm  │    Thời gian: ~50-70s
└─────────────────┘
         ↓
┌─────────────────────────────────────────┐
│        data.csv: 457 sản phẩm           │
│  219 RAM + 120 CPU + 118 Mainboard      │
└─────────────────────────────────────────┘
```

---

## ⚠️ ĐIỂM KHÁC BIỆT QUAN TRỌNG

### **1. Mode ghi data.csv:**
- ✅ RAM: `mode='w'` - **TẠO MỚI**
- ✅ CPU: `mode='a'` - **APPEND**
- ✅ Mainboard: `mode='a'` - **APPEND**

### **2. Thứ tự chạy:**
- ✅ RAM **phải chạy đầu tiên**
- ✅ CPU và Mainboard **phải chạy sau RAM**
- ❌ **KHÔNG** chạy ngược lại!

### **3. Cột Category:**
- RAM: `'category': 'RAM'`
- CPU: `'category': 'CPU'`
- Mainboard: `'category': 'Mainboard'`

---

## 📁 FILE OUTPUT

### **Files riêng:**
```
├── ram_data.csv        (219 dòng)
├── cpu_data.csv        (120 dòng)
└── mainboard_data.csv  (118 dòng)
```

### **File chung:**
```
└── data.csv            (457 dòng)
    ├── 219 dòng RAM
    ├── 120 dòng CPU
    └── 118 dòng Mainboard
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

---

## ✅ CHECKLIST SO SÁNH

| Tính năng | RAM | CPU | Mainboard |
|-----------|-----|-----|-----------|
| **Selector chính** | ✅ `.product-item` | ✅ `.product-item` | ✅ `.product-item` |
| **Tên** | ✅ `h3.pdLoopName a` | ✅ `h3.pdLoopName a` | ✅ `h3.pdLoopName a` |
| **Giá** | ✅ `p.pdPrice span` | ✅ `p.pdPrice span` | ✅ `p.pdPrice span` |
| **JS Click** | ✅ Có | ✅ Có | ✅ Có |
| **Kiểm tra URL** | ✅ Có | ✅ Có | ✅ Có |
| **WebDriverWait** | ✅ ≥ 20 | ✅ ≥ 20 | ✅ ≥ 20 |
| **Debug screenshots** | ✅ Có | ✅ Có | ✅ Có |
| **Auto-detect Brand** | ✅ DDR4/DDR5 | ✅ Intel/AMD | ✅ ASUS/MSI... |

---

## 🎉 KẾT LUẬN

Cả 3 crawler đều:
1. ✅ Dùng **CÙNG CẤU TRÚC CODE**
2. ✅ Dùng **CÙNG SELECTOR**
3. ✅ Dùng **CÙNG LOGIC CLICK**
4. ✅ Dùng **CÙNG CƠ CHẾ BẢO VỆ** (JS Click + URL Check)
5. ✅ Có **DEBUG SCREENSHOTS**
6. ✅ Có **TÀI LIỆU ĐẦY ĐỦ**

**Chỉ khác:**
- ❌ URL
- ❌ Category
- ❌ Field names
- ❌ Mode ghi file

**Tổng:** 457 sản phẩm từ 3 crawler! 🎉

---

**Version:** 8.0 (3 Crawlers)  
**Status:** ✅ Production Ready  
**Date:** 15/02/2026
