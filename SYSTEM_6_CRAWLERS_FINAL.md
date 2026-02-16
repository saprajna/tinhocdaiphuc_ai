# 🎯 HỆ THỐNG 6 CRAWLERS - HOÀN CHỈNH

## 📅 Ngày: 15/02/2026

---

## 🚀 TỔNG QUAN

```
┌────────────────────────────────────────────────────┐
│       TIN HỌC NGÔI SAO - CRAWLER SYSTEM           │
│                                                    │
│   6 Crawlers | 774 Products | 1 CSV Database     │
└────────────────────────────────────────────────────┘
```

---

## 📊 DANH SÁCH CRAWLER

| # | Crawler | URL | Sản phẩm | File | Mode |
|---|---------|-----|----------|------|------|
| 1️⃣ | **RAM** | `/bo-nho-ram/` | 219 | `ram_data.csv` | **'w'** |
| 2️⃣ | **CPU** | `/cpu-bo-vi-xu-ly` | 120 | `cpu_data.csv` | **'a'** |
| 3️⃣ | **Mainboard** | `/bo-mach-chu` | 180 | `mainboard_data.csv` | **'a'** |
| 4️⃣ | **VGA** | `/card-man-hinh` | 146 | `vga_data.csv` | **'a'** |
| 5️⃣ | **SSD** | `/o-cung-ssd` | 69 | `ssd_data.csv` | **'a'** |
| 6️⃣ | **HDD** | `/o-cung-hdd/` | 40 | `hdd_data.csv` | **'a'** |
| **TỔNG** | - | - | **774** | `data.csv` | - |

---

## 📈 PHÂN BỐ SẢN PHẨM

```
RAM:        219 sản phẩm  ████████████████████████████  (28.3%)
CPU:        120 sản phẩm  ███████████████               (15.5%)
Mainboard:  180 sản phẩm  ███████████████████████       (23.3%)
VGA:        146 sản phẩm  ██████████████████            (18.9%)
SSD:         69 sản phẩm  ████████                      (8.9%)
HDD:         40 sản phẩm  █████                         (5.2%)
──────────────────────────────────────────────────────────────
TỔNG:       774 sản phẩm  ████████████████████████████  (100%)
```

---

## ⚡ QUICK START

### **Tự động (Windows) - KHUYẾN NGHỊ:**
```bash
run_all_crawlers.bat
```

### **Thủ công:**
```bash
python crawler_ram.py
python crawler_cpu.py
python crawler_mainboard.py
python crawler_vga.py
python crawler_ssd.py
python crawler_hdd.py
```

**Thời gian:** ~5-6 phút

---

## 🔄 WORKFLOW TỰ ĐỘNG

```
START (0 sản phẩm)
  ↓
RAM (219) ────────→ data.csv: 219 dòng
  ↓
CPU (120) ────────→ data.csv: 339 dòng
  ↓
MAINBOARD (180) ──→ data.csv: 519 dòng
  ↓
VGA (146) ────────→ data.csv: 665 dòng
  ↓
SSD (69) ─────────→ data.csv: 734 dòng
  ↓
HDD (40) ─────────→ data.csv: 774 dòng
  ↓
END (774 sản phẩm)
```

---

## 📁 CẤU TRÚC HỆ THỐNG

```
📦 Crawler System v11.0
│
├── 🤖 Crawlers (6)
│   ├── crawler_ram.py
│   ├── crawler_cpu.py
│   ├── crawler_mainboard.py
│   ├── crawler_vga.py
│   ├── crawler_ssd.py
│   └── crawler_hdd.py
│
├── 📊 Data Files (7)
│   ├── ram_data.csv        (219)
│   ├── cpu_data.csv        (120)
│   ├── mainboard_data.csv  (180)
│   ├── vga_data.csv        (146)
│   ├── ssd_data.csv        (69)
│   ├── hdd_data.csv        (40)
│   └── data.csv            (774) ← File chính
│
├── 🎨 Debug Files (12+)
│   ├── debug_initial_load.png
│   ├── debug_cpu_initial_load.png
│   ├── debug_mainboard_initial_load.png
│   ├── debug_vga_initial_load.png
│   ├── debug_ssd_initial_load.png
│   ├── debug_hdd_initial_load.png
│   └── ... (after_load_all.png cho mỗi crawler)
│
├── 🚀 Automation (1)
│   └── run_all_crawlers.bat
│
└── 📚 Documentation (10+)
    ├── README_CRAWLERS.md
    ├── SYSTEM_6_CRAWLERS_FINAL.md (file này)
    ├── SO_SANH_6_CRAWLERS_FULL.md
    ├── HUONG_DAN_*_CRAWLER.md (6 files)
    └── ... (các file khác)
```

---

## 🛡️ CƠ CHẾ BẢO VỆ CHUNG

Cả 6 crawler đều có:

### **1. JavaScript Click**
```python
driver.execute_script("arguments[0].click();", button)
```

### **2. URL Validation**
```python
if 'collections' not in current_url:
    driver.back()
```

### **3. WebDriverWait**
```python
wait.until(lambda d: len(d.find_elements(...)) >= 20)
```

