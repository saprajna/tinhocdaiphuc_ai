# 📊 SO SÁNH: CRAWLER RAM vs CPU

## 📅 Ngày: 15/02/2026

---

## 🔍 ĐIỂM GIỐNG NHAU

Cả 2 crawler đều dùng **CÙN MỘT CẤU TRÚC** vì website dùng cùng theme:

| Tính năng | RAM | CPU | Trạng thái |
|-----------|-----|-----|------------|
| **Selector** | `.product-item` | `.product-item` | ✅ Giống |
| **Tên** | `h3.pdLoopName a` | `h3.pdLoopName a` | ✅ Giống |
| **Giá** | `p.pdPrice span` | `p.pdPrice span` | ✅ Giống |
| **Ảnh** | `img[data-src]` hoặc `src` | `img[data-src]` hoặc `src` | ✅ Giống |
| **Cơ chế** | Click "Xem thêm" | Click "Xem thêm" | ✅ Giống |
| **Click method** | JavaScript Click | JavaScript Click | ✅ Giống |
| **Kiểm tra URL** | Có | Có | ✅ Giống |
| **WebDriverWait** | ≥ 20 sản phẩm | ≥ 20 sản phẩm | ✅ Giống |

---

## 🔄 ĐIỂM KHÁC NHAU

| Tính năng | RAM | CPU |
|-----------|-----|-----|
| **URL** | `/collections/bo-nho-ram/` | `/collections/cpu-bo-vi-xu-ly` |
| **Class name** | `RAMCrawler` | `CPUCrawler` |
| **Field tên** | `ten_ram` | `ten_cpu` |
| **Field hãng** | `loai_ram` (DDR4/DDR5) | `hang` (Intel/AMD) |
| **Category** | `'RAM'` | `'CPU'` |
| **File riêng** | `ram_data.csv` | `cpu_data.csv` |
| **Mode ghi data.csv** | **'w'** (ghi mới) | **'a'** (append) |
| **Thứ tự chạy** | **1. Đầu tiên** | **2. Sau** |
| **Số sản phẩm** | ~219 | ~120 |

---

## 📊 CẤU TRÚC DỮ LIỆU

### **RAM:**
```python
ram_info = {
    'ten_ram': 'RAM Kingston Fury Beast 8GB DDR4 3200MHz',
    'loai_ram': 'DDR4',
    'dung_luong': '8GB',
    'thong_so': '8GB 3200MHz',
    'gia_vnd': 490000,
    'link_hinh_anh': 'https://...',
    'category': 'RAM'
}
```

### **CPU:**
```python
cpu_info = {
    'ten_cpu': 'Intel Core i5-12400F',
    'hang': 'Intel',
    'thong_so': 'Intel Core i5-12400F',
    'gia_vnd': 4290000,
    'link_hinh_anh': 'https://...',
    'category': 'CPU'
}
```

---

## 💾 LOGIC LƯU FILE

### **RAM (chạy đầu tiên):**

```python
# File riêng
with open('ram_data.csv', 'w', ...) as f:
    writer.writeheader()
    writer.writerows(ram_data)

# File chung - GHI MỚI (mode='w')
with open('data.csv', 'w', ...) as f:
    writer.writeheader()
    writer.writerows(ram_data)
```

**Kết quả:**
- `data.csv` được **TẠO MỚI** với 219 dòng RAM

---

### **CPU (chạy sau):**

```python
# File riêng
with open('cpu_data.csv', 'w', ...) as f:
    writer.writeheader()
    writer.writerows(cpu_data)

# File chung - APPEND (mode='a')
file_exists = os.path.exists('data.csv')
with open('data.csv', 'a', ...) as f:
    if not file_exists:
        writer.writeheader()  # Ghi header nếu file mới
    writer.writerows(cpu_data)  # Thêm vào cuối
```

**Kết quả:**
- `data.csv` được **THÊM VÀO** 120 dòng CPU
- Tổng: 339 dòng

---

## 🔧 LOGIC CLICK "XEM THÊM" (GIỐNG NHAU)

Cả 2 crawler đều dùng **CÙNG LOGIC:**

