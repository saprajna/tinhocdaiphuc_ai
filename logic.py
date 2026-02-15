# -*- coding: utf-8 -*-
"""Logic đọc CSV và ghép bộ PC hoàn chỉnh - AI Tư vấn Build PC (tối ưu pandas + lọc sớm)"""

import csv
import os
import re

import pandas as pd

# Số ứng viên tối đa mỗi loại sau khi lọc (giới hạn để vòng lặp < 1s)
MAX_PER_CATEGORY = 6


def doc_danh_sach_linh_kien(duong_dan_file="data.csv"):
    """
    Đọc file CSV chứa danh sách linh kiện.
    Trả về list các dict (tương thích code cũ).
    """
    if not os.path.exists(duong_dan_file):
        return []
    danh_sach = []
    with open(duong_dan_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["gia_vnd"] = int(row["gia_vnd"].replace(".", "").replace(",", "").strip())
            except (ValueError, KeyError):
                continue
            row.setdefault("nha_san_xuat", "")
            row.setdefault("chip_tuong_thich", "")
            if isinstance(row.get("nha_san_xuat"), str):
                row["nha_san_xuat"] = (row["nha_san_xuat"] or "").strip()
            if isinstance(row.get("chip_tuong_thich"), str):
                row["chip_tuong_thich"] = (row["chip_tuong_thich"] or "").strip()
            danh_sach.append(row)
    return danh_sach


def _load_df(duong_dan_file):
    """Đọc CSV bằng pandas, chuẩn hóa cột và kiểu."""
    if not os.path.exists(duong_dan_file):
        return None
    df = pd.read_csv(duong_dan_file, encoding="utf-8")
    df["gia_vnd"] = pd.to_numeric(df["gia_vnd"].astype(str).str.replace(r"[\.,]", "", regex=True), errors="coerce")
    df = df.dropna(subset=["gia_vnd"]).astype({"gia_vnd": "int64"})
    df["nha_san_xuat"] = df.get("nha_san_xuat", pd.Series([""] * len(df))).fillna("").astype(str).str.strip()
    df["chip_tuong_thich"] = df.get("chip_tuong_thich", pd.Series([""] * len(df))).fillna("").astype(str).str.strip()
    return df


def _vga_can_nguon_cao(ten_vga):
    """VGA dòng cao bắt buộc nguồn từ 600W trở lên."""
    if pd.isna(ten_vga):
        return False
    ten = str(ten_vga).upper()
    for m in ("RTX 3060", "RTX 4060", "RTX 4070", "RX 6600 XT", "RX 7600", "RX 7700"):
        if m in ten:
            return True
    return False


def _lay_cong_suat_nguon_w(ten_nguon):
    """Lấy công suất (W) từ tên nguồn."""
    if pd.isna(ten_nguon):
        return 0
    match = re.search(r"(\d+)\s*W", str(ten_nguon), re.IGNORECASE)
    return int(match.group(1)) if match else 0


def _filter_candidates(df, budget, min_other_sum, top_k=MAX_PER_CATEGORY):
    """
    Lọc dòng có gia_vnd <= budget - min_other_sum.
    Lấy nửa đắt nhất + nửa rẻ nhất để có tổ hợp gần ngân sách (không chỉ toàn đồ đắt).
    """
    if df is None or df.empty:
        return pd.DataFrame()
    max_price = budget - min_other_sum
    if max_price <= 0:
        return pd.DataFrame()
    out = df[df["gia_vnd"] <= max_price].copy()
    if out.empty:
        return pd.DataFrame()
    k = min(top_k // 2, len(out))
    if k == 0:
        k = 1
    expensive = out.nlargest(k, "gia_vnd")
    cheap = out.nsmallest(k, "gia_vnd")
    combined = pd.concat([expensive, cheap], ignore_index=True).drop_duplicates()
    return combined.head(top_k)


def build_pc_hoan_chinh(so_tien_vnd, duong_dan_file="data.csv"):
    """
    Ghép 1 bộ PC: 1 CPU + 1 Main (tương thích) + 1 RAM + 1 VGA + 1 Nguồn + 1 Case.
    Tổng < ngân sách; VGA cao => Nguồn >= 600W.
    Dùng pandas + lọc sớm để đảm bảo < 1s.
    Trả về dict {"cpu", "main", "ram", "vga", "nguon", "case", "tong_tien"} hoặc None.
    """
    df = _load_df(duong_dan_file)
    if df is None or df.empty:
        return None

    loai = ("Chip", "Main", "Ram", "VGA", "Nguon", "Case")
    dfs = {k: df[df["loai"].str.strip() == k].reset_index(drop=True) for k in loai}
    if any(dfs[k].empty for k in loai):
        return None

    # Tổng giá thấp nhất của 5 loại còn lại (để lọc từng loại)
    min_sums = {}
    for k in loai:
        others = [loai[j] for j in range(6) if loai[j] != k]
        min_sums[k] = sum(dfs[o]["gia_vnd"].min() for o in others)

    # Lọc từng loại: giá <= budget - min_others, lấy top theo giá giảm dần
    filtered = {}
    for k in loai:
        f = _filter_candidates(dfs[k], so_tien_vnd, min_sums[k], top_k=MAX_PER_CATEGORY)
        if f.empty:
            return None
        filtered[k] = f

    # Main: cần có cả Intel và AMD để ghép được mọi CPU → lấy top 4 mỗi chip_tuong_thich
    main_df = dfs["Main"]
    main_df = main_df[main_df["gia_vnd"] <= so_tien_vnd - min_sums["Main"]]
    if main_df.empty:
        return None
    main_parts = []
    for chip in ("Intel", "AMD"):
        sub = main_df[main_df["chip_tuong_thich"].fillna("").astype(str).str.strip().str.lower() == chip.lower()]
        sub = sub.nlargest(MAX_PER_CATEGORY // 2, "gia_vnd")
        main_parts.append(sub)
    mains = pd.concat(main_parts, ignore_index=True).drop_duplicates()
    if mains.empty:
        return None

    # Nguồn: cần có cả nguồn < 600W và >= 600W (cho VGA cao) → lấy top 4 giá cao + top 4 có công suất >= 600W
    nguon_df = dfs["Nguon"]
    nguon_df = nguon_df[nguon_df["gia_vnd"] <= so_tien_vnd - min_sums["Nguon"]]
    if nguon_df.empty:
        return None
    nguon_high_w = nguon_df[nguon_df["ten_linh_kien"].apply(_lay_cong_suat_nguon_w) >= 600]
    nguons_top = nguon_df.nlargest(MAX_PER_CATEGORY // 2, "gia_vnd")
    nguons_high = nguon_high_w.nlargest(MAX_PER_CATEGORY // 2, "gia_vnd") if not nguon_high_w.empty else pd.DataFrame()
    nguons = pd.concat([nguons_top, nguons_high], ignore_index=True).drop_duplicates()
    if nguons.empty:
        return None

    cpus = filtered["Chip"]
    rams = filtered["Ram"]
    vgas = filtered["VGA"]
    cases = filtered["Case"]

    # Chuyển sang list dict để lặp nhanh hơn iterrows()
    def to_list_of_dict(frame):
        return [row.to_dict() for _, row in frame.iterrows()]

    cpus_l = to_list_of_dict(cpus)
    mains_l = to_list_of_dict(mains)
    rams_l = to_list_of_dict(rams)
    vgas_l = to_list_of_dict(vgas)
    nguons_l = to_list_of_dict(nguons)
    cases_l = to_list_of_dict(cases)

    # Precompute nguon wattage và chia nguons thành 2 nhóm (đủ 600W / không)
    nguons_high = [n for n in nguons_l if _lay_cong_suat_nguon_w(n.get("ten_linh_kien")) >= 600]
    nguons_low = [n for n in nguons_l if _lay_cong_suat_nguon_w(n.get("ten_linh_kien")) < 600]

    best_tong = 0
    best_row = None

    for cpu in cpus_l:
        nha_sx = str(cpu.get("nha_san_xuat") or "").strip().lower()
        if not nha_sx:
            continue
        mains_match = [m for m in mains_l if (m.get("chip_tuong_thich") or "").strip().lower() == nha_sx]
        if not mains_match:
            continue
        pc = int(cpu["gia_vnd"])
        for main in mains_match:
            pm = int(main["gia_vnd"])
            for ram in rams_l:
                pr = int(ram["gia_vnd"])
                for vga in vgas_l:
                    pv = int(vga["gia_vnd"])
                    nguons_ok = nguons_high if _vga_can_nguon_cao(vga.get("ten_linh_kien")) else (nguons_high + nguons_low)
                    if not nguons_ok:
                        continue
                    for nguon in nguons_ok:
                        pn = int(nguon["gia_vnd"])
                        for case in cases_l:
                            tong = pc + pm + pr + pv + pn + int(case["gia_vnd"])
                            if tong < so_tien_vnd and tong > best_tong:
                                best_tong = tong
                                best_row = (cpu, main, ram, vga, nguon, case, tong)

    if best_row is None:
        return None
    cpu, main, ram, vga, nguon, case, tong = best_row

    def row_to_dict(r):
        d = dict(r)
        for k, v in d.items():
            if isinstance(v, float) and (v != v or v == float("inf")):
                d[k] = ""
            elif isinstance(v, float) and k == "gia_vnd":
                d[k] = int(v)
        d["gia_vnd"] = int(d["gia_vnd"])
        return d

    return {
        "cpu": row_to_dict(cpu),
        "main": row_to_dict(main),
        "ram": row_to_dict(ram),
        "vga": row_to_dict(vga),
        "nguon": row_to_dict(nguon),
        "case": row_to_dict(case),
        "tong_tien": tong,
    }


def loc_theo_ngan_sach(so_tien_vnd, duong_dan_file="data.csv"):
    """
    Lọc ra những linh kiện có giá <= số tiền (VNĐ). Trả về list dict, sắp theo loại rồi giá.
    """
    danh_sach = doc_danh_sach_linh_kien(duong_dan_file)
    mua_duoc = [lk for lk in danh_sach if lk["gia_vnd"] <= so_tien_vnd]
    thu_tu_loai = {"Chip": 0, "Main": 1, "Ram": 2, "VGA": 3, "Nguon": 4, "Case": 5}
    mua_duoc.sort(key=lambda x: (thu_tu_loai.get(x["loai"], 99), x["gia_vnd"]))
    return mua_duoc


def dinh_dang_tien(so_tien):
    """Format số tiền VNĐ dễ đọc."""
    s = str(so_tien)
    if len(s) <= 3:
        return s
    kq = []
    for i, c in enumerate(reversed(s)):
        if i > 0 and i % 3 == 0:
            kq.append(".")
        kq.append(c)
    return "".join(reversed(kq)) + " VNĐ"
