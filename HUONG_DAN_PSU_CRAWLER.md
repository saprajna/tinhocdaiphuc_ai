# 📘 HƯỚNG DẪN CRAWLER PSU (NGUỒN MÁY TÍNH)

> **File:** `crawler_psu.py`  
> **URL:** https://tinhocngoisao.com/collections/psu-nguon-may-tinh/  
> **Chức năng:** Crawl dữ liệu PSU (Nguồn máy tính) tự động từ Tin Học Ngôi Sao

---

## 📋 THÔNG TIN CƠ BẢN

### URL Collection
```
https://tinhocngoisao.com/collections/psu-nguon-may-tinh/
```

### Selectors
- **Container:** `.product-item`
- **Tên:** `h3.pdLoopName a` (text)
- **Giá:** `p.pdPrice span`
- **Ảnh:** `img` (data-src hoặc src)

### Category
```python
'category': 'PSU'
```

---

## 💾 FILE LƯU TRỮ

### File riêng
- **Tên file:** `psu_data.csv`
- **Chế độ:** `mode='w'` (Ghi đè, tạo mới)
- **Encoding:** `utf-8-sig`

### File chung
- **Tên file:** `data.csv`
- **Chế độ:** `mode='a'` (Append, nối tiếp)
- **Lưu ý:** Không ghi header nếu file đã tồn tại

---

## 🔧 TÍNH NĂNG ĐẶC BIỆT

### 1. JavaScript Click
```python
driver.execute_script("arguments[0].click();", load_more_button)
```
- Tránh click nhầm overlay "Tra cứu bảo hành"
- Click trực tiếp vào element mục tiêu

### 2. URL Validation
```python
if 'collections' not in current_url:
    driver.back()
    click_count -= 1
    continue
```
- Kiểm tra URL sau mỗi click
- Tự động back nếu bị chuyển trang

### 3. WebDriverWait
```python
WebDriverWait(driver, 20).until(
    lambda driver: len(driver.find_elements(By.CSS_SELECTOR, ".product-item")) >= 20
)
```
- Chờ ít nhất 20 sản phẩm xuất hiện
- Tránh bắt nhầm mục "Gợi ý"

### 4. Auto-detect Brand
```python
def extract_brand(self, name: str) -> str:
    """Xác định hãng PSU"""
    brands = {
        'Corsair': ['CORSAIR'],
        'Cooler Master': ['COOLER MASTER', 'COOLERMASTER'],
        'EVGA': ['EVGA'],
        'Seasonic': ['SEASONIC'],
        'Thermaltake': ['THERMALTAKE'],
        'be quiet!': ['BE QUIET', 'BEQUIET'],
        'NZXT': ['NZXT'],
        'Antec': ['ANTEC'],
        'FSP': ['FSP', 'FORTRON'],
        'SilverStone': ['SILVERSTONE'],
        'Deepcool': ['DEEPCOOL', 'DEEP COOL'],
        'Super Flower': ['SUPER FLOWER', 'SUPERFLOWER'],
        'Cougar': ['COUGAR'],
        # ... và nhiều hãng khác
    }
```

---

## 🚀 CÁCH CHẠY

### Chạy riêng lẻ
```bash
python crawler_psu.py
```

### Chạy trong workflow tổng thể
```bash
# Phải chạy sau crawler_case.py (Bước 8 - cuối cùng trong chuỗi 8 crawlers)
python crawler_ram.py        # Bước 1
python crawler_cpu.py        # Bước 2
python crawler_mainboard.py  # Bước 3
python crawler_vga.py        # Bước 4
python crawler_ssd.py        # Bước 5
python crawler_hdd.py        # Bước 6
python crawler_case.py       # Bước 7
python crawler_psu.py        # Bước 8 ← Đây (CUỐI CÙNG)
```

### Chạy tự động (Windows)
```bash
run_all_crawlers.bat
```

---

## 📊 DỮ LIỆU ĐẦU RA

### Cấu trúc psu_data.csv
```csv
ten_psu,hang,thong_so,gia_vnd,link_hinh_anh,category
"Corsair RM850x 850W 80 Plus Gold","Corsair","Corsair RM850x 850W 80 Plus Gold",3500000,"https://...jpg","PSU"
"Seasonic Focus GX-750 750W","Seasonic","Seasonic Focus GX-750 750W",2800000,"https://...jpg","PSU"
```