```python
while click_count < max_clicks:
    # 1. Đếm sản phẩm hiện tại
    current_count = len(driver.find_elements(..., ".product-item"))
    
    # 2. Tìm nút "Xem thêm"
    button = find_load_more_button()
    
    if not button:
        print("✅ Đã load hết!")
        break
    
    # 3. Lưu URL trước khi click
    original_url = driver.current_url
    
    # 4. Click bằng JavaScript (tránh overlay)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)
    
    # 5. Kiểm tra URL sau khi click
    current_url = driver.current_url
    
    if 'collections' not in current_url:
        # Click nhầm overlay!
        print("⚠️ URL bị đổi! Đang quay lại...")
        driver.back()
        click_count -= 1
        continue  # Thử lại
    
    # 6. Chờ sản phẩm mới load
    time.sleep(3)
    
    # 7. Đếm lại và kiểm tra tăng
    new_count = len(driver.find_elements(..., ".product-item"))
    
    if new_count <= current_count:
        no_change_count += 1
        if no_change_count >= 2:
            break
    else:
        print(f"✅ Tăng thêm {new_count - current_count} sản phẩm")
```

---

## 📈 THỐNG KÊ

### **RAM:**
- URL: `/collections/bo-nho-ram/`
- Số sản phẩm: ~219
- Loại: DDR4, DDR5, DDR3
- Dung lượng: 8GB, 16GB, 32GB, 64GB
- BUS: 3200MHz, 5600MHz, 6000MHz...

### **CPU:**
- URL: `/collections/cpu-bo-vi-xu-ly`
- Số sản phẩm: ~120
- Hãng: Intel, AMD
- Dòng: Core i3/i5/i7/i9, Ryzen 3/5/7/9

---

## 🚀 SCRIPT CHẠY TỰ ĐỘNG

### **Option 1: Chạy lần lượt**
```bash
python crawler_ram.py
python crawler_cpu.py
```

### **Option 2: Tạo script tự động**
```bash
# run_all.bat (Windows)
@echo off
echo ==========================================
echo CRAWLING RAM...
echo ==========================================
python crawler_ram.py

echo.
echo ==========================================
echo CRAWLING CPU...
echo ==========================================
python crawler_cpu.py

echo.
echo ==========================================
echo DONE!
echo ==========================================
pause
```

```bash
# run_all.sh (Linux/Mac)
#!/bin/bash
echo "=========================================="
echo "CRAWLING RAM..."
echo "=========================================="
python crawler_ram.py

echo ""
echo "=========================================="
echo "CRAWLING CPU..."
echo "=========================================="
python crawler_cpu.py

echo ""
echo "=========================================="
echo "DONE!"
echo "=========================================="
```

---

## ✅ CHECKLIST TOÀN BỘ HỆ THỐNG

### **Code:**
- [x] `crawler_ram.py` - JavaScript Click + Kiểm tra URL
- [x] `crawler_cpu.py` - JavaScript Click + Kiểm tra URL
- [x] Cả 2 đều có cột `category`
- [x] RAM: mode='w', CPU: mode='a'

### **Selector:**
- [x] Cả 2 đều dùng `.product-item`
- [x] Cả 2 đều dùng `h3.pdLoopName a`
- [x] Cả 2 đều dùng `p.pdPrice span`

### **Logic:**
- [x] WebDriverWait ≥ 20 sản phẩm
- [x] JavaScript Click (tránh overlay)
- [x] Kiểm tra URL sau click
- [x] Tự động back() nếu sai
- [x] Click liên tục cho đến hết

### **Output:**
- [x] `ram_data.csv` - File riêng RAM
- [x] `cpu_data.csv` - File riêng CPU
- [x] `data.csv` - File chung (RAM + CPU)

---

## 💡 LƯU Ý

1. **Luôn chạy RAM trước, CPU sau**
2. **Không chạy đồng thời** (cùng lúc)
3. **Kiểm tra data.csv** sau mỗi lần chạy
4. **Cột category** giúp phân biệt linh kiện

---

**Version:** RAM 7.0 + CPU 1.0  
**Status:** ✅ Production Ready  
**Date:** 15/02/2026
