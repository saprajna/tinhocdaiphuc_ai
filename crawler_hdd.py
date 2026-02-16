"""
Crawler để lấy dữ liệu HDD từ Tin Học Ngôi Sao
Website: https://tinhocngoisao.com/collections/o-cung-hdd/
Cập nhật: Sử dụng selector chuẩn .product-item
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
import time
import pandas as pd
import os
from typing import List, Dict, Optional


class HDDCrawler:
    """Class để crawl dữ liệu HDD từ Tin Học Ngôi Sao"""
    
    def __init__(self, url: str = "https://tinhocngoisao.com/collections/o-cung-hdd/"):
        self.url = url
        self.driver = None
        self.hdd_data = []
        
    def setup_driver(self):
        """Khởi tạo Chrome driver với User-Agent giả lập"""
        print("Đang khởi tạo Chrome driver...")
        
        # Cấu hình Chrome Options
        options = Options()
        
        # Thêm User-Agent giả lập trình duyệt thật (Chrome 120 trên Windows)
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Các tùy chọn để tránh bị phát hiện
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Tùy chọn hiệu suất
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-software-rasterizer')
        
        # Bỏ comment dòng dưới nếu muốn chạy headless (không hiện cửa sổ)
        # options.add_argument('--headless=new')
        
        # Khởi tạo driver với webdriver-manager (tự động tải chromedriver)
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"Lỗi khi cài đặt ChromeDriver tự động: {e}")
            print("Đang thử cách khác...")
            self.driver = webdriver.Chrome(options=options)
        
        # Xóa thuộc tính webdriver để tránh bị phát hiện
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })
        
        self.driver.maximize_window()
        print("Chrome driver đã sẵn sàng!")
    
    def extract_specs(self, name: str) -> str:
        """Trích xuất thông số HDD từ tên"""
        # Với HDD, thông số chính là model name
        return name if name else "N/A"
    
    def extract_brand(self, name: str) -> str:
        """Xác định hãng HDD"""
        name_upper = name.upper()
        
        # Các hãng HDD phổ biến
        brands = {
            'Seagate': ['SEAGATE', 'BARRACUDA', 'IRONWOLF', 'SKYHAWK'],
            'WD': ['WD', 'WESTERN DIGITAL', 'WD_BLACK', 'WD BLUE', 'WD RED', 'WD PURPLE', 'WD GOLD'],
            'Toshiba': ['TOSHIBA'],
            'Hitachi': ['HITACHI', 'HGST'],
            'Samsung': ['SAMSUNG'],
            'Maxtor': ['MAXTOR'],
            'Transcend': ['TRANSCEND'],
            'ADATA': ['ADATA'],
            'HP': ['HP'],
            'Acer': ['ACER']
        }
        
        for brand, keywords in brands.items():
            for keyword in keywords:
                if keyword in name_upper:
                    return brand
        
        return 'Unknown'
    
    def clean_price(self, price_text: str) -> Optional[int]:
        """Làm sạch và chuyển đổi giá sang số nguyên"""
        try:
            # Loại bỏ ký tự không phải số
            price_clean = re.sub(r'[^\d]', '', price_text)
            if price_clean:
                return int(price_clean)
        except Exception as e:
            print(f"Lỗi khi xử lý giá: {price_text} - {e}")
        return None
    
    def wait_for_products_to_load(self, min_products=20, timeout=20):
        """Chờ cho đến khi có ít nhất min_products thẻ .product-item xuất hiện"""
        print(f"⏳ Đang chờ ít nhất {min_products} thẻ .product-item xuất hiện (tối đa {timeout}s)...")
        print(f"   (Để tránh bắt nhầm mục 'Gợi ý')")
        
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: len(driver.find_elements(By.CSS_SELECTOR, ".product-item")) >= min_products
            )
            
            products = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
            print(f"✅ Đã phát hiện {len(products)} thẻ .product-item!")
            return True
        except Exception as e:
            # Nếu timeout, kiểm tra xem có bao nhiêu
            products = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
            print(f"⚠️ Timeout: Chỉ tìm thấy {len(products)} thẻ .product-item (yêu cầu tối thiểu {min_products})")
            
            # Chụp ảnh debug
            try:
                screenshot_path = f"debug_hdd_wait_timeout_{int(time.time())}.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"📸 Đã chụp ảnh debug: {screenshot_path}")
            except:
                pass
            
            return False
    
    def load_all_products_with_load_more(self):
        """Click nút 'Xem thêm' liên tục cho đến khi load hết tất cả sản phẩm"""
        print(f"\n{'='*80}")
        print(f"🔄 ĐANG TẢI TOÀN BỘ SẢN PHẨM BẰNG NÚT 'XEM THÊM'")
        print(f"{'='*80}")
        
        click_count = 0
        max_clicks = 50
        previous_count = 0
        no_change_count = 0
        
        while click_count < max_clicks:
            try:
                # Đếm số .product-item hiện tại trước khi click
                current_products = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
                current_count = len(current_products)
                
                print(f"📊 Hiện có {current_count} thẻ .product-item trên trang")
                
                # Tìm nút "Xem thêm"
                load_more_button = None
                
                # Cách 1: Class .btn-load-more
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, ".btn-load-more")
                    for btn in buttons:
                        if btn.is_displayed():
                            load_more_button = btn
                            break
                except:
                    pass
                
                # Cách 2: XPath với text "Xem thêm"
                if not load_more_button:
                    try:
                        buttons = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Xem thêm')] | //button[contains(text(), 'Xem thêm')]")
                        for btn in buttons:
                            if btn.is_displayed():
                                load_more_button = btn
                                break
                    except:
                        pass
                
                # Nếu không tìm thấy nút
                if not load_more_button:
                    print(f"\n✅ Không còn nút 'Xem thêm' - Đã load hết sản phẩm!")
                    print(f"📦 Tổng số sản phẩm cuối cùng: {current_count}")
                    break
                
                if not load_more_button.is_displayed():
                    print(f"\n✅ Nút 'Xem thêm' đã ẩn - Đã load hết sản phẩm!")
                    print(f"📦 Tổng số sản phẩm cuối cùng: {current_count}")
                    break
                
                # Click nút bằng JavaScript (tránh click nhầm overlay)
                click_count += 1
                print(f"\n🖱️  Đang bấm nút 'Xem thêm' lần {click_count}...")
                print(f"📦 Số .product-item trước khi click: {current_count}")
                
                # Lưu URL hiện tại trước khi click
                original_url = self.driver.current_url
                print(f"🔗 URL hiện tại: {original_url}")
                
                try:
                    # Scroll đến nút trước
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", load_more_button)
                    time.sleep(1)
                    
                    # Dùng JavaScript Click TRỰC TIẾP (tránh bị overlay che)
                    self.driver.execute_script("arguments[0].click();", load_more_button)
                    print(f"✅ Đã click JavaScript thành công!")
                    
                except Exception as js_error:
                    print(f"❌ Click JavaScript thất bại: {js_error}")
                    break
                
                # Chờ 2 giây trước khi kiểm tra URL
                time.sleep(2)
                
                # Kiểm tra URL sau khi click
                current_url = self.driver.current_url
                print(f"🔗 URL sau click: {current_url}")
                
                if 'collections' not in current_url:
                    print(f"⚠️ CẢNH BÁO: URL bị đổi sang trang khác!")
                    print(f"   Có thể click nhầm vào overlay 'Tra cứu bảo hành'")
                    print(f"🔙 Đang quay lại trang gốc...")
                    
                    try:
                        self.driver.back()
                        time.sleep(3)
                        print(f"✅ Đã quay lại: {self.driver.current_url}")
                        
                        # Giảm click_count vì lần này thất bại
                        click_count -= 1
                        continue  # Thử lại vòng lặp
                    except Exception as back_error:
                        print(f"❌ Lỗi khi back: {back_error}")
                        break
                
                # Chờ 3 giây để sản phẩm mới load
                print(f"⏳ Chờ 3 giây để sản phẩm mới hiện ra...")
                time.sleep(3)
                
                # Đếm lại
                new_products = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
                new_count = len(new_products)
                print(f"📦 Số .product-item sau khi click: {new_count}")
                print(f"➕ Tăng thêm: {new_count - current_count} sản phẩm")
                
                # Kiểm tra có tăng không
                if new_count <= current_count:
                    no_change_count += 1
                    print(f"⚠️ Không có sản phẩm mới xuất hiện! (lần {no_change_count})")
                    
                    if no_change_count >= 2:
                        print(f"\n✅ Đã thử {no_change_count} lần mà không có sản phẩm mới - Dừng lại!")
                        break
                else:
                    no_change_count = 0
                    print(f"✅ Đã tải thêm {new_count - current_count} sản phẩm mới!")
                
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
                previous_count = new_count
                
            except Exception as e:
                print(f"❌ Lỗi không mong đợi: {e}")
                break
        
        print(f"\n{'='*80}")
        print(f"✅ HOÀN TẤT VIỆC TẢI SẢN PHẨM")
        print(f"{'='*80}")
        print(f"🖱️  Tổng số lần bấm nút: {click_count}")
        
        print(f"🔝 Scroll về đầu trang...")
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    
    def crawl_hdd_data(self):
        """Crawl TOÀN BỘ dữ liệu HDD bằng cách click nút 'Xem thêm'"""
        print(f"\n{'='*80}")
        print(f"🚀 BẮT ĐẦU CRAWL TOÀN BỘ SẢN PHẨM HDD")
        print(f"{'='*80}")
        print(f"🌐 Website: {self.url}")
        print(f"⚙️  Phương pháp: Click nút 'Xem thêm' với WebDriverWait")
        print(f"{'='*80}")
        
        # Truy cập trang
        print(f"\n📍 Đang truy cập: {self.url}")
        self.driver.get(self.url)
        
        # Chụp ảnh ngay sau khi load
        try:
            screenshot_path = "debug_hdd_initial_load.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Đã chụp ảnh sau khi load: {screenshot_path}")
        except:
            pass
        
        # Đợi trang load
        print("\n" + "="*80)
        print("🔍 KIỂM TRA DANH SÁCH SẢN PHẨM CHÍNH")
        print("="*80)
        
        if not self.wait_for_products_to_load(min_products=20, timeout=20):
            print("⚠️ Chưa đủ 20 sản phẩm, nhưng sẽ tiếp tục...")
        
        # Click nút "Xem thêm"
        self.load_all_products_with_load_more()
        
        # Chụp ảnh sau khi load hết
        try:
            screenshot_path = "debug_hdd_after_load_all.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Đã chụp ảnh sau khi load hết: {screenshot_path}")
        except:
            pass
        
        # Thu thập dữ liệu
        print(f"\n{'='*80}")
        print(f"📊 BẮT ĐẦU THU THẬP DỮ LIỆU TỪ TẤT CẢ SẢN PHẨM")
        print(f"{'='*80}")
        
        products = []
        print("🔍 Đang tìm kiếm tất cả thẻ .product-item...")
        
        try:
            products = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
            print(f"   ✅ Tìm thấy {len(products)} thẻ .product-item")
        except Exception as e:
            print(f"   ❌ Lỗi khi tìm .product-item: {e}")
        
        if len(products) < 20:
            print(f"\n⚠️ CẢNH BÁO: Chỉ tìm thấy {len(products)} thẻ .product-item!")
        
        if not products:
            print("\n❌ KHÔNG TÌM THẤY SẢN PHẨM NÀO!")
            return
        
        print(f"\n✅ Bắt đầu crawl {len(products)} sản phẩm...\n")
        
        successful_count = 0
        error_count = 0
        
        for idx, product in enumerate(products, 1):
            try:
                # Lấy tên
                name = None
                try:
                    name_element = product.find_element(By.CSS_SELECTOR, "h3.pdLoopName a")
                    name = name_element.text.strip()
                except:
                    try:
                        name_element = product.find_element(By.CSS_SELECTOR, "h3 a, .pdLoopName a, .product-name a")
                        name = name_element.text.strip()
                    except:
                        pass
                
                if not name or name.strip() == "":
                    error_count += 1
                    if error_count <= 5:
                        print(f"   ⚠️ [{idx}] Không tìm thấy tên sản phẩm")
                    continue
                
                # Lấy giá
                price = None
                try:
                    price_element = product.find_element(By.CSS_SELECTOR, "p.pdPrice span")
                    price_text = price_element.text.strip()
                    price = self.clean_price(price_text)
                except:
                    try:
                        price_element = product.find_element(By.CSS_SELECTOR, ".pdPrice, .price, .pro-price")
                        price_text = price_element.text.strip()
                        price = self.clean_price(price_text)
                    except:
                        pass
                
                if not price:
                    error_count += 1
                    if error_count <= 5:
                        print(f"   ⚠️ [{idx}] {name[:40]} - Không tìm thấy giá")
                    continue
                
                # Lấy ảnh
                img_url = 'N/A'
                try:
                    img_element = product.find_element(By.CSS_SELECTOR, "img")
                    img_url = img_element.get_attribute("data-src") or img_element.get_attribute("src") or 'N/A'
                    
                    if img_url != 'N/A' and not img_url.startswith('http'):
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        elif img_url.startswith('/'):
                            img_url = 'https://tinhocngoisao.com' + img_url
                except:
                    pass
                
                # Trích xuất thông tin
                brand = self.extract_brand(name)
                specs = self.extract_specs(name)
                
                hdd_info = {
                    'ten_hdd': name,
                    'hang': brand,
                    'thong_so': specs,
                    'gia_vnd': price,
                    'link_hinh_anh': img_url,
                    'category': 'HDD'  # Thêm cột Category
                }
                
                self.hdd_data.append(hdd_info)
                successful_count += 1
                
                if successful_count % 10 == 0 or successful_count == 1:
                    print(f"   ✅ [{successful_count}/{len(products)}] {name[:60]:<60} | {price:>10,}₫")
                    
            except Exception as e:
                error_count += 1
                if error_count <= 5:
                    print(f"   ❌ [{idx}] Lỗi: {str(e)[:50]}")
                continue
        
        # Tổng kết
        print(f"\n{'='*80}")
        print(f"🎉 HOÀN THÀNH CRAWL!")
        print(f"{'='*80}")
        print(f"📊 Tổng số thẻ .product-item tìm thấy: {len(products)}")
        print(f"✅ Crawl thành công: {successful_count} sản phẩm")
        print(f"❌ Bỏ qua: {error_count} phần tử (thiếu thông tin)")
        print(f"💾 Dữ liệu đã lưu trong bộ nhớ: {len(self.hdd_data)} sản phẩm")
        print(f"{'='*80}")
    
    def save_to_csv(self, filename: str = "hdd_data.csv"):
        """Lưu dữ liệu vào file CSV riêng và append vào data.csv"""
        if not self.hdd_data:
            print("\n⚠️ Không có dữ liệu để lưu!")
            return False
        
        print(f"\n{'='*80}")
        print(f"💾 ĐANG LƯU DỮ LIỆU")
        print(f"{'='*80}")
        
        # 1. Lưu vào file riêng hdd_data.csv
        print(f"📁 Bước 1: Lưu vào file riêng '{filename}'...")
        
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"   🗑️  Đã xóa file cũ: {filename}")
            except Exception as e:
                print(f"   ⚠️ Không thể xóa file cũ: {e}")
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['ten_hdd', 'hang', 'thong_so', 'gia_vnd', 'link_hinh_anh', 'category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(self.hdd_data)
        
        print(f"   ✅ Đã lưu {len(self.hdd_data)} sản phẩm vào '{filename}'!")
        
        # 2. Append vào data.csv
        print(f"\n📁 Bước 2: Chèn nối tiếp vào 'data.csv'...")
        
        try:
            # Kiểm tra file data.csv có tồn tại không
            file_exists = os.path.exists('data.csv')
            
            with open('data.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
                # Nếu file chưa tồn tại, ghi header
                # Nếu đã tồn tại, không ghi header (header=False)
                fieldnames = ['ten_hdd', 'hang', 'thong_so', 'gia_vnd', 'link_hinh_anh', 'category']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                    print(f"   📝 File data.csv chưa tồn tại, đã tạo mới với header")
                
                writer.writerows(self.hdd_data)
            
            print(f"   ✅ Đã chèn nối tiếp {len(self.hdd_data)} sản phẩm vào 'data.csv'!")
            
        except Exception as e:
            print(f"   ❌ Lỗi khi append vào data.csv: {e}")
        
        # Thông báo cuối cùng
        print(f"\n{'='*80}")
        print(f"🎉 Đã thêm {len(self.hdd_data)} HDD vào kho dữ liệu chung")
        print(f"{'='*80}")
        print(f"📄 File riêng: {filename} ({len(self.hdd_data)} dòng)")
        print(f"📄 File chung: data.csv (đã thêm {len(self.hdd_data)} dòng)")
        print(f"{'='*80}")
        
        return True
    
    def close(self):
        """Đóng browser"""
        if self.driver:
            try:
                self.driver.quit()
                print("\n✅ Đã đóng browser!")
            except:
                pass


def main():
    """Hàm chính để chạy crawler"""
    print("=" * 80)
    print("🚀 CRAWLER HDD - TIN HỌC NGÔI SAO")
    print("=" * 80)
    print("📅 URL: https://tinhocngoisao.com/collections/o-cung-hdd/")
    print("🔧 Selector chính: .product-item")
    print("📝 Tên: h3.pdLoopName a (text)")
    print("💰 Giá: p.pdPrice span")
    print("📂 Category: HDD")
    print("💾 Mode: Append vào data.csv (mode='a')")
    print("=" * 80)
    
    crawler = HDDCrawler()
    
    try:
        # Khởi tạo driver
        crawler.setup_driver()
        
        # Crawl dữ liệu
        crawler.crawl_hdd_data()
        
        # Lưu vào CSV
        if crawler.hdd_data:
            crawler.save_to_csv("hdd_data.csv")
        else:
            print("\n⚠️ KHÔNG THỂ CRAWL DỮ LIỆU!")
        
        print("\n" + "=" * 80)
        print("🎉 HOÀN THÀNH TẤT CẢ CÁC BƯỚC!")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Người dùng dừng chương trình!")
        
    except Exception as e:
        print(f"\n❌ Lỗi không mong đợi: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        crawler.close()


if __name__ == "__main__":
    main()
