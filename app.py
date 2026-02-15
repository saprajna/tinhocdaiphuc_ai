# -*- coding: utf-8 -*-
"""Chương trình AI Tư vấn Build PC - Nhập ngân sách, in 1 bộ PC hoàn chỉnh."""

import sys
import io

# Giúp in tiếng Việt đúng trên console Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from logic import build_pc_hoan_chinh, dinh_dang_tien


def in_cau_hinh_chi_tiet(bo_pc):
    """In hóa đơn chi tiết 6 món và tổng tiền cuối cùng."""
    c = bo_pc
    print("\n  ═════════════════ HÓA ĐƠN CẤU HÌNH PC ═════════════════")
    print("  1. CPU:     ", c["cpu"]["ten_linh_kien"])
    print("               Giá: ", dinh_dang_tien(c["cpu"]["gia_vnd"]))
    print("  2. Main:    ", c["main"]["ten_linh_kien"])
    print("               Giá: ", dinh_dang_tien(c["main"]["gia_vnd"]))
    print("  3. RAM:     ", c["ram"]["ten_linh_kien"])
    print("               Giá: ", dinh_dang_tien(c["ram"]["gia_vnd"]))
    print("  4. VGA:     ", c["vga"]["ten_linh_kien"])
    print("               Giá: ", dinh_dang_tien(c["vga"]["gia_vnd"]))
    print("  5. Nguồn:   ", c["nguon"]["ten_linh_kien"])
    print("               Giá: ", dinh_dang_tien(c["nguon"]["gia_vnd"]))
    print("  6. Case:    ", c["case"]["ten_linh_kien"])
    print("               Giá: ", dinh_dang_tien(c["case"]["gia_vnd"]))
    print("  " + "─" * 50)
    print("  TỔNG TIỀN:  ", dinh_dang_tien(c["tong_tien"]))
    print("  ═══════════════════════════════════════════════════════\n")


def main():
    print("=" * 50)
    print("   AI TƯ VẤN BUILD PC - SHOP TIN HỌC ĐẠI PHÚC")
    print("=" * 50)

    while True:
        nhap = input("\nNhập số tiền (VNĐ, ví dụ 10000000 hoặc 10tr): ").strip()
        if not nhap:
            print("Bạn chưa nhập gì. Thử lại.")
            continue

        nhap = nhap.replace(" ", "").lower()
        if nhap.endswith("tr"):
            try:
                so_tien = int(float(nhap.replace("tr", "").strip()) * 1_000_000)
            except ValueError:
                so_tien = None
        elif "trieu" in nhap or "triệu" in nhap:
            try:
                so_tien = int(float(nhap.replace("trieu", "").replace("triệu", "").strip()) * 1_000_000)
            except ValueError:
                so_tien = None
        else:
            try:
                so_tien = int(nhap.replace(".", "").replace(",", ""))
            except ValueError:
                so_tien = None

        if so_tien is None or so_tien <= 0:
            print("Số tiền không hợp lệ. Vui lòng nhập số (vd: 10000000 hoặc 10tr).")
            continue

        print(f"\nNgân sách: {dinh_dang_tien(so_tien)}")
        print("-" * 50)

        bo_pc = build_pc_hoan_chinh(so_tien)
        if not bo_pc:
            print("Không ghép được bộ PC nào trong ngân sách (cần đủ 6 món: CPU + Main + RAM + VGA + Nguồn + Case; VGA cao cần nguồn ≥600W).")
        else:
            print("Cấu hình đề xuất (CPU & Main tương thích, VGA cao dùng nguồn ≥600W):")
            in_cau_hinh_chi_tiet(bo_pc)

        tiep = input("\nNhập thêm ngân sách khác? (y/n): ").strip().lower()
        if tiep != "y" and tiep != "yes":
            break

    print("\nCảm ơn bạn đã dùng AI Tư vấn Build PC. Chúc bạn build máy vừa ý!")


if __name__ == "__main__":
    main()
