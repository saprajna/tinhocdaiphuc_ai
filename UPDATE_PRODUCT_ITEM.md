# 🎯 CẬP NHẬT: SELECTOR CHÍNH XÁC `.product-item`

## 📅 Ngày cập nhật: 15/02/2026

---

## 🔍 PHÁT HIỆN TỪ INSPECT

Sau khi soi kỹ bằng **Inspect Element**, đã xác định được:

✅ **Selector chính xác:** `.product-item`  
❌ **Selector cũ (sai):** `.product-loop`, `.product-inner`

---

## 🔧 CÁC THAY ĐỔI CHI TIẾT

### 1️⃣ **WebDriverWait - Chờ .product-item**

**Trước:**
```python
WebDriverWait(driver, 20).until(
    lambda d: len(d.find_elements(..., ".product-loop, .product-item, .item")) >= 20
)
```

**Sau:**
```python
WebDriverWait(driver, 20).until(
    lambda d: len(d.find_elements(By.CSS_SELECTOR, ".product-item")) >= 20
)
```

**Lợi ích:**
- ✅ Chờ đúng selector
- ✅ Tránh bắt nhầm "Gợi ý" (< 20 sản phẩm)
- ✅ In rõ số lượng `.product-item` tìm thấy

---

### 2️⃣ **Đếm số lượng .product-item**

**Trong hàm `load_all_products_with_load_more()`:**

```python
# Trước mỗi lần click
current_products = driver.find_elements(By.CSS_SELECTOR, ".product-item")
current_count = len(current_products)
print(f"📊 Hiện có {current_count} thẻ .product-item trên trang")

# Click nút "Xem thêm"
button.click()
time.sleep(5)

# Sau khi click
new_products = driver.find_elements(By.CSS_SELECTOR, ".product-item")
new_count = len(new_products)
print(f"📦 Số .product-item sau khi click: {new_count}")
print(f"➕ Tăng thêm: {new_count - current_count} sản phẩm")
```

**Lợi ích:**
- ✅ Biết chính xác có bao nhiêu sản phẩm
- ✅ Theo dõi tiến độ realtime
- ✅ Phát hiện nếu không tăng (dừng lại)

---

### 3️⃣ **Tìm tất cả .product-item**

**Trước (dự phòng nhiều selector):**
```python
products = driver.find_elements(..., ".product-loop")
if not products:
    products = driver.find_elements(..., ".product-item")
if not products:
    products = driver.find_elements(..., ".item")
```

**Sau (chỉ dùng 1 selector chính xác):**
```python
products = driver.find_elements(By.CSS_SELECTOR, ".product-item")
print(f"✅ Tìm thấy {len(products)} thẻ .product-item")
```

**Lợi ích:**
- ✅ Đơn giản hơn
- ✅ Chính xác hơn
- ✅ Không lấy nhầm element khác

---

### 4️⃣ **Lấy TÊN sản phẩm**

**Cách mới:**
```python
# Tìm thẻ <a> bên trong .product-item
name_element = product.find_element(By.CSS_SELECTOR, "a")

# Ưu tiên lấy từ thuộc tính title
name = name_element.get_attribute("title")

# Nếu không có title, lấy text
if not name or name.strip() == "":
    name = name_element.text.strip()
```

**Thứ tự ưu tiên:**
1. `a.get_attribute("title")` ← Ưu tiên
2. `a.text` ← Dự phòng

---

### 5️⃣ **Lấy GIÁ sản phẩm**

**Cách mới:**
```python
# Thử các selector theo thứ tự
price_selectors = [
    ".price",           # Ưu tiên 1
    ".current-price",   # Ưu tiên 2
    ".p-price",         # Ưu tiên 3
    ".pro-price",       # Dự phòng 1
    ".product-price"    # Dự phòng 2
]

for price_selector in price_selectors:
    try:
        price_element = product.find_element(By.CSS_SELECTOR, price_selector)
        price_text = price_element.text.strip()
        price = clean_price(price_text)
        if price:
            break  # Tìm thấy rồi, dừng lại
    except:
        continue
```

**Thứ tự ưu tiên:**
1. `.price`
2. `.current-price`
3. `.p-price`
4. `.pro-price` (fallback)
5. `.product-price` (fallback)

---

### 6️⃣ **Lấy ẢNH sản phẩm**

**Cách mới:**
```python
# Tìm thẻ img bên trong .product-item
img_element = product.find_element(By.CSS_SELECTOR, "img")

# Ưu tiên lấy data-src (lazy load), nếu không có thì lấy src
img_url = img_element.get_attribute("data-src") or img_element.get_attribute("src")

# Đảm bảo URL đầy đủ
if not img_url.startswith('http'):
    if img_url.startswith('//'):
        img_url = 'https:' + img_url
    elif img_url.startswith('/'):
        img_url = 'https://tinhocngoisao.com' + img_url
```

