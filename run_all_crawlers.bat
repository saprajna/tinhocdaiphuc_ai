@echo off
REM ================================================================================
REM Script tự động chạy toàn bộ 8 crawler PC Components
REM Ngày: 15/02/2026
REM ================================================================================

echo.
echo ================================================================================
echo  CRAWLER TIN HOC NGOI SAO - FULL PC COMPONENTS (8 CRAWLERS)
echo ================================================================================
echo.
echo Chuong trinh se chay lan luot:
echo   1. crawler_ram.py (tao moi data.csv)
echo   2. crawler_cpu.py (append vao data.csv)
echo   3. crawler_mainboard.py (append vao data.csv)
echo   4. crawler_vga.py (append vao data.csv)
echo   5. crawler_ssd.py (append vao data.csv)
echo   6. crawler_hdd.py (append vao data.csv)
echo   7. crawler_case.py (append vao data.csv)
echo   8. crawler_psu.py (append vao data.csv)
echo.
echo ================================================================================
echo.

REM ============================================
REM BUOC 1: CRAWL RAM
REM ============================================
echo ============================================
echo BUOC 1: CRAWL RAM
echo ============================================
echo.
python crawler_ram.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Loi khi chay crawler_ram.py!
    pause
    exit /b 1
)

echo.
echo [OK] RAM crawl thanh cong!
echo.
timeout /t 3 /nobreak

REM ============================================
REM BUOC 2: CRAWL CPU
REM ============================================
echo.
echo ============================================
echo BUOC 2: CRAWL CPU
echo ============================================
echo.
python crawler_cpu.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Loi khi chay crawler_cpu.py!
    pause
    exit /b 1
)

echo.
echo [OK] CPU crawl thanh cong!
echo.
timeout /t 3 /nobreak

REM ============================================
REM BUOC 3: CRAWL MAINBOARD
REM ============================================
echo.
echo ============================================
echo BUOC 3: CRAWL MAINBOARD
echo ============================================
echo.
python crawler_mainboard.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Loi khi chay crawler_mainboard.py!
    pause
    exit /b 1
)

echo.
echo [OK] MAINBOARD crawl thanh cong!
echo.
timeout /t 3 /nobreak

REM ============================================
REM BUOC 4: CRAWL VGA
REM ============================================
echo.
echo ============================================
echo BUOC 4: CRAWL VGA (CARD MAN HINH)
echo ============================================
echo.
python crawler_vga.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Loi khi chay crawler_vga.py!
    pause
    exit /b 1
)

echo.
echo [OK] VGA crawl thanh cong!
echo.
timeout /t 3 /nobreak

REM ============================================
REM BUOC 5: CRAWL SSD
REM ============================================
echo.
echo ============================================
echo BUOC 5: CRAWL SSD
echo ============================================
echo.
python crawler_ssd.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Loi khi chay crawler_ssd.py!
    pause
    exit /b 1
)

echo.
echo [OK] SSD crawl thanh cong!
echo.
timeout /t 3 /nobreak

REM ============================================
REM BUOC 6: CRAWL HDD
REM ============================================
echo.
echo ============================================
echo BUOC 6: CRAWL HDD
echo ============================================
echo.
python crawler_hdd.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Loi khi chay crawler_hdd.py!
    pause
    exit /b 1
)

echo.
echo [OK] HDD crawl thanh cong!
echo.
timeout /t 3 /nobreak

REM ============================================
REM BUOC 7: CRAWL CASE
REM ============================================
echo.
echo ============================================
echo BUOC 7: CRAWL CASE (THUNG MAY)
echo ============================================
echo.
python crawler_case.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Loi khi chay crawler_case.py!
    pause
    exit /b 1
)

echo.
echo [OK] CASE crawl thanh cong!
echo.
timeout /t 3 /nobreak

REM ============================================
REM BUOC 8: CRAWL PSU
REM ============================================
echo.
echo ============================================
echo BUOC 8: CRAWL PSU (NGUON MAY TINH)
echo ============================================
echo.
python crawler_psu.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Loi khi chay crawler_psu.py!
    pause
    exit /b 1
)

echo.
echo [OK] PSU crawl thanh cong!
echo.

REM ============================================
REM HOAN THANH
REM ============================================
echo.
echo ================================================================================
echo                          HOAN THANH TAT CA!
echo ================================================================================
echo.
echo Cac file da tao:
echo   - ram_data.csv (~219 san pham RAM)
echo   - cpu_data.csv (~120 san pham CPU)
echo   - mainboard_data.csv (~180 san pham Mainboard)
echo   - vga_data.csv (~146 san pham VGA)
echo   - ssd_data.csv (~69 san pham SSD)
echo   - hdd_data.csv (~40 san pham HDD)
echo   - case_data.csv (~50 san pham Case)
echo   - psu_data.csv (~80 san pham PSU)
echo   - data.csv (~904 san pham tong cong)
echo.
echo ================================================================================
echo.
pause
