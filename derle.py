#!/usr/bin/env python3
"""
TÜRK Dili - Tek Komutla .exe Derleyici

Kullanim:
    python derle.py program.turk
    python derle.py program.turk -r      (derle ve calistir)
    python derle.py program.turk -o isim (farkli isimle kaydet)
"""

import sys
import os
import subprocess

# Proje kokunu path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from turk.lexer import Lexer
from turk.parser import Parser
from turk.compiler import KodUretici


def gcc_var_mi():
    try:
        subprocess.run(["gcc", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def derle(turk_dosya, calistir=False, cikti_adi=None):
    if not os.path.exists(turk_dosya):
        print(f"Hata: Dosya bulunamadi: {turk_dosya}")
        sys.exit(1)

    if not gcc_var_mi():
        print("Hata: gcc bulunamadi! PATH'e gcc ekleyin.")
        print("Windows: https://www.msys2.org/ veya https://www.mingw-w64.org/")
        sys.exit(1)

    # 1. Kaynak kodu oku
    print(f"[1/4] Okunuyor: {turk_dosya}")
    with open(turk_dosya, "r", encoding="utf-8") as f:
        kaynak = f.read()

    # 2. Lexer + Parser
    print("[2/4] Analiz ediliyor...")
    lexer = Lexer(kaynak)
    tokenler = lexer.analiz()
    if lexer.hatalar:
        for h in lexer.hatalar:
            print(f"  Lexer Hatasi: {h}")
        sys.exit(1)

    parser = Parser(tokenler)
    try:
        ast = parser.ayrıştır()
    except Exception as e:
        print(f"  Parser Hatasi: {e}")
        sys.exit(1)

    # 3. C kodu uret
    print("[3/4] C kodu uretiliyor...")
    uretici = KodUretici()
    c_kod = uretici.uret(ast)

    taban = cikti_adi or os.path.splitext(turk_dosya)[0]
    c_dosya = taban + ".c"
    exe_dosya = taban + ".exe" if os.name == "nt" else taban

    with open(c_dosya, "w", encoding="utf-8") as f:
        f.write(c_kod)

    # 4. GCC ile derle
    print(f"[4/4] GCC ile derleniyor...")
    cmd = ["gcc", c_dosya, "-o", exe_dosya, "-lm"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("GCC Hatasi:")
        print(result.stderr)
        sys.exit(1)

    # Temizlik
    if os.path.exists(c_dosya):
        os.remove(c_dosya)

    print(f"\nBasarili -> {exe_dosya}")

    if calistir:
        print(f"\n--- {turk_dosya} cikti ---")
        result = subprocess.run([exe_dosya], capture_output=True, text=True)
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("TÜRK Dili - .turk dosyasini .exe'ye derler")
        print()
        print("Kullanim:")
        print(f"  python {sys.argv[0]} program.turk")
        print(f"  python {sys.argv[0]} program.turk -r       (derle ve calistir)")
        print(f"  python {sys.argv[0]} program.turk -o isim  (farkli cikti adi)")
        sys.exit(1)

    dosya = sys.argv[1]
    run = "-r" in sys.argv or "--run" in sys.argv
    output = None

    if "-o" in sys.argv:
        idx = sys.argv.index("-o")
        if idx + 1 < len(sys.argv):
            output = sys.argv[idx + 1]

    derle(dosya, calistir=run, cikti_adi=output)
