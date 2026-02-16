# 📖 HƯỚNG DẪN CRAWLER CPU

## 🎯 Mục đích

Crawler tự động lấy dữ liệu **CPU** từ website **Tin Học Ngôi Sao** và lưu vào cả file riêng và file chung.

---

## 🌐 Thông tin

- **URL:** https://tinhocngoisao.com/collections/cpu-bo-vi-xu-ly
- **Selector:** `.product-item` (giống RAM)
- **Cơ chế:** Click nút "Xem thêm" (giống RAM)
- **Category:** `CPU`

---

## 📦 Cài đặt

### Bước 1: Cài đặt thư viện (nếu chưa)
```bash
pip install selenium webdriver-manager pandas
```

### Bước 2: Đảm bảo Chrome đã được cài đặt

---

## 🚀 Chạy Crawler

### Chạy trực tiếp:
```bash
python crawler_cpu.py
```

### Hoặc import vào code:
```python
from crawler_cpu import CPUCrawler

crawler = CPUCrawler()
crawler.setup_driver()
crawler.crawl_cpu_data()
crawler.save_to_csv()
crawler.close()
```

---

## 📊 Kết quả

Sau khi chạy, crawler sẽ tạo ra:

### 1. **`cpu_data.csv`** - File riêng CPU

Chứa toàn bộ CPU đã crawl với các cột:
- `ten_cpu`: Tên đầy đủ của CPU
- `hang`: Hãng (Intel, AMD)
- `thong_so`: Thông số (giữ nguyên tên đầy đủ)
- `gia_vnd`: Giá bán (VNĐ)
- `link_hinh_anh`: Link hình ảnh sản phẩm
- `category`: **CPU** (để phân biệt với RAM)

**Ví dụ:**
```csv
ten_cpu,hang,thong_so,gia_vnd,link_hinh_anh,category
"Intel Core i5-12400F",Intel,"Intel Core i5-12400F",4290000,https://...,CPU
"AMD Ryzen 5 5600X",AMD,"AMD Ryzen 5 5600X",4490000,https://...,CPU
```

### 2. **`data.csv`** - File chung (đã cập nhật)

Dữ liệu CPU được **chèn nối tiếp** (append) vào cuối file `data.csv`:
- **Mode:** `'a'` (append)
- **Header:** Chỉ ghi nếu file chưa tồn tại
- **Vị trí:** Cuối file

---

## 🔄 Logic Lưu File

### **Bước 1: Lưu file riêng `cpu_data.csv`**
```python
# Mode 'w' - Ghi đè (overwrite)
with open('cpu_data.csv', 'w', ...) as f:
    writer.writeheader()  # Ghi header
    writer.writerows(cpu_data)
```

### **Bước 2: Append vào `data.csv`**
```python
# Mode 'a' - Chèn nối tiếp (append)
file_exists = os.path.exists('data.csv')

with open('data.csv', 'a', ...) as f:
    if not file_exists:
        writer.writeheader()  # Chỉ ghi header nếu file chưa tồn tại
    writer.writerows(cpu_data)  # Thêm dữ liệu vào cuối
```

---

## 📋 Cột `category`

**Quan trọng:** Tất cả dòng CPU đều có:
```python
'category': 'CPU'
```

**Mục đích:**
- Phân biệt với RAM (`category: 'RAM'`)
- Dễ lọc và phân loại sau này
- AI có thể nhận diện đúng loại linh kiện

---

## 📈 Output mẫu