**Thứ tự ưu tiên:**
1. `img.get_attribute("data-src")` ← Ưu tiên (lazy load)
2. `img.get_attribute("src")` ← Dự phòng

---

## 📊 OUTPUT MẪU

```
================================================================================
🚀 BẮT ĐẦU CRAWL TOÀN BỘ SẢN PHẨM RAM
================================================================================
🌐 Website: https://tinhocngoisao.com/collections/bo-nho-ram/
⚙️  Phương pháp: Click nút 'Xem thêm' với WebDriverWait
================================================================================

📍 Đang truy cập: https://tinhocngoisao.com/collections/bo-nho-ram/
📸 Đã chụp ảnh sau khi load: debug_initial_load.png

================================================================================
🔍 KIỂM TRA DANH SÁCH SẢN PHẨM CHÍNH
================================================================================
⏳ Đang chờ ít nhất 20 thẻ .product-item xuất hiện (tối đa 20s)...
   (Để tránh bắt nhầm mục 'Gợi ý')
✅ Đã phát hiện 48 thẻ .product-item!

================================================================================
🔄 ĐANG TẢI TOÀN BỘ SẢN PHẨM BẰNG NÚT 'XEM THÊM'
================================================================================
📊 Hiện có 48 thẻ .product-item trên trang

🖱️  Đang bấm nút 'Xem thêm' lần 1...
📦 Số .product-item trước khi click: 48
✅ Đã click nút thành công!
⏳ Chờ 5 giây để sản phẩm mới hiện ra...
📦 Số .product-item sau khi click: 96
➕ Tăng thêm: 48 sản phẩm

📊 Hiện có 96 thẻ .product-item trên trang

🖱️  Đang bấm nút 'Xem thêm' lần 2...
📦 Số .product-item trước khi click: 96
✅ Đã click nút thành công!
⏳ Chờ 5 giây để sản phẩm mới hiện ra...
📦 Số .product-item sau khi click: 144
➕ Tăng thêm: 48 sản phẩm

📊 Hiện có 144 thẻ .product-item trên trang

🖱️  Đang bấm nút 'Xem thêm' lần 3...
📦 Số .product-item trước khi click: 144
✅ Đã click nút thành công!
⏳ Chờ 5 giây để sản phẩm mới hiện ra...
📦 Số .product-item sau khi click: 192
➕ Tăng thêm: 48 sản phẩm

📊 Hiện có 192 thẻ .product-item trên trang

🖱️  Đang bấm nút 'Xem thêm' lần 4...
📦 Số .product-item trước khi click: 192
✅ Đã click nút thành công!
⏳ Chờ 5 giây để sản phẩm mới hiện ra...
📦 Số .product-item sau khi click: 219
➕ Tăng thêm: 27 sản phẩm

📊 Hiện có 219 thẻ .product-item trên trang

🖱️  Đang bấm nút 'Xem thêm' lần 5...
📦 Số .product-item trước khi click: 219
✅ Đã click nút thành công!
⏳ Chờ 5 giây để sản phẩm mới hiện ra...
📦 Số .product-item sau khi click: 219
➕ Tăng thêm: 0 sản phẩm
⚠️ Không có sản phẩm mới xuất hiện! (lần 1)

📊 Hiện có 219 thẻ .product-item trên trang

🖱️  Đang bấm nút 'Xem thêm' lần 6...
📦 Số .product-item trước khi click: 219
✅ Đã click nút thành công!
⏳ Chờ 5 giây để sản phẩm mới hiện ra...
📦 Số .product-item sau khi click: 219
➕ Tăng thêm: 0 sản phẩm
⚠️ Không có sản phẩm mới xuất hiện! (lần 2)

✅ Đã thử 2 lần mà không có sản phẩm mới - Dừng lại!

================================================================================
✅ HOÀN TẤT VIỆC TẢI SẢN PHẨM
================================================================================
🖱️  Tổng số lần bấm nút: 6
🔝 Scroll về đầu trang...
📸 Đã chụp ảnh sau khi load hết: debug_after_load_all.png

================================================================================
📊 BẮT ĐẦU THU THẬP DỮ LIỆU TỪ TẤT CẢ SẢN PHẨM
================================================================================
🔍 Đang tìm kiếm tất cả thẻ .product-item...
   ✅ Tìm thấy 219 thẻ .product-item

✅ Bắt đầu crawl 219 sản phẩm...

   ✅ [1/219] RAM Kingston Fury Beast 8GB DDR4 3200MHz       | DDR4   8GB |    490,000₫
   ✅ [10/219] RAM Corsair Vengeance 16GB DDR4 3200MHz       | DDR4  16GB |    950,000₫
   ✅ [20/219] RAM G.Skill Trident Z5 32GB DDR5 6000MHz      | DDR5  32GB |  2,890,000₫
   ...
   ✅ [210/219] RAM ADATA XPG Lancer 16GB DDR5               | DDR5  16GB |  1,390,000₫
   ✅ [219/219] RAM Patriot Viper Steel 32GB DDR4            | DDR4  32GB |  1,850,000₫

================================================================================
🎉 HOÀN THÀNH CRAWL!
================================================================================
📊 Tổng số thẻ .product-item tìm thấy: 219
✅ Crawl thành công: 219 sản phẩm
❌ Bỏ qua: 0 phần tử (thiếu thông tin)
💾 Dữ liệu đã lưu trong bộ nhớ: 219 sản phẩm
================================================================================
```

