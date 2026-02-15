# -*- coding: utf-8 -*-
"""Web App - AI Tư vấn Cấu hình PC - Streamlit"""

import streamlit as st
from urllib.parse import quote
from logic import build_pc_hoan_chinh, dinh_dang_tien

# Số Zalo nhận đặt hàng (sửa tại đây khi cần)
ZALO_NUMBER = "0938394505"

# Cấu hình trang
st.set_page_config(
    page_title="AI Tư vấn Build PC - TINHOCDAIPHUC.COM",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS tùy chỉnh
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@600;700&display=swap');
    .main-title {
        font-family: 'Be Vietnam Pro', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a5f;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    .sub-title {
        font-size: 1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4) !important;
    }
    .card-box {
        background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .card-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
    }
    .card-name {
        font-size: 1rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.25rem;
    }
    .card-price {
        font-size: 0.95rem;
        color: #2563eb;
        font-weight: 600;
    }
    .total-box {
        background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
        color: white;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        text-align: center;
        margin-top: 1.5rem;
        box-shadow: 0 10px 40px rgba(30, 58, 95, 0.3);
    }
    .total-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.25rem;
    }
    .total-value {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    .no-result {
        text-align: center;
        padding: 2rem;
        color: #64748b;
        font-size: 1.05rem;
    }
    a.stLinkButton > button {
        width: 100%;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 0.7rem 1.5rem !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #0068FF 0%, #0052cc 100%) !important;
        color: white !important;
        border: none !important;
    }
    a.stLinkButton > button:hover {
        background: linear-gradient(135deg, #0052cc 0%, #003d99 100%) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)


def parse_budget(text):
    """Chuyển chuỗi nhập (15.000.000 hoặc 15tr) thành số VNĐ."""
    if not text or not str(text).strip():
        return None
    s = str(text).replace(" ", "").replace(".", "").replace(",", "").strip().lower()
    if s.endswith("tr"):
        try:
            return int(float(s.replace("tr", "").strip()) * 1_000_000)
        except ValueError:
            return None
    if "trieu" in s or "triệu" in s:
        try:
            return int(float(s.replace("trieu", "").replace("triệu", "").strip()) * 1_000_000)
        except ValueError:
            return None
    try:
        return int(s)
    except ValueError:
        return None


def main():
    st.markdown('<p class="main-title">TINHOCDAIPHUC.COM</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">AI TƯ VẤN CẤU HÌNH PC — Chọn 6 món: CPU + Main + RAM + VGA + Nguồn + Case</p>', unsafe_allow_html=True)

    col_input, col_btn = st.columns([2, 1])
    with col_input:
        budget_raw = st.text_input(
            "Nhập ngân sách (VNĐ)",
            value="15.000.000",
            placeholder="Ví dụ: 15.000.000 hoặc 20tr",
            label_visibility="collapsed",
        )
    with col_btn:
        st.write("")  # căn nút xuống cùng hàng
        st.write("")
        search_clicked = st.button("🔍 Tìm cấu hình ngay", use_container_width=True)

    if search_clicked:
        so_tien = parse_budget(budget_raw) if budget_raw else None
        if so_tien is None or so_tien <= 0:
            st.error("Vui lòng nhập số tiền hợp lệ (ví dụ: 15000000 hoặc 15tr).")
            return

        bo_pc = build_pc_hoan_chinh(so_tien)
        if not bo_pc:
            st.markdown(
                '<p class="no-result">Không ghép được bộ PC trong ngân sách này. '
                'Cần đủ 6 món (CPU + Main + RAM + VGA + Nguồn + Case); VGA cao cần nguồn ≥600W. Thử tăng ngân sách.</p>',
                unsafe_allow_html=True,
            )
            return

        c = bo_pc
        items = [
            ("1. CPU", c["cpu"]["ten_linh_kien"], c["cpu"]["gia_vnd"]),
            ("2. Mainboard", c["main"]["ten_linh_kien"], c["main"]["gia_vnd"]),
            ("3. RAM", c["ram"]["ten_linh_kien"], c["ram"]["gia_vnd"]),
            ("4. VGA", c["vga"]["ten_linh_kien"], c["vga"]["gia_vnd"]),
            ("5. Nguồn", c["nguon"]["ten_linh_kien"], c["nguon"]["gia_vnd"]),
            ("6. Case", c["case"]["ten_linh_kien"], c["case"]["gia_vnd"]),
        ]

        st.success(f"Đã tìm cấu hình trong ngân sách **{dinh_dang_tien(so_tien)}** (CPU & Main tương thích, VGA cao dùng nguồn ≥600W).")
        st.markdown("---")

        # Hiển thị 6 thẻ: 2 cột x 3 hàng
        for i in range(0, 6, 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                idx = i + j
                if idx >= len(items):
                    break
                label, name, price = items[idx]
                with col:
                    st.markdown(
                        f'<div class="card-box">'
                        f'<div class="card-label">{label}</div>'
                        f'<div class="card-name">{name}</div>'
                        f'<div class="card-price">{dinh_dang_tien(price)}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

        # Tổng tiền nổi bật
        st.markdown(
            f'<div class="total-box">'
            f'<div class="total-label">TỔNG TIỀN</div>'
            f'<div class="total-value">{dinh_dang_tien(c["tong_tien"])}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Nội dung tin nhắn mẫu (tên 6 linh kiện + tổng tiền)
        msg_lines = [
            "Đặt hàng cấu hình PC - TINHOCDAIPHUC.COM",
            "",
            "1. CPU: " + c["cpu"]["ten_linh_kien"],
            "2. Main: " + c["main"]["ten_linh_kien"],
            "3. RAM: " + c["ram"]["ten_linh_kien"],
            "4. VGA: " + c["vga"]["ten_linh_kien"],
            "5. Nguồn: " + c["nguon"]["ten_linh_kien"],
            "6. Case: " + c["case"]["ten_linh_kien"],
            "",
            "Tổng tiền: " + dinh_dang_tien(c["tong_tien"]),
        ]
        zalo_message = "\n".join(msg_lines)
        zalo_url = f"https://zalo.me/{ZALO_NUMBER}?text={quote(zalo_message)}"

        st.markdown("")  # khoảng cách
        st.link_button("💬 Chat Zalo & Đặt Ngay", zalo_url, type="primary", use_container_width=True)


if __name__ == "__main__":
    main()
