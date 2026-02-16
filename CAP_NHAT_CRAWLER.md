# 🔄 Cập Nhật Crawler RAM - Phiên Bản Mới

## ✨ Thay đổi chính

### ❌ Đã loại bỏ:
- `undetected-chromedriver` (gây lỗi WinError 6)

### ✅ Đã thêm:
- **Selenium tiêu chuẩn** với `webdriver.Chrome()`
- **webdriver-manager**: Tự động tải và cập nhật ChromeDriver
- **User-Agent giả lập**: Giả lập trình duyệt Chrome 120 thật
- **Chống phát hiện bot**: Xóa thuộc tính `navigator.webdriver`

## 🚀 Cách sử dụng

### 1. Gỡ cài đặt thư viện cũ (nếu đã cài):
```bash
pip uninstall undetected-chromedriver -y
```

### 2. Cài đặt thư viện mới:
```bash
pip install -r requirements.txt
```

### 3. Chạy crawler:
```bash
python crawler_ram.py
```

## 🛡️ Tính năng chống chặn

### User-Agent giả lập:
```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 
(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

### Các kỹ thuật tránh phát hiện:
- ✅ Xóa `navigator.webdriver`
- ✅ Tắt cờ automation
- ✅ Tắt extension automation
- ✅ User-Agent chuẩn như trình duyệt thật

## 📊 Tính năng giữ nguyên

- ✅ Crawl tên RAM
- ✅ Crawl giá bán
- ✅ Crawl link hình ảnh
- ✅ Phân loại DDR4/DDR5
- ✅ Trích xuất dung lượng
- ✅ Lưu vào `ram_data.csv`
- ✅ Lọc giá tốt nhất
- ✅ Cập nhật `data.csv`

## 🔧 Chế độ Headless (Tùy chọn)

Nếu muốn chạy ẩn (không hiện cửa sổ browser), mở file `crawler_ram.py` và bỏ comment dòng:

```python
# options.add_argument('--headless=new')
```

Thành:

```python
options.add_argument('--headless=new')
```

## 🐛 Xử lý lỗi thường gặp

### Lỗi: "chromedriver not found"
**Giải pháp**: `webdriver-manager` sẽ tự động tải. Nếu không được, thử:
```bash
pip install --upgrade webdriver-manager
```

### Lỗi: "Chrome version mismatch"
**Giải pháp**: Cập nhật Chrome browser lên phiên bản mới nhất

### Lỗi: "Selenium not installed"
**Giải pháp**:
```bash
pip install selenium --upgrade
```

## ⚡ Ưu điểm phiên bản mới

1. **Không bị WinError 6**: Đã giải quyết hoàn toàn
2. **Tự động cập nhật**: `webdriver-manager` tự động tải driver phù hợp
3. **Ổn định hơn**: Selenium chính thức ổn định hơn undetected
4. **Dễ debug**: Có thể thấy browser hoạt động (nếu không dùng headless)
5. **Tương thích tốt**: Hoạt động trên mọi phiên bản Windows

## 📝 Lưu ý

- Lần đầu chạy có thể mất thời gian tải ChromeDriver
- Nên để browser hiện ra lần đầu để kiểm tra
- Sau khi chạy thành công, có thể bật chế độ headless

## 🎯 Kết quả mong đợi

Sau khi chạy thành công:
```
🚀 BẮT ĐẦU CRAWL DỮ LIỆU RAM TỪ TIN HỌC NGÔI SAO
============================================================
Đang khởi tạo Chrome driver...
Chrome driver đã sẵn sàng!
Đang truy cập: https://tinhocngoisao.com/collections/ram-bo-nho-trong
Đang scroll để load tất cả sản phẩm...
Đã load xong tất cả sản phẩm!
Đã tìm thấy 85 sản phẩm!
...
✅ Đã crawl thành công 85 sản phẩm RAM!
✅ Đã lưu 85 sản phẩm vào ram_data.csv!
✅ Đã cập nhật 5 sản phẩm RAM vào data.csv!
🎉 HOÀN THÀNH!
```