---

## 🔄 SO SÁNH TRƯỚC VÀ SAU

| Tính năng | Trước | Sau |
|-----------|-------|-----|
| **Selector chính** | `.product-loop` (sai) | `.product-item` (đúng) |
| **WebDriverWait** | Chờ nhiều selector | Chỉ chờ `.product-item` |
| **Đếm sản phẩm** | Không rõ ràng | In ra mỗi lần click |
| **Lấy tên** | `.pro-loop-name a` | `a[title]` hoặc `a.text` |
| **Lấy giá** | `.pro-price` | `.price`, `.current-price`, `.p-price` |
| **Lấy ảnh** | `.product-img img` | `img[data-src]` hoặc `img[src]` |
| **Debug** | Ít thông tin | Chi tiết từng bước |

---

## 📋 CHECKLIST ĐỂ KIỂM TRA

Khi chạy crawler, kiểm tra:

- [ ] WebDriverWait tìm thấy ít nhất 20 thẻ `.product-item`
- [ ] Mỗi lần click "Xem thêm", số `.product-item` tăng lên
- [ ] Sau khi load hết, có ~200+ thẻ `.product-item`
- [ ] Crawl được ~200+ sản phẩm (không phải 4 sản phẩm "Gợi ý")
- [ ] Tên sản phẩm đầy đủ (không bị thiếu)
- [ ] Giá sản phẩm chính xác
- [ ] Link ảnh đầy đủ (https://...)

---

## 🚀 CÁCH CHẠY

```bash
python crawler_ram.py
```

---

## 💡 LƯU Ý QUAN TRỌNG

### ✅ **Selector chính xác là chìa khóa!**

Nếu bạn gặp lỗi tương tự, hãy:

1. **Mở website trong Chrome**
2. **Nhấn F12** (Developer Tools)
3. **Click vào biểu tượng "Select element"** (Ctrl+Shift+C)
4. **Click vào sản phẩm** trên trang
5. **Xem class nào được dùng** (VD: `.product-item`)
6. **Kiểm tra xem có bao nhiêu phần tử** với class đó:
   ```javascript
   document.querySelectorAll('.product-item').length
   ```
7. **Cập nhật selector** trong code

---

## 🐛 DEBUG NẾU VẪN LỖI

### Bước 1: Kiểm tra log
```
⏳ Đang chờ ít nhất 20 thẻ .product-item xuất hiện...
✅ Đã phát hiện 48 thẻ .product-item!  ← Phải ≥ 20
```

### Bước 2: Kiểm tra số lượng tăng
```
📦 Số .product-item trước: 48
📦 Số .product-item sau: 96
➕ Tăng thêm: 48 sản phẩm  ← Phải tăng
```

### Bước 3: Kiểm tra tổng cuối cùng
```
📊 Tổng số thẻ .product-item tìm thấy: 219  ← Phải ~200+
```

### Nếu vẫn lỗi:
1. Mở file `debug_initial_load.png` - Xem trang ban đầu
2. Mở file `debug_after_load_all.png` - Xem sau khi load hết
3. Mở file `debug_page.html` - Search `.product-item` để đếm
4. Console: `document.querySelectorAll('.product-item').length`

---

## ✅ KẾT LUẬN

Với selector chính xác `.product-item`, crawler sẽ:
1. ✅ Chờ đúng danh sách chính (≥ 20 sản phẩm)
2. ✅ Không bắt nhầm "Gợi ý" (4 sản phẩm)
3. ✅ Đếm chính xác số lượng sau mỗi lần click
4. ✅ Lấy đúng tên, giá, ảnh từ `.product-item`
5. ✅ Crawl được ~200+ sản phẩm

---

**Phiên bản:** 5.0 (Exact Selector - `.product-item`)  
**Cập nhật:** 15/02/2026  
**Tác giả:** AI Assistant  
**Fix:** Sử dụng selector chính xác từ Inspect Element
