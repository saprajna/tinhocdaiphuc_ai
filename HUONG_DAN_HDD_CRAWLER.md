# 💿 HƯỚNG DẪN CRAWLER HDD

## 📅 Ngày tạo: 15/02/2026

---

## 🎯 TỔNG QUAN

Crawler HDD được tạo dựa trên code chuẩn của `crawler_ssd.py` (đã có fix lỗi JavaScript click).

---

## 📋 THÔNG TIN

| Thông tin | Chi tiết |
|-----------|----------|
| **File** | `crawler_hdd.py` |
| **URL** | `https://tinhocngoisao.com/collections/o-cung-hdd/` |
| **Selector** | `.product-item` |
| **Category** | `'HDD'` |
| **File riêng** | `hdd_data.csv` |
| **File chung** | `data.csv` (append - mode='a') |
| **Hãng hỗ trợ** | Seagate, WD (Western Digital), Toshiba, Hitachi (HGST), Samsung, Maxtor, Transcend, ADATA, HP, Acer |

---

## 🔧 CÁC TÍNH NĂNG

### ✅ **JavaScript Click**
```python
driver.execute_script("arguments[0].click();", button)
```
- Tránh click nhầm overlay "Tra cứu bảo hành"
- Đã áp dụng fix từ `crawler_ssd.py`

### ✅ **Kiểm tra URL**
```python
if 'collections' not in current_url:
    driver.back()
    click_count -= 1
    continue
```
- Tự động phát hiện click nhầm
- Quay lại và thử lại

### ✅ **WebDriverWait**
```python
wait.until(lambda d: len(d.find_elements(...)) >= 20)
```
- Chờ đủ 20 sản phẩm trước khi crawl
- Tránh bắt nhầm mục "Gợi ý"

### ✅ **Auto-detect Brand**
```python
def extract_brand(name):
    # Tự động nhận diện: Seagate, WD, Toshiba, Hitachi...
```

**Các hãng HDD được hỗ trợ:**
- **Seagate** (Barracuda, IronWolf, SkyHawk)
- **WD** - Western Digital (WD Black, Blue, Red, Purple, Gold)
- **Toshiba**
- **Hitachi** (HGST)
- **Samsung**
- **Maxtor**
- **Transcend**
- **ADATA**
- **HP**
- **Acer**

### ✅ **Append vào data.csv**
```python
# Mode='a' - Chèn nối tiếp
with open('data.csv', 'a', ...) as f:
    writer.writerows(hdd_data)
```

---

## 🚀 CÁCH CHẠY

### **Chạy riêng HDD:**
```bash
python crawler_hdd.py
```

### **Thứ tự chạy đúng (6 crawler):**
```bash
# 1. RAM trước (tạo mới data.csv - mode='w')
python crawler_ram.py

# 2. CPU sau (append - mode='a')
python crawler_cpu.py

# 3. Mainboard sau (append - mode='a')
python crawler_mainboard.py

# 4. VGA sau (append - mode='a')
python crawler_vga.py

# 5. SSD sau (append - mode='a')
python crawler_ssd.py

# 6. HDD cuối (append - mode='a')
python crawler_hdd.py
```

### **Chạy tự động (Windows):**
```bash
run_all_crawlers.bat
```

---

## 📊 CẤU TRÚC DỮ LIỆU

### **File riêng: `hdd_data.csv`**
```csv
ten_hdd,hang,thong_so,gia_vnd,link_hinh_anh,category
"Seagate Barracuda 2TB 3.5'' SATA 3 7200RPM",Seagate,"Seagate Barracuda 2TB 3.5'' SATA 3 7200RPM",1490000,https://...,HDD
"WD Blue 1TB 3.5'' SATA 3 7200RPM",WD,"WD Blue 1TB 3.5'' SATA 3 7200RPM",990000,https://...,HDD
"Toshiba 4TB 3.5'' SATA 3 5400RPM",Toshiba,"Toshiba 4TB 3.5'' SATA 3 5400RPM",2490000,https://...,HDD
```

### **File chung: `data.csv` (sau khi append)**
```csv
ten,hang,thong_so,gia_vnd,link_hinh_anh,category
... (219 dòng RAM)
... (120 dòng CPU)
... (180 dòng Mainboard)
... (132 dòng VGA)
... (69 dòng SSD)
"Seagate Barracuda 2TB 3.5'' SATA 3 7200RPM",Seagate,"Seagate Barracuda 2TB 3.5'' SATA 3 7200RPM",1490000,https://...,HDD
"WD Blue 1TB 3.5'' SATA 3 7200RPM",WD,"WD Blue 1TB 3.5'' SATA 3 7200RPM",990000,https://...,HDD
... (X dòng HDD)
```

