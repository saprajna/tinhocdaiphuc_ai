# 💽 HƯỚNG DẪN CRAWLER SSD

## 📅 Ngày tạo: 15/02/2026

---

## 🎯 TỔNG QUAN

Crawler SSD được tạo dựa trên code chuẩn của `crawler_vga.py` (đã có fix lỗi JavaScript click).

---

## 📋 THÔNG TIN

| Thông tin | Chi tiết |
|-----------|----------|
| **File** | `crawler_ssd.py` |
| **URL** | `https://tinhocngoisao.com/collections/o-cung-ssd` |
| **Selector** | `.product-item` |
| **Category** | `'SSD'` |
| **File riêng** | `ssd_data.csv` |
| **File chung** | `data.csv` (append - mode='a') |
| **Hãng hỗ trợ** | Samsung, Kingston, WD, Crucial, Seagate, SanDisk, Intel, Corsair, ADATA, Gigabyte, MSI, PNY, Lexar, Team, Transcend, Patriot, và nhiều hãng khác |

---

## 🔧 CÁC TÍNH NĂNG

### ✅ **JavaScript Click**
```python
driver.execute_script("arguments[0].click();", button)
```
- Tránh click nhầm overlay "Tra cứu bảo hành"
- Đã áp dụng fix từ `crawler_vga.py`

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
    # Tự động nhận diện: Samsung, Kingston, WD, Crucial, Seagate...
```

**Các hãng SSD được hỗ trợ:**
- Samsung (phổ biến nhất)
- Kingston
- WD (Western Digital: WD Black, WD Blue, WD Green)
- Crucial
- Seagate
- SanDisk
- Intel
- Corsair
- ADATA
- Gigabyte (Aorus)
- MSI
- PNY
- Lexar
- Team
- Transcend
- Patriot
- Plextor
- KingSpec
- Acer
- HP
- Colorful
- Kingmax
- Toshiba
- SK Hynix
- Silicon Power
- Netac

### ✅ **Append vào data.csv**
```python
# Mode='a' - Chèn nối tiếp
with open('data.csv', 'a', ...) as f:
    writer.writerows(ssd_data)
```

---

## 🚀 CÁCH CHẠY

### **Chạy riêng SSD:**
```bash
python crawler_ssd.py
```

### **Thứ tự chạy đúng (5 crawler):**
```bash
# 1. RAM trước (tạo mới data.csv - mode='w')
python crawler_ram.py

# 2. CPU sau (append - mode='a')
python crawler_cpu.py

# 3. Mainboard sau (append - mode='a')
python crawler_mainboard.py

# 4. VGA sau (append - mode='a')
python crawler_vga.py

# 5. SSD cuối (append - mode='a')
python crawler_ssd.py
```

### **Chạy tự động (Windows):**
```bash
run_all_crawlers.bat
```

---

## 📊 CẤU TRÚC DỮ LIỆU

### **File riêng: `ssd_data.csv`**
```csv
ten_ssd,hang,thong_so,gia_vnd,link_hinh_anh,category
"SSD Samsung 980 PRO 1TB M.2 PCIe Gen 4.0 x4 NVMe",Samsung,"SSD Samsung 980 PRO 1TB M.2 PCIe Gen 4.0 x4 NVMe",3290000,https://...,SSD
"Kingston NV2 500GB M.2 2280 NVMe PCIe 4.0",Kingston,"Kingston NV2 500GB M.2 2280 NVMe PCIe 4.0",990000,https://...,SSD
"WD Black SN850X 2TB M.2 PCIe Gen 4.0",WD,"WD Black SN850X 2TB M.2 PCIe Gen 4.0",5490000,https://...,SSD
```

### **File chung: `data.csv` (sau khi append)**
```csv
ten,hang,thong_so,gia_vnd,link_hinh_anh,category
... (219 dòng RAM)
... (120 dòng CPU)
... (180 dòng Mainboard)
... (132 dòng VGA)
"SSD Samsung 980 PRO 1TB M.2 PCIe Gen 4.0 x4 NVMe",Samsung,"SSD Samsung 980 PRO 1TB M.2 PCIe Gen 4.0 x4 NVMe",3290000,https://...,SSD
"Kingston NV2 500GB M.2 2280 NVMe PCIe 4.0",Kingston,"Kingston NV2 500GB M.2 2280 NVMe PCIe 4.0",990000,https://...,SSD
... (X dòng SSD)
```

---

## 📸 DEBUG FILES

Crawler tạo các file debug:
- `debug_ssd_initial_load.png` - Ảnh sau khi load trang
- `debug_ssd_after_load_all.png` - Ảnh sau khi load hết sản phẩm
- `debug_ssd_wait_timeout_*.png` - Ảnh nếu timeout

---

## 📋 OUTPUT MẪU

```
================================================================================
🚀 CRAWLER SSD - TIN HỌC NGÔI SAO
================================================================================
📅 URL: https://tinhocngoisao.com/collections/o-cung-ssd
🔧 Selector chính: .product-item
📝 Tên: h3.pdLoopName a (text)
💰 Giá: p.pdPrice span
📂 Category: SSD
💾 Mode: Append vào data.csv (mode='a')
================================================================================

