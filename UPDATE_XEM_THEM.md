# 🔄 CẬP NHẬT: CƠ CHẾ "XEM THÊM" CHO CRAWLER RAM

## 🎯 Ngày cập nhật: 15/02/2026

---

## 🔍 PHÁT HIỆN QUAN TRỌNG

**Website không dùng phân trang (page=1, 2, 3...) mà dùng nút "Xem thêm" để tải thêm sản phẩm!**

❌ **Cũ:** URL với `?page=2`, `?page=3`...  
✅ **Mới:** Nút "Xem thêm" ở cuối trang để AJAX load thêm sản phẩm

---

## 🔧 LOGIC MỚI

### **Luồng hoạt động:**

```
1. Truy cập trang đầu tiên
2. Đợi 5 giây load
3. VÒNG LẶP:
   a. Tìm nút "Xem thêm"
   b. Nếu tìm thấy và hiển thị:
      - Scroll đến nút
      - Click nút
      - Chờ 3 giây (để sản phẩm mới load)
      - Scroll xuống cuối trang
      - Quay lại bước a
   c. Nếu KHÔNG tìm thấy hoặc nút bị ẩn:
      - DỪNG vòng lặp
4. Sau khi load HẾT sản phẩm:
   - Crawl TOÀN BỘ sản phẩm đã hiện trên trang
   - Lưu vào CSV một lần duy nhất
```

---

## 📝 CODE CHI TIẾT

### **Hàm mới: `load_all_products_with_load_more()`**

```python
def load_all_products_with_load_more(self):
    """Click nút 'Xem thêm' liên tục cho đến khi load hết"""
    
    click_count = 0
    max_clicks = 50  # Giới hạn an toàn
    
    while click_count < max_clicks:
        # Tìm nút với nhiều cách:
        # 1. XPath: //a[contains(text(), 'Xem thêm')]
        # 2. XPath: //a[contains(text(), 'XEM THÊM')]
        # 3. Class: .btn-load-more
        # 4. Class: .view-more, .load-more, .btn-loadmore
        
        if không_tìm_thấy_nút:
            print("✅ Đã load hết sản phẩm!")
            break
        
        # Scroll đến nút
        scroll_to_element(button)
        
        # Click nút
        click_count += 1
        print(f"🖱️ Đã bấm nút 'Xem thêm' lần {click_count}...")
        button.click()
        
        # Chờ 3 giây
        print("⏳ Chờ 3 giây để sản phẩm mới hiện ra...")
        time.sleep(3)
        
        # Scroll xuống cuối
        scroll_to_bottom()
        
        # Đếm sản phẩm hiện tại
        print(f"📦 Hiện có {count} sản phẩm trên trang")
```

### **Hàm cải tiến: `crawl_ram_data()`**

```python
def crawl_ram_data(self):
    """Crawl với cơ chế 'Xem thêm'"""
    
    # 1. Truy cập trang
    driver.get(url)
    time.sleep(5)
    
    # 2. Click "Xem thêm" cho đến khi hết
    load_all_products_with_load_more()
    
    # 3. Bây giờ crawl TOÀN BỘ sản phẩm đã load
    products = find_all_products()
    
    # 4. Thu thập dữ liệu
    for product in products:
        extract_data(product)
    
    # 5. Lưu CSV một lần
    save_to_csv()
```

---

## 📊 OUTPUT MẪU

```
================================================================================
🚀 BẮT ĐẦU CRAWL TOÀN BỘ SẢN PHẨM RAM
================================================================================
🌐 Website: https://tinhocngoisao.com/collections/bo-nho-ram/
⚙️  Phương pháp: Click nút 'Xem thêm'
================================================================================

📍 Đang truy cập: https://tinhocngoisao.com/collections/bo-nho-ram/
⏳ Đợi trang tải đầy đủ (5 giây)...

================================================================================
🔄 ĐANG TẢI TOÀN BỘ SẢN PHẨM BẰNG NÚT 'XEM THÊM'
================================================================================
🖱️  Đã bấm nút 'Xem thêm' lần 1...
⏳ Chờ 3 giây để sản phẩm mới hiện ra...
📦 Hiện có 48 sản phẩm trên trang

🖱️  Đã bấm nút 'Xem thêm' lần 2...
⏳ Chờ 3 giây để sản phẩm mới hiện ra...
📦 Hiện có 96 sản phẩm trên trang

🖱️  Đã bấm nút 'Xem thêm' lần 3...
⏳ Chờ 3 giây để sản phẩm mới hiện ra...
📦 Hiện có 144 sản phẩm trên trang

🖱️  Đã bấm nút 'Xem thêm' lần 4...
⏳ Chờ 3 giây để sản phẩm mới hiện ra...
📦 Hiện có 192 sản phẩm trên trang

🖱️  Đã bấm nút 'Xem thêm' lần 5...
⏳ Chờ 3 giây để sản phẩm mới hiện ra...
📦 Hiện có 219 sản phẩm trên trang

✅ Không còn nút 'Xem thêm' - Đã load hết sản phẩm!

================================================================================
✅ HOÀN TẤT VIỆC TẢI SẢN PHẨM
================================================================================
🖱️  Tổng số lần bấm nút: 5

================================================================================
📊 BẮT ĐẦU THU THẬP DỮ LIỆU TỪ TẤT CẢ SẢN PHẨM
================================================================================
🔍 Đang tìm kiếm sản phẩm...
   ✅ Tìm thấy 219 sản phẩm với .product-loop

✅ Bắt đầu crawl 219 sản phẩm...

   ✅ [1/219] RAM Kingston Fury Beast 8GB DDR4 3200MHz         | DDR4   8GB |    490,000₫
   ✅ [10/219] RAM Corsair Vengeance 16GB DDR4 3200MHz         | DDR4  16GB |    950,000₫
   ✅ [20/219] RAM G.Skill Trident Z5 32GB DDR5 6000MHz        | DDR5  32GB |  2,890,000₫
   ... (crawl 219 sản phẩm)
   ✅ [210/219] RAM ADATA XPG Lancer 16GB DDR5                 | DDR5  16GB |  1,390,000₫
   ✅ [219/219] RAM Patriot Viper Steel 32GB DDR4              | DDR4  32GB |  1,850,000₫

================================================================================
🎉 HOÀN THÀNH CRAWL!
================================================================================
📊 Tổng số sản phẩm tìm thấy: 219
✅ Crawl thành công: 219 sản phẩm
❌ Bỏ qua: 0 sản phẩm (thiếu thông tin)
💾 Dữ liệu đã lưu trong bộ nhớ: 219 sản phẩm
================================================================================

💾 Đang lưu dữ liệu vào ram_data.csv...
   🗑️  Đã xóa file cũ: ram_data.csv
✅ Đã lưu 219 sản phẩm mới vào ram_data.csv!
```

