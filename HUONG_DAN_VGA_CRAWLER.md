# 🎮 HƯỚNG DẪN CRAWLER VGA (CARD MÀN HÌNH)

## 📅 Ngày tạo: 15/02/2026

---

## 🎯 TỔNG QUAN

Crawler VGA được tạo dựa trên code chuẩn của `crawler_mainboard.py` (đã có fix lỗi JavaScript click).

---

## 📋 THÔNG TIN

| Thông tin | Chi tiết |
|-----------|----------|
| **File** | `crawler_vga.py` |
| **URL** | `https://tinhocngoisao.com/collections/card-man-hinh` |
| **Selector** | `.product-item` |
| **Category** | `'VGA'` |
| **File riêng** | `vga_data.csv` |
| **File chung** | `data.csv` (append - mode='a') |
| **Chipset** | NVIDIA (GeForce RTX/GTX), AMD (Radeon RX), Intel (Arc) |
| **Nhà sản xuất** | ASUS, MSI, Gigabyte, EVGA, Zotac, Palit, Galax, Sapphire, PowerColor, XFX, ASRock |

---

## 🔧 CÁC TÍNH NĂNG

### ✅ **JavaScript Click**
```python
driver.execute_script("arguments[0].click();", button)
```
- Tránh click nhầm overlay "Tra cứu bảo hành"
- Đã áp dụng fix từ `crawler_mainboard.py`

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

### ✅ **Smart Brand Detection**
```python
def extract_brand(name):
    # Ưu tiên Chipset (NVIDIA, AMD, Intel)
    # Sau đó mới đến Manufacturer (ASUS, MSI, Gigabyte...)
```

**Logic phát hiện:**
1. **Chipset (ưu tiên cao):**
   - NVIDIA: GeForce, RTX, GTX
   - AMD: Radeon, RX
   - Intel: Arc

2. **Manufacturer (ưu tiên thấp):**
   - ASUS, MSI, Gigabyte, EVGA, Zotac, Palit...

### ✅ **Append vào data.csv**
```python
# Mode='a' - Chèn nối tiếp
with open('data.csv', 'a', ...) as f:
    writer.writerows(vga_data)
```

---

## 🚀 CÁCH CHẠY

### **Chạy riêng VGA:**
```bash
python crawler_vga.py
```

### **Thứ tự chạy đúng (4 crawler):**
```bash
# 1. RAM trước (tạo mới data.csv - mode='w')
python crawler_ram.py

# 2. CPU sau (append - mode='a')
python crawler_cpu.py

# 3. Mainboard sau (append - mode='a')
python crawler_mainboard.py

# 4. VGA cuối (append - mode='a')
python crawler_vga.py
```

### **Chạy tự động (Windows):**
```bash
run_all_crawlers.bat
```

---

## 📊 CẤU TRÚC DỮ LIỆU

### **File riêng: `vga_data.csv`**
```csv
ten_vga,hang,thong_so,gia_vnd,link_hinh_anh,category
"ASUS ROG Strix GeForce RTX 4070 Ti",NVIDIA,"ASUS ROG Strix GeForce RTX 4070 Ti",21990000,https://...,VGA
"MSI GeForce RTX 4060 Ti Gaming X 8GB",NVIDIA,"MSI GeForce RTX 4060 Ti Gaming X 8GB",12490000,https://...,VGA
"Gigabyte Radeon RX 7800 XT Gaming OC",AMD,"Gigabyte Radeon RX 7800 XT Gaming OC",14990000,https://...,VGA
```

### **File chung: `data.csv` (sau khi append)**
```csv
ten,hang,thong_so,gia_vnd,link_hinh_anh,category
... (219 dòng RAM)
... (120 dòng CPU)
... (118 dòng Mainboard)
"ASUS ROG Strix GeForce RTX 4070 Ti",NVIDIA,"ASUS ROG Strix GeForce RTX 4070 Ti",21990000,https://...,VGA
"MSI GeForce RTX 4060 Ti Gaming X 8GB",NVIDIA,"MSI GeForce RTX 4060 Ti Gaming X 8GB",12490000,https://...,VGA
... (X dòng VGA)
```

---

## 📸 DEBUG FILES

Crawler tạo các file debug:
- `debug_vga_initial_load.png` - Ảnh sau khi load trang
- `debug_vga_after_load_all.png` - Ảnh sau khi load hết sản phẩm
- `debug_vga_wait_timeout_*.png` - Ảnh nếu timeout

---

## 📋 OUTPUT MẪU

