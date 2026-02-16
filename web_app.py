# -*- coding: utf-8 -*-
"""
AI PC Builder V2.0 - Ứng dụng AI tư vấn build PC
Tác giả: Cursor AI Agent  
Ngày: 16/02/2026
"""

import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime

# Cấu hình trang
st.set_page_config(
    page_title="Lê Thái Hưng - AI PC Builder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 2rem;
    }
    .category-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #424242;
        margin-top: 1rem;
        padding: 0.5rem;
        background: linear-gradient(90deg, #E3F2FD 0%, #FFFFFF 100%);
        border-left: 4px solid #1E88E5;
    }
    .product-card {
        padding: 1rem;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        margin: 0.5rem 0;
        background-color: #FAFAFA;
    }
    .price-tag {
        font-size: 1.2rem;
        font-weight: bold;
        color: #D32F2F;
    }
    .total-price {
        font-size: 2rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #C8E6C9 0%, #A5D6A7 100%);
        border-radius: 12px;
        margin: 1rem 0;
    }
    .ai-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .manual-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load dữ liệu từ clean_data.csv (ưu tiên) hoặc data.csv"""
    data_file = None
    
    if os.path.exists('clean_data.csv'):
        data_file = 'clean_data.csv'
        st.sidebar.success("✅ Dữ liệu đã sẵn sàng!")
    elif os.path.exists('data.csv'):
        data_file = 'data.csv'
        st.sidebar.warning("⚠️ Đang dùng dữ liệu gốc (chưa làm sạch)")
        st.sidebar.info("💡 Chạy `python clean_data.py` để làm sạch dữ liệu")
    else:
        st.error("❌ Không tìm thấy file dữ liệu! Vui lòng chạy crawler trước.")
        st.info("💡 Chạy lệnh: `python run_all.py` hoặc `run_all_crawlers.bat`")
        st.stop()
    
    try:
        df = pd.read_csv(data_file, encoding='utf-8-sig')
        
        # Kiểm tra cột 'ten' và 'gia'
        if 'ten' not in df.columns:
            if 'ten_ram' in df.columns or 'ten_cpu' in df.columns:
                st.error("❌ Dữ liệu chưa được làm sạch! Chạy `python clean_data.py`")
                st.stop()
        
        if 'gia' not in df.columns and 'gia_vnd' in df.columns:
            df['gia'] = df['gia_vnd']
        
        # Làm sạch category
        if 'category' in df.columns:
            df = df.dropna(subset=['category'])
            df['category'] = df['category'].astype(str).str.strip()
            df = df[~df['category'].isin(['nan', 'None', ''])]
        
        # Đảm bảo giá là số
        if 'gia' in df.columns:
            df['gia'] = pd.to_numeric(df['gia'], errors='coerce').fillna(0).astype(int)
        
        return df
        
    except Exception as e:
        st.error("❌ Lỗi khi đọc dữ liệu: {}".format(e))
        st.stop()


def format_price(price):
    """Format giá tiền theo kiểu Việt Nam"""
    if price == 0:
        return "Liên hệ"
    return "{:,.0f}₫".format(price)


def get_budget_allocation(need_type, budget):
    """
    Tính phân bổ ngân sách theo nhu cầu
    
    Args:
        need_type: 'game', 'design', 'office'
        budget: Ngân sách tổng
    
    Returns:
        dict: Phần trăm phân bổ cho từng linh kiện
    """
    allocations = {
        'game': {
            'CPU': 0.20,      # 20%
            'Mainboard': 0.12,  # 12%
            'RAM': 0.10,      # 10%
            'VGA': 0.40,      # 40% - Quan trọng nhất
            'SSD': 0.08,      # 8%
            'HDD': 0.02,      # 2%
            'Case': 0.04,     # 4%
            'PSU': 0.04       # 4%
        },
        'design': {
            'CPU': 0.30,      # 30% - Quan trọng
            'Mainboard': 0.12,  # 12%
            'RAM': 0.15,      # 15% - Cần nhiều RAM
            'VGA': 0.30,      # 30% - Quan trọng
            'SSD': 0.08,      # 8%
            'HDD': 0.02,      # 2%
            'Case': 0.02,     # 2%
            'PSU': 0.01       # 1%
        },
        'office': {
            'CPU': 0.35,      # 35% - Quan trọng nhất
            'Mainboard': 0.15,  # 15%
            'RAM': 0.15,      # 15%
            'VGA': 0.05,      # 5% - Không quan trọng
            'SSD': 0.20,      # 20% - Cần SSD nhanh
            'HDD': 0.02,      # 2%
            'Case': 0.04,     # 4%
            'PSU': 0.04       # 4%
        }
    }
    
    return allocations.get(need_type, allocations['office'])


def get_priority_keywords(need_type, category):
    """
    Lấy từ khóa ưu tiên cho từng loại nhu cầu và linh kiện
    
    Args:
        need_type: 'game', 'design', 'office'
        category: Tên loại linh kiện (CPU, VGA, etc.)
    
    Returns:
        list: Danh sách từ khóa ưu tiên
    """
    keywords = {
        'game': {
            'CPU': ['i5', 'i7', 'i9', 'ryzen 5', 'ryzen 7', 'ryzen 9'],
            'VGA': ['rtx', 'gtx', 'rx 7', 'rx 6'],
            'RAM': ['16gb', '32gb', 'ddr4', 'ddr5'],
            'SSD': ['nvme', 'm.2', '500gb', '1tb']
        },
        'design': {
            'CPU': ['i7', 'i9', 'ryzen 7', 'ryzen 9', 'threadripper'],
            'VGA': ['rtx', 'quadro', 'radeon pro'],
            'RAM': ['32gb', '64gb', 'ddr5'],
            'SSD': ['nvme', '1tb', '2tb']
        },
        'office': {
            'CPU': ['i3', 'i5', 'ryzen 3', 'ryzen 5'],
            'VGA': ['uhd', 'vega', 'gt'],
            'RAM': ['8gb', '16gb', 'ddr4'],
            'SSD': ['sata', '256gb', '512gb']
        }
    }
    
    return keywords.get(need_type, {}).get(category, [])


def select_component_smart(df, category, budget, need_type):
    """
    Chọn linh kiện thông minh theo ngân sách và nhu cầu
    
    Args:
        df: DataFrame chứa dữ liệu
        category: Loại linh kiện
        budget: Ngân sách phân bổ cho linh kiện này
        need_type: Loại nhu cầu (game/design/office)
    
    Returns:
        Series: Linh kiện được chọn
    """
    # Lọc theo category
    category_df = df[df['category'] == category].copy()
    
    if len(category_df) == 0:
        return None
    
    # Lọc theo giá (trong khoảng +/- 30% budget)
    min_price = budget * 0.5
    max_price = budget * 1.3
    category_df = category_df[(category_df['gia'] >= min_price) & (category_df['gia'] <= max_price)]
    
    if len(category_df) == 0:
        # Nếu không có trong khoảng, lấy gần nhất
        category_df = df[df['category'] == category].copy()
        category_df['price_diff'] = abs(category_df['gia'] - budget)
        return category_df.nsmallest(1, 'price_diff').iloc[0]
    
    # Tính điểm ưu tiên dựa trên từ khóa
    keywords = get_priority_keywords(need_type, category)
    category_df['priority_score'] = 0
    
    for keyword in keywords:
        mask = category_df['ten'].str.lower().str.contains(keyword, case=False, na=False)
        category_df.loc[mask, 'priority_score'] += 1
    
    # Tính điểm cuối: priority_score - abs(gia - budget) / budget
    category_df['price_diff'] = abs(category_df['gia'] - budget)
    category_df['final_score'] = category_df['priority_score'] - (category_df['price_diff'] / budget)
    
    # Chọn sản phẩm có điểm cao nhất
    best_product = category_df.nsmallest(1, 'price_diff').iloc[0]
    
    return best_product


def ai_build_pc(df, budget, need_type):
    """
    Tự động build PC theo ngân sách và nhu cầu
    
    Args:
        df: DataFrame chứa dữ liệu
        budget: Ngân sách tổng
        need_type: Loại nhu cầu ('game', 'design', 'office')
    
    Returns:
        dict: Cấu hình được chọn
    """
    allocation = get_budget_allocation(need_type, budget)
    
    build = {}
    total_cost = 0
    
    categories = ['CPU', 'Mainboard', 'RAM', 'VGA', 'SSD', 'HDD', 'Case', 'PSU']
    
    for category in categories:
        component_budget = budget * allocation[category]
        
        # Văn phòng có thể bỏ qua VGA
        if need_type == 'office' and category == 'VGA' and component_budget < 500000:
            continue
        
        selected = select_component_smart(df, category, component_budget, need_type)
        
        if selected is not None:
            build[category] = selected
            total_cost += selected['gia']
    
    build['total_cost'] = total_cost
    build['budget'] = budget
    
    return build


def display_ai_build(build):
    """Hiển thị cấu hình AI đã chọn"""
    if not build or len(build) == 0:
        st.warning("⚠️ Không tìm thấy cấu hình phù hợp!")
        return
    
    st.markdown("### 📋 Cấu hình AI đã chọn:")
    
    categories = ['CPU', 'Mainboard', 'RAM', 'VGA', 'SSD', 'HDD', 'Case', 'PSU']
    
    category_labels = {
        'CPU': '💻 CPU - Bộ Vi Xử Lý',
        'Mainboard': '🔧 Mainboard - Bo Mạch Chủ',
        'RAM': '🎮 RAM - Bộ Nhớ Trong',
        'VGA': '🎨 VGA - Card Màn Hình',
        'SSD': '💾 SSD - Ổ Cứng Thể Rắn',
        'HDD': '💿 HDD - Ổ Cứng Cơ',
        'Case': '📦 Case - Vỏ Máy Tính',
        'PSU': '⚡ PSU - Nguồn Máy Tính'
    }
    
    for category in categories:
        if category in build and build[category] is not None:
            component = build[category]
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("#### {}".format(category_labels[category]))
                st.write("**{}**".format(component['ten']))
                
                if 'hang' in component and pd.notna(component['hang']):
                    st.caption("🏷️ Hãng: {}".format(component['hang']))
                
                if 'thong_so' in component and pd.notna(component['thong_so']):
                    st.caption("📝 Thông số: {}".format(str(component['thong_so'])[:100]))
            
            with col2:
                st.markdown('<div class="price-tag">{}</div>'.format(
                    format_price(component['gia'])
                ), unsafe_allow_html=True)
            
            st.divider()
    
    # Tổng tiền
    total_cost = build.get('total_cost', 0)
    budget = build.get('budget', 0)
    
    st.markdown('<div class="total-price">💰 Tổng tiền: {}</div>'.format(
        format_price(total_cost)
    ), unsafe_allow_html=True)
    
    # So sánh với ngân sách
    diff = budget - total_cost
    if abs(diff) < budget * 0.1:  # Sai số < 10%
        st.success("✅ Cấu hình phù hợp với ngân sách của bạn!")
    elif diff > 0:
        st.info("💵 Còn dư: {} ({}%)".format(
            format_price(diff),
            int(diff / budget * 100)
        ))
    else:
        st.warning("⚠️ Vượt ngân sách: {} ({}%)".format(
            format_price(abs(diff)),
            int(abs(diff) / budget * 100)
        ))


def filter_compatible_components(df, selected_components, category):
    """
    Lọc linh kiện tương thích với những gì đã chọn
    
    Args:
        df: DataFrame dữ liệu
        selected_components: Dict chứa các linh kiện đã chọn
        category: Loại linh kiện cần lọc
    
    Returns:
        DataFrame: Dữ liệu đã lọc
    """
    filtered_df = df[df['category'] == category].copy()
    
    if len(filtered_df) == 0:
        return filtered_df
    
    # Nếu đã chọn CPU, lọc Mainboard tương thích
    if category == 'Mainboard' and 'CPU' in selected_components:
        cpu = selected_components['CPU']
        cpu_brand = str(cpu.get('hang', '')).upper()
        cpu_name = str(cpu.get('ten', '')).upper()
        
        if 'INTEL' in cpu_brand or 'INTEL' in cpu_name:
            # Lọc mainboard Intel
            filtered_df = filtered_df[
                filtered_df['ten'].str.upper().str.contains('INTEL|B660|H610|Z690|B760|H770|Z790', case=False, na=False) |
                ~filtered_df['ten'].str.upper().str.contains('AMD|A520|B450|B550|X570|B650|X670', case=False, na=False)
            ]
        elif 'AMD' in cpu_brand or 'AMD' in cpu_name or 'RYZEN' in cpu_name:
            # Lọc mainboard AMD
            filtered_df = filtered_df[
                filtered_df['ten'].str.upper().str.contains('AMD|A520|B450|B550|X570|B650|X670', case=False, na=False) |
                ~filtered_df['ten'].str.upper().str.contains('INTEL|B660|H610|Z690|B760', case=False, na=False)
            ]
    
    # Nếu đã chọn Mainboard, lọc RAM tương thích
    if category == 'RAM' and 'Mainboard' in selected_components:
        mainboard = selected_components['Mainboard']
        mb_name = str(mainboard.get('ten', '')).upper()
        
        if 'DDR5' in mb_name:
            filtered_df = filtered_df[
                filtered_df['ten'].str.upper().str.contains('DDR5', case=False, na=False)
            ]
        elif 'DDR4' in mb_name:
            filtered_df = filtered_df[
                filtered_df['ten'].str.upper().str.contains('DDR4', case=False, na=False)
            ]
    
    return filtered_df


def display_manual_selector(df):
    """Hiển thị chế độ chọn thủ công"""
    st.markdown('<div class="manual-badge">🛠️ Tự chọn linh kiện theo ý bạn</div>', unsafe_allow_html=True)
    
    selected_components = {}
    total_price = 0
    
    categories_config = [
        ('CPU', 'CPU - Bộ Vi Xử Lý', '💻'),
        ('Mainboard', 'Mainboard - Bo Mạch Chủ', '🔧'),
        ('RAM', 'RAM - Bộ Nhớ Trong', '🎮'),
        ('VGA', 'VGA - Card Màn Hình', '🎨'),
        ('SSD', 'SSD - Ổ Cứng Thể Rắn', '💾'),
        ('HDD', 'HDD - Ổ Cứng Cơ', '💿'),
        ('Case', 'Case - Vỏ Máy Tính', '📦'),
        ('PSU', 'PSU - Nguồn Máy Tính', '⚡')
    ]
    
    for category, label, icon in categories_config:
        st.markdown("### {} {}".format(icon, label))
        
        # Lọc linh kiện tương thích
        filtered_df = filter_compatible_components(df, selected_components, category)
        
        if len(filtered_df) == 0:
            st.warning("⚠️ Không có sản phẩm nào cho loại này")
            continue
        
        # Tạo options
        options = ['-- Chưa chọn sản phẩm --']
        for idx, row in filtered_df.iterrows():
            price_str = format_price(row['gia'])
            options.append("{} - {}".format(row['ten'], price_str))
        
        # Selectbox
        selected = st.selectbox(
            "Chọn {}:".format(label),
            options,
            key="select_{}".format(category)
        )
        
        if selected != '-- Chưa chọn sản phẩm --':
            # Tìm sản phẩm tương ứng
            selected_name = selected.split(' - ')[0]
            product = filtered_df[filtered_df['ten'] == selected_name].iloc[0]
            
            selected_components[category] = product
            total_price += product['gia']
            
            # Hiển thị thông tin chi tiết
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if 'hang' in product and pd.notna(product['hang']):
                    st.caption("🏷️ Hãng: {}".format(product['hang']))
                
                if 'thong_so' in product and pd.notna(product['thong_so']):
                    with st.expander("📋 Xem thông số chi tiết"):
                        st.write(product['thong_so'])
            
            with col2:
                if 'link_hinh_anh' in product and pd.notna(product['link_hinh_anh']):
                    try:
                        st.image(product['link_hinh_anh'], width=100)
                    except:
                        pass
        
        st.divider()
    
    # Hiển thị tổng tiền
    if total_price > 0:
        st.markdown('<div class="total-price">💰 Tổng tiền: {}</div>'.format(
            format_price(total_price)
        ), unsafe_allow_html=True)
        
        # Nút xuất file
        if st.button("💾 Xuất cấu hình ra file", type="primary"):
            export_config(selected_components, total_price)


def export_config(components, total_price):
    """Xuất cấu hình ra file txt"""
    if not components:
        st.warning("⚠️ Chưa chọn linh kiện nào!")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "PC_Build_{}.txt".format(timestamp)
    
    content = "="*60 + "\n"
    content += "CẤU HÌNH MÁY TÍNH\n"
    content += "Ngày tạo: {}\n".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    content += "="*60 + "\n\n"
    
    for category, component in components.items():
        content += "{}: {}\n".format(category, component['ten'])
        content += "  Giá: {}\n".format(format_price(component['gia']))
        if 'hang' in component and pd.notna(component['hang']):
            content += "  Hãng: {}\n".format(component['hang'])
        content += "\n"
    
    content += "="*60 + "\n"
    content += "TỔNG TIỀN: {}\n".format(format_price(total_price))
    content += "="*60 + "\n"
    
    st.download_button(
        label="📥 Tải xuống file",
        data=content,
        file_name=filename,
        mime="text/plain"
    )
    
    st.success("✅ Đã xuất thành công!")


def main():
    """Hàm chính"""
    # Header
    st.markdown('<div class="main-header">🤖 AI PC Builder</div>', unsafe_allow_html=True)
    st.markdown("### 🎯 AI Tư Vấn Cấu Hình Máy Tính Thông Minh")
    
    # Load dữ liệu
    df = load_data()
    
    # Sidebar thông tin
    st.sidebar.markdown("## 📊 Thông Tin Kho Hàng")
    st.sidebar.info("🎁 Tổng kho linh kiện: **{:,} sản phẩm**".format(len(df)))
    
    if 'category' in df.columns:
        st.sidebar.markdown("### 📦 Chi tiết kho hàng:")
        for cat in sorted(df['category'].unique()):
            count = len(df[df['category'] == cat])
            st.sidebar.write("• **{}**: {} sản phẩm".format(cat, count))
    
    # 2 TAB CHÍNH
    tab1, tab2 = st.tabs([
        "🤖 AI Tư Vấn Cấu Hình (Khuyến nghị)",
        "🛠️ Tự Chọn Linh Kiện"
    ])
    
    # TAB 1: AI TƯ VẤN
    with tab1:
        st.markdown('<div class="ai-badge">🤖 Chế độ AI tự động</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        st.info("💡 **Hướng dẫn:** Nhập ngân sách và chọn nhu cầu sử dụng, AI sẽ tự động tư vấn cấu hình phù hợp nhất cho bạn!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            budget = st.number_input(
                "💰 Ngân Sách Của Bạn (VNĐ):",
                min_value=5000000,
                max_value=100000000,
                value=15000000,
                step=1000000,
                format="%d"
            )
            st.caption("💡 Gợi ý: 10 triệu (Văn phòng), 15-20 triệu (Chơi game), 25 triệu+ (Đồ họa)")
        
        with col2:
            need = st.selectbox(
                "🎯 Nhu Cầu Sử Dụng:",
                [
                    "🎮 Chơi Game (Gaming)",
                    "🎨 Đồ Họa / Render (Design)",
                    "💼 Văn Phòng (Office)"
                ]
            )
        
        st.markdown("---")
        
        if st.button("🔍 Tìm Cấu Hình Ngay!", type="primary", use_container_width=True):
            # Xác định loại nhu cầu
            if "Game" in need:
                need_type = "game"
            elif "Đồ Họa" in need or "Design" in need:
                need_type = "design"
            else:
                need_type = "office"
            
            with st.spinner("🤖 AI đang phân tích và chọn linh kiện tốt nhất cho bạn..."):
                build = ai_build_pc(df, budget, need_type)
                
                if build:
                    st.success("🎉 Hoàn thành! Đây là cấu hình AI đề xuất:")
                    display_ai_build(build)
                    
                    # Lưu vào session state để có thể build lại
                    st.session_state['last_ai_build'] = {
                        'build': build,
                        'budget': budget,
                        'need_type': need_type
                    }
        
        # Nút build lại
        if 'last_ai_build' in st.session_state:
            if st.button("🔄 Tìm Cấu Hình Khác (Random)", use_container_width=True):
                last = st.session_state['last_ai_build']
                with st.spinner("🔄 Đang tìm cấu hình mới..."):
                    build = ai_build_pc(df, last['budget'], last['need_type'])
                    if build:
                        st.success("✨ Cấu hình mới đã sẵn sàng!")
                        display_ai_build(build)
    
    # TAB 2: TỰ CHỌN
    with tab2:
        display_manual_selector(df)
    
    # Footer
    st.markdown("---")
    st.markdown("© 2026 **Lê Thái Hưng** - AI PC Builder V2.0 | 🤖 Powered by AI")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("❌ Lỗi: {}".format(e))
        import traceback
        st.code(traceback.format_exc())