```
================================================================================
🚀 CRAWLER CPU - TIN HỌC NGÔI SAO
================================================================================
📅 URL: https://tinhocngoisao.com/collections/cpu-bo-vi-xu-ly
🔧 Selector chính: .product-item
📝 Tên: h3.pdLoopName a (text)
💰 Giá: p.pdPrice span
📂 Category: CPU
================================================================================

Đang khởi tạo Chrome driver...
Chrome driver đã sẵn sàng!

📍 Đang truy cập: https://tinhocngoisao.com/collections/cpu-bo-vi-xu-ly
📸 Đã chụp ảnh sau khi load: debug_cpu_initial_load.png

================================================================================
🔍 KIỂM TRA DANH SÁCH SẢN PHẨM CHÍNH
================================================================================
⏳ Đang chờ ít nhất 20 thẻ .product-item xuất hiện (tối đa 20s)...
   (Để tránh bắt nhầm mục 'Gợi ý')
✅ Đã phát hiện 40 thẻ .product-item!

================================================================================
🔄 ĐANG TẢI TOÀN BỘ SẢN PHẨM BẰNG NÚT 'XEM THÊM'
================================================================================
📊 Hiện có 40 thẻ .product-item trên trang

🖱️  Đang bấm nút 'Xem thêm' lần 1...
📦 Số .product-item trước khi click: 40
✅ Đã click nút thành công!
⏳ Chờ 5 giây để sản phẩm mới hiện ra...
📦 Số .product-item sau khi click: 80
➕ Tăng thêm: 40 sản phẩm
✅ Đã tải thêm 40 sản phẩm mới!

... (tiếp tục click cho đến hết)

================================================================================
✅ HOÀN TẤT VIỆC TẢI SẢN PHẨM
================================================================================
🖱️  Tổng số lần bấm nút: 3

================================================================================
📊 BẮT ĐẦU THU THẬP DỮ LIỆU TỪ TẤT CẢ SẢN PHẨM
================================================================================
🔍 Đang tìm kiếm tất cả thẻ .product-item...
   ✅ Tìm thấy 120 thẻ .product-item

✅ Bắt đầu crawl 120 sản phẩm...

   ✅ [1/120] Intel Core i3-12100F                                      |  2,450,000₫
   ✅ [10/120] Intel Core i5-13400F                                     |  5,490,000₫
   ✅ [20/120] AMD Ryzen 5 5600X                                        |  4,490,000₫
   ... (120 sản phẩm)

================================================================================
🎉 HOÀN THÀNH CRAWL!
================================================================================
📊 Tổng số thẻ .product-item tìm thấy: 120
✅ Crawl thành công: 120 sản phẩm
❌ Bỏ qua: 0 phần tử (thiếu thông tin)
💾 Dữ liệu đã lưu trong bộ nhớ: 120 sản phẩm
================================================================================

================================================================================
💾 ĐANG LƯU DỮ LIỆU
================================================================================
📁 Bước 1: Lưu vào file riêng 'cpu_data.csv'...
   🗑️  Đã xóa file cũ: cpu_data.csv
   ✅ Đã lưu 120 sản phẩm vào 'cpu_data.csv'!

📁 Bước 2: Chèn nối tiếp vào 'data.csv'...
   ✅ Đã chèn nối tiếp 120 sản phẩm vào 'data.csv'!

================================================================================
🎉 Đã lưu file riêng CPU và cập nhật vào kho data.csv thành công
================================================================================
📄 File riêng: cpu_data.csv (120 dòng)
📄 File chung: data.csv (đã thêm 120 dòng)
================================================================================

================================================================================
🎉 HOÀN THÀNH TẤT CẢ CÁC BƯỚC!
================================================================================

✅ Đã đóng browser!
```

---

## 🔍 So sánh RAM vs CPU Crawler

| Tính năng | RAM Crawler | CPU Crawler |
|-----------|-------------|-------------|
| **URL** | `/collections/bo-nho-ram/` | `/collections/cpu-bo-vi-xu-ly` |
| **Selector** | `.product-item` | `.product-item` ✅ |
| **Cơ chế** | Click "Xem thêm" | Click "Xem thêm" ✅ |
| **Tên field** | `ten_ram` | `ten_cpu` |
| **Hãng field** | `loai_ram` (DDR4/DDR5) | `hang` (Intel/AMD) |
| **Category** | `RAM` | `CPU` ✅ |
| **File riêng** | `ram_data.csv` | `cpu_data.csv` ✅ |
| **Append vào data.csv** | Không | **Có** ✅ |

---

## 💡 Điểm khác biệt quan trọng

### 1. **Thêm cột `category`**
```python
cpu_info = {
    'ten_cpu': name,
    'hang': brand,
    'thong_so': specs,
    'gia_vnd': price,
    'link_hinh_anh': img_url,
    'category': 'CPU'  # ← Điểm mới
}
```

### 2. **Append vào `data.csv`**
```python
# Mode 'a' thay vì 'w'
with open('data.csv', 'a', ...) as f:
    # Không ghi header nếu file đã tồn tại
    if not file_exists:
        writer.writeheader()
    writer.writerows(cpu_data)
```

### 3. **Thông báo debug**
```
🎉 Đã lưu file riêng CPU và cập nhật vào kho data.csv thành công
```

---

## 🐛 Debug

### File debug được tạo:
- `debug_cpu_initial_load.png` - Sau khi load trang
- `debug_cpu_after_load_all.png` - Sau khi load hết sản phẩm
- `debug_cpu_wait_timeout_*.png` - Nếu timeout

---

## ✅ Checklist

- [x] Selector `.product-item` (giống RAM)
- [x] Click "Xem thêm" tự động
- [x] Thêm cột `category: 'CPU'`
- [x] Lưu file riêng `cpu_data.csv` (mode 'w')
- [x] Append vào `data.csv` (mode 'a', header=False nếu file tồn tại)
- [x] Thông báo: "Đã lưu file riêng CPU và cập nhật vào kho data.csv thành công"

---

## 🚀 Kết hợp RAM + CPU

### Workflow hoàn chỉnh:
```bash
# Bước 1: Crawl RAM
python crawler_ram.py
# → Tạo: ram_data.csv

# Bước 2: Crawl CPU
python crawler_cpu.py
# → Tạo: cpu_data.csv
# → Append vào: data.csv

# Kết quả:
# - ram_data.csv: 219 sản phẩm RAM
# - cpu_data.csv: 120 sản phẩm CPU
# - data.csv: 339 sản phẩm (219 RAM + 120 CPU)
```

---

## 📞 Lưu ý

1. **Chạy RAM trước:** Để có file `data.csv` ban đầu
2. **Chạy CPU sau:** Để append vào file đã có
3. **Cột `category`:** Dùng để phân biệt RAM vs CPU
4. **Không ghi đè:** Mode `'a'` đảm bảo không mất dữ liệu cũ

---

**Phiên bản:** 1.0  
**Ngày:** 15/02/2026  
**Tác giả:** AI Assistant  
**Dựa trên:** `crawler_ram.py`
