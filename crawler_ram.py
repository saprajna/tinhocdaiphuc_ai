"""
Crawler để lấy dữ liệu RAM từ Tin Học Ngôi Sao
Website: https://tinhocngoisao.com/collections/bo-nho-ram/
Cập nhật: Sử dụng selector chuẩn của Tin Học Ngôi Sao
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
from typing import List, Dict, Optional


class RAMCrawler:
    """Class để crawl dữ liệu RAM từ Tin Học Ngôi Sao"""
    
    def __init__(self, url: str = "https://tinhocngoisao.com/collections/bo-nho-ram/"):
        self.url = url
        self.driver = None
        self.ram_data = []
        
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
        
    def extract_capacity(self, name: str) -> Optional[str]:
        """Trích xuất dung lượng RAM từ tên sản phẩm"""
        # Tìm pattern như 8GB, 16GB, 32GB, 64GB, 2x8GB, 2x16GB
        capacity_pattern = r'(\d+\s*[xX×]\s*\d+\s*GB|\d+\s*GB)'
        match = re.search(capacity_pattern, name, re.IGNORECASE)
        if match:
            return match.group(1).replace(' ', '').upper()
        return None
    
    def extract_bus_speed(self, name: str) -> Optional[str]:
        """Trích xuất tốc độ BUS từ tên sản phẩm (VD: 3200MHz, 5600MHz)"""
        bus_pattern = r'(\d{4,5})\s*MHz'
        match = re.search(bus_pattern, name, re.IGNORECASE)
        if match:
            return f"{match.group(1)}MHz"
        return None
    
    def extract_specs(self, name: str) -> str:
        """Trích xuất thông số (dung lượng + BUS) từ tên"""
        specs = []
        
        # Lấy dung lượng
        capacity = self.extract_capacity(name)
        if capacity:
            specs.append(capacity)
        
        # Lấy tốc độ BUS
        bus = self.extract_bus_speed(name)
        if bus:
            specs.append(bus)
        
        return " ".join(specs) if specs else "N/A"
    
    def extract_ram_type(self, name: str) -> str:
        """Xác định loại RAM (DDR4 hay DDR5)"""
        name_upper = name.upper()
        if 'DDR5' in name_upper:
            return 'DDR5'
        elif 'DDR4' in name_upper:
            return 'DDR4'
        elif 'DDR3' in name_upper:
            return 'DDR3'
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
    
    def scroll_to_load_all(self):
        """Scroll xuống để load tất cả sản phẩm"""
        print("Đang scroll để load tất cả sản phẩm...")
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_attempts = 10  # Giới hạn số lần scroll
        
        while scroll_attempts < max_attempts:
            # Scroll xuống cuối trang
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Đợi load
            
            # Tính chiều cao mới
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_attempts += 1
        
        print(f"Đã load xong tất cả sản phẩm sau {scroll_attempts} lần scroll!")
    
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
                screenshot_path = f"debug_wait_timeout_{int(time.time())}.png"
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
        max_clicks = 50  # Giới hạn để tránh vòng lặp vô hạn
        previous_count = 0
        no_change_count = 0  # Đếm số lần không có thay đổi
        
        while click_count < max_clicks:
            try:
                # Đếm số .product-item hiện tại trước khi click
                current_products = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
                current_count = len(current_products)
                
                print(f"📊 Hiện có {current_count} thẻ .product-item trên trang")
                
                # Tìm nút "Xem thêm" với nhiều cách khác nhau
                load_more_button = None
                
                # Cách 1: Class .btn-load-more (ưu tiên cao nhất)
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
                
                # Cách 3: Các class khác
                if not load_more_button:
                    try:
                        for selector in [".view-more", ".load-more", ".btn-loadmore", ".viewmore"]:
                            buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            for btn in buttons:
                                if btn.is_displayed():
                                    load_more_button = btn
                                    break
                            if load_more_button:
                                break
                    except:
                        pass
                
                # Nếu không tìm thấy nút hoặc nút bị ẩn
                if not load_more_button:
                    print(f"\n✅ Không còn nút 'Xem thêm' - Đã load hết sản phẩm!")
                    print(f"📦 Tổng số sản phẩm cuối cùng: {current_count}")
                    break
                
                # Kiểm tra nút có hiển thị không
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
                    
                    # Chụp ảnh debug
                    try:
                        screenshot_path = f"debug_click_failed_{click_count}.png"
                        self.driver.save_screenshot(screenshot_path)
                        print(f"📸 Đã chụp ảnh lỗi: {screenshot_path}")
                    except:
                        pass
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
                
                # Đếm lại số .product-item sau khi click
                new_products = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
                new_count = len(new_products)
                print(f"📦 Số .product-item sau khi click: {new_count}")
                print(f"➕ Tăng thêm: {new_count - current_count} sản phẩm")
                
                # Kiểm tra xem có sản phẩm mới không
                if new_count <= current_count:
                    no_change_count += 1
                    print(f"⚠️ Không có sản phẩm mới xuất hiện! (lần {no_change_count})")
                    
                    if no_change_count >= 2:
                        print(f"\n✅ Đã thử {no_change_count} lần mà không có sản phẩm mới - Dừng lại!")
                        break
                else:
                    no_change_count = 0  # Reset nếu có sản phẩm mới
                    print(f"✅ Đã tải thêm {new_count - current_count} sản phẩm mới!")
                
                # Scroll xuống cuối trang
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
                previous_count = new_count
                
            except Exception as e:
                print(f"❌ Lỗi không mong đợi: {e}")
                import traceback
                traceback.print_exc()
                
                # Chụp ảnh debug
                try:
                    screenshot_path = f"debug_error_{click_count}.png"
                    self.driver.save_screenshot(screenshot_path)
                    print(f"📸 Đã chụp ảnh lỗi: {screenshot_path}")
                except:
                    pass
                
                break
        
        print(f"\n{'='*80}")
        print(f"✅ HOÀN TẤT VIỆC TẢI SẢN PHẨM")
        print(f"{'='*80}")
        print(f"🖱️  Tổng số lần bấm nút: {click_count}")
        
        # Scroll lên đầu trang
        print(f"🔝 Scroll về đầu trang...")
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    
    def crawl_ram_data(self):
        """Crawl TOÀN BỘ dữ liệu RAM bằng cách click nút 'Xem thêm'"""
        print(f"\n{'='*80}")
        print(f"🚀 BẮT ĐẦU CRAWL TOÀN BỘ SẢN PHẨM RAM")
        print(f"{'='*80}")
        print(f"🌐 Website: {self.url}")
        print(f"⚙️  Phương pháp: Click nút 'Xem thêm' với WebDriverWait")
        print(f"{'='*80}")
        
        # Truy cập trang
        print(f"\n📍 Đang truy cập: {self.url}")
        self.driver.get(self.url)
        
        # Chụp ảnh ngay sau khi load trang
        try:
            screenshot_path = "debug_initial_load.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Đã chụp ảnh sau khi load: {screenshot_path}")
        except:
            pass
        
        # Đợi trang load và có ít nhất 20 sản phẩm xuất hiện
        print("\n" + "="*80)
        print("🔍 KIỂM TRA DANH SÁCH SẢN PHẨM CHÍNH")
        print("="*80)
        
        if not self.wait_for_products_to_load(min_products=20, timeout=20):
            print("⚠️ Chưa đủ 20 sản phẩm, nhưng sẽ tiếp tục...")
        
        # Click nút "Xem thêm" liên tục để load hết sản phẩm
        self.load_all_products_with_load_more()
        
        # Chụp ảnh sau khi load hết
        try:
            screenshot_path = "debug_after_load_all.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Đã chụp ảnh sau khi load hết: {screenshot_path}")
        except:
            pass
        
        # Bây giờ bắt đầu crawl toàn bộ sản phẩm đã load
        print(f"\n{'='*80}")
        print(f"📊 BẮT ĐẦU THU THẬP DỮ LIỆU TỪ TẤT CẢ SẢN PHẨM")
        print(f"{'='*80}")
        
        # Tìm tất cả sản phẩm với selector chính xác: .product-item
        products = []
        print("🔍 Đang tìm kiếm tất cả thẻ .product-item...")
        
        try:
            products = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
            print(f"   ✅ Tìm thấy {len(products)} thẻ .product-item")
        except Exception as e:
            print(f"   ❌ Lỗi khi tìm .product-item: {e}")
        
        # Kiểm tra nếu vẫn quá ít sản phẩm (nghi ngờ bắt nhầm "Gợi ý")
        if len(products) < 20:
            print(f"\n⚠️ CẢNH BÁO: Chỉ tìm thấy {len(products)} thẻ .product-item!")
            print(f"   Có thể đang bắt nhầm mục 'Gợi ý' thay vì danh sách chính!")
            
            # Chụp ảnh để debug
            try:
                screenshot_path = "debug_too_few_products.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"   📸 Đã chụp ảnh để debug: {screenshot_path}")
            except:
                pass
            
            # Lưu HTML
            try:
                with open("debug_page.html", "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                print(f"   💾 Đã lưu HTML để debug: debug_page.html")
            except:
                pass
        
        if not products:
            print("\n❌ KHÔNG TÌM THẤY SẢN PHẨM NÀO!")
            return
        
        print(f"\n✅ Bắt đầu crawl {len(products)} sản phẩm...\n")
        
        successful_count = 0
        error_count = 0
        
        for idx, product in enumerate(products, 1):
            try:
                # === LẤY TÊN & THÔNG SỐ ĐẦY ĐỦ ===
                # Tìm thẻ h3.pdLoopName a và lấy text
                # Chuỗi này chứa: Tên, dung lượng, BUS, loại DDR
                name = None
                try:
                    name_element = product.find_element(By.CSS_SELECTOR, "h3.pdLoopName a")
                    name = name_element.text.strip()
                except:
                    # Fallback: thử các selector khác
                    try:
                        name_element = product.find_element(By.CSS_SELECTOR, "h3 a, .pdLoopName a, .product-name a")
                        name = name_element.text.strip()
                    except:
                        pass
                
                if not name or name.strip() == "":
                    error_count += 1
                    if error_count <= 5:  # Chỉ hiển thị 5 lỗi đầu
                        print(f"   ⚠️ [{idx}] Không tìm thấy tên sản phẩm (h3.pdLoopName a)")
                    continue
                
                # === LẤY GIÁ SẢN PHẨM ===
                # Tìm chính xác p.pdPrice span
                price = None
                try:
                    price_element = product.find_element(By.CSS_SELECTOR, "p.pdPrice span")
                    price_text = price_element.text.strip()
                    # Xóa dấu chấm và ký tự ₫ để lưu dạng số nguyên
                    price = self.clean_price(price_text)
                except:
                    # Fallback: thử selector dự phòng
                    try:
                        price_element = product.find_element(By.CSS_SELECTOR, ".pdPrice, .price, .pro-price")
                        price_text = price_element.text.strip()
                        price = self.clean_price(price_text)
                    except:
                        pass
                
                if not price:
                    error_count += 1
                    if error_count <= 5:
                        print(f"   ⚠️ [{idx}] {name[:40]} - Không tìm thấy giá (p.pdPrice span)")
                    continue
                
                # === LẤY HÌNH ẢNH ===
                # Tìm thẻ img (ưu tiên lấy data-src hoặc src)
                img_url = 'N/A'
                try:
                    img_element = product.find_element(By.CSS_SELECTOR, "img")
                    # Ưu tiên lấy data-src (lazy load), nếu không có thì lấy src
                    img_url = img_element.get_attribute("data-src") or img_element.get_attribute("src") or 'N/A'
                    
                    # Đảm bảo URL đầy đủ
                    if img_url != 'N/A' and not img_url.startswith('http'):
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        elif img_url.startswith('/'):
                            img_url = 'https://tinhocngoisao.com' + img_url
                except:
                    pass
                
                # Trích xuất thông tin
                capacity = self.extract_capacity(name)
                ram_type = self.extract_ram_type(name)
                specs = self.extract_specs(name)  # Dung lượng + BUS
                
                ram_info = {
                    'ten_ram': name,  # Giữ nguyên cả chuỗi dài
                    'loai_ram': ram_type,
                    'dung_luong': capacity if capacity else 'N/A',
                    'thong_so': specs,  # Cột mới: dung lượng + BUS
                    'gia_vnd': price,
                    'link_hinh_anh': img_url,
                    'category': 'RAM'  # Thêm cột Category
                }
                
                self.ram_data.append(ram_info)
                successful_count += 1
                
                # Hiển thị tiến độ mỗi 10 sản phẩm hoặc sản phẩm đầu tiên
                if successful_count % 10 == 0 or successful_count == 1:
                    print(f"   ✅ [{successful_count}/{len(products)}] {name[:60]:<60} | {price:>10,}₫")
                    
            except Exception as e:
                error_count += 1
                if error_count <= 5:
                    print(f"   ❌ [{idx}] Lỗi khi crawl sản phẩm: {str(e)[:50]}")
                continue
        
        # Tổng kết
        print(f"\n{'='*80}")
        print(f"🎉 HOÀN THÀNH CRAWL!")
        print(f"{'='*80}")
        print(f"📊 Tổng số thẻ .product-item tìm thấy: {len(products)}")
        print(f"✅ Crawl thành công: {successful_count} sản phẩm")
        print(f"❌ Bỏ qua: {error_count} phần tử (thiếu thông tin)")
        print(f"💾 Dữ liệu đã lưu trong bộ nhớ: {len(self.ram_data)} sản phẩm")
        print(f"{'='*80}")
        
        # Nếu số lượng quá ít, cảnh báo
        if successful_count < 100:
            print(f"\n⚠️⚠️⚠️ CẢNH BÁO ⚠️⚠️⚠️")
            print(f"Chỉ crawl được {successful_count} sản phẩm!")
            print(f"Kỳ vọng: ~200+ sản phẩm")
            print(f"Có thể đang bắt nhầm mục 'Gợi ý' hoặc selector không đúng.")
            print(f"Vui lòng kiểm tra các file debug đã tạo!")
            print(f"{'='*80}")
    
    def save_to_csv(self, filename: str = "ram_data.csv"):
        """Lưu dữ liệu vào file CSV riêng và ghi mới vào data.csv"""
        if not self.ram_data:
            print("\n⚠️ Không có dữ liệu để lưu!")
            return False
        
        print(f"\n{'='*80}")
        print(f"💾 ĐANG LƯU DỮ LIỆU")
        print(f"{'='*80}")
        
        # 1. Lưu vào file riêng ram_data.csv
        print(f"📁 Bước 1: Lưu vào file riêng '{filename}'...")
        
        import os
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"   🗑️  Đã xóa file cũ: {filename}")
            except Exception as e:
                print(f"   ⚠️ Không thể xóa file cũ: {e}")
        
        # Ghi file mới hoàn toàn với cột 'category'
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['ten_ram', 'loai_ram', 'dung_luong', 'thong_so', 'gia_vnd', 'link_hinh_anh', 'category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(self.ram_data)
        
        print(f"   ✅ Đã lưu {len(self.ram_data)} sản phẩm vào '{filename}'!")
        
        # 2. Ghi MỚI vào data.csv (mode='w' - Bot RAM chạy đầu tiên)
        print(f"\n📁 Bước 2: Ghi MỚI vào 'data.csv' (mode='w')...")
        
        try:
            with open('data.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['ten_ram', 'loai_ram', 'dung_luong', 'thong_so', 'gia_vnd', 'link_hinh_anh', 'category']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(self.ram_data)
            
            print(f"   ✅ Đã tạo mới 'data.csv' với {len(self.ram_data)} sản phẩm RAM!")
            print(f"   📝 (Bot CPU sẽ append vào file này sau)")
            
        except Exception as e:
            print(f"   ❌ Lỗi khi ghi data.csv: {e}")
        
        # Thông báo cuối cùng
        print(f"\n{'='*80}")
        print(f"🎉 Đã lưu file riêng RAM và tạo mới kho data.csv thành công")
        print(f"{'='*80}")
        print(f"📄 File riêng: {filename} ({len(self.ram_data)} dòng)")
        print(f"📄 File chung: data.csv ({len(self.ram_data)} dòng - mới tạo)")
        print(f"{'='*80}")
        
        return True
    
    def filter_best_prices(self) -> Dict[str, List[Dict]]:
        """Lọc ra các sản phẩm RAM có giá tốt nhất cho mỗi loại"""
        print("\n🔍 Đang phân tích giá tốt nhất...")
        
        # Kiểm tra dữ liệu
        if not self.ram_data:
            print("⚠️ Không có dữ liệu để phân tích!")
            return {}
        
        # Chuyển sang DataFrame để xử lý dễ hơn
        df = pd.DataFrame(self.ram_data)
        
        # DEBUG: In ra thông tin DataFrame
        print(f"\n📊 DEBUG - Thông tin DataFrame:")
        print(f"   - Số dòng: {len(df)}")
        print(f"   - Các cột: {list(df.columns)}")
        
        # Kiểm tra cột loai_ram có tồn tại không
        if 'loai_ram' not in df.columns:
            print("   ⚠️ Cột 'loai_ram' không tồn tại! Đang tạo thủ công...")
            
            # Tạo cột loai_ram thủ công từ tên sản phẩm
            if 'ten_ram' in df.columns:
                df['loai_ram'] = df['ten_ram'].apply(self.extract_ram_type)
                print("   ✅ Đã tạo cột 'loai_ram' từ tên sản phẩm")
            else:
                print("   ❌ Không thể tạo cột 'loai_ram' vì thiếu cột 'ten_ram'")
                return {}
        
        # Kiểm tra các cột cần thiết khác
        required_columns = ['ten_ram', 'loai_ram', 'dung_luong', 'gia_vnd']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"   ❌ Thiếu các cột: {missing_columns}")
            return {}
        
        # In ra số lượng từng loại RAM
        print(f"\n📈 Thống kê loại RAM:")
        ram_type_counts = df['loai_ram'].value_counts()
        for ram_type, count in ram_type_counts.items():
            print(f"   - {ram_type}: {count} sản phẩm")
        
        # Lọc ra DDR4 và DDR5
        ddr4 = df[df['loai_ram'] == 'DDR4'].copy()
        ddr5 = df[df['loai_ram'] == 'DDR5'].copy()
        
        best_prices = {}
        
        # Tìm giá tốt nhất cho DDR4
        if not ddr4.empty:
            print("\n📊 DDR4 - Giá tốt nhất theo dung lượng:")
            for capacity in ['8GB', '16GB', '32GB', '64GB']:
                capacity_data = ddr4[ddr4['dung_luong'] == capacity]
                if not capacity_data.empty:
                    best = capacity_data.loc[capacity_data['gia_vnd'].idxmin()]
                    print(f"   • {capacity}: {best['ten_ram'][:50]}... - {best['gia_vnd']:,} VNĐ")
                    
                    if 'DDR4' not in best_prices:
                        best_prices['DDR4'] = []
                    best_prices['DDR4'].append(best.to_dict())
        else:
            print("\n⚠️ Không tìm thấy RAM DDR4 nào!")
        
        # Tìm giá tốt nhất cho DDR5
        if not ddr5.empty:
            print("\n📊 DDR5 - Giá tốt nhất theo dung lượng:")
            for capacity in ['8GB', '16GB', '32GB', '64GB']:
                capacity_data = ddr5[ddr5['dung_luong'] == capacity]
                if not capacity_data.empty:
                    best = capacity_data.loc[capacity_data['gia_vnd'].idxmin()]
                    print(f"   • {capacity}: {best['ten_ram'][:50]}... - {best['gia_vnd']:,} VNĐ")
                    
                    if 'DDR5' not in best_prices:
                        best_prices['DDR5'] = []
                    best_prices['DDR5'].append(best.to_dict())
        else:
            print("\n⚠️ Không tìm thấy RAM DDR5 nào!")
        
        if not best_prices:
            print("\n⚠️ Không tìm thấy sản phẩm nào để lọc giá!")
        
        return best_prices
    
    def update_main_data_csv(self, best_prices: Dict[str, List[Dict]]):
        """Cập nhật dữ liệu RAM vào file data.csv của dự án"""
        print("\n🔄 Đang cập nhật data.csv...")
        
        if not best_prices:
            print("⚠️ Không có dữ liệu giá tốt nhất để cập nhật!")
            return
        
        try:
            # Đọc file data.csv hiện tại
            try:
                df = pd.read_csv('data.csv', encoding='utf-8')
            except FileNotFoundError:
                print("⚠️ Không tìm thấy file data.csv. Tạo file mới...")
                df = pd.DataFrame(columns=['id', 'ten_linh_kien', 'loai', 'gia_vnd', 'nha_san_xuat', 'chip_tuong_thich'])
            
            # Xóa các RAM cũ
            original_count = len(df)
            df = df[df['loai'] != 'Ram']
            removed_count = original_count - len(df)
            print(f"   - Đã xóa {removed_count} RAM cũ")
            
            # Lấy ID lớn nhất hiện tại
            max_id = df['id'].max() if not df.empty and 'id' in df.columns else 0
            
            # Thêm RAM mới
            new_id = int(max_id) + 1
            new_rams = []
            
            for ram_type, rams in best_prices.items():
                for ram in rams:
                    new_ram = {
                        'id': new_id,
                        'ten_linh_kien': ram['ten_ram'],
                        'loai': 'Ram',
                        'gia_vnd': ram['gia_vnd'],
                        'nha_san_xuat': '',
                        'chip_tuong_thich': ''
                    }
                    new_rams.append(new_ram)
                    new_id += 1
            
            # Thêm vào DataFrame
            if new_rams:
                new_df = pd.DataFrame(new_rams)
                df = pd.concat([df, new_df], ignore_index=True)
                
                # Lưu lại file
                df.to_csv('data.csv', index=False, encoding='utf-8')
                print(f"✅ Đã cập nhật {len(new_rams)} sản phẩm RAM vào data.csv!")
            else:
                print("⚠️ Không có RAM mới để thêm vào!")
            
        except Exception as e:
            print(f"❌ Lỗi khi cập nhật data.csv: {e}")
            import traceback
            traceback.print_exc()
    
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
    print("🚀 CRAWLER RAM - TIN HỌC NGÔI SAO")
    print("=" * 80)
    print("📅 URL: https://tinhocngoisao.com/collections/bo-nho-ram/")
    print("🔧 Selector chính: .product-item")
    print("📝 Tên: h3.pdLoopName a (text)")
    print("💰 Giá: p.pdPrice span")
    print("📊 Thông số: Tự động trích xuất dung lượng + BUS")
    print("📂 Category: RAM")
    print("💾 Mode: Ghi MỚI data.csv (mode='w')")
    print("=" * 80)
    
    crawler = RAMCrawler()
    
    try:
        # Khởi tạo driver
        crawler.setup_driver()
        
        # Crawl dữ liệu
        crawler.crawl_ram_data()
        
        # Kiểm tra nếu không có dữ liệu
        if not crawler.ram_data:
            print("\n" + "=" * 70)
            print("⚠️ KHÔNG THỂ CRAWL DỮ LIỆU!")
            print("=" * 70)
            print("\n💡 Gợi ý:")
            print("   1. Kiểm tra kết nối internet")
            print("   2. Kiểm tra website có hoạt động: https://tinhocngoisao.com/collections/bo-nho-ram/")
            print("   3. Website có thể đã thay đổi cấu trúc HTML")
            print("   4. Xem file debug_screenshot.png và debug_page.html để phân tích")
            return
        
        # Lưu vào CSV
        crawler.save_to_csv("ram_data.csv")
        
        print("\n" + "=" * 80)
        print("🎉 HOÀN THÀNH TẤT CẢ CÁC BƯỚC!")
        print("=" * 80)
        print("📁 Các file đã tạo:")
        print("   1. ram_data.csv - File riêng RAM")
        print("   2. data.csv - File chung (ghi mới)")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Người dùng dừng chương trình!")
        
    except Exception as e:
        print(f"\n❌ Lỗi không mong đợi: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Đóng browser
        crawler.close()


if __name__ == "__main__":
    main()
