@echo off
REM ═══════════════════════════════════════════════════════════════
REM  export_pdf.bat — Export Jupyter Notebook as PDF and HTML
REM ═══════════════════════════════════════════════════════════════
REM  Usage: scripts\export_pdf.bat
REM ═══════════════════════════════════════════════════════════════

echo ================================================
echo  Exporting Notebook to PDF and HTML
echo ================================================

REM Generate HTML (always works)
echo.
echo [1/2] Generating HTML...
python -m jupyter nbconvert --to html notebooks\analysis.ipynb --output-dir docs --output analysis
if %ERRORLEVEL% EQU 0 (
    echo       Done: docs\analysis.html
) else (
    echo       FAILED: HTML generation failed.
)

REM Generate PDF (requires pandoc + LaTeX)
echo.
echo [2/2] Generating PDF...
python -m jupyter nbconvert --to pdf notebooks\analysis.ipynb --output-dir docs --output analysis
if %ERRORLEVEL% EQU 0 (
    echo       Done: docs\analysis.pdf
) else (
    echo       NOTE: PDF generation requires LaTeX (MikTeX/TeXLive).
    echo       If not installed, use the HTML version or print HTML to PDF.
    echo       Install MikTeX from: https://miktex.org/download
)

echo.
echo ================================================
echo  Export complete! Check the docs\ folder.
echo ================================================
pause