Đang khởi tạo Chrome driver...
Chrome driver đã sẵn sàng!

================================================================================
🚀 BẮT ĐẦU CRAWL TOÀN BỘ SẢN PHẨM SSD
================================================================================
🌐 Website: https://tinhocngoisao.com/collections/o-cung-ssd
⚙️  Phương pháp: Click nút 'Xem thêm' với WebDriverWait
================================================================================

📍 Đang truy cập: https://tinhocngoisao.com/collections/o-cung-ssd
📸 Đã chụp ảnh sau khi load: debug_ssd_initial_load.png

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
🔗 URL hiện tại: https://tinhocngoisao.com/collections/o-cung-ssd
✅ Đã click JavaScript thành công!
🔗 URL sau click: https://tinhocngoisao.com/collections/o-cung-ssd
⏳ Chờ 3 giây để sản phẩm mới hiện ra...
📦 Số .product-item sau khi click: 48
➕ Tăng thêm: 24 sản phẩm
✅ Đã tải thêm 24 sản phẩm mới!

... (tiếp tục click cho đến hết)

================================================================================
✅ HOÀN TẤT VIỆC TẢI SẢN PHẨM
================================================================================
🖱️  Tổng số lần bấm nút: 7
🔝 Scroll về đầu trang...

================================================================================
📊 BẮT ĐẦU THU THẬP DỮ LIỆU TỪ TẤT CẢ SẢN PHẨM
================================================================================
🔍 Đang tìm kiếm tất cả thẻ .product-item...
   ✅ Tìm thấy 168 thẻ .product-item

✅ Bắt đầu crawl 168 sản phẩm...

   ✅ [1/168] SSD Samsung 980 PRO 1TB M.2 PCIe Gen 4.0 x4 NVMe            |  3,290,000₫
   ✅ [10/168] Kingston NV2 500GB M.2 2280 NVMe PCIe 4.0                  |    990,000₫
   ✅ [20/168] WD Black SN850X 2TB M.2 PCIe Gen 4.0                       |  5,490,000₫
   ...

================================================================================
🎉 HOÀN THÀNH CRAWL!
================================================================================
📊 Tổng số thẻ .product-item tìm thấy: 168
✅ Crawl thành công: 165 sản phẩm
❌ Bỏ qua: 3 phần tử (thiếu thông tin)
💾 Dữ liệu đã lưu trong bộ nhớ: 165 sản phẩm
================================================================================

================================================================================
💾 ĐANG LƯU DỮ LIỆU
================================================================================
📁 Bước 1: Lưu vào file riêng 'ssd_data.csv'...
   ✅ Đã lưu 165 sản phẩm vào 'ssd_data.csv'!

📁 Bước 2: Chèn nối tiếp vào 'data.csv'...
   ✅ Đã chèn nối tiếp 165 sản phẩm vào 'data.csv'!

================================================================================
🎉 Đã thêm 165 SSD vào kho dữ liệu chung
================================================================================
📄 File riêng: ssd_data.csv (165 dòng)
📄 File chung: data.csv (đã thêm 165 dòng)
================================================================================

================================================================================
🎉 HOÀN THÀNH TẤT CẢ CÁC BƯỚC!
================================================================================

