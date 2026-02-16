# 🎮 CRAWLER VGA - TÓM TẮT NHANH

## 📅 Ngày: 15/02/2026

---

## ⚡ THÔNG TIN NHANH

| Thông tin | Chi tiết |
|-----------|----------|
| **File** | `crawler_vga.py` |
| **URL** | https://tinhocngoisao.com/collections/card-man-hinh |
| **Selector** | `.product-item` |
| **Category** | `'VGA'` |
| **Số sản phẩm** | ~142 |
| **File riêng** | `vga_data.csv` |
| **File chung** | `data.csv` (append - mode='a') |
| **Thông báo** | "Đã thêm X VGA vào kho dữ liệu chung" |

---

## 🚀 CHẠY NGAY

```bash
python crawler_vga.py
```

**Lưu ý:** Phải chạy SAU `crawler_ram.py`, `crawler_cpu.py` và `crawler_mainboard.py`

---

## ✅ ĐẶC ĐIỂM

1. ✅ **JavaScript Click** - Tránh overlay
2. ✅ **Kiểm tra URL** - Tự động fix
3. ✅ **WebDriverWait** - ≥ 20 sản phẩm
4. ✅ **Smart Brand Detection** - Chipset > Manufacturer
5. ✅ **Mode='a'** - Append vào data.csv
6. ✅ **Category='VGA'** - Phân biệt loại linh kiện

---

## 🎯 SMART BRAND DETECTION

### **Ưu tiên Chipset (quan trọng nhất):**
- NVIDIA: GeForce, RTX, GTX
- AMD: Radeon, RX
- Intel: Arc

### **Fallback Manufacturer:**
- ASUS, MSI, Gigabyte, EVGA, Zotac, Palit, Galax, Sapphire, PowerColor, XFX, ASRock

**Ví dụ:**
```
"ASUS ROG Strix GeForce RTX 4070 Ti" → NVIDIA ✅
"Gigabyte Radeon RX 7800 XT Gaming OC" → AMD ✅
"MSI GeForce GTX 1660 Super" → NVIDIA ✅
```

---

## 📊 DỮ LIỆU

### **Output:**
```csv
ten_vga,hang,thong_so,gia_vnd,link_hinh_anh,category
"ASUS ROG Strix GeForce RTX 4070 Ti",NVIDIA,"ASUS ROG Strix GeForce RTX 4070 Ti",21990000,https://...,VGA
"MSI GeForce RTX 4060 Ti Gaming X 8GB",NVIDIA,"MSI GeForce RTX 4060 Ti Gaming X 8GB",12490000,https://...,VGA
"Gigabyte Radeon RX 7800 XT Gaming OC",AMD,"Gigabyte Radeon RX 7800 XT Gaming OC",14990000,https://...,VGA
```

---

## 🔄 WORKFLOW

```
1. RAM       → mode='w' (tạo mới data.csv)
2. CPU       → mode='a' (append)
3. MAINBOARD → mode='a' (append)
4. VGA       → mode='a' (append)  ← Crawler này
```

---

## 📁 FILES

- ✅ `crawler_vga.py` - Crawler chính
- ✅ `vga_data.csv` - File riêng
- ✅ `data.csv` - File chung (append)
- ✅ `HUONG_DAN_VGA_CRAWLER.md` - Hướng dẫn đầy đủ
- ✅ `VGA_CRAWLER_SUMMARY.md` - File này

---

## ⏱️ THỜI GIAN

**~60-80 giây**

---

## 🎉 KẾT QUẢ

```
🎉 Đã thêm 142 VGA vào kho dữ liệu chung
📄 File riêng: vga_data.csv (142 dòng)
📄 File chung: data.csv (đã thêm 142 dòng)
```

---

**Version:** 1.0  
**Status:** ✅ Ready  
**Date:** 15/02/2026