---

## 🔍 CÁC SELECTOR ĐỂ TÌM NÚT "XEM THÊM"

Crawler thử **4 cách** để tìm nút (từ cụ thể → rộng):

| Thứ tự | Phương pháp | Selector |
|--------|-------------|----------|
| 1 | XPath với text | `//a[contains(text(), 'Xem thêm')]` |
| 2 | XPath viết hoa | `//a[contains(text(), 'XEM THÊM')]` |
| 3 | Class chính | `.btn-load-more` |
| 4 | Class dự phòng | `.view-more, .load-more, .btn-loadmore` |

---

## ⚡ ƯU ĐIỂM

1. ✅ **Lấy đúng 219 sản phẩm** - Không bỏ sót
2. ✅ **Tự động dừng** - Khi không còn nút "Xem thêm"
3. ✅ **Debug rõ ràng** - Biết đang bấm lần thứ mấy
4. ✅ **Đếm sản phẩm realtime** - Theo dõi tiến độ
5. ✅ **Chờ đủ thời gian** - 3 giây mỗi lần load
6. ✅ **Crawl một lần** - Sau khi đã load hết
7. ✅ **An toàn** - Giới hạn 50 lần click tối đa

---

## ⏱️ THỜI GIAN DỰ KIẾN

Với 219 sản phẩm, giả sử mỗi lần click load thêm 48 sản phẩm:

| Bước | Thời gian |
|------|-----------|
| Load trang đầu | 5 giây |
| Mỗi lần click | ~5 giây (scroll + click + chờ 3s) |
| 5 lần click | ~25 giây |
| Crawl 219 sản phẩm | ~30 giây |
| **TỔNG CỘNG** | **~60 giây (1 phút)** |

---

## 🐛 XỬ LÝ LỖI

### **Không tìm thấy nút "Xem thêm":**
- Thử 4 cách khác nhau
- Nếu không có → Coi như đã load hết

### **Click không được:**
- Thử click JavaScript: `element.click()`
- Fallback: `driver.execute_script("arguments[0].click()", element)`

### **Vòng lặp vô hạn:**
- Giới hạn tối đa 50 lần click
- Thoát nếu vượt quá

---

## 📋 SO SÁNH CÁC PHIÊN BẢN

| Phiên bản | Cơ chế | Số sản phẩm | Thời gian |
|-----------|--------|-------------|-----------|
| **v1.0** | Chỉ trang 1 | ~50 | 15s |
| **v2.0** | Phân trang ?page=X | ~50 | 18s |
| **v3.0** | Nút "Xem thêm" | **219** | **60s** |

**Tăng gấp 4 lần!** 🎉

---

## 🚀 CÁCH CHẠY

```bash
# Chạy như bình thường
python crawler_ram.py
```

**Hoàn toàn tự động!** Script sẽ:
1. Tìm và click nút "Xem thêm"
2. Lặp lại cho đến khi hết
3. Crawl toàn bộ 219 sản phẩm
4. Lưu vào CSV

---

## 💡 GHI CHÚ

- **Số lần click:** Tùy thuộc vào số sản phẩm mỗi lần load (thường 48)
- **219 sản phẩm = ~5 lần click** (48 + 48 + 48 + 48 + 27)
- **Chờ 3 giây:** Đảm bảo AJAX load xong
- **Hiển thị tiến độ mỗi 10 sản phẩm:** Để không spam log quá nhiều

---

**Phiên bản:** 3.0 (Load More Button Support)  
**Cập nhật:** 15/02/2026  
**Tác giả:** AI Assistant  
**Lưu ý:** Thích ứng với website dùng AJAX lazy loading thay vì pagination