✅ Đã đóng browser!
```

---

## ⚙️ SO SÁNH VỚI VGA CRAWLER

| Tính năng | VGA Crawler | SSD Crawler | Trạng thái |
|-----------|-------------|-------------|------------|
| **Selector** | `.product-item` | `.product-item` | ✅ Giống |
| **JS Click** | Có | Có | ✅ Giống |
| **Kiểm tra URL** | Có | Có | ✅ Giống |
| **WebDriverWait** | ≥ 20 sản phẩm | ≥ 20 sản phẩm | ✅ Giống |
| **Mode ghi data.csv** | `'a'` (append) | `'a'` (append) | ✅ Giống |
| **URL** | `/card-man-hinh` | `/o-cung-ssd` | ❌ Khác |
| **Category** | `'VGA'` | `'SSD'` | ❌ Khác |
| **Field name** | `ten_vga` | `ten_ssd` | ❌ Khác |
| **Hãng** | NVIDIA/AMD/Intel | Samsung/Kingston/WD... | ❌ Khác |
| **Brand Logic** | Smart (Chipset > Mfr) | Đơn giản | ❌ Khác |

---

## 🔄 WORKFLOW ĐẦY ĐỦ (5 CRAWLER)

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
│   5. SSD        │ → mode='a' (append vào data.csv)  ← Crawler này
└─────────────────┘
         ↓
┌──────────────────────────────────────────────────────┐
│  data.csv: 219 RAM + 120 CPU + 180 MB + 132 VGA     │
│            + 165 SSD = 816 sản phẩm tổng cộng       │
└──────────────────────────────────────────────────────┘
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

1. **SSD PHẢI chạy SAU RAM, CPU, Mainboard và VGA**
   - Vì dùng mode='a' (append)
   - Nếu chạy trước, sẽ không có header hoặc mất dữ liệu

2. **Thứ tự đúng:**
   ```bash
   python crawler_ram.py       # 1. Tạo mới
   python crawler_cpu.py       # 2. Append
   python crawler_mainboard.py # 3. Append
   python crawler_vga.py       # 4. Append
   python crawler_ssd.py       # 5. Append
   ```

3. **Không chạy ngược lại!**
   ```bash
   # ❌ SAI
   python crawler_ssd.py       # Chạy trước
   python crawler_ram.py       # GHI ĐÈ - mất dữ liệu SSD!
   ```

4. **Cột Category quan trọng:**
   - Dùng để phân biệt loại linh kiện
   - RAM: `'RAM'`
   - CPU: `'CPU'`
   - Mainboard: `'Mainboard'`
   - VGA: `'VGA'`
   - SSD: `'SSD'`

---

## ✅ CHECKLIST

- [ ] Cài đặt: `pip install selenium webdriver-manager pandas`
- [ ] Đảm bảo đã chạy `crawler_ram.py` trước
- [ ] Đảm bảo đã chạy `crawler_cpu.py` trước
- [ ] Đảm bảo đã chạy `crawler_mainboard.py` trước
- [ ] Đảm bảo đã chạy `crawler_vga.py` trước
- [ ] Chạy: `python crawler_ssd.py`
- [ ] Kiểm tra `ssd_data.csv` có dữ liệu
- [ ] Kiểm tra `data.csv` đã thêm SSD
- [ ] Kiểm tra cột `category` = 'SSD'

---

## 📁 FILES LIÊN QUAN

1. ✅ `crawler_ssd.py` - Crawler SSD
2. ✅ `ssd_data.csv` - File riêng SSD
3. ✅ `data.csv` - File chung (RAM + CPU + Mainboard + VGA + SSD)
4. ✅ `HUONG_DAN_SSD_CRAWLER.md` - File này

---

## 🎉 KẾT LUẬN

**`crawler_ssd.py`** có đầy đủ:
1. ✅ JavaScript Click (tránh overlay)
2. ✅ Kiểm tra URL (tự động fix)
3. ✅ WebDriverWait (≥ 20 sản phẩm)
4. ✅ Auto-detect Brand (Samsung/Kingston/WD/Crucial...)
5. ✅ Cột Category = 'SSD'
6. ✅ Mode='a' (append vào data.csv)
7. ✅ Thông báo: "Đã thêm X SSD vào kho dữ liệu chung"

**Crawler thứ 5 hoàn chỉnh!** 🎉

---

**Version:** 1.0  
**Date:** 15/02/2026  
**Status:** ✅ Production Ready
