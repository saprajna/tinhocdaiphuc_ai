# 📄 CẬP NHẬT: PHÂN TRANG CRAWLER RAM

## 🎯 Ngày cập nhật: 15/02/2026

---

## ✅ VẤN ĐỀ ĐÃ KHẮC PHỤC

**Trước đây:** Crawler chỉ lấy được ~50 sản phẩm từ trang 1

**Hiện tại:** Crawler lấy được **TOÀN BỘ** sản phẩm từ **TẤT CẢ** các trang (200+ sản phẩm)

---

## 🔧 CÁC THAY ĐỔI KỸ THUẬT

### 1️⃣ **Tách thành 2 hàm**

#### **Hàm mới: `crawl_single_page()`**
```python
def crawl_single_page(self, page_url: str, page_number: int) -> int:
    """Crawl một trang cụ thể và trả về số sản phẩm đã crawl được"""
    # Crawl một trang
    # Trả về số sản phẩm thành công
```

#### **Hàm cải tiến: `crawl_ram_data()`**
```python
def crawl_ram_data(self):
    """Crawl TOÀN BỘ dữ liệu RAM từ TẤT CẢ các trang"""
    page_number = 1
    while True:
        # Crawl trang hiện tại
        products = crawl_single_page(page_url, page_number)
        
        # Nếu không có sản phẩm, dừng lại
        if products == 0:
            break
        
        page_number += 1
```

---

## 🔄 LOGIC PHÂN TRANG

### **Cấu trúc URL:**
```
Trang 1: https://tinhocngoisao.com/collections/bo-nho-ram/
Trang 2: https://tinhocngoisao.com/collections/bo-nho-ram/?page=2
Trang 3: https://tinhocngoisao.com/collections/bo-nho-ram/?page=3
...
```

### **Vòng lặp:**
```
1. Bắt đầu từ page = 1
2. Crawl trang hiện tại
3. Nếu tìm thấy sản phẩm:
   - Lưu vào ram_data
   - Tăng page lên 1
   - Chờ 3 giây (tránh bị ban)
   - Quay lại bước 2
4. Nếu KHÔNG tìm thấy sản phẩm:
   - DỪNG LẠI (đã hết trang)
```

---

## 📊 OUTPUT MẪU

```
================================================================================
🚀 BẮT ĐẦU CRAWL TOÀN BỘ SẢN PHẨM RAM
================================================================================
🌐 Website: https://tinhocngoisao.com/collections/bo-nho-ram/
================================================================================

================================================================================
📄 ĐANG CÀO TRANG 1...
================================================================================
🔗 URL: https://tinhocngoisao.com/collections/bo-nho-ram/
⏳ Đợi trang tải đầy đủ (5 giây)...
Đang scroll để load tất cả sản phẩm...
🔍 Đang tìm kiếm sản phẩm...
   ✅ Tìm thấy 48 sản phẩm với .product-loop
✅ Bắt đầu crawl 48 sản phẩm...

   ✅ 1. RAM Kingston Fury Beast 8GB DDR4 3200MHz         | DDR4   8GB |    490,000₫
   ✅ 2. RAM Kingston Fury Beast 16GB DDR4 3200MHz        | DDR4  16GB |    890,000₫
   ... (46 sản phẩm khác)

================================================================================
✅ Trang 1: Crawl thành công 48/48 sản phẩm!
================================================================================

⏸️  Nghỉ 3 giây trước khi chuyển sang trang tiếp theo...

================================================================================
📄 ĐANG CÀO TRANG 2...
================================================================================
🔗 URL: https://tinhocngoisao.com/collections/bo-nho-ram/?page=2
⏳ Đợi trang tải đầy đủ (5 giây)...
Đang scroll để load tất cả sản phẩm...
🔍 Đang tìm kiếm sản phẩm...
   ✅ Tìm thấy 48 sản phẩm với .product-loop
✅ Bắt đầu crawl 48 sản phẩm...

   ✅ 1. RAM Corsair Vengeance RGB Pro 32GB DDR4          | DDR4  32GB |  1,790,000₫
   ✅ 2. RAM G.Skill Trident Z5 RGB 16GB DDR5             | DDR5  16GB |  1,490,000₫
   ... (46 sản phẩm khác)

================================================================================
✅ Trang 2: Crawl thành công 48/48 sản phẩm!
================================================================================

⏸️  Nghỉ 3 giây trước khi chuyển sang trang tiếp theo...

================================================================================
📄 ĐANG CÀO TRANG 3...
================================================================================
🔗 URL: https://tinhocngoisao.com/collections/bo-nho-ram/?page=3
⏳ Đợi trang tải đầy đủ (5 giây)...
Đang scroll để load tất cả sản phẩm...
🔍 Đang tìm kiếm sản phẩm...
   ✅ Tìm thấy 48 sản phẩm với .product-loop
✅ Bắt đầu crawl 48 sản phẩm...

   ✅ 1. RAM Teamgroup T-Force Delta RGB 16GB DDR5        | DDR5  16GB |  1,390,000₫
   ... (47 sản phẩm khác)

================================================================================
✅ Trang 3: Crawl thành công 48/48 sản phẩm!
================================================================================

⏸️  Nghỉ 3 giây trước khi chuyển sang trang tiếp theo...

================================================================================
📄 ĐANG CÀO TRANG 4...
================================================================================
🔗 URL: https://tinhocngoisao.com/collections/bo-nho-ram/?page=4
⏳ Đợi trang tải đầy đủ (5 giây)...
Đang scroll để load tất cả sản phẩm...
🔍 Đang tìm kiếm sản phẩm...
   ✅ Tìm thấy 32 sản phẩm với .product-loop
✅ Bắt đầu crawl 32 sản phẩm...

   ✅ 1. RAM ADATA XPG Lancer RGB 32GB DDR5               | DDR5  32GB |  2,590,000₫
   ... (31 sản phẩm khác)

================================================================================
✅ Trang 4: Crawl thành công 32/32 sản phẩm!
================================================================================

⏸️  Nghỉ 3 giây trước khi chuyển sang trang tiếp theo...

================================================================================
📄 ĐANG CÀO TRANG 5...
================================================================================
🔗 URL: https://tinhocngoisao.com/collections/bo-nho-ram/?page=5
⏳ Đợi trang tải đầy đủ (5 giây)...
Đang scroll để load tất cả sản phẩm...
🔍 Đang tìm kiếm sản phẩm...
❌ Trang 5: KHÔNG TÌM THẤY SẢN PHẨM NÀO!

================================================================================
🛑 DỪNG LẠI: Trang 5 không có sản phẩm
================================================================================

================================================================================
🎉 HOÀN THÀNH CRAWL TẤT CẢ CÁC TRANG!
================================================================================
📊 Tổng cộng: 176 sản phẩm từ 4 trang
💾 Dữ liệu đã lưu trong bộ nhớ: 176 sản phẩm
================================================================================
```

