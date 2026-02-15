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


def _cpu_tier(ten_cpu):
    """Phân tầng CPU: 0=budget (Celeron,Pentium,i3,R3), 1=mid (i5,R5), 2=high (i7,i9,R7,R9)."""
    if pd.isna(ten_cpu):
        return 0
    t = str(ten_cpu).upper()
    if "CELERON" in t or "PENTIUM" in t or "I3-" in t or "RYZEN 3" in t or "4100" in t or "5300G" in t:
        return 0
    if "I5-" in t or "RYZEN 5" in t:
        return 1
    return 2  # i7, i9, R7, R9


def _main_tier(ten_main):
    """Phân tầng Main: 0=budget (H610,A520), 1=mid (B660,B760,B550,B650), 2=high (Z690,Z790,X570,X670)."""
    if pd.isna(ten_main):
        return 0
    t = str(ten_main).upper()
    if "H610" in t or "A520" in t:
        return 0
    if "B660" in t or "B760" in t or "B550" in t or "B650" in t:
        return 1
    return 2  # Z690, Z790, X570, X670


def _cpu_main_can_pair(cpu_row, main_row):
    """Cân đối: không chip yếu đi với main đắt (Celeron + Z790). Main tầm không vượt quá CPU + 1; giá main <= 2.5x CPU."""
    tc, tm = _cpu_tier(cpu_row.get("ten_linh_kien")), _main_tier(main_row.get("ten_linh_kien"))
    if tm > tc + 1:
        return False
    pc = int(cpu_row.get("gia_vnd", 0))
    pm = int(main_row.get("gia_vnd", 0))
    if pc <= 0:
        return True
    if pm > 2.5 * pc:
        return False
    return True


def _cpu_has_igp(ten_cpu):
    """CPU có đồ họa tích hợp: Intel không F, AMD có G."""
    if pd.isna(ten_cpu):
        return False
    t = str(ten_cpu).upper()
    if "INTEL" in t and "F" not in t:
        return True
    if "G" in t and ("RYZEN" in t or "5600G" in t or "5300G" in t):
        return True
    return False


def _ram_capacity_gb(ten_ram):
    """Lấy dung lượng RAM (GB) từ tên, ưu tiên số lớn (32GB, 2x32)."""
    if pd.isna(ten_ram):
        return 0
    s = str(ten_ram)
    m = re.search(r"2\s*[xX×]\s*32", s)
    if m:
        return 64
    for x in (32, 16, 8):
        if str(x) + "GB" in s or str(x) + " GB" in s:
            return x
    return 16


def _main_chi_ddr4(ten_main):
    """Mainboard có 'D4' trong tên thì hỗ trợ DDR4."""
    if pd.isna(ten_main):
        return False
    return "D4" in str(ten_main).upper()


def _ram_is_ddr4(ten_ram):
    """RAM là loại DDR4."""
    if pd.isna(ten_ram):
        return False
    return "DDR4" in str(ten_ram).upper()


def _ram_is_ddr5(ten_ram):
    """RAM là loại DDR5."""
    if pd.isna(ten_ram):
        return False
    return "DDR5" in str(ten_ram).upper()


def _ram_compatible_with_main(ten_ram, ten_main):
    """
    RAM tương thích Main:
    - Nếu Main có 'D4' → chỉ dùng DDR4
    - Nếu Main không có 'D4' → ưu tiên DDR5, nhưng cũng cho phép DDR4 (một số main hỗ trợ cả 2)
    """
    if _main_chi_ddr4(ten_main):
        # Main D4 chỉ dùng DDR4
        return _ram_is_ddr4(ten_ram)
    else:
        # Main không D4: cho phép cả DDR4 và DDR5
        return _ram_is_ddr4(ten_ram) or _ram_is_ddr5(ten_ram)


# Tỷ lệ tối đa Nguồn + Case so với ngân sách (tối đa 20% để cân đối chi phí)
NGUON_CASE_MAX_PERCENT = 0.20


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
                if not _ram_compatible_with_main(ram.get("ten_linh_kien"), main.get("ten_linh_kien")):
                    continue
                pr = int(ram["gia_vnd"])
                for vga in vgas_l:
                    pv = int(vga["gia_vnd"])
                    nguons_ok = nguons_high if _vga_can_nguon_cao(vga.get("ten_linh_kien")) else (nguons_high + nguons_low)
                    if not nguons_ok:
                        continue
                    for nguon in nguons_ok:
                        pn = int(nguon["gia_vnd"])
                        for case in cases_l:
                            pcase = int(case["gia_vnd"])
                            if (pn + pcase) > so_tien_vnd * NGUON_CASE_MAX_PERCENT:
                                continue
                            tong = pc + pm + pr + pv + pn + pcase
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


