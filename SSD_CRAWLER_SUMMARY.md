# 💽 CRAWLER SSD - TÓM TẮT NHANH

## 📅 Ngày: 15/02/2026

---

## ⚡ THÔNG TIN NHANH

| Thông tin | Chi tiết |
|-----------|----------|
| **File** | `crawler_ssd.py` |
| **URL** | https://tinhocngoisao.com/collections/o-cung-ssd |
| **Selector** | `.product-item` |
| **Category** | `'SSD'` |
| **Số sản phẩm** | ~165 |
| **File riêng** | `ssd_data.csv` |
| **File chung** | `data.csv` (append - mode='a') |
| **Thông báo** | "Đã thêm X SSD vào kho dữ liệu chung" |

---

## 🚀 CHẠY NGAY

```bash
python crawler_ssd.py
```

**Lưu ý:** Phải chạy SAU `crawler_ram.py`, `crawler_cpu.py`, `crawler_mainboard.py` và `crawler_vga.py`

---

## ✅ ĐẶC ĐIỂM

1. ✅ **JavaScript Click** - Tránh overlay
2. ✅ **Kiểm tra URL** - Tự động fix
3. ✅ **WebDriverWait** - ≥ 20 sản phẩm
4. ✅ **Auto-detect Brand** - Samsung/Kingston/WD/Crucial...
5. ✅ **Mode='a'** - Append vào data.csv
6. ✅ **Category='SSD'** - Phân biệt loại linh kiện

---

## 📊 DỮ LIỆU

### **Hãng hỗ trợ (25+ brands):**
- Samsung (phổ biến nhất)
- Kingston
- WD (Western Digital: WD Black, Blue, Green)
- Crucial
- Seagate
- SanDisk
- Intel
- Corsair
- ADATA
- Gigabyte, MSI
- PNY, Lexar, Team
- Transcend, Patriot
- SK Hynix, Silicon Power
- Và nhiều hãng khác...

### **Output:**
```csv
ten_ssd,hang,thong_so,gia_vnd,link_hinh_anh,category
"SSD Samsung 980 PRO 1TB M.2 PCIe Gen 4.0 x4 NVMe",Samsung,"SSD Samsung 980 PRO 1TB M.2 PCIe Gen 4.0 x4 NVMe",3290000,https://...,SSD
"Kingston NV2 500GB M.2 2280 NVMe PCIe 4.0",Kingston,"Kingston NV2 500GB M.2 2280 NVMe PCIe 4.0",990000,https://...,SSD
"WD Black SN850X 2TB M.2 PCIe Gen 4.0",WD,"WD Black SN850X 2TB M.2 PCIe Gen 4.0",5490000,https://...,SSD
```

---

## 🔄 WORKFLOW

```
1. RAM       → mode='w' (tạo mới data.csv)
2. CPU       → mode='a' (append)
3. MAINBOARD → mode='a' (append)
4. VGA       → mode='a' (append)
5. SSD       → mode='a' (append)  ← Crawler này
```

---

## 📁 FILES

- ✅ `crawler_ssd.py` - Crawler chính
- ✅ `ssd_data.csv` - File riêng
- ✅ `data.csv` - File chung (append)
- ✅ `HUONG_DAN_SSD_CRAWLER.md` - Hướng dẫn đầy đủ
- ✅ `SSD_CRAWLER_SUMMARY.md` - File này

---

## ⏱️ THỜI GIAN

**~70-90 giây**

---

## 🎉 KẾT QUẢ

```
🎉 Đã thêm 165 SSD vào kho dữ liệu chung
📄 File riêng: ssd_data.csv (165 dòng)
📄 File chung: data.csv (đã thêm 165 dòng)
```

---

**Version:** 1.0  
**Status:** ✅ Ready  
**Date:** 15/02/2026
