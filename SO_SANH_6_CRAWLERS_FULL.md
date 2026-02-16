# 📊 SO SÁNH ĐẦY ĐỦ 6 CRAWLERS

## 📅 Ngày: 15/02/2026

---

## 🔍 BẢNG SO SÁNH TỔNG QUAN

| Tính năng | RAM | CPU | Mainboard | VGA | SSD | HDD |
|-----------|-----|-----|-----------|-----|-----|-----|
| **File** | `crawler_ram.py` | `crawler_cpu.py` | `crawler_mainboard.py` | `crawler_vga.py` | `crawler_ssd.py` | `crawler_hdd.py` |
| **URL** | `/bo-nho-ram/` | `/cpu-bo-vi-xu-ly` | `/bo-mach-chu` | `/card-man-hinh` | `/o-cung-ssd` | `/o-cung-hdd/` |
| **Category** | `'RAM'` | `'CPU'` | `'Mainboard'` | `'VGA'` | `'SSD'` | `'HDD'` |
| **Số SP** | ~219 | ~120 | ~180 | ~146 | ~69 | ~40 |
| **File riêng** | `ram_data.csv` | `cpu_data.csv` | `mainboard_data.csv` | `vga_data.csv` | `ssd_data.csv` | `hdd_data.csv` |
| **Mode** | **'w'** | **'a'** | **'a'** | **'a'** | **'a'** | **'a'** |
| **Thứ tự** | **1** | **2** | **3** | **4** | **5** | **6** |
| **Thời gian** | ~60-90s | ~45-60s | ~60-80s | ~60-80s | ~40-50s | ~30-40s |

---

## ✅ ĐIỂM GIỐNG NHAU (TẤT CẢ 6 CRAWLER)

| Tính năng | Trạng thái |
|-----------|------------|
| **Selector chính** | ✅ `.product-item` |
| **Tên** | ✅ `h3.pdLoopName a` |
| **Giá** | ✅ `p.pdPrice span` |
| **Ảnh** | ✅ `img[data-src]` hoặc `img[src]` |
| **JS Click** | ✅ Có (tránh overlay) |
| **Kiểm tra URL** | ✅ Có (tự động fix) |
| **WebDriverWait** | ✅ ≥ 20 sản phẩm |
| **Debug screenshots** | ✅ Có |
| **User-Agent Spoofing** | ✅ Có |
| **CDP Commands** | ✅ Có |

---

## 📊 CẤU TRÚC DỮ LIỆU

### **1. RAM:**
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

### **2. CPU:**
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

### **3. Mainboard:**
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

### **4. VGA:**
```python
vga_info = {
    'ten_vga': 'ASUS ROG Strix GeForce RTX 4070 Ti',
    'hang': 'NVIDIA',  # Smart Detection: Chipset
    'thong_so': 'ASUS ROG Strix GeForce RTX 4070 Ti',
    'gia_vnd': 21990000,
    'link_hinh_anh': 'https://...',
    'category': 'VGA'
}
```

### **5. SSD:**
```python
ssd_info = {
    'ten_ssd': 'SSD Samsung 980 PRO 1TB M.2 PCIe Gen 4.0',
    'hang': 'Samsung',
    'thong_so': 'SSD Samsung 980 PRO 1TB M.2 PCIe Gen 4.0',
    'gia_vnd': 3290000,
    'link_hinh_anh': 'https://...',
    'category': 'SSD'
}
```

### **6. HDD:**
```python
hdd_info = {
    'ten_hdd': 'Seagate Barracuda 2TB 3.5'' SATA 3 7200RPM',
    'hang': 'Seagate',
    'thong_so': 'Seagate Barracuda 2TB 3.5'' SATA 3 7200RPM',
    'gia_vnd': 1490000,
    'link_hinh_anh': 'https://...',
    'category': 'HDD'
}
```

---

## 📈 THỐNG KÊ CHI TIẾT

| Loại | Số sản phẩm | % | Thời gian |
|------|-------------|---|-----------|
| **RAM** | 219 | 28.3% | ~60-90s |
| **CPU** | 120 | 15.5% | ~45-60s |
| **Mainboard** | 180 | 23.3% | ~60-80s |
| **VGA** | 146 | 18.9% | ~60-80s |
| **SSD** | 69 | 8.9% | ~40-50s |
| **HDD** | 40 | 5.2% | ~30-40s |
| **TỔNG** | **774** | **100%** | **~5-6 phút** |

---

