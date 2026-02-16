"""
Script tự động chạy tất cả 8 crawler PC Components
Tác giả: Cursor AI Agent
Ngày: 15/02/2026
"""

import subprocess
import os
import sys
import time
from datetime import datetime


def print_header(text):
    """In header với format đẹp"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_step(step_num, total_steps, text):
    """In thông tin bước hiện tại"""
    print(f"\n[Bước {step_num}/{total_steps}] {text}")
    print("-" * 80)


def delete_old_data_csv():
    """Xóa file data.csv cũ để đảm bảo dữ liệu sạch"""
    if os.path.exists('data.csv'):
        try:
            os.remove('data.csv')
            print("✅ Đã xóa file data.csv cũ")
        except Exception as e:
            print(f"⚠️ Không thể xóa data.csv: {e}")
    else:
        print("ℹ️ File data.csv không tồn tại (sẽ tạo mới)")


def run_crawler(crawler_name, step_num, total_steps):
    """
    Chạy một crawler và kiểm tra kết quả
    
    Args:
        crawler_name: Tên file crawler (ví dụ: 'crawler_ram.py')
        step_num: Số thứ tự bước hiện tại
        total_steps: Tổng số bước
    
    Returns:
        bool: True nếu thành công, False nếu thất bại
    """
    crawler_display_name = crawler_name.replace('crawler_', '').replace('.py', '').upper()
    
    print_step(step_num, total_steps, f"Chạy {crawler_display_name} Crawler")
    
    start_time = time.time()
    
    try:
        # Chạy crawler với subprocess
        result = subprocess.run(
            [sys.executable, crawler_name],
            check=True,
            capture_output=False,  # Hiển thị output trực tiếp
            text=True
        )
        
        elapsed_time = time.time() - start_time
        
        print(f"\n✅ {crawler_display_name} crawler hoàn thành!")
        print(f"⏱️  Thời gian: {elapsed_time:.1f} giây ({elapsed_time/60:.1f} phút)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        elapsed_time = time.time() - start_time
        print(f"\n❌ Lỗi khi chạy {crawler_display_name} crawler!")
        print(f"⏱️  Thời gian trước khi lỗi: {elapsed_time:.1f} giây")
        print(f"Error code: {e.returncode}")
        return False
        
    except FileNotFoundError:
        print(f"\n❌ Không tìm thấy file {crawler_name}!")
        print(f"Vui lòng kiểm tra file có tồn tại trong thư mục hiện tại.")
        return False
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"\n❌ Lỗi không mong đợi khi chạy {crawler_display_name}!")
        print(f"⏱️  Thời gian trước khi lỗi: {elapsed_time:.1f} giây")
        print(f"Lỗi: {str(e)}")
        return False


def check_output_files():
    """Kiểm tra các file output đã được tạo"""
    print_header("KIỂM TRA FILE OUTPUT")
    
    files = [
        'data.csv',
        'ram_data.csv',
        'cpu_data.csv',
        'mainboard_data.csv',
        'vga_data.csv',
        'ssd_data.csv',
        'hdd_data.csv',
        'case_data.csv',
        'psu_data.csv'
    ]
    
    all_exist = True
    for filename in files:
        if os.path.exists(filename):
            # Đếm số dòng
            try:
                with open(filename, 'r', encoding='utf-8-sig') as f:
                    lines = len(f.readlines())
                print(f"  ✅ {filename:<20} ({lines} dòng)")
            except:
                print(f"  ✅ {filename:<20} (không đếm được)")
        else:
            print(f"  ❌ {filename:<20} (không tồn tại)")
            all_exist = False
    
    return all_exist


def main():
    """Hàm chính - chạy tất cả crawler"""
    
    # Header
    print_header("🚀 CRAWLER TIN HỌC NGÔI SAO - AUTO RUN ALL 8 CRAWLERS")
    print(f"📅 Thời gian bắt đầu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 Thư mục làm việc: {os.getcwd()}")
    
    # Danh sách crawler theo thứ tự (RAM phải chạy đầu tiên)
    crawlers = [
        'crawler_ram.py',        # Bước 1: Tạo mới data.csv (mode='w')
        'crawler_cpu.py',        # Bước 2: Append vào data.csv
        'crawler_mainboard.py',  # Bước 3: Append vào data.csv
        'crawler_vga.py',        # Bước 4: Append vào data.csv
        'crawler_ssd.py',        # Bước 5: Append vào data.csv
        'crawler_hdd.py',        # Bước 6: Append vào data.csv
        'crawler_case.py',       # Bước 7: Append vào data.csv
        'crawler_psu.py'         # Bước 8: Append vào data.csv
    ]
    
    total_steps = len(crawlers)
    
    # Xóa file data.csv cũ
    print_header("CHUẨN BỊ")
    delete_old_data_csv()
    
    # Chạy từng crawler
    overall_start_time = time.time()
    success_count = 0
    failed_crawlers = []
    
    for idx, crawler in enumerate(crawlers, 1):
        success = run_crawler(crawler, idx, total_steps)
        
        if success:
            success_count += 1
        else:
            failed_crawlers.append(crawler)
            
            # Hỏi người dùng có muốn tiếp tục không
            print(f"\n⚠️ Crawler {crawler} thất bại!")
            user_input = input("Bạn có muốn tiếp tục chạy các crawler còn lại? (y/n): ").strip().lower()
            
            if user_input != 'y':
                print("\n🛑 Người dùng dừng chương trình.")
                break
        
        # Nghỉ 2 giây giữa các crawler
        if idx < total_steps:
            print(f"\n⏳ Chờ 2 giây trước khi chạy crawler tiếp theo...")
            time.sleep(2)
    
    # Tổng kết
    overall_elapsed = time.time() - overall_start_time
    
    print_header("🎉 HOÀN THÀNH")
    print(f"📊 Tổng số crawler: {total_steps}")
    print(f"✅ Thành công: {success_count}")
    print(f"❌ Thất bại: {len(failed_crawlers)}")
    
    if failed_crawlers:
        print(f"\n⚠️ Các crawler thất bại:")
        for crawler in failed_crawlers:
            print(f"  - {crawler}")
    
    print(f"\n⏱️  Tổng thời gian: {overall_elapsed:.1f} giây ({overall_elapsed/60:.1f} phút)")
    print(f"📅 Thời gian kết thúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Kiểm tra file output
    print("")
    check_output_files()
    
    # Thông báo cuối cùng
    print_header("📝 KẾT LUẬN")
    
    if success_count == total_steps:
        print("✅ Tất cả crawler đã chạy thành công!")
        print("📄 File data.csv đã được tạo với đầy đủ dữ liệu từ 8 loại linh kiện PC")
        print("🚀 Bạn có thể sử dụng data.csv cho dự án AI Build PC!")
    elif success_count > 0:
        print(f"⚠️ Chỉ {success_count}/{total_steps} crawler chạy thành công.")
        print("📄 File data.csv có thể chưa đầy đủ dữ liệu.")
        print("🔧 Vui lòng kiểm tra và chạy lại các crawler bị lỗi.")
    else:
        print("❌ Tất cả crawler đều thất bại!")
        print("🔧 Vui lòng kiểm tra:")
        print("  - Kết nối internet")
        print("  - Cài đặt thư viện (selenium, webdriver-manager, pandas)")
        print("  - Chrome browser")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Người dùng dừng chương trình bằng Ctrl+C!")
        print("⏹️  Chương trình đã dừng.")
    except Exception as e:
        print(f"\n\n❌ Lỗi không mong đợi: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n👋 Tạm biệt!")
