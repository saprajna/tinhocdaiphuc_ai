# Hướng Dẫn Sử Dụng Crawler RAM

## 📋 Mô tả
Script `crawler_ram.py` được thiết kế để crawl dữ liệu RAM từ website Tin Học Ngôi Sao và tự động cập nhật vào file `data.csv` của dự án AI build PC.

## 🛠️ Cài đặt

### 1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 2. Đảm bảo Google Chrome đã được cài đặt trên máy

## 🚀 Cách sử dụng

### Chạy crawler:
```bash
python crawler_ram.py
```

## 📊 Kết quả

Sau khi chạy xong, bạn sẽ có:

1. **ram_data.csv** - File chứa TẤT CẢ dữ liệu RAM được crawl từ website:
   - `ten_ram`: Tên đầy đủ của RAM
   - `loai_ram`: Loại RAM (DDR4, DDR5, DDR3)
   - `dung_luong`: Dung lượng (8GB, 16GB, 32GB, 64GB)
   - `gia_vnd`: Giá bán (VNĐ)
   - `link_hinh_anh`: Link hình ảnh sản phẩm

2. **data.csv được cập nhật** - File chính của dự án sẽ được cập nhật với:
   - RAM có **GIÁ TỐT NHẤT** cho mỗi loại (DDR4/DDR5)
   - RAM có **GIÁ TỐT NHẤT** cho mỗi dung lượng (8GB, 16GB, 32GB, 64GB)
   - Các RAM cũ sẽ bị XÓA và thay thế bằng dữ liệu mới

## 🔧 Tính năng

### ✅ Vượt tường lửa
- Sử dụng `undetected-chromedriver` để tránh bị phát hiện là bot
- Tự động scroll để load tất cả sản phẩm

### ✅ Trích xuất thông tin thông minh
- Tự động phân loại DDR4/DDR5 từ tên sản phẩm
- Tự động trích xuất dung lượng (8GB, 16GB, 32GB, 64GB)
- Làm sạch giá và chuyển đổi sang số nguyên

### ✅ Lọc giá tốt nhất
- So sánh giá tất cả sản phẩm
- Chọn giá thấp nhất cho mỗi loại và dung lượng
- Hiển thị báo cáo giá tốt nhất

### ✅ Tự động cập nhật data.csv
- Xóa dữ liệu RAM cũ
- Thêm dữ liệu RAM mới với giá tốt nhất
- Giữ nguyên các linh kiện khác (CPU, VGA, Main, v.v.)

## 📝 Ví dụ Output

```
🚀 BẮT ĐẦU CRAWL DỮ LIỆU RAM TỪ TIN HỌC NGÔI SAO
============================================================
Đang khởi tạo Chrome driver...
Chrome driver đã sẵn sàng!
Đang truy cập: https://tinhocngoisao.com/collections/ram-bo-nho-trong
Đang scroll để load tất cả sản phẩm...
Đã load xong tất cả sản phẩm!
Đã tìm thấy 85 sản phẩm!

1. RAM Kingston Fury Beast 8GB DDR4 3200 - 490,000 VNĐ - DDR4 - 8GB
2. RAM Kingston Fury Beast 16GB DDR4 3200 - 890,000 VNĐ - DDR4 - 16GB
...

✅ Đã crawl thành công 85 sản phẩm RAM!

🔍 Đang phân tích giá tốt nhất...

📊 DDR4 - Giá tốt nhất theo dung lượng:
  • 8GB: RAM G.Skill Aegis 8GB DDR4 3200 - 480,000 VNĐ
  • 16GB: RAM G.Skill Aegis 16GB DDR4 3200 - 880,000 VNĐ
  • 32GB: RAM Kingston Fury Beast 32GB DDR4 3200 - 1,690,000 VNĐ

📊 DDR5 - Giá tốt nhất theo dung lượng:
  • 16GB: RAM ADATA XPG 16GB DDR5 5200 - 1,190,000 VNĐ
  • 32GB: RAM ADATA XPG 32GB DDR5 5200 - 2,390,000 VNĐ

🔄 Đang cập nhật data.csv...
✅ Đã cập nhật 5 sản phẩm RAM vào data.csv!

============================================================
🎉 HOÀN THÀNH!
============================================================
```

## ⚠️ Lưu ý

1. **Kết nối Internet**: Cần kết nối internet ổn định
2. **Google Chrome**: Phải cài đặt Chrome browser
3. **Thời gian chạy**: Có thể mất 30-60 giây tùy số lượng sản phẩm
4. **Backup**: Nên backup file `data.csv` trước khi chạy

## 🐛 Xử lý lỗi

Nếu gặp lỗi:
- Kiểm tra kết nối internet
- Đảm bảo Chrome đã cài đặt
- Thử chạy lại script
- Kiểm tra xem website có thay đổi cấu trúc không

## 📞 Hỗ trợ

Nếu có vấn đề, hãy kiểm tra:
1. Phiên bản Chrome và chromedriver có tương thích
2. Website có còn hoạt động bình thường
3. Cấu trúc HTML của website có thay đổi