### Các cột dữ liệu
| Cột | Mô tả | Ví dụ |
|-----|-------|-------|
| `ten_psu` | Tên đầy đủ PSU | "Corsair RM850x 850W" |
| `hang` | Hãng sản xuất | "Corsair" |
| `thong_so` | Thông số (giống tên) | "Corsair RM850x 850W 80 Plus Gold" |
| `gia_vnd` | Giá VNĐ (số nguyên) | 3500000 |
| `link_hinh_anh` | URL ảnh | "https://..." |
| `category` | Danh mục | "PSU" |

---

## 🐛 DEBUG FILES

### Screenshots tự động
1. **debug_psu_initial_load.png** - Sau khi load trang đầu tiên
2. **debug_psu_after_load_all.png** - Sau khi click hết nút "Xem thêm"
3. **debug_psu_wait_timeout_XXXXX.png** - Nếu timeout khi chờ 20 sản phẩm

### Khi nào cần xem?
- Số lượng sản phẩm < 20
- Crawler không tìm thấy nút "Xem thêm"
- Bị redirect sang trang khác

---

## 📋 SẢN PHẨM MẪU

```python
{
    'ten_psu': 'Corsair RM850x 850W 80 Plus Gold Modular',
    'hang': 'Corsair',
    'thong_so': 'Corsair RM850x 850W 80 Plus Gold Modular',
    'gia_vnd': 3500000,
    'link_hinh_anh': 'https://product.hstatic.net/200000722513/product/...',
    'category': 'PSU'
}
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

### Thứ tự chạy
- ✅ **PHẢI chạy sau:** `crawler_case.py` (Bước 7)
- ✅ **Crawler cuối cùng:** Bước 8 trong workflow 8 crawlers
- ❌ **KHÔNG chạy đầu tiên:** Vì cần append vào `data.csv` đã có sẵn

### Brand Detection
- Ưu tiên tên hãng đầy đủ: "Cooler Master" thay vì "CM"
- PSU có sub-brand như MWE, MasterWatt sẽ trả về "Cooler Master"
- FSP có thể được gọi là "Fortron" trong một số tên sản phẩm
- Nếu không detect được → `'Unknown'`

### Power Rating Detection
- Công suất PSU thường có trong tên: "850W", "750W", "650W"
- Certification: "80 Plus Gold", "80 Plus Bronze", "80 Plus Platinum"
- Modular/Semi-modular/Non-modular cũng có trong tên

### Error Handling
- Bỏ qua sản phẩm thiếu tên hoặc giá
- Chỉ in 5 lỗi đầu tiên để tránh spam
- Lỗi không làm dừng crawler

---

## 🎯 HOÀN THÀNH WORKFLOW

Sau khi chạy xong `crawler_psu.py`:
- ✅ Đã có 8/8 crawler hoàn thành
- ✅ File `data.csv` chứa đầy đủ ~904 sản phẩm
- ✅ Đủ dữ liệu cho dự án AI Build PC

### Các file CSV được tạo
1. `ram_data.csv` (~219 dòng)
2. `cpu_data.csv` (~120 dòng)
3. `mainboard_data.csv` (~180 dòng)
4. `vga_data.csv` (~146 dòng)
5. `ssd_data.csv` (~69 dòng)
6. `hdd_data.csv` (~40 dòng)
7. `case_data.csv` (~50 dòng)
8. `psu_data.csv` (~80 dòng)
9. **`data.csv`** (~904 dòng - FILE TỔNG HỢP)

---

## 📞 HỖ TRỢ

### Xem thêm
- [README_CRAWLERS.md](README_CRAWLERS.md) - Tổng quan hệ thống
- [WORKFLOW_FINAL.md](WORKFLOW_FINAL.md) - Workflow chi tiết
- [SO_SANH_6_CRAWLERS_FULL.md](SO_SANH_6_CRAWLERS_FULL.md) - So sánh các crawler

### Liên hệ
- GitHub Issues
- Email support

---

**Version:** 1.0  
**Ngày:** 15/02/2026  
**Tác giả:** Cursor AI Agent
