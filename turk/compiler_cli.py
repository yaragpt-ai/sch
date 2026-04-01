"""
TÜRK Programlama Dili - Compiler CLI
.turk dosyalarını C'ye derler ve opsiyonel olarak gcc ile çalıştırılabilir üretir
"""

import sys
import os
import subprocess
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from turk.lexer import Lexer
from turk.parser import Parser, ParserHata
from turk.compiler import KodUretici


def derle(kaynak: str) -> str:
    lexer = Lexer(kaynak)
    tokenler = lexer.analiz()
    if lexer.hatalar:
        for h in lexer.hatalar:
            print(f"Lexer Hatası: {h}", file=sys.stderr)
        sys.exit(1)

    parser = Parser(tokenler)
    try:
        ast = parser.ayrıştır()
    except ParserHata as e:
        print(f"Parser Hatası: {e}", file=sys.stderr)
        sys.exit(1)

    uretici = KodUretici()
    return uretici.uret(ast)


def dosya_derle(turk_dosya: str, c_dosya: str = None, calistir: bool = False,
                cikti_dosya: str = None, temizle: bool = False):
    if not os.path.exists(turk_dosya):
        print(f"Hata: Dosya bulunamadı: {turk_dosya}", file=sys.stderr)
        sys.exit(1)

    with open(turk_dosya, 'r', encoding='utf-8') as f:
        kaynak = f.read()

    c_kod = derle(kaynak)

    if c_dosya is None:
        c_dosya = os.path.splitext(turk_dosya)[0] + ".c"

    with open(c_dosya, 'w', encoding='utf-8') as f:
        f.write(c_kod)
    print(f"C kodu yazıldı: {c_dosya}")

    if calistir or cikti_dosya:
        if not _gcc_var_mi():
            print("Hata: gcc bulunamadı. PATH'e ekleyin.", file=sys.stderr)
            sys.exit(1)

        if cikti_dosya is None:
            cikti_dosya = os.path.splitext(turk_dosya)[0]

        cmd = ["gcc", c_dosya, "-o", cikti_dosya, "-lm"]
        print(f"Derleniyor: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print("GCC Hatası:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            sys.exit(1)

        print(f"Çalıştırılabilir üretildi: {cikti_dosya}")

        if temizle and os.path.exists(c_dosya):
            os.remove(c_dosya)
            print(f"Geçici dosya silindi: {c_dosya}")

        if calistir:
            print(f"\n--- {turk_dosya} çıktısı ---")
            result = subprocess.run([cikti_dosya], capture_output=True, text=True)
            print(result.stdout, end='')
            if result.stderr:
                print(result.stderr, end='', file=sys.stderr)


def _gcc_var_mi() -> bool:
    try:
        subprocess.run(["gcc", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def main():
    parser = argparse.ArgumentParser(
        description="TÜRK Programlama Dili Derleyicisi",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python -m turk.compiler program.turk              # C kodu üret
  python -m turk.compiler program.turk -c            # C + gcc ile derle
  python -m turk.compiler program.turk -r            # C + gcc + çalıştır
  python -m turk.compiler program.turk -c -o program # Özel çıktı adı
  python -m turk.compiler program.turk -r --temizle  # Çalıştır ve geçici dosyayı sil
        """)

    parser.add_argument("dosya", help="TÜRK kaynak dosyası (.turk)")
    parser.add_argument("-o", "--cikti", help="Çıktı dosya adı")
    parser.add_argument("-c", "--compile", action="store_true",
                        help="C kodunu gcc ile derle")
    parser.add_argument("-r", "--run", action="store_true",
                        help="Derle ve çalıştır")
    parser.add_argument("--temizle", action="store_true",
                        help="Geçici .c dosyasını sil")
    parser.add_argument("--stdout", action="store_true",
                        help="C kodunu stdout'a yazdır")

    args = parser.parse_args()

    if args.stdout:
        with open(args.dosya, 'r', encoding='utf-8') as f:
            kaynak = f.read()
        print(derle(kaynak))
        return

    dosya_derle(
        turk_dosya=args.dosya,
        c_dosya=args.cikti if args.cikti and not args.run else None,
        calistir=args.run,
        cikti_dosya=args.cikti if args.run else None,
        temizle=args.temizle,
    )


if __name__ == "__main__":
    main()
