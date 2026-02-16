# 💿 CRAWLER HDD - TÓM TẮT NHANH

## 📅 Ngày: 15/02/2026

---

## ⚡ THÔNG TIN NHANH

| Thông tin | Chi tiết |
|-----------|----------|
| **File** | `crawler_hdd.py` |
| **URL** | https://tinhocngoisao.com/collections/o-cung-hdd/ |
| **Selector** | `.product-item` |
| **Category** | `'HDD'` |
| **Số sản phẩm** | ~40 |
| **File riêng** | `hdd_data.csv` |
| **File chung** | `data.csv` (append - mode='a') |
| **Thông báo** | "Đã thêm X HDD vào kho dữ liệu chung" |

---

## 🚀 CHẠY NGAY

```bash
python crawler_hdd.py
```

**Lưu ý:** Phải chạy SAU tất cả các crawler khác (RAM, CPU, Mainboard, VGA, SSD)

---

## ✅ ĐẶC ĐIỂM

1. ✅ **JavaScript Click** - Tránh overlay
2. ✅ **Kiểm tra URL** - Tự động fix
3. ✅ **WebDriverWait** - ≥ 20 sản phẩm
4. ✅ **Auto-detect Brand** - Seagate/WD/Toshiba/Hitachi...
5. ✅ **Mode='a'** - Append vào data.csv
6. ✅ **Category='HDD'** - Phân biệt loại linh kiện

---

## 📊 DỮ LIỆU

### **Hãng hỗ trợ:**
- **Seagate** (Barracuda, IronWolf, SkyHawk)
- **WD** - Western Digital (WD Black, Blue, Red, Purple, Gold)
- **Toshiba**
- **Hitachi** (HGST)
- **Samsung**
- **Maxtor**
- **Transcend**
- **ADATA**
- **HP**
- **Acer**

### **Output:**
```csv
ten_hdd,hang,thong_so,gia_vnd,link_hinh_anh,category
"Seagate Barracuda 2TB 3.5'' SATA 3 7200RPM",Seagate,"Seagate Barracuda 2TB 3.5'' SATA 3 7200RPM",1490000,https://...,HDD
"WD Blue 1TB 3.5'' SATA 3 7200RPM",WD,"WD Blue 1TB 3.5'' SATA 3 7200RPM",990000,https://...,HDD
"Toshiba 4TB 3.5'' SATA 3 5400RPM",Toshiba,"Toshiba 4TB 3.5'' SATA 3 5400RPM",2490000,https://...,HDD
```

---

## 🔄 WORKFLOW

```
1. RAM       → mode='w' (tạo mới data.csv)
2. CPU       → mode='a' (append)
3. MAINBOARD → mode='a' (append)
4. VGA       → mode='a' (append)
5. SSD       → mode='a' (append)
6. HDD       → mode='a' (append)  ← Crawler này
```

---

## 📁 FILES

- ✅ `crawler_hdd.py` - Crawler chính
- ✅ `hdd_data.csv` - File riêng
- ✅ `data.csv` - File chung (append)
- ✅ `HUONG_DAN_HDD_CRAWLER.md` - Hướng dẫn đầy đủ
- ✅ `HDD_CRAWLER_SUMMARY.md` - File này

---

## ⏱️ THỜI GIAN

**~30-40 giây**

---

## 🎉 KẾT QUẢ

```
🎉 Đã thêm 40 HDD vào kho dữ liệu chung
📄 File riêng: hdd_data.csv (40 dòng)
📄 File chung: data.csv (đã thêm 40 dòng)
```

---

**Version:** 1.0  
**Status:** ✅ Ready  
**Date:** 15/02/2026