---

## 📸 DEBUG FILES

Crawler tạo các file debug:
- `debug_hdd_initial_load.png` - Ảnh sau khi load trang
- `debug_hdd_after_load_all.png` - Ảnh sau khi load hết sản phẩm
- `debug_hdd_wait_timeout_*.png` - Ảnh nếu timeout

---

## 🔄 WORKFLOW ĐẦY ĐỦ (6 CRAWLER)

```
┌─────────────────┐
│   1. RAM        │ → mode='w' (tạo mới data.csv)
└─────────────────┘
         ↓
┌─────────────────┐
│   2. CPU        │ → mode='a' (append vào data.csv)
└─────────────────┘
         ↓
┌─────────────────┐
│ 3. MAINBOARD    │ → mode='a' (append vào data.csv)
└─────────────────┘
         ↓
┌─────────────────┐
│   4. VGA        │ → mode='a' (append vào data.csv)
└─────────────────┘
         ↓
┌─────────────────┐
│   5. SSD        │ → mode='a' (append vào data.csv)
└─────────────────┘
         ↓
┌─────────────────┐
│   6. HDD        │ → mode='a' (append vào data.csv)  ← Crawler này
└─────────────────┘
         ↓
┌──────────────────────────────────────────────────────┐
│  data.csv: 219 RAM + 120 CPU + 180 MB + 132 VGA     │
│            + 69 SSD + X HDD = ~850+ sản phẩm        │
└──────────────────────────────────────────────────────┘
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

1. **HDD PHẢI chạy SAU tất cả các crawler khác**
   - Vì dùng mode='a' (append)
   - Nếu chạy trước, sẽ không có header hoặc mất dữ liệu

2. **Thứ tự đúng:**
   ```bash
   python crawler_ram.py       # 1. Tạo mới
   python crawler_cpu.py       # 2. Append
   python crawler_mainboard.py # 3. Append
   python crawler_vga.py       # 4. Append
   python crawler_ssd.py       # 5. Append
   python crawler_hdd.py       # 6. Append
   ```

3. **Không chạy ngược lại!**
   ```bash
   # ❌ SAI
   python crawler_hdd.py       # Chạy trước
   python crawler_ram.py       # GHI ĐÈ - mất dữ liệu HDD!
   ```

4. **Cột Category quan trọng:**
   - Dùng để phân biệt loại linh kiện
   - RAM: `'RAM'`
   - CPU: `'CPU'`
   - Mainboard: `'Mainboard'`
   - VGA: `'VGA'`
   - SSD: `'SSD'`
   - HDD: `'HDD'`

---

## ✅ CHECKLIST

- [ ] Cài đặt: `pip install selenium webdriver-manager pandas`
- [ ] Đảm bảo đã chạy `crawler_ram.py` trước
- [ ] Đảm bảo đã chạy `crawler_cpu.py` trước
- [ ] Đảm bảo đã chạy `crawler_mainboard.py` trước
- [ ] Đảm bảo đã chạy `crawler_vga.py` trước
- [ ] Đảm bảo đã chạy `crawler_ssd.py` trước
- [ ] Chạy: `python crawler_hdd.py`
- [ ] Kiểm tra `hdd_data.csv` có dữ liệu
- [ ] Kiểm tra `data.csv` đã thêm HDD
- [ ] Kiểm tra cột `category` = 'HDD'

---

## 📁 FILES LIÊN QUAN

1. ✅ `crawler_hdd.py` - Crawler HDD
2. ✅ `hdd_data.csv` - File riêng HDD
3. ✅ `data.csv` - File chung (RAM + CPU + Mainboard + VGA + SSD + HDD)
4. ✅ `HUONG_DAN_HDD_CRAWLER.md` - File này

---

## 🎉 KẾT LUẬN

**`crawler_hdd.py`** có đầy đủ:
1. ✅ JavaScript Click (tránh overlay)
2. ✅ Kiểm tra URL (tự động fix)
3. ✅ WebDriverWait (≥ 20 sản phẩm)
4. ✅ Auto-detect Brand (Seagate/WD/Toshiba/Hitachi...)
5. ✅ Cột Category = 'HDD'
6. ✅ Mode='a' (append vào data.csv)
7. ✅ Thông báo: "Đã thêm X HDD vào kho dữ liệu chung"

**Crawler thứ 6 hoàn chỉnh!** 🎉

---

**Version:** 1.0  
**Date:** 15/02/2026  
**Status:** ✅ Production Ready
