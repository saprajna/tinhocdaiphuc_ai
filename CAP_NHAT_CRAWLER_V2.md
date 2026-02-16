# 📋 CẬP NHẬT CRAWLER RAM - PHIÊN BẢN 2.0

## 🎯 Ngày cập nhật: 15/02/2026

---

## ✅ CÁC THAY ĐỔI CHÍNH

### 1️⃣ **Thay đổi URL mới**
```
CŨ: https://tinhocngoisao.com/collections/ram-bo-nho-trong
MỚI: https://tinhocngoisao.com/collections/bo-nho-ram/
```

### 2️⃣ **Selector chuẩn Tin Học Ngôi Sao**

| Thành phần | Selector | Ghi chú |
|------------|----------|---------|
| **Khối sản phẩm** | `.product-loop` hoặc `.product-inner` | Container chứa thông tin sản phẩm |
| **Tên sản phẩm** | `.pro-loop-name a` | Lấy text từ thẻ a |
| **Giá sản phẩm** | `.pro-price` hoặc `.compare-price` | Ưu tiên giá khuyến mãi nếu có |
| **Hình ảnh** | `.product-img img` | Lấy `data-src` trước, sau đó `src` |

### 3️⃣ **Tăng thời gian chờ tải trang**
```python
# Thêm time.sleep(5) sau khi mở link
time.sleep(5)  # Đảm bảo web load hết danh sách sản phẩm
```

### 4️⃣ **Xóa dữ liệu cũ trước khi ghi**
```python
# Xóa file ram_data.csv cũ trước khi ghi mới
if os.path.exists(filename):
    os.remove(filename)
    print(f"🗑️  Đã xóa file cũ: {filename}")
```

---

## 🔧 LOGIC XỬ LÝ GIÁ MỚI

### Ưu tiên giá khuyến mãi:
1. **Bước 1:** Kiểm tra có `.compare-price` (giá gạch) không
2. **Bước 2:** Nếu có, so sánh với `.pro-price` (giá hiện tại)
3. **Bước 3:** Lấy giá thấp hơn (chính là giá khuyến mãi)
4. **Bước 4:** Nếu không có giá khuyến mãi, lấy `.pro-price` thường

```python
# Pseudo code
if có .compare-price:
    giá_gạch = lấy_từ(.compare-price)
    giá_hiện_tại = lấy_từ(.pro-price)
    giá_cuối = min(giá_gạch, giá_hiện_tại)  # Lấy giá thấp hơn
else:
    giá_cuối = lấy_từ(.pro-price)  # Giá thường
```

---

## 🚀 CÁCH CHẠY

```bash
# Bước 1: Đảm bảo đã cài đặt thư viện
pip install selenium webdriver-manager pandas

# Bước 2: Chạy crawler
python crawler_ram.py
```

---

## 📊 KẾT QUẢ MẪU

```
================================================================================
🚀 CRAWLER RAM - TIN HỌC NGÔI SAO
================================================================================
📅 URL: https://tinhocngoisao.com/collections/bo-nho-ram/
🔧 Selector: .product-loop | .pro-loop-name | .pro-price | .product-img
================================================================================

Đang khởi tạo Chrome driver...
Chrome driver đã sẵn sàng!

📍 Đang truy cập: https://tinhocngoisao.com/collections/bo-nho-ram/
⏳ Đợi trang tải đầy đủ (5 giây)...
Đang scroll để load tất cả sản phẩm...
Đã load xong tất cả sản phẩm sau 3 lần scroll!

🔍 Đang tìm kiếm sản phẩm với selector chuẩn...
   🎯 Thử selector: .product-loop
   ✅ Tìm thấy 48 sản phẩm với .product-loop

✅ Đã tìm thấy 48 sản phẩm! Bắt đầu crawl dữ liệu...

   ✅ 1. RAM Kingston Fury Beast 8GB DDR4 3200MHz          | DDR4   8GB |    490,000₫
   ✅ 2. RAM Kingston Fury Beast 16GB DDR4 3200MHz         | DDR4  16GB |    890,000₫
   ✅ 3. RAM Corsair Vengeance 16GB DDR5 5600MHz           | DDR5  16GB |  1,390,000₫
   ...

================================================================================
✅ Crawl thành công 48/48 sản phẩm RAM!
================================================================================

💾 Đang lưu dữ liệu vào ram_data.csv...
   🗑️  Đã xóa file cũ: ram_data.csv
✅ Đã lưu 48 sản phẩm mới vào ram_data.csv!

🔍 Đang phân tích giá tốt nhất...

📊 DDR4 - Giá tốt nhất theo dung lượng:
   • 8GB: RAM Kingston Fury Beast 8GB DDR4 3200MHz... - 490,000 VNĐ
   • 16GB: RAM Kingston Fury Beast 16GB DDR4 3200MHz... - 890,000 VNĐ
   • 32GB: RAM Kingston Fury Beast 32GB DDR4 3200MHz... - 1,690,000 VNĐ

📊 DDR5 - Giá tốt nhất theo dung lượng:
   • 16GB: RAM ADATA XPG 16GB DDR5 5200MHz... - 1,190,000 VNĐ
   • 32GB: RAM ADATA XPG 32GB DDR5 5200MHz... - 2,390,000 VNĐ

🔄 Đang cập nhật data.csv...
   - Đã xóa 29 RAM cũ
✅ Đã cập nhật 8 sản phẩm RAM vào data.csv!

================================================================================
🎉 HOÀN THÀNH!
================================================================================
```

---

## 📁 CÁC FILE ĐƯỢC TẠO

1. **`ram_data.csv`** - Toàn bộ RAM đã crawl (48 sản phẩm)
2. **`ram_best_deals.csv`** - TOP giá tốt cho mỗi loại (8 sản phẩm)
3. **`data.csv`** - File chính đã được cập nhật

---

## 🐛 XỬ LÝ LỖI

### Nếu không tìm thấy sản phẩm:
Crawler sẽ tự động tạo 2 file debug:
- **`debug_screenshot.png`** - Ảnh chụp màn hình
- **`debug_page.html`** - HTML của trang

### Các lỗi thường gặp:

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| Không tìm thấy sản phẩm | Selector không đúng | Kiểm tra file `debug_page.html` |
| Không tìm thấy tên | `.pro-loop-name a` không tồn tại | Kiểm tra cấu trúc HTML |
| Không tìm thấy giá | `.pro-price` không tồn tại | Kiểm tra selector giá |
| File CSV rỗng | Tất cả sản phẩm bị lỗi | Xem log chi tiết |

---

## 💡 LƯU Ý QUAN TRỌNG

1. ✅ **Selector đã được cập nhật chính xác** theo theme Tin Học Ngôi Sao
2. ✅ **Thời gian chờ 5 giây** đảm bảo web load đầy đủ
3. ✅ **Xóa file cũ trước khi ghi** để không bị trùng dữ liệu
4. ✅ **Ưu tiên giá khuyến mãi** để lấy giá tốt nhất
5. ✅ **Xử lý ảnh lazy load** với `data-src`

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề:
1. Kiểm tra file `debug_page.html`
2. Xem screenshot `debug_screenshot.png`
3. Đọc log chi tiết trên console
4. So sánh selector với HTML thực tế

---

**Phiên bản:** 2.0  
**Cập nhật:** 15/02/2026  
**Tác giả:** AI Assistant