```
================================================================================
🚀 CRAWLER VGA (CARD MÀN HÌNH) - TIN HỌC NGÔI SAO
================================================================================
📅 URL: https://tinhocngoisao.com/collections/card-man-hinh
🔧 Selector chính: .product-item
📝 Tên: h3.pdLoopName a (text)
💰 Giá: p.pdPrice span
📂 Category: VGA
💾 Mode: Append vào data.csv (mode='a')
================================================================================

Đang khởi tạo Chrome driver...
Chrome driver đã sẵn sàng!

================================================================================
🚀 BẮT ĐẦU CRAWL TOÀN BỘ SẢN PHẨM VGA
================================================================================
🌐 Website: https://tinhocngoisao.com/collections/card-man-hinh
⚙️  Phương pháp: Click nút 'Xem thêm' với WebDriverWait
================================================================================

📍 Đang truy cập: https://tinhocngoisao.com/collections/card-man-hinh
📸 Đã chụp ảnh sau khi load: debug_vga_initial_load.png

================================================================================
🔍 KIỂM TRA DANH SÁCH SẢN PHẨM CHÍNH
================================================================================
⏳ Đang chờ ít nhất 20 thẻ .product-item xuất hiện (tối đa 20s)...
   (Để tránh bắt nhầm mục 'Gợi ý')
✅ Đã phát hiện 24 thẻ .product-item!

================================================================================
🔄 ĐANG TẢI TOÀN BỘ SẢN PHẨM BẰNG NÚT 'XEM THÊM'
================================================================================
📊 Hiện có 24 thẻ .product-item trên trang

🖱️  Đang bấm nút 'Xem thêm' lần 1...
📦 Số .product-item trước khi click: 24
🔗 URL hiện tại: https://tinhocngoisao.com/collections/card-man-hinh
✅ Đã click JavaScript thành công!
🔗 URL sau click: https://tinhocngoisao.com/collections/card-man-hinh
⏳ Chờ 3 giây để sản phẩm mới hiện ra...
📦 Số .product-item sau khi click: 48
➕ Tăng thêm: 24 sản phẩm
✅ Đã tải thêm 24 sản phẩm mới!

... (tiếp tục click cho đến hết)

================================================================================
✅ HOÀN TẤT VIỆC TẢI SẢN PHẨM
================================================================================
🖱️  Tổng số lần bấm nút: 6
🔝 Scroll về đầu trang...

================================================================================
📊 BẮT ĐẦU THU THẬP DỮ LIỆU TỪ TẤT CẢ SẢN PHẨM
================================================================================
🔍 Đang tìm kiếm tất cả thẻ .product-item...
   ✅ Tìm thấy 144 thẻ .product-item

✅ Bắt đầu crawl 144 sản phẩm...

   ✅ [1/144] ASUS ROG Strix GeForce RTX 4070 Ti                           | 21,990,000₫
   ✅ [10/144] MSI GeForce RTX 4060 Ti Gaming X 8GB                        | 12,490,000₫
   ✅ [20/144] Gigabyte Radeon RX 7800 XT Gaming OC                        | 14,990,000₫
   ...

================================================================================
🎉 HOÀN THÀNH CRAWL!
================================================================================
📊 Tổng số thẻ .product-item tìm thấy: 144
✅ Crawl thành công: 142 sản phẩm
❌ Bỏ qua: 2 phần tử (thiếu thông tin)
💾 Dữ liệu đã lưu trong bộ nhớ: 142 sản phẩm
================================================================================

================================================================================
💾 ĐANG LƯU DỮ LIỆU
================================================================================
📁 Bước 1: Lưu vào file riêng 'vga_data.csv'...
   ✅ Đã lưu 142 sản phẩm vào 'vga_data.csv'!

📁 Bước 2: Chèn nối tiếp vào 'data.csv'...
   ✅ Đã chèn nối tiếp 142 sản phẩm vào 'data.csv'!

================================================================================
🎉 Đã thêm 142 VGA vào kho dữ liệu chung
================================================================================
📄 File riêng: vga_data.csv (142 dòng)
📄 File chung: data.csv (đã thêm 142 dòng)
================================================================================

================================================================================
🎉 HOÀN THÀNH TẤT CẢ CÁC BƯỚC!
================================================================================

✅ Đã đóng browser!
```

---

## ⚙️ SO SÁNH VỚI MAINBOARD CRAWLER

| Tính năng | Mainboard Crawler | VGA Crawler | Trạng thái |
|-----------|-------------------|-------------|------------|
| **Selector** | `.product-item` | `.product-item` | ✅ Giống |
| **JS Click** | Có | Có | ✅ Giống |
| **Kiểm tra URL** | Có | Có | ✅ Giống |
| **WebDriverWait** | ≥ 20 sản phẩm | ≥ 20 sản phẩm | ✅ Giống |
| **Mode ghi data.csv** | `'a'` (append) | `'a'` (append) | ✅ Giống |
| **URL** | `/bo-mach-chu` | `/card-man-hinh` | ❌ Khác |
| **Category** | `'Mainboard'` | `'VGA'` | ❌ Khác |
| **Field name** | `ten_mainboard` | `ten_vga` | ❌ Khác |
| **Hãng** | ASUS/MSI/Gigabyte... | NVIDIA/AMD/Intel | ❌ Khác |
| **Brand Logic** | Đơn giản | **Smart Detection** | ❌ Khác |