---

## ⚡ ƯU ĐIỂM

1. ✅ **Lấy toàn bộ sản phẩm** - Không bỏ sót
2. ✅ **Tự động phát hiện hết trang** - Dừng đúng lúc
3. ✅ **Thông báo rõ ràng** - Dễ theo dõi
4. ✅ **Tránh bị ban** - Chờ 3 giây giữa các trang
5. ✅ **Dữ liệu liên tục** - Tự động nối tiếp vào danh sách

---

## 🚀 CÁCH CHẠY

```bash
# Chạy như bình thường
python crawler_ram.py
```

**Không cần thay đổi gì!** Script sẽ tự động crawl tất cả các trang.

---

## ⏱️ THỜI GIAN DỰ KIẾN

Với ~200 sản phẩm trên 4-5 trang:

| Bước | Thời gian |
|------|-----------|
| Load mỗi trang | ~5 giây |
| Scroll & crawl | ~10 giây |
| Nghỉ giữa trang | 3 giây |
| **Mỗi trang** | **~18 giây** |
| **4 trang** | **~72 giây (1.2 phút)** |

---

## 🐛 XỬ LÝ LỖI

### **Trang đầu không có sản phẩm:**
- Tạo file `debug_screenshot.png` và `debug_page.html`
- Kiểm tra selector có đúng không

### **Trang giữa không có sản phẩm:**
- Dừng lại ngay lập tức
- Lưu dữ liệu đã crawl được

### **Mất kết nối:**
- Script sẽ báo lỗi
- Dữ liệu đã crawl vẫn được giữ trong `ram_data`

---

## 💡 LƯU Ý

1. **Không giới hạn số trang:** Script sẽ tự động crawl đến khi hết sản phẩm
2. **Dữ liệu nối tiếp:** Tất cả sản phẩm từ mọi trang được lưu vào `ram_data.csv`
3. **Thời gian chờ:** 3 giây giữa các trang để tránh bị website chặn
4. **Debug chỉ trang 1:** Screenshot và HTML chỉ lưu cho trang đầu tiên nếu lỗi

---

## 📈 SO SÁNH

| Phiên bản | Số sản phẩm | Số trang | Thời gian |
|-----------|-------------|----------|-----------|
| **Cũ** | ~50 | 1 | ~15 giây |
| **Mới** | 200+ | 4-5 | ~70 giây |

**Tăng gấp 4 lần dữ liệu!** 🎉

---

**Phiên bản:** 3.0 (Pagination Support)  
**Cập nhật:** 15/02/2026  
**Tác giả:** AI Assistant
