# ⚡ PSU CRAWLER - TÓM TẮT NHANH

## 🔍 THÔNG TIN CƠ BẢN

| Thuộc tính | Giá trị |
|------------|---------|
| **File** | `crawler_psu.py` |
| **URL** | https://tinhocngoisao.com/collections/psu-nguon-may-tinh/ |
| **Category** | `PSU` |
| **Số lượng** | ~80 sản phẩm |
| **File riêng** | `psu_data.csv` (mode='w') |
| **File chung** | `data.csv` (mode='a', append) |
| **Thứ tự** | Bước 8/8 (CUỐI CÙNG) |

---

## ⚡ HIGHLIGHTS

### ✅ Tính năng chính
- ✅ **JS Click:** Dùng `driver.execute_script("arguments[0].click();", btn)` tránh overlay
- ✅ **URL Check:** Kiểm tra `driver.current_url` sau mỗi click, auto `back()` nếu sai
- ✅ **WebDriverWait:** Chờ ít nhất 20 `.product-item` xuất hiện (tránh "Gợi ý")
- ✅ **Auto Brand Detection:** Tự động detect 20+ hãng PSU (Corsair, Seasonic, EVGA, FSP, Super Flower...)

### 📊 Cấu trúc dữ liệu
```python
{
    'ten_psu': 'Corsair RM850x 850W 80 Plus Gold Modular',
    'hang': 'Corsair',
    'thong_so': 'Corsair RM850x 850W 80 Plus Gold Modular',
    'gia_vnd': 3500000,
    'link_hinh_anh': 'https://...',
    'category': 'PSU'
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
7. CASE   ──→ data.csv (append)
8. PSU    ──→ data.csv (append) ← ĐÂY (CUỐI CÙNG)
```

---

## 🚀 CHẠY NHANH

```bash
# Chạy riêng
python crawler_psu.py

# Chạy tự động (tất cả 8 crawlers)
run_all_crawlers.bat
```

---

## 🎯 HOÀN THÀNH HỆ THỐNG

Sau khi chạy xong `crawler_psu.py`:
- ✅ **8/8 crawlers hoàn thành**
- ✅ **data.csv có đầy đủ ~904 sản phẩm**
- ✅ **Sẵn sàng cho dự án AI Build PC**

---

## 🔗 TÀI LIỆU CHI TIẾT

- [HUONG_DAN_PSU_CRAWLER.md](HUONG_DAN_PSU_CRAWLER.md) - Hướng dẫn đầy đủ
- [README_CRAWLERS.md](README_CRAWLERS.md) - Tổng quan hệ thống

---

**Tác giả:** Cursor AI Agent  
**Ngày:** 15/02/2026
