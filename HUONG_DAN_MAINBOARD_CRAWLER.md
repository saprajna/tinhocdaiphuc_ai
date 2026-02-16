# 🛡️ HƯỚNG DẪN CRAWLER MAINBOARD

## 📅 Ngày tạo: 15/02/2026

---

## 🎯 TỔNG QUAN

Crawler Mainboard được tạo dựa trên code chuẩn của `crawler_cpu.py` (đã có fix lỗi JavaScript click).

---

## 📋 THÔNG TIN

| Thông tin | Chi tiết |
|-----------|----------|
| **File** | `crawler_mainboard.py` |
| **URL** | `https://tinhocngoisao.com/collections/bo-mach-chu` |
| **Selector** | `.product-item` |
| **Category** | `'Mainboard'` |
| **File riêng** | `mainboard_data.csv` |
| **File chung** | `data.csv` (append - mode='a') |
| **Hãng hỗ trợ** | ASUS, MSI, Gigabyte, ASRock, Biostar, EVGA, NZXT |

---

## 🔧 CÁC TÍNH NĂNG

### ✅ **JavaScript Click**
```python
driver.execute_script("arguments[0].click();", button)
```
- Tránh click nhầm overlay "Tra cứu bảo hành"
- Đã áp dụng fix từ `crawler_cpu.py`

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
    # Tự động nhận diện: ASUS, MSI, Gigabyte, ASRock...
```

### ✅ **Append vào data.csv**
```python
# Mode='a' - Chèn nối tiếp
with open('data.csv', 'a', ...) as f:
    writer.writerows(mainboard_data)
```

---

## 🚀 CÁCH CHẠY

### **Chạy riêng Mainboard:**
```bash
python crawler_mainboard.py
```

### **Thứ tự chạy đúng:**
```bash
# 1. RAM trước (tạo mới data.csv - mode='w')
python crawler_ram.py

# 2. CPU sau (append - mode='a')
python crawler_cpu.py

# 3. Mainboard cuối (append - mode='a')
python crawler_mainboard.py
```

### **Chạy tự động (Windows):**
```bash
run_all_crawlers.bat
```

---

## 📊 CẤU TRÚC DỮ LIỆU

### **File riêng: `mainboard_data.csv`**
```csv
ten_mainboard,hang,thong_so,gia_vnd,link_hinh_anh,category
"ASUS TUF GAMING B550M-PLUS",ASUS,"ASUS TUF GAMING B550M-PLUS",2790000,https://...,Mainboard
"MSI MAG B660M MORTAR WIFI",MSI,"MSI MAG B660M MORTAR WIFI",3490000,https://...,Mainboard
"Gigabyte B550 AORUS ELITE V2",Gigabyte,"Gigabyte B550 AORUS ELITE V2",2990000,https://...,Mainboard
```

### **File chung: `data.csv` (sau khi append)**
```csv
ten_mainboard,hang,thong_so,gia_vnd,link_hinh_anh,category
... (219 dòng RAM)
... (120 dòng CPU)
"ASUS TUF GAMING B550M-PLUS",ASUS,"ASUS TUF GAMING B550M-PLUS",2790000,https://...,Mainboard
"MSI MAG B660M MORTAR WIFI",MSI,"MSI MAG B660M MORTAR WIFI",3490000,https://...,Mainboard
... (X dòng Mainboard)
```

---

## 📸 DEBUG FILES

Crawler tạo các file debug:
- `debug_mainboard_initial_load.png` - Ảnh sau khi load trang
- `debug_mainboard_after_load_all.png` - Ảnh sau khi load hết sản phẩm
- `debug_mainboard_wait_timeout_*.png` - Ảnh nếu timeout

---

## 📋 OUTPUT MẪU

```
================================================================================
🚀 CRAWLER MAINBOARD - TIN HỌC NGÔI SAO
================================================================================
📅 URL: https://tinhocngoisao.com/collections/bo-mach-chu
🔧 Selector chính: .product-item
📝 Tên: h3.pdLoopName a (text)
💰 Giá: p.pdPrice span
📂 Category: Mainboard
💾 Mode: Append vào data.csv (mode='a')
================================================================================

Đang khởi tạo Chrome driver...
Chrome driver đã sẵn sàng!

================================================================================
🚀 BẮT ĐẦU CRAWL TOÀN BỘ SẢN PHẨM MAINBOARD
================================================================================
🌐 Website: https://tinhocngoisao.com/collections/bo-mach-chu
⚙️  Phương pháp: Click nút 'Xem thêm' với WebDriverWait
================================================================================

📍 Đang truy cập: https://tinhocngoisao.com/collections/bo-mach-chu
📸 Đã chụp ảnh sau khi load: debug_mainboard_initial_load.png

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
🔗 URL hiện tại: https://tinhocngoisao.com/collections/bo-mach-chu
✅ Đã click JavaScript thành công!
🔗 URL sau click: https://tinhocngoisao.com/collections/bo-mach-chu
⏳ Chờ 3 giây để sản phẩm mới hiện ra...
📦 Số .product-item sau khi click: 48
➕ Tăng thêm: 24 sản phẩm
✅ Đã tải thêm 24 sản phẩm mới!

... (tiếp tục click cho đến hết)

================================================================================
✅ HOÀN TẤT VIỆC TẢI SẢN PHẨM
================================================================================
🖱️  Tổng số lần bấm nút: 5
🔝 Scroll về đầu trang...

================================================================================
📊 BẮT ĐẦU THU THẬP DỮ LIỆU TỪ TẤT CẢ SẢN PHẨM
================================================================================
🔍 Đang tìm kiếm tất cả thẻ .product-item...
   ✅ Tìm thấy 120 thẻ .product-item

