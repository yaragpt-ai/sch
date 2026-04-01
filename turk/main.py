"""
TÜRK Programlama Dili - Ana Çalıştırıcı
"""

import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Proje kökünü path'e ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from turk.lexer import Lexer
from turk.parser import Parser, ParserHata
from turk.interpreter import Yorumlayici, YorumlayiciHata


def calistir(kaynak: str, girdiler: list = None) -> list:
    """TÜRK kaynak kodunu çalıştır ve çıktıyı döndür"""
    # 1. Sözcüksel analiz
    lexer = Lexer(kaynak)
    tokenler = lexer.analiz()

    if lexer.hatalar:
        for hata in lexer.hatalar:
            print(f"Lexer Hatası: {hata}", file=sys.stderr)
        return []

    # 2. Ayrıştırma
    parser = Parser(tokenler)
    try:
        ast = parser.ayrıştır()
    except ParserHata as e:
        print(f"Parser Hatası: {e}", file=sys.stderr)
        return []

    if parser.hatalar:
        for hata in parser.hatalar:
            print(f"Parser Hatası: {hata}", file=sys.stderr)
        return []

    # 3. Yorumlama
    yorumlayici = Yorumlayici()
    if girdiler:
        yorumlayici.girdi_ayarla(girdiler)

    try:
        cikti = yorumlayici.calistir(ast)
        return cikti
    except YorumlayiciHata as e:
        print(f"Çalışma Hatası: {e}", file=sys.stderr)
        return []


def dosya_calistir(dosya_yolu: str):
    """TÜRK dosyasını çalıştır"""
    with open(dosya_yolu, 'r', encoding='utf-8') as f:
        kaynak = f.read()

    cikti = calistir(kaynak)
    for satir in cikti:
        print(satir)


def main():
    if len(sys.argv) > 1:
        dosya_yolu = sys.argv[1]
        if not os.path.exists(dosya_yolu):
            print(f"Hata: Dosya bulunamadı: {dosya_yolu}", file=sys.stderr)
            sys.exit(1)
        dosya_calistir(dosya_yolu)
    else:
        # Etkileşimli mod
        print("TÜRK Programlama Dili v1.0")
        print("Çıkmak için 'çıkış' yazın\n")
        yorumlayici = Yorumlayici()

        while True:
            try:
                girdi = input("türk> ")
                if girdi.strip() == "çıkış":
                    break
                if not girdi.strip():
                    continue

                cikti = calistir(girdi)
                for satir in cikti:
                    print(satir)
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\nÇıkılıyor...")
                break


if __name__ == "__main__":
    main()
