# 📦 CASE CRAWLER - TÓM TẮT NHANH

## 🔍 THÔNG TIN CƠ BẢN

| Thuộc tính | Giá trị |
|------------|---------|
| **File** | `crawler_case.py` |
| **URL** | https://tinhocngoisao.com/collections/case-thung-may/ |
| **Category** | `Case` |
| **Số lượng** | ~50 sản phẩm |
| **File riêng** | `case_data.csv` (mode='w') |
| **File chung** | `data.csv` (mode='a', append) |
| **Thứ tự** | Bước 7/8 |

---

## ⚡ HIGHLIGHTS

### ✅ Tính năng chính
- ✅ **JS Click:** Dùng `driver.execute_script("arguments[0].click();", btn)` tránh overlay
- ✅ **URL Check:** Kiểm tra `driver.current_url` sau mỗi click, auto `back()` nếu sai
- ✅ **WebDriverWait:** Chờ ít nhất 20 `.product-item` xuất hiện (tránh "Gợi ý")
- ✅ **Auto Brand Detection:** Tự động detect 20+ hãng Case (NZXT, Corsair, Cooler Master, Lian Li...)

### 📊 Cấu trúc dữ liệu
```python
{
    'ten_case': 'NZXT H510 Elite Mid Tower - Tempered Glass',
    'hang': 'NZXT',
    'thong_so': 'NZXT H510 Elite Mid Tower - Tempered Glass',
    'gia_vnd': 2500000,
    'link_hinh_anh': 'https://...',
    'category': 'Case'
}
```

---

## 🔄 WORKFLOW

```
1. RAM    ──→ data.csv (tạo mới, mode='w')
2. CPU    ──→ data.csv (append)
3. Mainboard ──→ data.csv (append)
4. VGA    ──→ data.csv (append)
5. SSD    ──→ data.csv (append)
6. HDD    ──→ data.csv (append)
7. CASE   ──→ data.csv (append) ← ĐÂY
8. PSU    ──→ data.csv (append)
```

---

## 🚀 CHẠY NHANH

```bash
# Chạy riêng
python crawler_case.py

# Chạy tự động (tất cả 8 crawlers)
run_all_crawlers.bat
```

---

## 🔗 TÀI LIỆU CHI TIẾT

- [HUONG_DAN_CASE_CRAWLER.md](HUONG_DAN_CASE_CRAWLER.md) - Hướng dẫn đầy đủ
- [README_CRAWLERS.md](README_CRAWLERS.md) - Tổng quan hệ thống

---

**Tác giả:** Cursor AI Agent  
**Ngày:** 15/02/2026
