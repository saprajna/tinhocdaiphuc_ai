# -*- coding: utf-8 -*-
"""
AI PC Builder V2.0 - Ung dung AI tu van build PC
Tac gia: Cursor AI Agent  
Ngay: 16/02/2026
"""

import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime

# Cau hinh trang
st.set_page_config(
    page_title="AI PC Builder - Tin Hoc Ngoi Sao",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tuy chinh
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
    """Load du lieu tu clean_data.csv (uu tien) hoac data.csv"""
    data_file = None
    
    if os.path.exists('clean_data.csv'):
        data_file = 'clean_data.csv'
        st.sidebar.success("OK Du lieu da lam sach")
    elif os.path.exists('data.csv'):
        data_file = 'data.csv'
        st.sidebar.warning("CANH BAO Dung du lieu goc (chua lam sach)")
        st.sidebar.info("Chay `python clean_data.py` de lam sach du lieu")
    else:
        st.error("Khong tim thay file du lieu! Vui long chay crawler truoc.")
        st.info("Chay lenh: `python run_all.py` hoac `run_all_crawlers.bat`")
        st.stop()
    
    try:
        df = pd.read_csv(data_file, encoding='utf-8-sig')
        
        # Kiem tra cot 'ten' va 'gia'
        if 'ten' not in df.columns:
            if 'ten_ram' in df.columns or 'ten_cpu' in df.columns:
                st.error("Du lieu chua duoc lam sach! Chay `python clean_data.py`")
                st.stop()
        
        if 'gia' not in df.columns and 'gia_vnd' in df.columns:
            df['gia'] = df['gia_vnd']
        
        # Lam sach category
        if 'category' in df.columns:
            df = df.dropna(subset=['category'])
            df['category'] = df['category'].astype(str).str.strip()
            df = df[~df['category'].isin(['nan', 'None', ''])]
        
        # Dam bao gia la so
        if 'gia' in df.columns:
            df['gia'] = pd.to_numeric(df['gia'], errors='coerce').fillna(0).astype(int)
        
        return df
        
    except Exception as e:
        st.error("Loi khi doc du lieu: {}".format(e))
        st.stop()


def format_price(price):
    """Format gia tien theo kieu Viet Nam"""
    if price == 0:
        return "Lien he"
    return "{:,.0f}d".format(price)


def get_budget_allocation(need_type, budget):
    """
    Tinh phan bo ngan sach theo nhu cau
    
    Args:
        need_type: 'game', 'design', 'office'
        budget: Ngan sach tong
    
    Returns:
        dict: Phan tram phan bo cho tung linh kien
    """
    allocations = {
        'game': {
            'CPU': 0.20,      # 20%
            'Mainboard': 0.12,  # 12%
            'RAM': 0.10,      # 10%
            'VGA': 0.40,      # 40% - Quan trong nhat
            'SSD': 0.08,      # 8%
            'HDD': 0.02,      # 2%
            'Case': 0.04,     # 4%
            'PSU': 0.04       # 4%
        },
        'design': {
            'CPU': 0.30,      # 30% - Quan trong
            'Mainboard': 0.12,  # 12%
            'RAM': 0.15,      # 15% - Can nhieu RAM
            'VGA': 0.30,      # 30% - Quan trong
            'SSD': 0.08,      # 8%
            'HDD': 0.02,      # 2%
            'Case': 0.02,     # 2%
            'PSU': 0.01       # 1%
        },
        'office': {
            'CPU': 0.35,      # 35% - Quan trong nhat
            'Mainboard': 0.15,  # 15%
            'RAM': 0.15,      # 15%
            'VGA': 0.05,      # 5% - Khong quan trong
            'SSD': 0.20,      # 20% - Can SSD nhanh
            'HDD': 0.02,      # 2%
            'Case': 0.04,     # 4%
            'PSU': 0.04       # 4%
        }
    }
    
    return allocations.get(need_type, allocations['office'])


def get_priority_keywords(need_type, category):
    """
    Lay tu khoa uu tien cho tung loai nhu cau va linh kien
    
    Args:
        need_type: 'game', 'design', 'office'
        category: Ten loai linh kien (CPU, VGA, etc.)
    
    Returns:
        list: Danh sach tu khoa uu tien
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
    Chon linh kien thong minh theo ngan sach va nhu cau
    
    Args:
        df: DataFrame chua du lieu
        category: Loai linh kien
        budget: Ngan sach phan bo cho linh kien nay
        need_type: Loai nhu cau (game/design/office)
    
    Returns:
        Series: Linh kien duoc chon
    """
    # Loc theo category
    category_df = df[df['category'] == category].copy()
    
    if len(category_df) == 0:
        return None
    
    # Loc theo gia (trong khoang +/- 30% budget)
    min_price = budget * 0.5
    max_price = budget * 1.3
    category_df = category_df[(category_df['gia'] >= min_price) & (category_df['gia'] <= max_price)]
    
    if len(category_df) == 0:
        # Neu khong co trong khoang, lay gan nhat
        category_df = df[df['category'] == category].copy()
        category_df['price_diff'] = abs(category_df['gia'] - budget)
        return category_df.nsmallest(1, 'price_diff').iloc[0]
    
    # Tinh diem uu tien dua tren tu khoa
    keywords = get_priority_keywords(need_type, category)
    category_df['priority_score'] = 0
    
    for keyword in keywords:
        mask = category_df['ten'].str.lower().str.contains(keyword, case=False, na=False)
        category_df.loc[mask, 'priority_score'] += 1
    
    # Tinh diem cuoi: priority_score - abs(gia - budget) / budget
    category_df['price_diff'] = abs(category_df['gia'] - budget)
    category_df['final_score'] = category_df['priority_score'] - (category_df['price_diff'] / budget)
    
    # Chon san pham co diem cao nhat
    best_product = category_df.nsmallest(1, 'price_diff').iloc[0]
    
    return best_product


def ai_build_pc(df, budget, need_type):
    """
    Tu dong build PC theo ngan sach va nhu cau
    
    Args:
        df: DataFrame chua du lieu
        budget: Ngan sach tong
        need_type: Loai nhu cau ('game', 'design', 'office')
    
    Returns:
        dict: Cau hinh duoc chon
    """
    allocation = get_budget_allocation(need_type, budget)
    
    build = {}
    total_cost = 0
    
    categories = ['CPU', 'Mainboard', 'RAM', 'VGA', 'SSD', 'HDD', 'Case', 'PSU']
    
    for category in categories:
        component_budget = budget * allocation[category]
        
        # Van phong co the bo qua VGA
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
    """Hien thi cau hinh AI da chon"""
    if not build or len(build) == 0:
        st.warning("Khong tim thay cau hinh phu hop!")
        return
    
    st.markdown("### Cau hinh AI da chon:")
    
    categories = ['CPU', 'Mainboard', 'RAM', 'VGA', 'SSD', 'HDD', 'Case', 'PSU']
    
    for category in categories:
        if category in build and build[category] is not None:
            component = build[category]
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("#### {} {}".format(
                    {'CPU': '💻', 'Mainboard': '🔧', 'RAM': '🎮', 'VGA': '🎨', 
                     'SSD': '💾', 'HDD': '💿', 'Case': '📦', 'PSU': '⚡'}[category],
                    category
                ))
                st.write("**{}**".format(component['ten']))
                
                if 'hang' in component and pd.notna(component['hang']):
                    st.caption("Hang: {}".format(component['hang']))
                
                if 'thong_so' in component and pd.notna(component['thong_so']):
                    st.caption("Thong so: {}".format(str(component['thong_so'])[:100]))
            
            with col2:
                st.markdown('<div class="price-tag">{}</div>'.format(
                    format_price(component['gia'])
                ), unsafe_allow_html=True)
            
            st.divider()
    
    # Tong tien
    total_cost = build.get('total_cost', 0)
    budget = build.get('budget', 0)
    
    st.markdown('<div class="total-price">Tong tien: {}</div>'.format(
        format_price(total_cost)
    ), unsafe_allow_html=True)
    
    # So sanh voi ngan sach
    diff = budget - total_cost
    if abs(diff) < budget * 0.1:  # Sai so < 10%
        st.success("OK Cau hinh phu hop voi ngan sach!")
    elif diff > 0:
        st.info("Con du: {} ({}%)".format(
            format_price(diff),
            int(diff / budget * 100)
        ))
    else:
        st.warning("Vuot ngan sach: {} ({}%)".format(
            format_price(abs(diff)),
            int(abs(diff) / budget * 100)
        ))


def filter_compatible_components(df, selected_components, category):
    """
    Loc linh kien tuong thich voi nhung gi da chon
    
    Args:
        df: DataFrame du lieu
        selected_components: Dict chua cac linh kien da chon
        category: Loai linh kien can loc
    
    Returns:
        DataFrame: Du lieu da loc
    """
    filtered_df = df[df['category'] == category].copy()
    
    if len(filtered_df) == 0:
        return filtered_df
    
    # Neu da chon CPU, loc Mainboard tuong thich
    if category == 'Mainboard' and 'CPU' in selected_components:
        cpu = selected_components['CPU']
        cpu_brand = str(cpu.get('hang', '')).upper()
        cpu_name = str(cpu.get('ten', '')).upper()
        
        if 'INTEL' in cpu_brand or 'INTEL' in cpu_name:
            # Loc mainboard Intel
            filtered_df = filtered_df[
                filtered_df['ten'].str.upper().str.contains('INTEL|B660|H610|Z690|B760|H770|Z790', case=False, na=False) |
                ~filtered_df['ten'].str.upper().str.contains('AMD|A520|B450|B550|X570|B650|X670', case=False, na=False)
            ]
        elif 'AMD' in cpu_brand or 'AMD' in cpu_name or 'RYZEN' in cpu_name:
            # Loc mainboard AMD
            filtered_df = filtered_df[
                filtered_df['ten'].str.upper().str.contains('AMD|A520|B450|B550|X570|B650|X670', case=False, na=False) |
                ~filtered_df['ten'].str.upper().str.contains('INTEL|B660|H610|Z690|B760', case=False, na=False)
            ]
    
    # Neu da chon Mainboard, loc RAM tuong thich
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
    """Hien thi che do chon thu cong"""
    st.markdown('<div class="manual-badge">Tu chon linh kien</div>', unsafe_allow_html=True)
    
    selected_components = {}
    total_price = 0
    
    categories_config = [
        ('CPU', 'CPU - Vi xu ly', '💻'),
        ('Mainboard', 'Mainboard - Bo mach chu', '🔧'),
        ('RAM', 'RAM - Bo nho', '🎮'),
        ('VGA', 'VGA - Card man hinh', '🎨'),
        ('SSD', 'SSD - O cung thuan', '💾'),
        ('HDD', 'HDD - O cung co', '💿'),
        ('Case', 'Case - Thung may', '📦'),
        ('PSU', 'PSU - Nguon may tinh', '⚡')
    ]
    
    for category, label, icon in categories_config:
        st.markdown("### {} {}".format(icon, label))
        
        # Loc linh kien tuong thich
        filtered_df = filter_compatible_components(df, selected_components, category)
        
        if len(filtered_df) == 0:
            st.warning("Khong co san pham nao cho loai nay")
            continue
        
        # Tao options
        options = ['--- Khong chon ---']
        for idx, row in filtered_df.iterrows():
            price_str = format_price(row['gia'])
            options.append("{} - {}".format(row['ten'], price_str))
        
        # Selectbox
        selected = st.selectbox(
            "Chon {}:".format(label),
            options,
            key="select_{}".format(category)
        )
        
        if selected != '--- Khong chon ---':
            # Tim san pham tuong ung
            selected_name = selected.split(' - ')[0]
            product = filtered_df[filtered_df['ten'] == selected_name].iloc[0]
            
            selected_components[category] = product
            total_price += product['gia']
            
            # Hien thi thong tin chi tiet
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if 'hang' in product and pd.notna(product['hang']):
                    st.caption("Hang: {}".format(product['hang']))
                
                if 'thong_so' in product and pd.notna(product['thong_so']):
                    with st.expander("Xem thong so"):
                        st.write(product['thong_so'])
            
            with col2:
                if 'link_hinh_anh' in product and pd.notna(product['link_hinh_anh']):
                    try:
                        st.image(product['link_hinh_anh'], width=100)
                    except:
                        pass
        
        st.divider()
    
    # Hien thi tong tien
    if total_price > 0:
        st.markdown('<div class="total-price">Tong tien: {}</div>'.format(
            format_price(total_price)
        ), unsafe_allow_html=True)
        
        # Nut xuat file
        if st.button("Xuat cau hinh ra file", type="primary"):
            export_config(selected_components, total_price)


def export_config(components, total_price):
    """Xuat cau hinh ra file txt"""
    if not components:
        st.warning("Chua chon linh kien nao!")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "PC_Build_{}.txt".format(timestamp)
    
    content = "="*60 + "\n"
    content += "CAU HINH MAY TINH\n"
    content += "Ngay tao: {}\n".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    content += "="*60 + "\n\n"
    
    for category, component in components.items():
        content += "{}: {}\n".format(category, component['ten'])
        content += "  Gia: {}\n".format(format_price(component['gia']))
        if 'hang' in component and pd.notna(component['hang']):
            content += "  Hang: {}\n".format(component['hang'])
        content += "\n"
    
    content += "="*60 + "\n"
    content += "TONG TIEN: {}\n".format(format_price(total_price))
    content += "="*60 + "\n"
    
    st.download_button(
        label="Tai xuong file",
        data=content,
        file_name=filename,
        mime="text/plain"
    )
    
    st.success("Da xuat thanh cong!")


def main():
    """Ham chinh"""
    # Header
    st.markdown('<div class="main-header">🤖 AI PC Builder</div>', unsafe_allow_html=True)
    st.markdown("### Tu van build PC tu dong voi AI")
    
    # Load du lieu
    df = load_data()
    
    # Sidebar thong tin
    st.sidebar.markdown("## Thong tin")
    st.sidebar.info("Tong san pham: {:,}".format(len(df)))
    
    if 'category' in df.columns:
        st.sidebar.markdown("### Phan bo linh kien:")
        for cat in sorted(df['category'].unique()):
            count = len(df[df['category'] == cat])
            st.sidebar.write("- {}: {} san pham".format(cat, count))
    
    # 2 TAB CHINH
    tab1, tab2 = st.tabs([
        "🤖 AI Tu Van (Khuyen nghi)",
        "🛠️ Tu Chon Manual"
    ])
    
    # TAB 1: AI TU VAN
    with tab1:
        st.markdown('<div class="ai-badge">Che do AI tu dong</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            budget = st.number_input(
                "Ngan sach (VND):",
                min_value=5000000,
                max_value=100000000,
                value=15000000,
                step=1000000,
                format="%d"
            )
            st.caption("Goi y: 10tr (Van phong), 15-20tr (Choi game), 25tr+ (Do hoa)")
        
        with col2:
            need = st.selectbox(
                "Nhu cau su dung:",
                [
                    "Choi Game (Gaming)",
                    "Do Hoa / Render (Design)",
                    "Van Phong (Office)"
                ]
            )
        
        st.markdown("---")
        
        if st.button("🚀 AI Build cho toi!", type="primary", use_container_width=True):
            # Xac dinh loai nhu cau
            if "Game" in need:
                need_type = "game"
            elif "Do Hoa" in need or "Design" in need:
                need_type = "design"
            else:
                need_type = "office"
            
            with st.spinner("AI dang phan tich va chon linh kien..."):
                build = ai_build_pc(df, budget, need_type)
                
                if build:
                    st.success("Hoan thanh! Day la cau hinh AI de xuat:")
                    display_ai_build(build)
                    
                    # Luu vao session state de co the build lai
                    st.session_state['last_ai_build'] = {
                        'build': build,
                        'budget': budget,
                        'need_type': need_type
                    }
        
        # Nut build lai
        if 'last_ai_build' in st.session_state:
            if st.button("🔄 Build lai (Random)", use_container_width=True):
                last = st.session_state['last_ai_build']
                with st.spinner("Dang build lai..."):
                    build = ai_build_pc(df, last['budget'], last['need_type'])
                    if build:
                        st.success("Build moi thanh cong!")
                        display_ai_build(build)
    
    # TAB 2: TU CHON
    with tab2:
        display_manual_selector(df)
    
    # Footer
    st.markdown("---")
    st.markdown("© 2026 Tin Hoc Ngoi Sao - AI PC Builder V2.0")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("Loi: {}".format(e))
        import traceback
        st.code(traceback.format_exc())