### **4. User-Agent Spoofing**
```python
options.add_argument('user-agent=Mozilla/5.0 ...')
```

### **5. CDP Commands**
```python
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {...})
```

---

## 📊 DATA.CSV STRUCTURE

```csv
ten,hang,dung_luong,thong_so,gia_vnd,link_hinh_anh,category
"RAM Kingston Fury Beast 8GB DDR4",DDR4,8GB,8GB 3200MHz,490000,https://...,RAM
"Intel Core i5-12400F",Intel,"Intel Core i5-12400F",4290000,https://...,CPU
"ASUS TUF GAMING B550M-PLUS",ASUS,"ASUS TUF GAMING B550M-PLUS",2790000,https://...,Mainboard
"ASUS ROG Strix GeForce RTX 4070 Ti",NVIDIA,"ASUS ROG Strix GeForce RTX 4070 Ti",21990000,https://...,VGA
"SSD Samsung 980 PRO 1TB M.2 PCIe",Samsung,"SSD Samsung 980 PRO 1TB M.2 PCIe",3290000,https://...,SSD
"Seagate Barracuda 2TB 7200RPM",Seagate,"Seagate Barracuda 2TB 7200RPM",1490000,https://...,HDD
... (774 dòng)
```

---

## ⏱️ THỜI GIAN CHI TIẾT

| Crawler | Load trang | Click "Xem thêm" | Crawl data | Lưu CSV | Tổng |
|---------|------------|-------------------|------------|---------|------|
| RAM | 5s | ~5 lần × 5s = 25s | 30s | 5s | ~65s |
| CPU | 5s | ~3 lần × 5s = 15s | 20s | 5s | ~45s |
| Mainboard | 5s | ~6 lần × 5s = 30s | 25s | 5s | ~65s |
| VGA | 5s | ~5 lần × 5s = 25s | 25s | 5s | ~60s |
| SSD | 5s | ~2 lần × 5s = 10s | 15s | 5s | ~35s |
| HDD | 5s | ~1 lần × 5s = 5s | 10s | 5s | ~25s |
| **TỔNG** | - | - | - | - | **~5-6 phút** |

---

## 🎯 BRAND DETECTION

| Crawler | Logic | Ví dụ |
|---------|-------|-------|
| **RAM** | Đơn giản | DDR4, DDR5, DDR3 |
| **CPU** | Đơn giản | Intel, AMD |
| **Mainboard** | Đơn giản | ASUS, MSI, Gigabyte |
| **VGA** | **SMART** (Chipset > Mfr) | NVIDIA, AMD, Intel |
| **SSD** | Đơn giản | Samsung, Kingston, WD |
| **HDD** | Đơn giản | Seagate, WD, Toshiba |

---

## ✅ CHECKLIST HOÀN CHỈNH

### **Setup:**
- [ ] Python 3.7+
- [ ] Chrome browser
- [ ] `pip install selenium webdriver-manager pandas`

### **Chạy:**
- [ ] `run_all_crawlers.bat`
- [ ] Chờ ~5-6 phút

### **Kiểm tra:**
- [ ] `ram_data.csv` - 219 dòng
- [ ] `cpu_data.csv` - 120 dòng
- [ ] `mainboard_data.csv` - 180 dòng
- [ ] `vga_data.csv` - 146 dòng
- [ ] `ssd_data.csv` - 69 dòng
- [ ] `hdd_data.csv` - 40 dòng
- [ ] `data.csv` - **774 dòng**
- [ ] Cột `category` có đủ 6 loại

---

## 📚 TÀI LIỆU ĐẦY ĐỦ

| File | Mô tả |
|------|-------|
| `README_CRAWLERS.md` | Hướng dẫn tổng quan |
| `SYSTEM_6_CRAWLERS_FINAL.md` | File này |
| `SO_SANH_6_CRAWLERS_FULL.md` | So sánh 6 crawler |
| `HUONG_DAN_MAINBOARD_CRAWLER.md` | Mainboard |
| `HUONG_DAN_VGA_CRAWLER.md` | VGA |
| `HUONG_DAN_SSD_CRAWLER.md` | SSD |
| `HUONG_DAN_HDD_CRAWLER.md` | HDD |
| `*_CRAWLER_SUMMARY.md` | Tóm tắt nhanh |

---

## 🎉 KẾT LUẬN

**Hệ thống hoàn chỉnh với:**
- ✅ 6 crawlers chuyên nghiệp
- ✅ 774 sản phẩm
- ✅ 7 files CSV (6 riêng + 1 chung)
- ✅ Anti-bot đa lớp
- ✅ Error handling robust
- ✅ Debug support đầy đủ
- ✅ Tài liệu chi tiết
- ✅ Script tự động

**Production Ready!** 🚀

---

**System Version:** 11.0 (6 Crawlers)  
**Status:** ✅ Production Ready  
**Last Update:** 15/02/2026  
**Total Products:** 774  
**Total Time:** ~5-6 phút

---

## 📞 SUPPORT

Nếu gặp vấn đề:
1. Xem debug screenshots
2. Đọc tài liệu
3. Kiểm tra kết nối
4. Chạy lại từ đầu

**Chúc bạn crawl thành công! 🎉**