---

## 🎯 SMART BRAND DETECTION

### **Ưu tiên Chipset:**
```python
# Tìm chipset trước (quan trọng nhất)
if 'GEFORCE' in name or 'RTX' in name or 'GTX' in name:
    return 'NVIDIA'
elif 'RADEON' in name or 'RX' in name:
    return 'AMD'
elif 'ARC' in name:
    return 'Intel'
```

**Ví dụ:**
- "ASUS ROG Strix GeForce RTX 4070 Ti" → **NVIDIA** (không phải ASUS)
- "Gigabyte Radeon RX 7800 XT Gaming OC" → **AMD** (không phải Gigabyte)
- "MSI GeForce GTX 1660 Super" → **NVIDIA** (không phải MSI)

### **Fallback Manufacturer:**
```python
# Nếu không tìm thấy chipset, tìm nhà sản xuất
if 'ASUS' in name:
    return 'ASUS'
elif 'MSI' in name:
    return 'MSI'
# ...
```

**Ví dụ:**
- "ASUS TUF Gaming A1" → **ASUS** (không có chipset rõ ràng)
- "Zotac Gaming Twin Edge" → **Zotac**

---

## 🔄 WORKFLOW ĐẦY ĐỦ (4 CRAWLER)

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
│   4. VGA        │ → mode='a' (append vào data.csv)  ← Crawler này
└─────────────────┘
         ↓
┌───────────────────────────────────────────────┐
│  data.csv: 219 RAM + 120 CPU + 118 MB + 142 VGA │
│  = 599 sản phẩm tổng cộng                      │
└───────────────────────────────────────────────┘
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

1. **VGA PHẢI chạy SAU RAM, CPU và Mainboard**
   - Vì dùng mode='a' (append)
   - Nếu chạy trước, sẽ không có header hoặc mất dữ liệu

2. **Thứ tự đúng:**
   ```bash
   python crawler_ram.py       # 1. Tạo mới
   python crawler_cpu.py       # 2. Append
   python crawler_mainboard.py # 3. Append
   python crawler_vga.py       # 4. Append
   ```

3. **Không chạy ngược lại!**
   ```bash
   # ❌ SAI
   python crawler_vga.py       # Chạy trước
   python crawler_ram.py       # GHI ĐÈ - mất dữ liệu VGA!
   ```

4. **Cột Category quan trọng:**
   - Dùng để phân biệt loại linh kiện
   - RAM: `'RAM'`
   - CPU: `'CPU'`
   - Mainboard: `'Mainboard'`
   - VGA: `'VGA'`

5. **Brand Detection:**
   - Ưu tiên Chipset (NVIDIA/AMD/Intel)
   - Fallback Manufacturer (ASUS/MSI/Gigabyte...)

---

## ✅ CHECKLIST

- [ ] Cài đặt: `pip install selenium webdriver-manager pandas`
- [ ] Đảm bảo đã chạy `crawler_ram.py` trước
- [ ] Đảm bảo đã chạy `crawler_cpu.py` trước
- [ ] Đảm bảo đã chạy `crawler_mainboard.py` trước
- [ ] Chạy: `python crawler_vga.py`
- [ ] Kiểm tra `vga_data.csv` có dữ liệu
- [ ] Kiểm tra `data.csv` đã thêm VGA
- [ ] Kiểm tra cột `category` = 'VGA'
- [ ] Kiểm tra cột `hang` ưu tiên Chipset (NVIDIA/AMD/Intel)

---

## 📁 FILES LIÊN QUAN

1. ✅ `crawler_vga.py` - Crawler VGA
2. ✅ `vga_data.csv` - File riêng VGA
3. ✅ `data.csv` - File chung (RAM + CPU + Mainboard + VGA)
4. ✅ `HUONG_DAN_VGA_CRAWLER.md` - File này

---

## 🎉 KẾT LUẬN

**`crawler_vga.py`** có đầy đủ:
1. ✅ JavaScript Click (tránh overlay)
2. ✅ Kiểm tra URL (tự động fix)
3. ✅ WebDriverWait (≥ 20 sản phẩm)
4. ✅ **Smart Brand Detection** (Chipset > Manufacturer)
5. ✅ Cột Category = 'VGA'
6. ✅ Mode='a' (append vào data.csv)
7. ✅ Thông báo: "Đã thêm X VGA vào kho dữ liệu chung"

**Crawler thứ 4 hoàn chỉnh!** 🎉

---

**Version:** 1.0  
**Date:** 15/02/2026  
**Status:** ✅ Production Ready