✅ Bắt đầu crawl 120 sản phẩm...

   ✅ [1/120] ASUS TUF GAMING B550M-PLUS                                  |  2,790,000₫
   ✅ [10/120] MSI MAG B660M MORTAR WIFI                                  |  3,490,000₫
   ✅ [20/120] Gigabyte B550 AORUS ELITE V2                               |  2,990,000₫
   ...

================================================================================
🎉 HOÀN THÀNH CRAWL!
================================================================================
📊 Tổng số thẻ .product-item tìm thấy: 120
✅ Crawl thành công: 118 sản phẩm
❌ Bỏ qua: 2 phần tử (thiếu thông tin)
💾 Dữ liệu đã lưu trong bộ nhớ: 118 sản phẩm
================================================================================

================================================================================
💾 ĐANG LƯU DỮ LIỆU
================================================================================
📁 Bước 1: Lưu vào file riêng 'mainboard_data.csv'...
   ✅ Đã lưu 118 sản phẩm vào 'mainboard_data.csv'!

📁 Bước 2: Chèn nối tiếp vào 'data.csv'...
   ✅ Đã chèn nối tiếp 118 sản phẩm vào 'data.csv'!

================================================================================
🎉 Đã thêm 118 Mainboard vào kho dữ liệu chung
================================================================================
📄 File riêng: mainboard_data.csv (118 dòng)
📄 File chung: data.csv (đã thêm 118 dòng)
================================================================================

================================================================================
🎉 HOÀN THÀNH TẤT CẢ CÁC BƯỚC!
================================================================================

✅ Đã đóng browser!
```

---

## ⚙️ SO SÁNH VỚI CPU CRAWLER

| Tính năng | CPU Crawler | Mainboard Crawler | Trạng thái |
|-----------|-------------|-------------------|------------|
| **Selector** | `.product-item` | `.product-item` | ✅ Giống |
| **JS Click** | Có | Có | ✅ Giống |
| **Kiểm tra URL** | Có | Có | ✅ Giống |
| **WebDriverWait** | ≥ 20 sản phẩm | ≥ 20 sản phẩm | ✅ Giống |
| **Mode ghi data.csv** | `'a'` (append) | `'a'` (append) | ✅ Giống |
| **URL** | `/cpu-bo-vi-xu-ly` | `/bo-mach-chu` | ❌ Khác |
| **Category** | `'CPU'` | `'Mainboard'` | ❌ Khác |
| **Field name** | `ten_cpu` | `ten_mainboard` | ❌ Khác |
| **Hãng** | Intel/AMD | ASUS/MSI/Gigabyte... | ❌ Khác |

---

## 🔄 WORKFLOW ĐẦY ĐỦ (3 CRAWLER)

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
┌─────────────────────────────────────────┐
│  data.csv: 219 RAM + 120 CPU + 118 MB  │
│  = 457 sản phẩm tổng cộng               │
└─────────────────────────────────────────┘
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

1. **Mainboard PHẢI chạy SAU RAM và CPU**
   - Vì dùng mode='a' (append)
   - Nếu chạy trước, sẽ không có header hoặc mất dữ liệu

2. **Thứ tự đúng:**
   ```bash
   python crawler_ram.py       # 1. Tạo mới
   python crawler_cpu.py       # 2. Append
   python crawler_mainboard.py # 3. Append
   ```

3. **Không chạy ngược lại!**
   ```bash
   # ❌ SAI
   python crawler_mainboard.py  # Chạy trước
   python crawler_ram.py        # GHI ĐÈ - mất dữ liệu Mainboard!
   ```

4. **Cột Category quan trọng:**
   - Dùng để phân biệt loại linh kiện
   - RAM: `'RAM'`
   - CPU: `'CPU'`
   - Mainboard: `'Mainboard'`

---

## ✅ CHECKLIST

- [ ] Cài đặt: `pip install selenium webdriver-manager pandas`
- [ ] Đảm bảo đã chạy `crawler_ram.py` trước
- [ ] Đảm bảo đã chạy `crawler_cpu.py` trước
- [ ] Chạy: `python crawler_mainboard.py`
- [ ] Kiểm tra `mainboard_data.csv` có dữ liệu
- [ ] Kiểm tra `data.csv` đã thêm Mainboard
- [ ] Kiểm tra cột `category` = 'Mainboard'

---

## 📁 FILES LIÊN QUAN

1. ✅ `crawler_mainboard.py` - Crawler Mainboard
2. ✅ `mainboard_data.csv` - File riêng Mainboard
3. ✅ `data.csv` - File chung (RAM + CPU + Mainboard)
4. ✅ `HUONG_DAN_MAINBOARD_CRAWLER.md` - File này

---

## 🎉 KẾT LUẬN

**`crawler_mainboard.py`** có đầy đủ:
1. ✅ JavaScript Click (tránh overlay)
2. ✅ Kiểm tra URL (tự động fix)
3. ✅ WebDriverWait (≥ 20 sản phẩm)
4. ✅ Auto-detect Brand (ASUS/MSI/Gigabyte...)
5. ✅ Cột Category = 'Mainboard'
6. ✅ Mode='a' (append vào data.csv)
7. ✅ Thông báo: "Đã thêm X Mainboard vào kho dữ liệu chung"

**Crawler thứ 3 hoàn chỉnh!** 🎉

---

**Version:** 1.0  
**Date:** 15/02/2026  
**Status:** ✅ Production Ready
