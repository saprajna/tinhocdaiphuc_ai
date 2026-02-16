# 📘 HƯỚNG DẪN CRAWLER CASE (THÙNG MÁY)

> **File:** `crawler_case.py`  
> **URL:** https://tinhocngoisao.com/collections/case-thung-may/  
> **Chức năng:** Crawl dữ liệu Case (Thùng máy) tự động từ Tin Học Ngôi Sao

---

## 📋 THÔNG TIN CƠ BẢN

### URL Collection
```
https://tinhocngoisao.com/collections/case-thung-may/
```

### Selectors
- **Container:** `.product-item`
- **Tên:** `h3.pdLoopName a` (text)
- **Giá:** `p.pdPrice span`
- **Ảnh:** `img` (data-src hoặc src)

### Category
```python
'category': 'Case'
```

---

## 💾 FILE LƯU TRỮ

### File riêng
- **Tên file:** `case_data.csv`
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
    """Xác định hãng Case"""
    brands = {
        'NZXT': ['NZXT'],
        'Corsair': ['CORSAIR'],
        'Cooler Master': ['COOLER MASTER', 'COOLERMASTER'],
        'Thermaltake': ['THERMALTAKE'],
        'Fractal Design': ['FRACTAL DESIGN', 'FRACTAL'],
        'Lian Li': ['LIAN LI', 'LIAN-LI'],
        'be quiet!': ['BE QUIET', 'BEQUIET'],
        'Phanteks': ['PHANTEKS'],
        'Antec': ['ANTEC'],
        'Deepcool': ['DEEPCOOL', 'DEEP COOL'],
        'MSI': ['MSI'],
        'ASUS': ['ASUS', 'ROG', 'TUF'],
        'Gigabyte': ['GIGABYTE', 'AORUS'],
        # ... và nhiều hãng khác
    }
```

---

## 🚀 CÁCH CHẠY

### Chạy riêng lẻ
```bash
python crawler_case.py
```

### Chạy trong workflow tổng thể
```bash
# Phải chạy sau crawler_hdd.py (Bước 7 trong chuỗi 8 crawlers)
python crawler_ram.py        # Bước 1
python crawler_cpu.py        # Bước 2
python crawler_mainboard.py  # Bước 3
python crawler_vga.py        # Bước 4
python crawler_ssd.py        # Bước 5
python crawler_hdd.py        # Bước 6
python crawler_case.py       # Bước 7 ← Đây
python crawler_psu.py        # Bước 8
```

### Chạy tự động (Windows)
```bash
run_all_crawlers.bat
```

---

## 📊 DỮ LIỆU ĐẦU RA

### Cấu trúc case_data.csv
```csv
ten_case,hang,thong_so,gia_vnd,link_hinh_anh,category
"NZXT H510 Elite","NZXT","NZXT H510 Elite",2500000,"https://...jpg","Case"
"Corsair 4000D Airflow","Corsair","Corsair 4000D Airflow",2200000,"https://...jpg","Case"
```

### Các cột dữ liệu
| Cột | Mô tả | Ví dụ |
|-----|-------|-------|
| `ten_case` | Tên đầy đủ Case | "NZXT H510 Elite" |
| `hang` | Hãng sản xuất | "NZXT" |
| `thong_so` | Thông số (giống tên) | "NZXT H510 Elite" |
| `gia_vnd` | Giá VNĐ (số nguyên) | 2500000 |
| `link_hinh_anh` | URL ảnh | "https://..." |
| `category` | Danh mục | "Case" |

---

## 🐛 DEBUG FILES

### Screenshots tự động
1. **debug_case_initial_load.png** - Sau khi load trang đầu tiên
2. **debug_case_after_load_all.png** - Sau khi click hết nút "Xem thêm"
3. **debug_case_wait_timeout_XXXXX.png** - Nếu timeout khi chờ 20 sản phẩm

### Khi nào cần xem?
- Số lượng sản phẩm < 20
- Crawler không tìm thấy nút "Xem thêm"
- Bị redirect sang trang khác

---

## 📋 SẢN PHẨM MẪU

```python
{
    'ten_case': 'NZXT H510 Elite Mid Tower - Tempered Glass',
    'hang': 'NZXT',
    'thong_so': 'NZXT H510 Elite Mid Tower - Tempered Glass',
    'gia_vnd': 2500000,
    'link_hinh_anh': 'https://product.hstatic.net/200000722513/product/...',
    'category': 'Case'
}
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

### Thứ tự chạy
- ✅ **PHẢI chạy sau:** `crawler_hdd.py` (Bước 6)
- ✅ **Chạy trước:** `crawler_psu.py` (Bước 8)
- ❌ **KHÔNG chạy đầu tiên:** Vì cần append vào `data.csv` đã có sẵn

### Brand Detection
- Ưu tiên tên hãng đầy đủ: "Cooler Master" thay vì "CM"
- Case có sub-brand như ASUS ROG, TUF sẽ trả về "ASUS"
- Nếu không detect được → `'Unknown'`

### Error Handling
- Bỏ qua sản phẩm thiếu tên hoặc giá
- Chỉ in 5 lỗi đầu tiên để tránh spam
- Lỗi không làm dừng crawler

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
