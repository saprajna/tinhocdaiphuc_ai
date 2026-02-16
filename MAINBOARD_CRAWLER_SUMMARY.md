# 🛡️ CRAWLER MAINBOARD - TÓM TẮT NHANH

## 📅 Ngày: 15/02/2026

---

## ⚡ THÔNG TIN NHANH

| Thông tin | Chi tiết |
|-----------|----------|
| **File** | `crawler_mainboard.py` |
| **URL** | https://tinhocngoisao.com/collections/bo-mach-chu |
| **Selector** | `.product-item` |
| **Category** | `'Mainboard'` |
| **Số sản phẩm** | ~118 |
| **File riêng** | `mainboard_data.csv` |
| **File chung** | `data.csv` (append - mode='a') |
| **Thông báo** | "Đã thêm X Mainboard vào kho dữ liệu chung" |

---

## 🚀 CHẠY NGAY

```bash
python crawler_mainboard.py
```

**Lưu ý:** Phải chạy SAU `crawler_ram.py` và `crawler_cpu.py`

---

## ✅ ĐẶC ĐIỂM

1. ✅ **JavaScript Click** - Tránh overlay
2. ✅ **Kiểm tra URL** - Tự động fix
3. ✅ **WebDriverWait** - ≥ 20 sản phẩm
4. ✅ **Auto-detect Brand** - ASUS/MSI/Gigabyte/ASRock...
5. ✅ **Mode='a'** - Append vào data.csv
6. ✅ **Category='Mainboard'** - Phân biệt loại linh kiện

---

## 📊 DỮ LIỆU

### **Hãng hỗ trợ:**
- ASUS (ROG, TUF, Prime)
- MSI
- Gigabyte (Aorus)
- ASRock
- Biostar
- EVGA
- NZXT

### **Output:**
```csv
ten_mainboard,hang,thong_so,gia_vnd,link_hinh_anh,category
"ASUS TUF GAMING B550M-PLUS",ASUS,"ASUS TUF GAMING B550M-PLUS",2790000,https://...,Mainboard
```

---

## 🔄 WORKFLOW

```
1. RAM      → mode='w' (tạo mới data.csv)
2. CPU      → mode='a' (append)
3. MAINBOARD → mode='a' (append)  ← Crawler này
```

---

## 📁 FILES

- ✅ `crawler_mainboard.py` - Crawler chính
- ✅ `mainboard_data.csv` - File riêng
- ✅ `data.csv` - File chung (append)
- ✅ `HUONG_DAN_MAINBOARD_CRAWLER.md` - Hướng dẫn đầy đủ
- ✅ `MAINBOARD_CRAWLER_SUMMARY.md` - File này

---

## ⏱️ THỜI GIAN

**~50-70 giây**

---

## 🎉 KẾT QUẢ

```
🎉 Đã thêm 118 Mainboard vào kho dữ liệu chung
📄 File riêng: mainboard_data.csv (118 dòng)
📄 File chung: data.csv (đã thêm 118 dòng)
```

---

**Version:** 1.0  
**Status:** ✅ Ready  
**Date:** 15/02/2026
