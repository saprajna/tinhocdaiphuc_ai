# 🎯 TÓM TẮT: CPU CRAWLER

## ✅ Đã hoàn thành

Tạo file `crawler_cpu.py` dựa trên `crawler_ram.py`

---

## 📋 Thông tin chính

| Thông số | Giá trị |
|----------|---------|
| **File** | `crawler_cpu.py` |
| **URL** | https://tinhocngoisao.com/collections/cpu-bo-vi-xu-ly |
| **Selector** | `.product-item` (giống RAM) |
| **Cơ chế** | Click "Xem thêm" (giống RAM) |
| **Category** | `CPU` |

---

## 📊 Cấu trúc CSV

### **File riêng: `cpu_data.csv`**
```csv
ten_cpu,hang,thong_so,gia_vnd,link_hinh_anh,category
```

**Các cột:**
1. `ten_cpu` - Tên đầy đủ
2. `hang` - Intel hoặc AMD
3. `thong_so` - Thông số (giữ nguyên tên)
4. `gia_vnd` - Giá (số nguyên)
5. `link_hinh_anh` - URL ảnh
6. `category` - **CPU** ← Mới!

---

## 💾 Logic lưu file

### **Bước 1: File riêng**
```python
# Mode 'w' - Ghi đè
with open('cpu_data.csv', 'w', ...) as f:
    writer.writeheader()
    writer.writerows(cpu_data)
```

### **Bước 2: Append vào data.csv**
```python
# Mode 'a' - Chèn nối tiếp
with open('data.csv', 'a', ...) as f:
    # Header chỉ ghi nếu file chưa tồn tại
    if not file_exists:
        writer.writeheader()
    writer.writerows(cpu_data)
```

---

## ⚡ Điểm khác biệt với RAM

| Tính năng | RAM | CPU |
|-----------|-----|-----|
| Class | `RAMCrawler` | `CPUCrawler` |
| URL | `/bo-nho-ram/` | `/cpu-bo-vi-xu-ly` |
| Field | `ten_ram` | `ten_cpu` |
| Hãng | `loai_ram` (DDR4/DDR5) | `hang` (Intel/AMD) |
| Category | `RAM` | `CPU` ✅ |
| File riêng | `ram_data.csv` | `cpu_data.csv` |
| Append data.csv | ❌ Không | ✅ **Có** |

---

## 🚀 Cách chạy

```bash
python crawler_cpu.py
```

**Kết quả:**
- ✅ `cpu_data.csv` - File riêng (~120 CPU)
- ✅ `data.csv` - Đã thêm CPU vào cuối

---

## 📝 Thông báo debug

```
🎉 Đã lưu file riêng CPU và cập nhật vào kho data.csv thành công
```

---

## 📁 Files đã tạo

1. ✅ **`crawler_cpu.py`** - Script chính
2. ✅ **`HUONG_DAN_CPU_CRAWLER.md`** - Hướng dẫn chi tiết
3. ✅ **`CPU_CRAWLER_SUMMARY.md`** - File này

---

## 🔄 Workflow đầy đủ

```bash
# 1. Crawl RAM
python crawler_ram.py
# → ram_data.csv (219 sản phẩm)

# 2. Crawl CPU
python crawler_cpu.py
# → cpu_data.csv (120 sản phẩm)
# → data.csv (219 + 120 = 339 sản phẩm)
```

---

## ✅ Checklist

- [x] Giữ nguyên selector `.product-item`
- [x] Giữ nguyên cơ chế "Xem thêm"
- [x] Thêm cột `category: 'CPU'`
- [x] Lưu file riêng `cpu_data.csv` (mode 'w')
- [x] Append vào `data.csv` (mode 'a')
- [x] Header chỉ ghi nếu file chưa tồn tại
- [x] Thông báo debug đầy đủ

---

**Status:** ✅ Ready to use  
**Version:** 1.0  
**Date:** 15/02/2026