## 🎯 PHÂN LOẠI HÃNG

### **RAM:**
- DDR4 (~60%)
- DDR5 (~35%)
- DDR3 (~5%)

### **CPU:**
- Intel (~55%)
- AMD (~45%)

### **Mainboard:**
- ASUS (~35%)
- MSI (~25%)
- Gigabyte (~25%)
- Khác (~15%)

### **VGA (Smart Detection):**
- NVIDIA (~60%)
- AMD (~35%)
- Intel (~5%)

### **SSD:**
- Samsung (~30%)
- Kingston (~20%)
- WD (~15%)
- Crucial (~10%)
- Khác (~25%)

### **HDD:**
- Seagate (~45%)
- WD (~40%)
- Toshiba (~10%)
- Khác (~5%)

---

## 💾 LOGIC GHI FILE

### **RAM (mode='w'):**
```python
# Tạo MỚI data.csv
with open('data.csv', 'w', ...) as f:
    writer.writeheader()
    writer.writerows(ram_data)
```
**Kết quả:** data.csv = 219 dòng RAM (mới tạo)

---

### **CPU, Mainboard, VGA, SSD, HDD (mode='a'):**
```python
# APPEND vào data.csv
with open('data.csv', 'a', ...) as f:
    if not file_exists:
        writer.writeheader()
    writer.writerows(data)
```

**Kết quả:**
- CPU: data.csv = 219 + 120 = 339
- Mainboard: data.csv = 339 + 180 = 519
- VGA: data.csv = 519 + 146 = 665
- SSD: data.csv = 665 + 69 = 734
- HDD: data.csv = 734 + 40 = **774 dòng**

---

## 🚀 WORKFLOW HOÀN CHỈNH

```
START
  ↓
┌────────────────────────┐
│ 1. RAM (219)           │ mode='w' - Tạo mới
└────────────────────────┘
  ↓
┌────────────────────────┐
│ 2. CPU (120)           │ mode='a' - Append
└────────────────────────┘
  ↓
┌────────────────────────┐
│ 3. MAINBOARD (180)     │ mode='a' - Append
└────────────────────────┘
  ↓
┌────────────────────────┐
│ 4. VGA (146)           │ mode='a' - Append
└────────────────────────┘
  ↓
┌────────────────────────┐
│ 5. SSD (69)            │ mode='a' - Append
└────────────────────────┘
  ↓
┌────────────────────────┐
│ 6. HDD (40)            │ mode='a' - Append
└────────────────────────┘
  ↓
┌────────────────────────┐
│ data.csv: 774 dòng     │
└────────────────────────┘
  ↓
END
```

---

## 📁 FILE OUTPUT

### **Files riêng:**
```
├── ram_data.csv        (219 dòng)
├── cpu_data.csv        (120 dòng)
├── mainboard_data.csv  (180 dòng)
├── vga_data.csv        (146 dòng)
├── ssd_data.csv        (69 dòng)
└── hdd_data.csv        (40 dòng)
```

### **File chung:**
```
└── data.csv            (774 dòng)
    ├── 219 dòng RAM
    ├── 120 dòng CPU
    ├── 180 dòng Mainboard
    ├── 146 dòng VGA
    ├── 69 dòng SSD
    └── 40 dòng HDD
```

---

## 🔧 LOGIC CLICK "XEM THÊM" (GIỐNG NHAU)

Cả 6 crawler đều dùng **CÙNG LOGIC:**

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
```

---

## ✅ CHECKLIST SO SÁNH

| Tính năng | RAM | CPU | MB | VGA | SSD | HDD |
|-----------|-----|-----|----|-----|-----|-----|
| **Selector** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **JS Click** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **URL Check** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **WebDriverWait** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Debug** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Brand Detection** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 🎉 KẾT LUẬN

**Cả 6 crawler đều:**
1. ✅ Dùng **CÙNG CẤU TRÚC CODE**
2. ✅ Dùng **CÙNG SELECTOR**
3. ✅ Dùng **CÙNG LOGIC CLICK**
4. ✅ Dùng **CÙNG CƠ CHẾ BẢO VỆ**
5. ✅ Có **DEBUG SCREENSHOTS**
6. ✅ Có **TÀI LIỆU ĐẦY ĐỦ**

**Tổng:** 774 sản phẩm từ 6 crawler! 🎉

---

**Version:** 11.0 (6 Crawlers)  
**Status:** ✅ Production Ready  
**Date:** 15/02/2026