def _build_one_with_filters(
    df, so_tien_vnd, nhu_cau, duong_dan_file="data.csv"
):
    """
    Ghép 1 bộ PC theo nhu_cau (van_phong | choi_game | render), có kiểm tra cân đối CPU-Main.
    Trả về dict build hoặc None.
    """
    if df is None or df.empty:
        return None
    loai = ("Chip", "Main", "Ram", "VGA", "Nguon", "Case")
    dfs = {k: df[df["loai"].str.strip() == k].reset_index(drop=True) for k in loai}
    if any(dfs[k].empty for k in loai):
        return None

    min_sums = {}
    for k in loai:
        others = [loai[j] for j in range(6) if loai[j] != k]
        min_sums[k] = sum(dfs[o]["gia_vnd"].min() for o in others)

    def price_ok(frame, key):
        return frame[frame["gia_vnd"] <= so_tien_vnd - min_sums[key]]

    # Lọc theo nhu cầu
    cpus = price_ok(dfs["Chip"], "Chip")
    mains_all = price_ok(dfs["Main"], "Main")
    rams = price_ok(dfs["Ram"], "Ram")
    vgas = price_ok(dfs["VGA"], "VGA")
    nguon_df = price_ok(dfs["Nguon"], "Nguon")
    cases = price_ok(dfs["Case"], "Case")

    if nhu_cau == "van_phong":
        # Ưu tiên CPU i5/i7 đời mới, có đồ họa tích hợp
        def _is_i5_i7(ten):
            if pd.isna(ten):
                return False
            t = str(ten).upper()
            return ("I5-" in t or "I7-" in t) and _cpu_has_igp(ten)
        cpus_i5_i7 = cpus[cpus["ten_linh_kien"].apply(_is_i5_i7)]
        if not cpus_i5_i7.empty:
            cpus = cpus_i5_i7
        else:
            cpus_igp = cpus[cpus["ten_linh_kien"].apply(_cpu_has_igp)]
            cpus = cpus_igp if not cpus_igp.empty else cpus
        # RAM 16GB cho văn phòng
        rams_16 = rams[rams["ten_linh_kien"].apply(lambda x: _ram_capacity_gb(x) == 16 or "16GB" in str(x))]
        rams = rams_16 if not rams_16.empty else rams
        # VGA rất rẻ hoặc không cần rời (lấy rẻ nhất)
        vgas_cheap = vgas[vgas["gia_vnd"] <= 2_500_000]
        vgas = vgas_cheap if not vgas_cheap.empty else vgas
        # Nguồn văn phòng chỉ 450W–600W tối đa
        nguon_vp = nguon_df[nguon_df["ten_linh_kien"].apply(lambda x: 450 <= _lay_cong_suat_nguon_w(x) <= 600)]
        nguon_df = nguon_vp if not nguon_vp.empty else nguon_df[nguon_df["ten_linh_kien"].apply(lambda x: _lay_cong_suat_nguon_w(x) <= 600)]
    elif nhu_cau == "choi_game":
        # VGA ít nhất 35%, tối đa 50% ngân sách
        vga_min = int(so_tien_vnd * 0.35)
        vga_max = int(so_tien_vnd * 0.50)
        vgas_g = vgas[vgas["gia_vnd"].between(vga_min, vga_max)]
        vgas = vgas_g if not vgas_g.empty else vgas
        # CPU tầm trung (i5, R5)
        cpus_mid = cpus[cpus["ten_linh_kien"].apply(lambda x: _cpu_tier(x) == 1)]
        cpus = cpus_mid if not cpus_mid.empty else cpus
        # RAM 16GB
        rams_16 = rams[rams["ten_linh_kien"].apply(lambda x: _ram_capacity_gb(x) == 16 or "16GB" in str(x))]
        rams = rams_16 if not rams_16.empty else rams
    elif nhu_cau == "render":
        cpus_high = cpus[cpus["ten_linh_kien"].apply(lambda x: _cpu_tier(x) == 2)]
        cpus = cpus_high if not cpus_high.empty else cpus
        rams_32 = rams[rams["ten_linh_kien"].apply(lambda x: _ram_capacity_gb(x) >= 32)]
        rams = rams_32 if not rams_32.empty else rams
        vgas_mid = vgas[vgas["gia_vnd"] >= 4_000_000]
        vgas = vgas_mid if not vgas_mid.empty else vgas

    if cpus.empty or mains_all.empty or rams.empty or vgas.empty or nguon_df.empty or cases.empty:
        return None

    # Giới hạn ứng viên, đảm bảo đa dạng
    k = min(MAX_PER_CATEGORY, len(cpus))
    cpus = pd.concat([cpus.nlargest(k // 2, "gia_vnd"), cpus.nsmallest(k // 2, "gia_vnd")]).drop_duplicates().head(MAX_PER_CATEGORY)
    k = min(MAX_PER_CATEGORY, len(rams))
    rams = pd.concat([rams.nlargest(k // 2, "gia_vnd"), rams.nsmallest(k // 2, "gia_vnd")]).drop_duplicates().head(MAX_PER_CATEGORY)
    k = min(MAX_PER_CATEGORY, len(vgas))
    vgas = pd.concat([vgas.nlargest(k // 2, "gia_vnd"), vgas.nsmallest(k // 2, "gia_vnd")]).drop_duplicates().head(MAX_PER_CATEGORY)
    k = min(MAX_PER_CATEGORY, len(cases))
    cases = pd.concat([cases.nlargest(k // 2, "gia_vnd"), cases.nsmallest(k // 2, "gia_vnd")]).drop_duplicates().head(MAX_PER_CATEGORY)

    main_parts = []
    for chip in ("Intel", "AMD"):
        sub = mains_all[mains_all["chip_tuong_thich"].fillna("").astype(str).str.strip().str.lower() == chip.lower()]
        if sub.empty:
            continue
        k = min(MAX_PER_CATEGORY // 2, len(sub))
        hi = sub.nlargest(k // 2, "gia_vnd")
        lo = sub.nsmallest(k // 2, "gia_vnd")
        main_parts.append(pd.concat([hi, lo], ignore_index=True).drop_duplicates())
    if not main_parts:
        return None
    mains = pd.concat(main_parts, ignore_index=True).drop_duplicates()
    if mains.empty:
        return None

    nguon_high_w = nguon_df[nguon_df["ten_linh_kien"].apply(_lay_cong_suat_nguon_w) >= 600]
    nguons_top = nguon_df.nlargest(MAX_PER_CATEGORY // 2, "gia_vnd")
    nguons_high = nguon_high_w.nlargest(MAX_PER_CATEGORY // 2, "gia_vnd") if not nguon_high_w.empty else pd.DataFrame()
    nguons = pd.concat([nguons_top, nguons_high], ignore_index=True).drop_duplicates().head(MAX_PER_CATEGORY)
    if nguons.empty:
        return None

    def to_list_of_dict(frame):
        return [row.to_dict() for _, row in frame.iterrows()]

    cpus_l = to_list_of_dict(cpus)
    mains_l = to_list_of_dict(mains)
    rams_l = to_list_of_dict(rams)
    vgas_l = to_list_of_dict(vgas)
    nguons_l = to_list_of_dict(nguons)
    cases_l = to_list_of_dict(cases)
    nguons_high_l = [n for n in nguons_l if _lay_cong_suat_nguon_w(n.get("ten_linh_kien")) >= 600]
    nguons_low_l = [n for n in nguons_l if _lay_cong_suat_nguon_w(n.get("ten_linh_kien")) < 600]

    best_tong = 0
    best_row = None

    for cpu in cpus_l:
        nha_sx = str(cpu.get("nha_san_xuat") or "").strip().lower()
        if not nha_sx:
            continue
        mains_match = [m for m in mains_l if (m.get("chip_tuong_thich") or "").strip().lower() == nha_sx]
        for main in mains_match:
            if not _cpu_main_can_pair(cpu, main):
                continue
            pc = int(cpu["gia_vnd"])
            pm = int(main["gia_vnd"])
            for ram in rams_l:
                if not _ram_compatible_with_main(ram.get("ten_linh_kien"), main.get("ten_linh_kien")):
                    continue
                pr = int(ram["gia_vnd"])
                for vga in vgas_l:
                    pv = int(vga["gia_vnd"])
                    nguons_ok = nguons_high_l if _vga_can_nguon_cao(vga.get("ten_linh_kien")) else (nguons_high_l + nguons_low_l)
                    if not nguons_ok:
                        continue
                    for nguon in nguons_ok:
                        pn = int(nguon["gia_vnd"])
                        for case in cases_l:
                            pcase = int(case["gia_vnd"])
                            if (pn + pcase) > so_tien_vnd * NGUON_CASE_MAX_PERCENT:
                                continue
                            tong = pc + pm + pr + pv + pn + pcase
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


def build_pc_theo_nhu_cau(ngan_sach, nhu_cau, duong_dan_file="data.csv"):
    """
    Ghép 1 bộ PC theo nhu cầu: van_phong | choi_game | render.
    - Văn phòng: CPU có IGP, VGA rất rẻ/không cần rời, Main bền, cân đối CPU-Main.
    - Chơi game: 40-50% ngân sách VGA, CPU tầm trung, RAM 16GB, cân đối CPU-Main.
    - Render/Đồ họa: CPU nhiều nhân, RAM 32GB+, VGA khá, cân đối CPU-Main.
    Trả về dict build hoặc None. Luôn kiểm tra cân đối (không Celeron + Z790).
    """
    if nhu_cau not in ("van_phong", "choi_game", "render"):
        return None
    df = _load_df(duong_dan_file)
    return _build_one_with_filters(df, int(ngan_sach), nhu_cau, duong_dan_file)


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
