@echo off
REM ============================================
REM TURK Dili - Tek Komutla .exe Derleyici
REM Kullanim: derle program.turk
REM ============================================
if "%~1"=="" (
    echo TURK Dili - .turk dosyasini .exe'ye derler
    echo.
    echo Kullanim: derle program.turk
    echo Kullanim: derle program.turk -r
    exit /b 1
)
python "%~dp0derle.py" %*
